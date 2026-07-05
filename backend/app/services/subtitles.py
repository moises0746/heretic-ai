import textwrap

from app.schemas import Scene


def format_srt_timestamp(total_seconds: float) -> str:
    total_milliseconds = round(total_seconds * 1000)
    hours, remainder = divmod(total_milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, milliseconds = divmod(remainder, 1_000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def generate_srt(scenes: list[Scene], line_width: int = 42) -> str:
    cues: list[str] = []
    start_seconds = 0.0
    for index, scene in enumerate(scenes, start=1):
        end_seconds = start_seconds + scene.duration_seconds
        narration = " ".join(scene.narration.split())
        wrapped = "\n".join(
            textwrap.wrap(
                narration,
                width=line_width,
                break_long_words=False,
                break_on_hyphens=False,
            )
        )
        cues.append(
            f"{index}\n"
            f"{format_srt_timestamp(start_seconds)} --> {format_srt_timestamp(end_seconds)}\n"
            f"{wrapped}\n"
        )
        start_seconds = end_seconds
    return "\n".join(cues)

