# Portability Notes

Required:

- Python 3.10+
- ffmpeg and ffprobe

Recommended:

- Manim for animated diagrams and equations
- A TTS system such as Kokoro, OpenAI TTS, ElevenLabs, or local Piper
- poppler-utils for PDF extraction (`pdftotext`, `pdftoppm`)
- PIL/Pillow for crops and frame generation
- Tailscale only if you want private link hosting

Environment variables:

- `VIDEO_PRODUCTION_ROOT`: durable output directory. Defaults to `~/video-productions`.

The skill intentionally avoids hardcoded user paths. If an environment has a preferred TTS or hosting stack, document it outside the public skill or inject it through agent/workspace-specific notes.
