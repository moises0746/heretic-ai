from pydantic import BaseModel, Field


class ScriptGenerateRequest(BaseModel):
    prompt: str = Field(min_length=3, max_length=2_000)
    duration_seconds: int = Field(default=60, ge=30, le=60)


class ScriptGenerateResponse(BaseModel):
    script: str
    model: str

