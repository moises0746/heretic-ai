from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_env: str = "development"
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "qwen3"
    ollama_timeout_seconds: float = 120
    cors_origins: str = "http://localhost:3000"
    storage_root: Path = PROJECT_ROOT / "storage"
    f5_tts_command: str = "f5-tts_infer-cli"
    f5_tts_model: str = "F5TTS_v1_Base"
    f5_tts_device: str = ""
    f5_tts_timeout_seconds: float = 900
    f5_tts_cache_dir: Path | None = None
    f5_tts_ffmpeg_dir: Path | None = None
    flux_python_command: str = "python"
    flux_script: Path = PROJECT_ROOT / "scripts" / "flux_infer.py"
    flux_model: str = "black-forest-labs/FLUX.1-schnell"
    flux_device: str = "cuda"
    flux_steps: int = 4
    flux_timeout_seconds: float = 1800
    flux_cache_dir: Path | None = None
    ffmpeg_command: str = "ffmpeg"
    ffmpeg_timeout_seconds: float = 900

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
