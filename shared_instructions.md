# Background

- Project: VideoGen agency producing researched scripts, voiceovers, code snapshots, images, and final videos.
- Audience/brand: _Add brand voice, tone, and safety rules here._
- Deliverables: Voiceovers (mp3), code snapshots (PNG), images (per prompt) under `outputs/`; final videos should be written to `/mnt/video_final/<filename>` (ask user to ensure the directory exists; do not create it yourself).

# Collaboration Norms

- Manager is entry point and approves work; Research Agent handles web research; Assets Generator produces media; Video Editor runs ffmpeg shell edits and writes finals to `/mnt/video_final/<filename>` when available.
- Cite sources for research; include file paths for generated assets.
- Avoid creating or using `files/` folders; keep work inside `outputs/` and agent directories.

# Quality Bar

- Factual summaries with links.
- Assets match requested format, style, and path.
- Explicitly flag missing inputs, API keys, or installation needs (e.g., Playwright browsers).
