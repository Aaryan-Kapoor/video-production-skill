# Changelog

## 0.2.0 - 2026-06-17

- First public release.
- Wired Kokoro TTS into the skill via a portable `synth_kokoro.py` helper (`KOKORO_PYTHON`/`KOKORO_TTS_DIR`/`KOKORO_VOICE`/`KOKORO_LANG_CODE`), with per-segment WAVs, normalized voiceover, and `timings.json`.
- Added `INSTALL_FOR_AGENTS.md`, a step-by-step guide for AI agents to install the skill into their skills directory, and promoted it in the README.
- Replaced demo clips with real generated showcase videos (repo intro, GenLIP and ClawMark paper walkthroughs) including source notes and verification logs.

## 0.1.0 - 2026-05-04

- Initial private release of `video-production`.
- Added portable workspace helpers for initializing, archiving, and optionally hosting video jobs.
- Added source playbooks, high-effort production standards, packaged `.skill` and `.zip` artifacts, and README showcase videos.
