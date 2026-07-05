"""Isolated FLUX inference entrypoint used by the FastAPI backend."""

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate one image with FLUX")
    parser.add_argument("--model", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--device", default="cuda", choices=("cuda", "mps"))
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    parser.add_argument("--steps", type=int, default=4)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--cache-dir", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        import torch
        from diffusers import FluxPipeline
    except ImportError as exc:
        raise SystemExit(
            "FLUX runtime is incomplete; install torch, diffusers, transformers, and accelerate"
        ) from exc

    if args.device == "cuda" and not torch.cuda.is_available():
        raise SystemExit("CUDA is not available in the configured FLUX runtime")
    if args.device == "mps" and not torch.backends.mps.is_available():
        raise SystemExit("MPS is not available in the configured FLUX runtime")

    dtype = torch.bfloat16
    pipeline = FluxPipeline.from_pretrained(
        args.model,
        torch_dtype=dtype,
        cache_dir=args.cache_dir,
    ).to(args.device)
    is_schnell = args.model.lower().endswith("schnell")
    image = pipeline(
        prompt=args.prompt,
        width=args.width,
        height=args.height,
        num_inference_steps=args.steps,
        guidance_scale=0.0 if is_schnell else 3.5,
        max_sequence_length=256 if is_schnell else 512,
        generator=torch.Generator(device="cpu").manual_seed(args.seed),
    ).images[0]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.output, format="PNG")


if __name__ == "__main__":
    main()

