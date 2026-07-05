# Heretic AI Studio

## Vision

Build a complete self-hosted AI Creative Studio capable of generating professional marketing content from a single prompt.

Instead of only creating videos, the platform becomes an all-in-one AI content production suite.

```
Prompt → AI Story Planner → Script, Storyboard, Voice, Images, Video, Music, Subtitles, Podcast, Blog, Social Media, Commercial, Vlog, Product Ads, Presentation, Marketing Assets
```

---

## Mission

Provide businesses, creators, churches, agencies, educators, and entrepreneurs with a single platform to generate high-quality marketing content without requiring professional editing skills.

---

## Core Features

### AI Studio

- Prompt to Video
- Prompt to Image
- Prompt to Podcast
- Prompt to Voice
- Prompt to Commercial
- Prompt to Vlog
- Prompt to Story
- Prompt to Presentation
- Prompt to Blog
- Prompt to Social Media Post
- Prompt to Animation
- Prompt to Marketing Campaign

---

## AI Video Generator

Supports

- YouTube
- TikTok
- Facebook
- Instagram
- LinkedIn
- Commercial Ads
- TV Ads
- Product Promotion
- Company Introduction
- Church Ministry
- Educational Videos
- Training Videos
- Explainer Videos
- Documentary
- Movie Trailer

---

## AI Image Studio

- Text to Image
- Image to Image
- Character Consistency
- Product Photography
- AI Logo
- AI Banner
- AI Poster
- AI Thumbnail
- AI Illustration
- AI Background Removal
- AI Upscaler

---

## AI Voice Studio

- Voice Cloning
- Emotional Voice
- Multi-language
- Text to Speech
- Speech to Text
- Podcast Narration
- Audiobook Narration
- Commercial Voice
- Character Voices
- AI Singer (Future)

---

## AI Podcast Studio

Generate complete podcasts.

- Intro
- Outro
- Background Music
- Multi Speaker
- Interview
- Discussion
- Audio Cleanup
- Publish to Spotify

---

## AI Marketing Studio

Create

- Facebook Ads
- Google Ads
- TikTok Ads
- Instagram Reels
- YouTube Shorts
- Email Marketing
- Sales Copy
- Landing Pages
- Product Descriptions
- Call to Action
- Promotional Videos

---

## AI Brand Studio

Store reusable brand assets.

- Logos
- Fonts
- Brand Colors
- Company Information
- Product Catalog
- Voice Profiles
- Brand Guidelines
- Marketing Templates

---

## AI Character Studio

Create reusable AI characters.

- Character reference sheets
- Storyboard reference panels
- Character Memory
- Facial Consistency
- Clothing Consistency
- Voice Consistency
- Animation
- Expressions
- Multiple Angles

---

## AI Workflow Engine

```
Idea → Prompt → AI Planning → Script → Storyboard → Voice → Images → Animation → Video → Subtitles → Music → Export
```

---

## Web Application

- Responsive
- Drag & Drop
- Timeline Editor
- Storyboard Editor
- Scene Editor
- Prompt History
- Version Control
- Team Collaboration
- Dark Mode

---

## Mobile App

iOS & Android

Supports

- Generate videos
- Voice recording
- Voice cloning
- Camera upload
- Image upload
- Project management
- Background rendering
- Push notifications

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

- Drag-and-drop local Asset Library
- Image, audio, and video uploads
- Scene-level asset assignment and reordering
- Media previews, thumbnails, and metadata extraction
- Research-material uploads and text extraction
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

- [x] Scene-timed SRT subtitle engine
- [x] FFmpeg image, audio, and subtitle assembly
- [x] Local MP4 playback and download UI
- [ ] Validate a full video using real Phase 2 and Phase 3 assets

### Phase 5

- [x] In-memory development queue and job-status API
- [x] Redis/RQ production queue with JSON serialization
- [x] Redis Docker Compose service and health check
- [x] Frontend, backend, Redis, and video-worker containers
- [ ] Validate the Compose stack after Docker Desktop is installed
- [ ] Authentication
- [ ] Login, registration, and subscription pages

### Phase 6 - Asset Library

- [ ] Drag-and-drop multiple-file upload UI with progress
- [ ] Images: PNG, JPEG, and WebP
- [ ] Audio: WAV, MP3, and M4A
- [ ] Video: MP4, MOV, and WebM
- [ ] Stream large uploads directly to local storage
- [ ] Validate file signatures, MIME types, size, and duration
- [ ] Generate thumbnails and extract metadata with FFprobe
- [ ] Preview, reorder, remove, and assign assets to scenes
- [ ] Protect assets by user and workspace after authentication
- [ ] Add PDF, DOCX, and text research materials in a later increment

### Phase 7 - Character and Storyboard Studio

- [ ] Create reusable character profiles from original reference sheets
- [ ] Upload and organize storyboard panels through the Asset Library
- [ ] Define structured shots with duration, action, camera, dialogue, and SFX
- [ ] Link characters and reference assets to individual shots
- [ ] Generate reference-conditioned keyframes for visual consistency
- [ ] Add an image-to-video provider interface for shot animation
- [ ] Validate character, clothing, environment, and prop continuity
- [ ] Assemble animated shots with narration, SFX, subtitles, and transitions
- [ ] Validate the workflow on a supported accelerator host
- [ ] Add safeguards for original designs and licensed reference material

------------------------------------------------------------------------

## Planned Asset Library

The Asset Library will let users drag and drop their own images, narration,
music, video clips, and other source material into a project. Uploaded media
will remain local under `storage/assets/` and will use generated internal IDs
instead of trusting user-supplied filenames.

The first increment will support media files only:

- Multi-file drag and drop with per-file upload progress
- Image, audio, and video previews
- Scene assignment and asset ordering
- FFprobe duration, codec, dimensions, and file-size metadata
- Background thumbnail and media processing through the job queue
- Controlled download and preview endpoints rather than public file paths

Large files must be streamed instead of loaded fully into application memory.
The backend must validate actual file signatures and MIME types, apply
configurable limits, sanitize display names, and reject unsupported media.

PDF, DOCX, Markdown, and plain-text research materials will follow after the
media library is stable. That increment will add safe text extraction and
prompt-grounding behavior without treating uploaded documents as trusted
instructions.

------------------------------------------------------------------------

## Planned Character and Storyboard Studio

The Character and Storyboard Studio will turn reference sheets, storyboard
panels, and a story plan into consistent animated shots. Prompts alone are not
enough for reliable character continuity, so each shot will reference explicit
character and storyboard assets from the Asset Library.

Shot instructions will use structured data rather than a single unbounded
prompt. Example:

``` json
{
  "shot": 1,
  "duration_seconds": 3,
  "characters": ["luna", "bun"],
  "action": "Walk through the glowing forest",
  "camera": "Slow low-angle tracking shot",
  "dialogue": "Whoa... look at this place!",
  "sfx": ["forest ambience", "leaves rustling"],
  "reference_assets": ["character-sheet", "storyboard-panel-1"]
}
```

Planned workflow:

1. Upload original character sheets and storyboard panels.
2. Create reusable character profiles and continuity rules.
3. Generate a structured shot list with timing and camera direction.
4. Produce keyframes using a reference-conditioned image provider.
5. Animate approved keyframes through an image-to-video provider.
6. Check continuity across characters, clothing, props, and environments.
7. Add dialogue, narration, SFX, subtitles, and transitions.
8. Assemble and export the final MP4 through the existing FFmpeg pipeline.

The exact reference-conditioning and image-to-video models will remain
configurable provider integrations. Video generation must run on a supported
accelerator host and must not be presented as available on the current
CPU-only development laptop.

Reference uploads must be original, properly licensed, or otherwise authorized
for use. Product copy and prompts should describe the intended visual traits
directly instead of requesting imitation of a named studio, living artist, or
protected character.

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

### Phase 4 video rendering

Configure the shared FFmpeg executable in the backend `.env`:

``` dotenv
FFMPEG_COMMAND=C:\path\to\ffmpeg.exe
FFMPEG_TIMEOUT_SECONDS=900
```

`POST /api/v1/videos/render` accepts the video title, scene list, Phase 2 audio
assets, and Phase 3 image assets. Every scene must have exactly one audio file
and one image in matching order. The renderer normalizes them to 1280x720 at
30 FPS, pads or trims audio to the planned duration, embeds selectable English
subtitles in the MP4, and also returns the standalone SRT file.

### Phase 5 job queue

Long-running audio, image, and video operations use `/api/v1/jobs/audio`,
`/api/v1/jobs/images`, and `/api/v1/jobs/video`. Poll
`GET /api/v1/jobs/{job_id}` until the status becomes `finished` or `failed`.

Local development defaults to an in-memory queue and requires no additional
service. Jobs are not durable across backend restarts. For durable jobs, install
Docker Desktop and start the local-only Redis service:

``` powershell
docker compose up -d redis
docker compose ps
```

Configure `backend/.env`:

``` dotenv
QUEUE_BACKEND=redis
REDIS_URL=redis://127.0.0.1:6379/0
QUEUE_NAME=heretic
QUEUE_JOB_TIMEOUT_SECONDS=3600
```

Start a Windows-compatible AI worker from `backend/` in another terminal. It
uses the host F5-TTS and FLUX runtimes while the container worker handles video:

``` powershell
.\.venv\Scripts\rq.exe worker -u redis://127.0.0.1:6379/0 -S json -w rq.worker.SpawnWorker heretic-audio heretic-images
```

Redis is bound to `127.0.0.1` by default. Do not expose this unauthenticated
development service to other networks.

### Docker deployment

The Compose stack builds the Next.js frontend and FastAPI backend, starts a
persistent Redis queue, and runs an FFmpeg video worker. Ollama remains on the
host and is reached through `host.docker.internal`. Generated assets are bind
mounted from the repository's `storage/` directory.

Prerequisites:

- Docker Desktop with access to drive D:
- Ollama running on the host with the configured model installed
- The Windows AI worker above for F5-TTS and FLUX jobs

Start and verify the stack:

``` powershell
docker compose up -d --build
docker compose ps
docker compose logs --tail 100 backend video-worker
```

Open `http://localhost:3000`. Stop containers without deleting Redis data:

``` powershell
docker compose down
```

All published ports bind to `127.0.0.1`. The backend and worker run as non-root
users with read-only root filesystems; only `/tmp` and the mounted `storage/`
directory are writable.

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
