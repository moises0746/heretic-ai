from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import app
from app.schemas import ImageAsset, ImageGenerateResponse, Scene
from app.services.image import FluxImageService, ImageGenerationError


class FakeImageRunner:
    def __init__(self, create_output: bool = True) -> None:
        self.commands: list[list[str]] = []
        self.create_output = create_output

    async def run(
        self,
        command: list[str],
        timeout_seconds: float,
        environment: dict[str, str],
    ) -> None:
        self.commands.append(command)
        if self.create_output:
            output = Path(command[command.index("--output") + 1])
            output.write_bytes(b"PNG-test-image")


def scenes() -> list[Scene]:
    return [
        Scene(
            narration="First narration.",
            image_prompt="A cinematic violet city at night.",
            duration_seconds=30,
        ),
        Scene(
            narration="Second narration.",
            image_prompt="A sunrise over a futuristic skyline.",
            duration_seconds=30,
        ),
    ]


@pytest.mark.asyncio
async def test_flux_generates_one_image_per_scene(tmp_path: Path) -> None:
    runner = FakeImageRunner()
    service = FluxImageService(Settings(storage_root=tmp_path), runner=runner)

    response = await service.generate(scenes(), width=1280, height=720, seed=42)

    assert len(response.images) == 2
    assert [image.seed for image in response.images] == [42, 43]
    assert len(runner.commands) == 2
    assert (tmp_path / response.images[0].path).read_bytes() == b"PNG-test-image"


@pytest.mark.asyncio
async def test_flux_cleans_partial_job_when_output_is_missing(tmp_path: Path) -> None:
    service = FluxImageService(
        Settings(storage_root=tmp_path),
        runner=FakeImageRunner(create_output=False),
    )

    with pytest.raises(ImageGenerationError, match="expected image"):
        await service.generate(scenes()[:1], width=1280, height=720, seed=0)

    assert not list((tmp_path / "images").iterdir())


def test_image_api_returns_generated_assets(monkeypatch: pytest.MonkeyPatch) -> None:
    async def generate(
        self: FluxImageService,
        scenes: list[Scene],
        width: int,
        height: int,
        seed: int,
    ) -> ImageGenerateResponse:
        assert (width, height, seed) == (1280, 720, 7)
        return ImageGenerateResponse(
            job_id="image-job",
            images=[
                ImageAsset(
                    scene_index=1,
                    prompt=scenes[0].image_prompt,
                    seed=7,
                    path="images/image-job/scene-001.png",
                    url="/media/images/image-job/scene-001.png",
                )
            ],
        )

    monkeypatch.setattr(FluxImageService, "generate", generate)
    response = TestClient(app).post(
        "/api/v1/images/generate",
        json={"scenes": [scene.model_dump() for scene in scenes()[:1]], "seed": 7},
    )

    assert response.status_code == 200
    assert response.json()["images"][0]["seed"] == 7


def test_image_api_rejects_invalid_dimensions() -> None:
    response = TestClient(app).post(
        "/api/v1/images/generate",
        json={"scenes": [scene.model_dump() for scene in scenes()[:1]], "width": 257},
    )

    assert response.status_code == 422


def test_image_api_returns_503_when_flux_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fail(
        self: FluxImageService,
        scenes: list[Scene],
        width: int,
        height: int,
        seed: int,
    ) -> ImageGenerateResponse:
        raise ImageGenerationError("FLUX runtime is unavailable")

    monkeypatch.setattr(FluxImageService, "generate", fail)
    response = TestClient(app).post(
        "/api/v1/images/generate",
        json={"scenes": [scene.model_dump() for scene in scenes()[:1]]},
    )

    assert response.status_code == 503
    assert response.json() == {"detail": "FLUX runtime is unavailable"}
