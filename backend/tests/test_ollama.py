import json

import httpx
import pytest

from app.config import Settings
from app.services.ollama import OllamaService, OllamaUnavailableError


@pytest.mark.asyncio
async def test_ollama_service_parses_structured_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content)
        assert payload["format"]["properties"]["scenes"]
        return httpx.Response(
            200,
            json={
                "response": json.dumps(
                    {
                        "title": "A Test Video",
                        "scenes": [
                            {
                                "narration": "A concise narration.",
                                "image_prompt": "A detailed cinematic test scene",
                                "duration_seconds": 60,
                            }
                        ],
                    }
                )
            },
        )

    service = OllamaService(Settings(), transport=httpx.MockTransport(handler))

    plan = await service.generate_video_plan("Test topic", 60)

    assert plan.title == "A Test Video"
    assert plan.scenes[0].image_prompt == "A detailed cinematic test scene"


@pytest.mark.asyncio
async def test_ollama_service_rejects_invalid_model_output() -> None:
    transport = httpx.MockTransport(
        lambda request: httpx.Response(200, json={"response": "not-json"})
    )
    service = OllamaService(Settings(), transport=transport)

    with pytest.raises(OllamaUnavailableError, match="invalid video plan"):
        await service.generate_video_plan("Test topic", 60)


@pytest.mark.asyncio
async def test_ollama_service_normalizes_scene_durations() -> None:
    model_plan = {
        "title": "Uneven Timeline",
        "scenes": [
            {
                "narration": f"Narration {index}",
                "image_prompt": f"Detailed image prompt {index}",
                "duration_seconds": duration,
            }
            for index, duration in enumerate([30, 15, 10, 10, 10], start=1)
        ],
    }
    transport = httpx.MockTransport(
        lambda request: httpx.Response(200, json={"response": json.dumps(model_plan)})
    )
    service = OllamaService(Settings(), transport=transport)

    plan = await service.generate_video_plan("Test topic", 60)

    assert sum(scene.duration_seconds for scene in plan.scenes) == 60
    assert plan.scenes[0].duration_seconds > plan.scenes[-1].duration_seconds
