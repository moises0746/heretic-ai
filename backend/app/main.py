import logging

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import Settings, get_settings
from app.schemas import (
    ScriptGenerateRequest,
    ScriptGenerateResponse,
    ImageGenerateRequest,
    ImageGenerateResponse,
    TTSGenerateRequest,
    TTSGenerateResponse,
    VoiceProfile,
)
from app.services.ollama import OllamaService, OllamaUnavailableError
from app.services.image import FluxImageService, ImageGenerationError
from app.services.tts import F5TTSService, TTSUnavailableError
from app.services.voices import VoiceProfileError, VoiceProfileRepository

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)
MAX_REFERENCE_AUDIO_BYTES = 25 * 1024 * 1024

settings = get_settings()
settings.storage_root.mkdir(parents=True, exist_ok=True)
(settings.storage_root / "audio").mkdir(parents=True, exist_ok=True)
(settings.storage_root / "images").mkdir(parents=True, exist_ok=True)
app = FastAPI(title="Heretic AI API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
app.mount(
    "/media/audio",
    StaticFiles(directory=settings.storage_root / "audio"),
    name="generated-audio",
)
app.mount(
    "/media/images",
    StaticFiles(directory=settings.storage_root / "images"),
    name="generated-images",
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/scripts/generate", response_model=ScriptGenerateResponse)
async def generate_script(
    request: ScriptGenerateRequest,
    app_settings: Settings = Depends(get_settings),
) -> ScriptGenerateResponse:
    try:
        plan = await OllamaService(app_settings).generate_video_plan(
            request.prompt, request.duration_seconds
        )
    except OllamaUnavailableError as exc:
        logger.warning("Script generation failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    return ScriptGenerateResponse(**plan.model_dump(), model=app_settings.ollama_model)


@app.get("/api/v1/voices", response_model=list[VoiceProfile])
async def list_voices(app_settings: Settings = Depends(get_settings)) -> list[VoiceProfile]:
    return VoiceProfileRepository(app_settings.storage_root).list()


@app.post(
    "/api/v1/voices",
    response_model=VoiceProfile,
    status_code=status.HTTP_201_CREATED,
)
async def create_voice(
    name: str = Form(min_length=1, max_length=80),
    reference_text: str = Form(min_length=1, max_length=1_000),
    reference_audio: UploadFile = File(),
    app_settings: Settings = Depends(get_settings),
) -> VoiceProfile:
    audio = await reference_audio.read(MAX_REFERENCE_AUDIO_BYTES + 1)
    await reference_audio.close()
    if not audio:
        raise HTTPException(status_code=400, detail="Reference audio is empty")
    if len(audio) > MAX_REFERENCE_AUDIO_BYTES:
        raise HTTPException(status_code=413, detail="Reference audio exceeds 25 MB")
    try:
        return VoiceProfileRepository(app_settings.storage_root).create(
            name=name,
            reference_text=reference_text,
            filename=reference_audio.filename or "reference.wav",
            audio=audio,
        )
    except VoiceProfileError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/v1/audio/generate", response_model=TTSGenerateResponse)
async def generate_audio(
    request: TTSGenerateRequest,
    app_settings: Settings = Depends(get_settings),
) -> TTSGenerateResponse:
    try:
        voice = VoiceProfileRepository(app_settings.storage_root).get(
            request.voice_profile_id
        )
        return await F5TTSService(app_settings).generate(voice, request.scenes)
    except VoiceProfileError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except TTSUnavailableError as exc:
        logger.warning("Audio generation failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc


@app.post("/api/v1/images/generate", response_model=ImageGenerateResponse)
async def generate_images(
    request: ImageGenerateRequest,
    app_settings: Settings = Depends(get_settings),
) -> ImageGenerateResponse:
    try:
        return await FluxImageService(app_settings).generate(
            scenes=request.scenes,
            width=request.width,
            height=request.height,
            seed=request.seed,
        )
    except ImageGenerationError as exc:
        logger.warning("Image generation failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
