from app.schemas import Scene
from app.services.subtitles import format_srt_timestamp, generate_srt


def test_format_srt_timestamp() -> None:
    assert format_srt_timestamp(0) == "00:00:00,000"
    assert format_srt_timestamp(61.234) == "00:01:01,234"


def test_generate_srt_uses_scene_timeline() -> None:
    scenes = [
        Scene(narration="First scene narration.", image_prompt="First visual.", duration_seconds=12),
        Scene(narration="Second scene narration.", image_prompt="Second visual.", duration_seconds=18),
    ]

    subtitles = generate_srt(scenes)

    assert "00:00:00,000 --> 00:00:12,000" in subtitles
    assert "00:00:12,000 --> 00:00:30,000" in subtitles
    assert "First scene narration." in subtitles

