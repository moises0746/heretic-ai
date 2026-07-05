import logging

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.config import Settings, get_settings
from app.schemas import ScriptGenerateRequest, ScriptGenerateResponse
from app.services.ollama import OllamaService, OllamaUnavailableError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)

settings = get_settings()
app = FastAPI(title="Heretic AI API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
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
