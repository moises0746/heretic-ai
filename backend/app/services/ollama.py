import json

import httpx
from pydantic import ValidationError

from app.config import Settings
from app.schemas import VideoPlan


class OllamaUnavailableError(RuntimeError):
    pass


def normalize_scene_durations(plan: VideoPlan, target_seconds: int) -> VideoPlan:
    raw_durations = [scene.duration_seconds for scene in plan.scenes]
    raw_total = sum(raw_durations)
    scaled = [duration * target_seconds / raw_total for duration in raw_durations]
    normalized = [max(1, int(duration)) for duration in scaled]

    remaining = target_seconds - sum(normalized)
    if remaining > 0:
        order = sorted(
            range(len(scaled)),
            key=lambda index: scaled[index] - int(scaled[index]),
            reverse=True,
        )
        for offset in range(remaining):
            normalized[order[offset % len(order)]] += 1
    elif remaining < 0:
        order = sorted(range(len(normalized)), key=normalized.__getitem__, reverse=True)
        for _ in range(-remaining):
            for index in order:
                if normalized[index] > 1:
                    normalized[index] -= 1
                    break

    scenes = [
        scene.model_copy(update={"duration_seconds": duration})
        for scene, duration in zip(plan.scenes, normalized, strict=True)
    ]
    return plan.model_copy(update={"scenes": scenes})


class OllamaService:
    def __init__(
        self,
        settings: Settings,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self.settings = settings
        self.transport = transport

    async def generate_video_plan(self, prompt: str, duration_seconds: int) -> VideoPlan:
        instruction = (
            f"Create a scene plan for a {duration_seconds}-second video about: {prompt}. "
            "Return a concise title and 4 to 8 scenes. Each scene must contain narration, "
            "a detailed image-generation prompt, and its duration in seconds. Scene durations "
            f"must total {duration_seconds} seconds. Return only valid JSON matching the schema."
        )
        payload = {
            "model": self.settings.ollama_model,
            "prompt": instruction,
            "stream": False,
            "format": VideoPlan.model_json_schema(),
            "options": {"temperature": 0.3},
        }

        try:
            async with httpx.AsyncClient(
                base_url=self.settings.ollama_base_url,
                timeout=self.settings.ollama_timeout_seconds,
                transport=self.transport,
            ) as client:
                response = await client.post("/api/generate", json=payload)
                response.raise_for_status()
        except httpx.HTTPError as exc:
            raise OllamaUnavailableError("Ollama is unavailable or returned an error") from exc

        raw_plan = response.json().get("response", "").strip()
        if not raw_plan:
            raise OllamaUnavailableError("Ollama returned an empty response")

        try:
            plan = VideoPlan.model_validate(json.loads(raw_plan))
        except (json.JSONDecodeError, ValidationError) as exc:
            raise OllamaUnavailableError("Ollama returned an invalid video plan") from exc
        return normalize_scene_durations(plan, duration_seconds)

