# VideoGen Agency

AI-powered media crew built on Agency Swarm (OpenAI Agents SDK) with three specialists:
- **Manager Agent** (entry point): scopes work, routes tasks, enforces quality, delivers final packages.
- **Research Agent**: live web research with citations and script/talking-point outlines.
- **Assets Generator**: voiceovers (ElevenLabs), ray.so code snapshots, and AI images.
- **Video Editor**: ffmpeg-based edits and renders via persistent shell commands (uses `/mnt/video_final/<filename>` for final outputs when available).

## What it can do
- Research any topic with fresh sources, summarize with links, and draft scripts.
- Generate multimedia: polished voiceovers, code snippet images, and AI visuals.
- Edit and render videos (trim/concat/overlay/transcode) with reproducible ffmpeg commands.
- Deliver organized outputs under `outputs/` and final videos to `/mnt/video_final/<filename>` (ask user to ensure the path exists).

## Agents, tools, models
- Model: `gpt-5.2` with medium reasoning for all agents.
- **Research Agent tools**: `WebSearchTool` (built-in).
- **Assets Generator tools**:
  - `GenerateVoiceoverTool` (custom ElevenLabs TTS; needs `ELEVENLABS_API_KEY`).
  - `RaySoSnapshotTool` (custom Playwright ray.so export; requires `python -m playwright install chromium` once).
  - `ImageGenerationTool` (built-in, OpenAI image models).
- **Video Editor tools**: `PersistentShellTool` for ffmpeg pipelines (non-destructive, scoped to project paths).

## Inputs & outputs
- Inputs: topic/goal, audience/tone, desired assets (voiceover script or text length, code snippet, image prompt), video edit specs (cuts, concat order, overlays, target resolution/codec/bitrate).
- Outputs: voiceovers (`outputs/voiceovers`), snapshots (`outputs/snapshots`), images (`outputs/images`), video intermediates (`outputs/video_edits`), finals `/mnt/video_final/<filename>` (only if the directory exists).

## Setup
1) Create `.env` with `OPENAI_API_KEY` and `ELEVENLABS_API_KEY`.
2) Install deps: `.venv/bin/pip install -r requirements.txt`
3) Install Playwright browser (for snapshots): `.venv/bin/python -m playwright install chromium`

## Run
- Terminal demo: `python agency.py`
- FastAPI (already wired in `main.py`): `python main.py` (serves on port 8080 by default).

## Usage tips
- Be explicit about style/voice: e.g., “warm, concise, 60–90s script,” “1080p 30fps, H.264 CRF 18,” “dark ray.so theme.”
- Ensure `/mnt/video_final` exists before requesting final renders there; otherwise provide an alternate path.
- For ffmpeg loops, ask the Video Editor to show commands and `ffprobe` summaries after each render.
