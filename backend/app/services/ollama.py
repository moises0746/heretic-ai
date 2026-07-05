import httpx

from app.config import Settings


class OllamaUnavailableError(RuntimeError):
    pass


class OllamaService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def generate_script(self, prompt: str, duration_seconds: int) -> str:
        instruction = (
            f"Write a narration script for a {duration_seconds}-second video about: {prompt}. "
            "Return only the narration, with concise scene-friendly paragraphs."
        )
        payload = {
            "model": self.settings.ollama_model,
            "prompt": instruction,
            "stream": False,
        }

        try:
            async with httpx.AsyncClient(
                base_url=self.settings.ollama_base_url,
                timeout=self.settings.ollama_timeout_seconds,
            ) as client:
                response = await client.post("/api/generate", json=payload)
                response.raise_for_status()
        except (httpx.HTTPError, httpx.TimeoutException) as exc:
            raise OllamaUnavailableError("Ollama is unavailable or returned an error") from exc

        script = response.json().get("response", "").strip()
        if not script:
            raise OllamaUnavailableError("Ollama returned an empty response")
        return script

