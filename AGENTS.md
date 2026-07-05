# AGENTS.md

## Purpose
This repository is an open-source, self-hosted AI video generation app with a Next.js frontend and a FastAPI backend. Use this file to understand the overall architecture, avoid assumptions, and stay aligned with the project vision.

## Primary source of truth
- `README.md` contains the current project vision, tech stack, architecture, and roadmap.

## What this repo contains
- `frontend/` — Next.js + React + TypeScript + Tailwind UI
- `backend/` — FastAPI services, Python 3.12, AI model integrations, and worker logic
- `storage/` — local data directories for generated assets and caches
- `docker/` — deployment and self-hosting support
- `scripts/` — automation helpers

## Developer guidance
- Preserve the self-hosted goal: local AI models, local storage, and no unnecessary cloud dependencies.
- Keep backend logic modular: separate LLM, TTS, image, subtitle, and video steps.
- Prefer small, incremental changes that improve functionality or developer experience.
- If new files are added, keep naming consistent with `frontend/`, `backend/`, `storage/`, `docker/`, and `scripts/`.

## When you need to inspect before editing
- Search for package manifests or dependency files under `frontend/` and `backend/` before making environment or build changes.
- If the repository gains `package.json`, `pyproject.toml`, `requirements.txt`, or `docker-compose.yml`, use them as the authoritative build/test commands.

## Useful hints for AI agents
- The app is a pipeline: prompt → script → TTS → image generation → subtitles → video assembly.
- Target formats are local MP4 downloads and self-hosted deployment.
- Postpone major architecture decisions until package/config files exist and more code is available.

## Future customization suggestions
- Add `.github/copilot-instructions.md` with contributor-specific workflow once the repo defines exact setup and build commands.
- Add a repo skill for common tasks like `setup-dev-environment`, `run-frontend`, or `run-backend` when manifest files appear.
