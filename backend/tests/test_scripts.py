import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas import Scene, VideoPlan
from app.services.ollama import OllamaService, OllamaUnavailableError

client = TestClient(app)


def test_generate_script_returns_structured_video_plan(monkeypatch: pytest.MonkeyPatch) -> None:
    async def generate_plan(
        self: OllamaService, prompt: str, duration_seconds: int
    ) -> VideoPlan:
        assert prompt == "Solar storms"
        assert duration_seconds == 60
        return VideoPlan(
            title="Solar Storms Explained",
            scenes=[
                Scene(
                    narration="A solar storm begins on the Sun.",
                    image_prompt="A cinematic view of a solar flare erupting from the Sun",
                    duration_seconds=60,
                )
            ],
        )

    monkeypatch.setattr(OllamaService, "generate_video_plan", generate_plan)

    response = client.post(
        "/api/v1/scripts/generate",
        json={"prompt": "Solar storms", "duration_seconds": 60},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Solar Storms Explained"
    assert body["scenes"][0]["duration_seconds"] == 60
    assert body["model"]


@pytest.mark.parametrize(
    "payload",
    [
        {"prompt": "no", "duration_seconds": 60},
        {"prompt": "Valid topic", "duration_seconds": 29},
        {"prompt": "Valid topic", "duration_seconds": 61},
    ],
)
def test_generate_script_rejects_invalid_requests(payload: dict[str, object]) -> None:
    response = client.post("/api/v1/scripts/generate", json=payload)

    assert response.status_code == 422


def test_generate_script_returns_503_when_ollama_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fail(self: OllamaService, prompt: str, duration_seconds: int) -> VideoPlan:
        raise OllamaUnavailableError("Ollama is unavailable or returned an error")

    monkeypatch.setattr(OllamaService, "generate_video_plan", fail)

    response = client.post(
        "/api/v1/scripts/generate",
        json={"prompt": "Solar storms", "duration_seconds": 60},
    )

    assert response.status_code == 503
    assert response.json() == {"detail": "Ollama is unavailable or returned an error"}

