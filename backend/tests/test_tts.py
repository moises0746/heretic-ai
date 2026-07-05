from pathlib import Path

import pytest

from app.config import Settings
from app.schemas import Scene, VoiceProfile
from app.services.tts import F5TTSService, TTSUnavailableError


class FakeRunner:
    def __init__(self, create_output: bool = True) -> None:
        self.commands: list[list[str]] = []
        self.create_output = create_output

    async def run(self, command: list[str], timeout_seconds: float) -> None:
        self.commands.append(command)
        if self.create_output:
            output_dir = Path(command[command.index("--output_dir") + 1])
            output_file = command[command.index("--output_file") + 1]
            (output_dir / output_file).write_bytes(b"RIFF-generated-audio")


def create_voice(storage_root: Path) -> VoiceProfile:
    reference_audio = storage_root / "voices" / "reference.wav"
    reference_audio.parent.mkdir(parents=True)
    reference_audio.write_bytes(b"RIFF-reference-audio")
    return VoiceProfile(
        id="a" * 32,
        name="Narrator",
        reference_audio_path="voices/reference.wav",
        reference_text="Reference transcript.",
    )


@pytest.mark.asyncio
async def test_f5_tts_generates_one_audio_file_per_scene(tmp_path: Path) -> None:
    runner = FakeRunner()
    service = F5TTSService(Settings(storage_root=tmp_path), runner=runner)
    scenes = [
        Scene(
            narration="First narration.",
            image_prompt="First detailed visual prompt.",
            duration_seconds=30,
        ),
        Scene(
            narration="Second narration.",
            image_prompt="Second detailed visual prompt.",
            duration_seconds=30,
        ),
    ]

    response = await service.generate(create_voice(tmp_path), scenes)

    assert len(response.audio) == 2
    assert len(runner.commands) == 2
    assert runner.commands[0][runner.commands[0].index("--gen_text") + 1] == "First narration."
    assert (tmp_path / response.audio[0].path).read_bytes() == b"RIFF-generated-audio"


@pytest.mark.asyncio
async def test_f5_tts_cleans_partial_job_when_output_is_missing(tmp_path: Path) -> None:
    service = F5TTSService(
        Settings(storage_root=tmp_path), runner=FakeRunner(create_output=False)
    )
    scene = Scene(
        narration="Narration.",
        image_prompt="A detailed visual prompt.",
        duration_seconds=30,
    )

    with pytest.raises(TTSUnavailableError, match="expected audio file"):
        await service.generate(create_voice(tmp_path), [scene])

    assert not list((tmp_path / "audio").iterdir())

