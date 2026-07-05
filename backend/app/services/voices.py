import json
import re
from pathlib import Path
from uuid import uuid4

from app.schemas import VoiceProfile

VOICE_ID_PATTERN = re.compile(r"^[0-9a-f]{32}$")
SUPPORTED_AUDIO_EXTENSIONS = {".flac", ".m4a", ".mp3", ".wav"}


class VoiceProfileError(RuntimeError):
    pass


class VoiceProfileRepository:
    def __init__(self, storage_root: Path) -> None:
        self.storage_root = storage_root.resolve()
        self.voices_root = self.storage_root / "voices"
        self.voices_root.mkdir(parents=True, exist_ok=True)

    def create(
        self,
        name: str,
        reference_text: str,
        filename: str,
        audio: bytes,
    ) -> VoiceProfile:
        suffix = Path(filename).suffix.lower()
        if suffix not in SUPPORTED_AUDIO_EXTENSIONS:
            raise VoiceProfileError("Reference audio must be WAV, FLAC, MP3, or M4A")

        voice_id = uuid4().hex
        audio_path = self.voices_root / f"{voice_id}{suffix}"
        metadata_path = self.voices_root / f"{voice_id}.json"
        relative_audio_path = audio_path.relative_to(self.storage_root).as_posix()
        profile = VoiceProfile(
            id=voice_id,
            name=name.strip(),
            reference_audio_path=relative_audio_path,
            reference_text=reference_text.strip(),
        )

        audio_path.write_bytes(audio)
        temporary_metadata = metadata_path.with_suffix(".json.tmp")
        try:
            temporary_metadata.write_text(profile.model_dump_json(indent=2), encoding="utf-8")
            temporary_metadata.replace(metadata_path)
        except OSError:
            audio_path.unlink(missing_ok=True)
            temporary_metadata.unlink(missing_ok=True)
            raise
        return profile

    def list(self) -> list[VoiceProfile]:
        profiles: list[VoiceProfile] = []
        for metadata_path in sorted(self.voices_root.glob("*.json")):
            try:
                profiles.append(VoiceProfile.model_validate_json(metadata_path.read_text("utf-8")))
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                raise VoiceProfileError(f"Invalid voice metadata: {metadata_path.name}") from exc
        return profiles

    def get(self, voice_id: str) -> VoiceProfile:
        if not VOICE_ID_PATTERN.fullmatch(voice_id):
            raise VoiceProfileError("Invalid voice profile ID")
        metadata_path = self.voices_root / f"{voice_id}.json"
        if not metadata_path.is_file():
            raise VoiceProfileError("Voice profile not found")
        try:
            return VoiceProfile.model_validate_json(metadata_path.read_text("utf-8"))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            raise VoiceProfileError("Voice profile metadata is invalid") from exc

