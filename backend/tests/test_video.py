from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import app
from app.schemas import (
    AudioAsset,
    ImageAsset,
    Scene,
    VideoRenderResponse,
)
from app.services.video import VideoRenderer, VideoRenderError


class FakeFFmpegRunner:
    def __init__(self, create_output: bool = True) -> None:
        self.command: list[str] = []
        self.create_output = create_output

    async def run(self, command: list[str], timeout_seconds: float) -> None:
        self.command = command
        if self.create_output:
            Path(command[-1]).write_bytes(b"fake-mp4")


def create_assets(storage_root: Path) -> tuple[list[Scene], list[AudioAsset], list[ImageAsset]]:
    (storage_root / "audio" / "job").mkdir(parents=True)
    (storage_root / "images" / "job").mkdir(parents=True)
    scenes: list[Scene] = []
    audio: list[AudioAsset] = []
    images: list[ImageAsset] = []
    for index in (1, 2):
        audio_path = storage_root / "audio" / "job" / f"scene-{index:03d}.wav"
        image_path = storage_root / "images" / "job" / f"scene-{index:03d}.png"
        audio_path.write_bytes(b"audio")
        image_path.write_bytes(b"image")
        scenes.append(
            Scene(
                narration=f"Narration {index}.",
                image_prompt=f"Detailed image prompt {index}.",
                duration_seconds=30,
            )
        )
        audio.append(
            AudioAsset(
                scene_index=index,
                path=audio_path.relative_to(storage_root).as_posix(),
                url="/media/audio/test.wav",
            )
        )
        images.append(
            ImageAsset(
                scene_index=index,
                prompt=scenes[-1].image_prompt,
                seed=index,
                path=image_path.relative_to(storage_root).as_posix(),
                url="/media/images/test.png",
            )
        )
    return scenes, audio, images


@pytest.mark.asyncio
async def test_renderer_builds_mp4_and_subtitles(tmp_path: Path) -> None:
    runner = FakeFFmpegRunner()
    renderer = VideoRenderer(Settings(storage_root=tmp_path), runner=runner)
    scenes, audio, images = create_assets(tmp_path)

    response = await renderer.render("Test Video", scenes, audio, images, 1280, 720)

    assert (tmp_path / response.video_path).read_bytes() == b"fake-mp4"
    assert "00:00:30,000 --> 00:01:00,000" in (
        tmp_path / response.subtitle_path
    ).read_text("utf-8")
    assert "concat=n=2:v=1:a=1" in runner.command[runner.command.index("-filter_complex") + 1]
    assert "mov_text" in runner.command


def test_renderer_rejects_mismatched_assets(tmp_path: Path) -> None:
    renderer = VideoRenderer(Settings(storage_root=tmp_path), runner=FakeFFmpegRunner())
    scenes, audio, images = create_assets(tmp_path)

    with pytest.raises(VideoRenderError, match="Audio assets do not match"):
        renderer.resolve_assets(scenes, audio[:1], images)


def test_video_api_returns_rendered_asset(monkeypatch: pytest.MonkeyPatch) -> None:
    async def render(
        self: VideoRenderer,
        title: str,
        scenes: list[Scene],
        audio: list[AudioAsset],
        images: list[ImageAsset],
        width: int,
        height: int,
    ) -> VideoRenderResponse:
        return VideoRenderResponse(
            job_id="video-job",
            video_path="videos/video-job/video.mp4",
            video_url="/media/videos/video-job/video.mp4",
            subtitle_path="videos/video-job/subtitles.srt",
            subtitle_url="/media/videos/video-job/subtitles.srt",
        )

    monkeypatch.setattr(VideoRenderer, "render", render)
    scenes, audio, images = create_assets(Path.cwd() / ".pytest-video-assets")
    try:
        response = TestClient(app).post(
            "/api/v1/videos/render",
            json={
                "title": "Test Video",
                "scenes": [scene.model_dump() for scene in scenes],
                "audio": [asset.model_dump() for asset in audio],
                "images": [asset.model_dump() for asset in images],
            },
        )
    finally:
        import shutil

        shutil.rmtree(Path.cwd() / ".pytest-video-assets", ignore_errors=True)

    assert response.status_code == 200
    assert response.json()["video_url"].endswith("video.mp4")

