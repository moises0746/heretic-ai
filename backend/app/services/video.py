import asyncio
import logging
import shutil
from pathlib import Path
from typing import Protocol
from uuid import uuid4

from app.config import Settings
from app.schemas import (
    AudioAsset,
    ImageAsset,
    Scene,
    VideoRenderResponse,
)
from app.services.subtitles import generate_srt

logger = logging.getLogger(__name__)


class VideoRenderError(RuntimeError):
    pass


class FFmpegRunner(Protocol):
    async def run(self, command: list[str], timeout_seconds: float) -> None: ...


class SubprocessFFmpegRunner:
    async def run(self, command: list[str], timeout_seconds: float) -> None:
        executable = shutil.which(command[0])
        if executable is None:
            raise VideoRenderError("FFmpeg is unavailable or FFMPEG_COMMAND is incorrect")
        command[0] = executable
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=timeout_seconds
            )
        except TimeoutError as exc:
            process.kill()
            await process.communicate()
            raise VideoRenderError("FFmpeg rendering timed out") from exc
        if process.returncode != 0:
            last_error = stderr.decode(errors="replace").strip().splitlines()[-1:]
            logger.error("FFmpeg failed: %s", last_error[0] if last_error else "unknown error")
            raise VideoRenderError("FFmpeg failed to render the video")
        logger.debug("FFmpeg output: %s", stdout.decode(errors="replace").strip())


class VideoRenderer:
    def __init__(
        self,
        settings: Settings,
        runner: FFmpegRunner | None = None,
    ) -> None:
        self.settings = settings
        self.storage_root = settings.storage_root.resolve()
        self.runner = runner or SubprocessFFmpegRunner()

    def resolve_assets(
        self,
        scenes: list[Scene],
        audio: list[AudioAsset],
        images: list[ImageAsset],
    ) -> list[tuple[Scene, Path, Path]]:
        expected_indexes = list(range(1, len(scenes) + 1))
        if [asset.scene_index for asset in audio] != expected_indexes:
            raise VideoRenderError("Audio assets do not match the scene order")
        if [asset.scene_index for asset in images] != expected_indexes:
            raise VideoRenderError("Image assets do not match the scene order")

        resolved: list[tuple[Scene, Path, Path]] = []
        for scene, audio_asset, image_asset in zip(scenes, audio, images, strict=True):
            audio_path = (self.storage_root / audio_asset.path).resolve()
            image_path = (self.storage_root / image_asset.path).resolve()
            if not audio_path.is_relative_to(self.storage_root) or not audio_path.is_file():
                raise VideoRenderError("A scene audio file is missing or outside local storage")
            if not image_path.is_relative_to(self.storage_root) or not image_path.is_file():
                raise VideoRenderError("A scene image file is missing or outside local storage")
            resolved.append((scene, image_path, audio_path))
        return resolved

    def build_command(
        self,
        assets: list[tuple[Scene, Path, Path]],
        subtitle_path: Path,
        output_path: Path,
        title: str,
        width: int,
        height: int,
    ) -> list[str]:
        command = [self.settings.ffmpeg_command, "-hide_banner", "-loglevel", "error", "-y"]
        filters: list[str] = []
        concat_inputs: list[str] = []

        for index, (scene, image_path, audio_path) in enumerate(assets):
            duration = scene.duration_seconds
            image_input = index * 2
            audio_input = image_input + 1
            command.extend(
                [
                    "-loop",
                    "1",
                    "-framerate",
                    "30",
                    "-t",
                    str(duration),
                    "-i",
                    str(image_path),
                    "-i",
                    str(audio_path),
                ]
            )
            filters.append(
                f"[{image_input}:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
                f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,"
                f"trim=duration={duration},setpts=PTS-STARTPTS[v{index}]"
            )
            filters.append(
                f"[{audio_input}:a]aresample=48000,apad=pad_dur={duration},"
                f"atrim=0:{duration},asetpts=PTS-STARTPTS[a{index}]"
            )
            concat_inputs.extend([f"[v{index}]", f"[a{index}]"])

        subtitle_input = len(assets) * 2
        command.extend(["-i", str(subtitle_path)])
        filters.append(
            f"{''.join(concat_inputs)}concat=n={len(assets)}:v=1:a=1[vout][aout]"
        )
        command.extend(
            [
                "-filter_complex",
                ";".join(filters),
                "-map",
                "[vout]",
                "-map",
                "[aout]",
                "-map",
                f"{subtitle_input}:s:0",
                "-c:v",
                "libx264",
                "-preset",
                "medium",
                "-crf",
                "20",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-c:s",
                "mov_text",
                "-metadata",
                f"title={title}",
                "-metadata:s:s:0",
                "language=eng",
                "-movflags",
                "+faststart",
                str(output_path),
            ]
        )
        return command

    async def render(
        self,
        title: str,
        scenes: list[Scene],
        audio: list[AudioAsset],
        images: list[ImageAsset],
        width: int,
        height: int,
    ) -> VideoRenderResponse:
        assets = self.resolve_assets(scenes, audio, images)
        job_id = uuid4().hex
        output_dir = self.storage_root / "videos" / job_id
        output_dir.mkdir(parents=True, exist_ok=False)
        subtitle_path = output_dir / "subtitles.srt"
        output_path = output_dir / "video.mp4"

        try:
            subtitle_path.write_text(generate_srt(scenes), encoding="utf-8")
            command = self.build_command(
                assets,
                subtitle_path,
                output_path,
                title,
                width,
                height,
            )
            await self.runner.run(command, self.settings.ffmpeg_timeout_seconds)
            if not output_path.is_file():
                raise VideoRenderError("FFmpeg did not create the expected MP4 file")
        except Exception:
            shutil.rmtree(output_dir, ignore_errors=True)
            raise

        video_path = output_path.relative_to(self.storage_root).as_posix()
        subtitle_relative_path = subtitle_path.relative_to(self.storage_root).as_posix()
        return VideoRenderResponse(
            job_id=job_id,
            video_path=video_path,
            video_url=f"/media/{video_path}",
            subtitle_path=subtitle_relative_path,
            subtitle_url=f"/media/{subtitle_relative_path}",
        )

