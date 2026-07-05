from pydantic import BaseModel, Field


class ScriptGenerateRequest(BaseModel):
    prompt: str = Field(min_length=3, max_length=2_000)
    duration_seconds: int = Field(default=60, ge=30, le=60)


class Scene(BaseModel):
    narration: str = Field(min_length=1)
    image_prompt: str = Field(min_length=3)
    duration_seconds: int = Field(ge=1, le=60)


class VideoPlan(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    scenes: list[Scene] = Field(min_length=1, max_length=12)


class ScriptGenerateResponse(VideoPlan):
    model: str


class VoiceProfile(BaseModel):
    id: str
    name: str
    reference_audio_path: str
    reference_text: str


class TTSGenerateRequest(BaseModel):
    voice_profile_id: str = Field(pattern=r"^[0-9a-f]{32}$")
    scenes: list[Scene] = Field(min_length=1, max_length=12)


class AudioAsset(BaseModel):
    scene_index: int = Field(ge=1)
    path: str
    url: str


class TTSGenerateResponse(BaseModel):
    job_id: str
    audio: list[AudioAsset]


class ImageGenerateRequest(BaseModel):
    scenes: list[Scene] = Field(min_length=1, max_length=12)
    width: int = Field(default=1280, ge=256, le=1920, multiple_of=8)
    height: int = Field(default=720, ge=256, le=1920, multiple_of=8)
    seed: int = Field(default=0, ge=0, le=2_147_483_647)


class ImageAsset(BaseModel):
    scene_index: int = Field(ge=1)
    prompt: str
    seed: int
    path: str
    url: str


class ImageGenerateResponse(BaseModel):
    job_id: str
    images: list[ImageAsset]


class VideoRenderRequest(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    scenes: list[Scene] = Field(min_length=1, max_length=12)
    audio: list[AudioAsset] = Field(min_length=1, max_length=12)
    images: list[ImageAsset] = Field(min_length=1, max_length=12)
    width: int = Field(default=1280, ge=256, le=1920, multiple_of=2)
    height: int = Field(default=720, ge=256, le=1920, multiple_of=2)


class VideoRenderResponse(BaseModel):
    job_id: str
    video_path: str
    video_url: str
    subtitle_path: str
    subtitle_url: str

