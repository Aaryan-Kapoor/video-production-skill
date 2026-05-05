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
- `KOKORO_PYTHON`: Python executable for an environment where `import kokoro` works. The Kokoro helper re-execs through this interpreter.
- `KOKORO_TTS_DIR`: optional local Kokoro checkout to prepend to `PYTHONPATH`.
- `KOKORO_VOICE`: default Kokoro voice, for example `af_heart`.
- `KOKORO_LANG_CODE`: Kokoro language code. Defaults to `a`.
- `KOKORO_SPEED`: optional speaking speed. Defaults to `1.0`.

The bundled Kokoro script is `skills/video-production/scripts/synth_kokoro.py`. It accepts a `segments.json` or plain text file, writes per-segment WAVs, combines `voice_raw.wav`, loudness-normalizes `voice.wav`, and emits `timings.json`. Validate a host with:

```bash
python skills/video-production/scripts/synth_kokoro.py --check
```

The skill intentionally avoids hardcoded user paths. If an environment has a preferred TTS or hosting stack, inject it through these environment variables or workspace-specific notes instead of editing the public skill.
