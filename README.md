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

- FLUX.1-dev

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

1.  User enters topic.
2.  LLM generates a 60-second script.
3.  F5-TTS synthesizes speech using the selected cloned voice.
4.  FLUX generates scene images.
5.  Subtitles are created from the script.
6.  FFmpeg assembles images, narration, subtitles, and optional music.
7.  User downloads the finished MP4.

------------------------------------------------------------------------

## Development Roadmap

### Phase 1

- Project setup
- Next.js UI
- FastAPI backend
- Ollama integration

### Phase 2

- F5-TTS integration
- Voice profile management

### Phase 3

- FLUX image generation
- Scene planning

### Phase 4

- FFmpeg renderer
- Subtitle engine

### Phase 5

- Queue system
- Docker deployment
- Authentication

------------------------------------------------------------------------

## Stretch Goals

- Talking avatar
- AI B-roll selection
- AI thumbnail generation
- Social media publishing
- Mobile app
- SaaS deployment

------------------------------------------------------------------------

## License

MIT License
