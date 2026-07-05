# AI Video Generator (Open Source)

## Vision

Build a self-hosted AI-powered web application that generates 30--60
second videos from a single prompt.

Pipeline:

Prompt → LLM Script → Voice Clone (TTS) → AI Images → Video Assembly →
Subtitles → MP4

------------------------------------------------------------------------

## Goals

- 100% self-hosted
- Open-source AI models
- Modern web interface
- One-click video generation
- Extensible architecture
- Optional GPU acceleration
- Containerized Web app for future SaaS

------------------------------------------------------------------------

## Tech Stack

### Frontend

- Next.js
- React
- Tailwind CSS
- TypeScript

### Backend

- FastAPI
- Python 3.12
- Celery (optional)
- Redis (job queue)

### AI Models

#### LLM

- Ollama
- Qwen 3 (default)
- Llama 3 (optional)

#### Text-to-Speech

- F5-TTS

#### Image Generation

- FLUX.1-schnell (default, Apache-2.0)
- FLUX.1-dev (optional, non-commercial license)

#### Optional Talking Avatar

- LivePortrait

### Video

- FFmpeg
- OpenCV (optional)

### Storage

- Local filesystem
- SQLite (development)
- PostgreSQL (production)

------------------------------------------------------------------------

## MVP Features

- Prompt input
- AI script generation
- Voice cloning
- Voice generation
- AI image generation
- Subtitle generation
- Automatic video assembly
- Download MP4

------------------------------------------------------------------------

## Future Features

- Multiple voice profiles
- YouTube export
- TikTok format
- Background music
- Timeline editor
- Multi-language support
- API access
- Team workspaces

------------------------------------------------------------------------

## Project Structure

``` text
ai-video-generator/

├── frontend/
│   ├── app/
│   ├── components/
│   ├── hooks/
│   ├── lib/
│   └── public/
│
├── backend/
│   ├── api/
│   ├── services/
│   │   ├── llm/
│   │   ├── tts/
│   │   ├── image/
│   │   ├── subtitle/
│   │   ├── video/
│   │   └── workflow/
│   ├── workers/
│   ├── models/
│   └── utils/
│
├── storage/
│   ├── scripts/
│   ├── voices/
│   ├── images/
│   ├── videos/
│   └── cache/
│
├── docker/
├── docs/
├── scripts/
└── docker-compose.yml
```

------------------------------------------------------------------------

## Workflow

1. User enters topic.
2. LLM generates a 60-second script.
3. F5-TTS synthesizes speech using the selected cloned voice.
4. FLUX generates scene images.
5. Subtitles are created from the script.
6. FFmpeg assembles images, narration, subtitles, and optional music.
7. User downloads the finished MP4.

------------------------------------------------------------------------

## Development Roadmap

### Phase 1

- [x] Project setup
- [x] Next.js prompt and structured scene UI
- [x] FastAPI backend
- [x] Ollama integration
- [x] Structured video plan with exact scene durations
- [x] Backend and frontend automated tests

### Phase 2

- [x] F5-TTS CLI adapter
- [x] Local voice profile API and storage
- [x] Per-scene narration API and audio playback UI
- [x] Install FFmpeg and a device-matched F5-TTS runtime
- [x] Validate real synthesis with reference audio

### Phase 3

- [x] Isolated FLUX inference adapter
- [x] Per-scene image generation API and local storage
- [x] Deterministic seeds and 16:9 image preview UI
- [ ] Install and validate FLUX on a supported accelerator host

### Phase 4

- FFmpeg renderer
- Subtitle engine

### Phase 5

- Queue system
- Docker deployment
- Authentication
- Login, registration, and subscription pages

------------------------------------------------------------------------

## Stretch Goals

- Voice cloning
- Speech with real emotion
- Talking avatar
- AI B-roll selection
- AI thumbnail generation
- Social media publishing
- Mobile app
- SaaS deployment

------------------------------------------------------------------------

## Local Development

Prerequisites: Python 3.12, Node.js 20.9 or newer, and Ollama with the
configured model available locally.

Backend (PowerShell):

``` powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

Frontend (a second PowerShell terminal):

``` powershell
cd frontend
npm install
Copy-Item .env.example .env.local
npm run dev
```

Verify the API at `http://127.0.0.1:8000/health` and open the UI at
`http://localhost:3000`.

Run the Phase 1 checks before committing changes:

``` powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -q

cd ..\frontend
npm run test
npm run lint
npm run build
```

### Phase 2 TTS configuration

F5-TTS runs as a separate local runtime so its PyTorch and accelerator
dependencies do not destabilize the FastAPI environment. Install FFmpeg and
F5-TTS using the device-specific instructions in the
[official F5-TTS repository](https://github.com/SWivid/F5-TTS). Then configure
the backend `.env`:

``` dotenv
F5_TTS_COMMAND=C:\path\to\f5-tts_infer-cli.exe
F5_TTS_MODEL=F5TTS_v1_Base
F5_TTS_DEVICE=cpu
F5_TTS_TIMEOUT_SECONDS=900
```

Set `F5_TTS_DEVICE` to the accelerator supported by the installed PyTorch
build. CPU-only generation is supported but may take several minutes per
scene. Keep model caches on a drive with sufficient free space. Reference
recordings should be shorter than 12 seconds and include an exact transcript;
see the [official inference guidance](https://github.com/SWivid/F5-TTS/blob/main/src/f5_tts/infer/README.md).

Phase 2 API flow:

1. `POST /api/v1/voices` with a voice name, transcript, and reference audio.
2. `GET /api/v1/voices` to list local profiles.
3. `POST /api/v1/audio/generate` with a voice profile ID and scene list.
4. Play generated WAV files from the returned local `/media/...` URLs.

### Phase 3 image configuration

The default model is `FLUX.1-schnell` because its Apache-2.0 license permits
commercial use. `FLUX.1-dev` is optional and uses a non-commercial model
license. Run the image model in a separate environment on a supported CUDA or
MPS host; full FLUX components require substantially more memory than the
FastAPI server.

Install `torch`, `diffusers`, `transformers`, and `accelerate` in that isolated
environment, accept the model access conditions on Hugging Face, and configure
the backend `.env` without committing access tokens:

``` dotenv
FLUX_PYTHON_COMMAND=C:\path\to\flux-runtime\python.exe
FLUX_SCRIPT=..\scripts\flux_infer.py
FLUX_MODEL=black-forest-labs/FLUX.1-schnell
FLUX_DEVICE=cuda
FLUX_STEPS=4
FLUX_TIMEOUT_SECONDS=1800
FLUX_CACHE_DIR=D:\path\to\model-cache
```

`POST /api/v1/images/generate` accepts the Phase 1 scene list, dimensions, and
a base seed. It generates one local PNG per scene and returns `/media/images/...`
URLs for preview and later video assembly.

------------------------------------------------------------------------

## Git and GitHub Setup

### Install and configure Git on Windows

``` powershell
winget install --id Git.Git --exact
git --version
```

Restart the terminal after installation. Configure your identity for this
repository. When GitHub email privacy is enabled, copy your GitHub-provided
`noreply` address from <https://github.com/settings/emails>.

``` powershell
git config user.name "YOUR_GITHUB_USERNAME"
git config user.email "YOUR_GITHUB_NOREPLY_EMAIL"
git config --get user.name
git config --get user.email
```

These commands use repository-local configuration. Add `--global` only if the
same identity should apply to every repository on the computer.

### Clone the existing repository

``` powershell
git clone https://github.com/moises0746/heretic-ai.git
cd heretic-ai
```

### Connect an existing local project

Run these commands from the project root only when it is not already connected
to GitHub:

``` powershell
git init
git branch -M main
git remote add origin https://github.com/moises0746/heretic-ai.git
git remote -v
```

If `origin` already exists but has the wrong URL, correct it with:

``` powershell
git remote set-url origin https://github.com/moises0746/heretic-ai.git
```

### First push

Review the staged files before committing. Local `.env` files, virtual
environments, dependencies, and generated artifacts must remain excluded by
`.gitignore`.

``` powershell
git add .
git status
git commit -m "Initial project setup"
git push -u origin main
```

### Pull and push routine changes

Pull before starting work. `--ff-only` prevents Git from creating an
unexpected merge commit.

``` powershell
git pull --ff-only origin main
```

After making and validating changes:

``` powershell
git add .
git status
git commit -m "Describe the change"
git push origin main
```

### Fix an email privacy rejection

If GitHub rejects a new repository's first push because existing local commits
contain a private email, set the correct `noreply` address and rewrite the
local commits before retrying:

``` powershell
git config user.email "YOUR_GITHUB_NOREPLY_EMAIL"
git rebase --root --exec "git commit --amend --no-edit --reset-author"
git log --format="%h %an <%ae>"
git push origin main
```

Rewriting published history requires coordination and a force push. Do not use
this procedure on commits already shared with other contributors.

------------------------------------------------------------------------

## License

MIT License
