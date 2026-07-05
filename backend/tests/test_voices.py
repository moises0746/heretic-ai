from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.config import Settings, get_settings
from app.main import app
from app.services.voices import VoiceProfileError, VoiceProfileRepository


def test_voice_repository_creates_and_lists_profile(tmp_path: Path) -> None:
    repository = VoiceProfileRepository(tmp_path)

    created = repository.create(
        name="Narrator",
        reference_text="This is the reference transcript.",
        filename="voice.wav",
        audio=b"RIFF-test-audio",
    )

    assert repository.get(created.id) == created
    assert repository.list() == [created]
    assert (tmp_path / created.reference_audio_path).read_bytes() == b"RIFF-test-audio"


def test_voice_repository_rejects_unsupported_audio(tmp_path: Path) -> None:
    repository = VoiceProfileRepository(tmp_path)

    with pytest.raises(VoiceProfileError, match="must be WAV"):
        repository.create("Narrator", "Transcript", "voice.exe", b"invalid")


def test_voice_api_uploads_and_lists_profile(tmp_path: Path) -> None:
    app.dependency_overrides[get_settings] = lambda: Settings(storage_root=tmp_path)
    client = TestClient(app)
    try:
        response = client.post(
            "/api/v1/voices",
            data={"name": "Narrator", "reference_text": "Reference transcript."},
            files={"reference_audio": ("voice.wav", b"RIFF-test-audio", "audio/wav")},
        )
        voices = client.get("/api/v1/voices")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 201
    assert response.json()["name"] == "Narrator"
    assert voices.status_code == 200
    assert len(voices.json()) == 1

