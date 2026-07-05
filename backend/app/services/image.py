import asyncio
import logging
import os
import shutil
from pathlib import Path
from typing import Protocol
from uuid import uuid4

from app.config import Settings
from app.schemas import ImageAsset, ImageGenerateResponse, Scene

logger = logging.getLogger(__name__)


class ImageGenerationError(RuntimeError):
    pass


class ImageCommandRunner(Protocol):
    async def run(
        self,
        command: list[str],
        timeout_seconds: float,
        environment: dict[str, str],
    ) -> None: ...


class SubprocessImageCommandRunner:
    async def run(
        self,
        command: list[str],
        timeout_seconds: float,
        environment: dict[str, str],
    ) -> None:
        executable = shutil.which(command[0])
        if executable is None:
            raise ImageGenerationError(
                "FLUX Python runtime is unavailable or FLUX_PYTHON_COMMAND is incorrect"
            )
        command[0] = executable
        process_environment = os.environ.copy()
        process_environment.update(environment)
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=process_environment,
        )
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=timeout_seconds
            )
        except TimeoutError as exc:
            process.kill()
            await process.communicate()
            raise ImageGenerationError("FLUX image generation timed out") from exc
        if process.returncode != 0:
            last_error = stderr.decode(errors="replace").strip().splitlines()[-1:]
            logger.error("FLUX failed: %s", last_error[0] if last_error else "unknown error")
            raise ImageGenerationError("FLUX failed to generate an image")
        logger.debug("FLUX output: %s", stdout.decode(errors="replace").strip())


class FluxImageService:
    def __init__(
        self,
        settings: Settings,
        runner: ImageCommandRunner | None = None,
    ) -> None:
        self.settings = settings
        self.storage_root = settings.storage_root.resolve()
        self.runner = runner or SubprocessImageCommandRunner()

    async def generate(
        self,
        scenes: list[Scene],
        width: int,
        height: int,
        seed: int,
    ) -> ImageGenerateResponse:
        script = self.settings.flux_script.resolve()
        if not script.is_file():
            raise ImageGenerationError("FLUX inference script is missing")

        job_id = uuid4().hex
        output_dir = self.storage_root / "images" / job_id
        output_dir.mkdir(parents=True, exist_ok=False)
        environment: dict[str, str] = {}
        if self.settings.flux_cache_dir:
            environment["HF_HOME"] = str(self.settings.flux_cache_dir.resolve())
        images: list[ImageAsset] = []

        try:
            for index, scene in enumerate(scenes, start=1):
                scene_seed = seed + index - 1
                output_path = output_dir / f"scene-{index:03d}.png"
                command = [
                    self.settings.flux_python_command,
                    str(script),
                    "--model",
                    self.settings.flux_model,
                    "--prompt",
                    scene.image_prompt,
                    "--output",
                    str(output_path),
                    "--device",
                    self.settings.flux_device,
                    "--width",
                    str(width),
                    "--height",
                    str(height),
                    "--steps",
                    str(self.settings.flux_steps),
                    "--seed",
                    str(scene_seed),
                ]
                if self.settings.flux_cache_dir:
                    command.extend(["--cache-dir", str(self.settings.flux_cache_dir.resolve())])
                await self.runner.run(
                    command,
                    self.settings.flux_timeout_seconds,
                    environment,
                )
                if not output_path.is_file():
                    raise ImageGenerationError("FLUX did not create the expected image")
                relative_path = output_path.relative_to(self.storage_root).as_posix()
                images.append(
                    ImageAsset(
                        scene_index=index,
                        prompt=scene.image_prompt,
                        seed=scene_seed,
                        path=relative_path,
                        url=f"/media/{relative_path}",
                    )
                )
        except Exception:
            shutil.rmtree(output_dir, ignore_errors=True)
            raise

        return ImageGenerateResponse(job_id=job_id, images=images)

