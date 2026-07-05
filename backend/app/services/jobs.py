import asyncio

from app.config import Settings, get_settings
from app.schemas import ImageGenerateRequest, TTSGenerateRequest, VideoRenderRequest
from app.services.image import FluxImageService
from app.services.tts import F5TTSService
from app.services.video import VideoRenderer
from app.services.voices import VoiceProfileRepository


async def execute_job(
    job_type: str,
    payload: dict[str, object],
    settings: Settings,
) -> dict[str, object]:
    if job_type == "audio":
        request = TTSGenerateRequest.model_validate(payload)
        voice = VoiceProfileRepository(settings.storage_root).get(request.voice_profile_id)
        result = await F5TTSService(settings).generate(voice, request.scenes)
    elif job_type == "images":
        request = ImageGenerateRequest.model_validate(payload)
        result = await FluxImageService(settings).generate(
            request.scenes,
            request.width,
            request.height,
            request.seed,
        )
    elif job_type == "video":
        request = VideoRenderRequest.model_validate(payload)
        result = await VideoRenderer(settings).render(
            request.title,
            request.scenes,
            request.audio,
            request.images,
            request.width,
            request.height,
        )
    else:
        raise ValueError(f"Unsupported job type: {job_type}")
    return result.model_dump(mode="json")


def run_job(job_type: str, payload: dict[str, object]) -> dict[str, object]:
    """RQ worker entrypoint. Arguments and results remain JSON serializable."""
    return asyncio.run(execute_job(job_type, payload, get_settings()))

