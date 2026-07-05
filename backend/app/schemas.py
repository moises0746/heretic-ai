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

