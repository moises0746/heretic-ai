import asyncio
import logging
import os
import shutil
from pathlib import Path
from typing import Protocol
from uuid import uuid4

from app.config import Settings
from app.schemas import AudioAsset, Scene, TTSGenerateResponse, VoiceProfile

logger = logging.getLogger(__name__)


class TTSUnavailableError(RuntimeError):
    pass


class CommandRunner(Protocol):
    async def run(self, command: list[str], timeout_seconds: float) -> None: ...


class SubprocessCommandRunner:
    def __init__(self, environment: dict[str, str] | None = None) -> None:
        self.environment = environment or {}

    async def run(self, command: list[str], timeout_seconds: float) -> None:
        executable = shutil.which(command[0])
        if executable is None:
            raise TTSUnavailableError(
                "F5-TTS CLI is not installed or F5_TTS_COMMAND is incorrect"
            )
        command[0] = executable
        environment = os.environ.copy()
        environment.update(self.environment)
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=environment,
        )
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=timeout_seconds
            )
        except TimeoutError as exc:
            process.kill()
            await process.communicate()
            raise TTSUnavailableError("F5-TTS generation timed out") from exc
        if process.returncode != 0:
            detail = stderr.decode(errors="replace").strip().splitlines()[-1:] or ["unknown error"]
            logger.error("F5-TTS failed: %s", detail[0])
            raise TTSUnavailableError("F5-TTS failed to generate audio")
        logger.debug("F5-TTS output: %s", stdout.decode(errors="replace").strip())


class F5TTSService:
    def __init__(
        self,
        settings: Settings,
        runner: CommandRunner | None = None,
    ) -> None:
        self.settings = settings
        self.storage_root = settings.storage_root.resolve()
        environment: dict[str, str] = {}
        if settings.f5_tts_cache_dir:
            environment["HF_HOME"] = str(settings.f5_tts_cache_dir.resolve())
        if settings.f5_tts_ffmpeg_dir:
            environment["PATH"] = (
                f"{settings.f5_tts_ffmpeg_dir.resolve()}{os.pathsep}"
                f"{os.environ.get('PATH', '')}"
            )
        self.runner = runner or SubprocessCommandRunner(environment)

    async def generate(
        self,
        voice: VoiceProfile,
        scenes: list[Scene],
    ) -> TTSGenerateResponse:
        reference_audio = (self.storage_root / voice.reference_audio_path).resolve()
        if not reference_audio.is_relative_to(self.storage_root) or not reference_audio.is_file():
            raise TTSUnavailableError("Voice reference audio is missing")

        job_id = uuid4().hex
        output_dir = self.storage_root / "audio" / job_id
        output_dir.mkdir(parents=True, exist_ok=False)
        audio_assets: list[AudioAsset] = []

        try:
            for index, scene in enumerate(scenes, start=1):
                output_file = f"scene-{index:03d}.wav"
                command = [
                    self.settings.f5_tts_command,
                    "--model",
                    self.settings.f5_tts_model,
                    "--ref_audio",
                    str(reference_audio),
                    "--ref_text",
                    voice.reference_text,
                    "--gen_text",
                    scene.narration,
                    "--output_dir",
                    str(output_dir),
                    "--output_file",
                    output_file,
                ]
                if self.settings.f5_tts_device:
                    command.extend(["--device", self.settings.f5_tts_device])
                await self.runner.run(command, self.settings.f5_tts_timeout_seconds)

                output_path = output_dir / output_file
                if not output_path.is_file():
                    raise TTSUnavailableError("F5-TTS did not create the expected audio file")
                relative_path = output_path.relative_to(self.storage_root).as_posix()
                audio_assets.append(
                    AudioAsset(
                        scene_index=index,
                        path=relative_path,
                        url=f"/media/{relative_path}",
                    )
                )
        except Exception:
            shutil.rmtree(output_dir, ignore_errors=True)
            raise

        return TTSGenerateResponse(job_id=job_id, audio=audio_assets)
