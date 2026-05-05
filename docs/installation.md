# Installation

## OpenClaw

Clone this private repo, then copy the skill into a workspace:

```bash
git clone https://github.com/Aaryan-Kapoor/video-production-skill.git
mkdir -p /path/to/openclaw-workspace/skills
cp -R video-production-skill/skills/video-production /path/to/openclaw-workspace/skills/
```

Start a new OpenClaw session so the skill snapshot reloads.

## Claude / generic AgentSkills upload

Use `dist/video-production.zip` or `dist/video-production.skill`. The archive contains one root folder named `video-production/` with `SKILL.md`, `scripts/`, and `references/`.

## Claude Code local development

Clone the repo and point your agent at the `skills/` directory or copy `skills/video-production` into your local skills folder.

## Gemini CLI

```bash
gemini skills install ./skills/video-production
```

## Kokoro voiceover setup

The skill includes a portable Kokoro helper at `skills/video-production/scripts/synth_kokoro.py`. Install Kokoro in the active Python environment, or point the helper at an existing environment:

```bash
# Option A: active environment
python -m pip install kokoro
# Install system espeak-ng through your OS package manager if Kokoro requires it.

# Option B: separate Kokoro environment
export KOKORO_PYTHON=/path/to/kokoro-env/bin/python
export KOKORO_TTS_DIR=/path/to/kokoro/repo   # optional local checkout
export KOKORO_VOICE=af_heart

python skills/video-production/scripts/synth_kokoro.py --check
```

Run synthesis from a job folder with:

```bash
python /path/to/skills/video-production/scripts/synth_kokoro.py src/segments.json --out audio
```

Expected outputs: `audio/segments/*.wav`, `audio/voice_raw.wav`, normalized `audio/voice.wav`, and `audio/timings.json`.

## Generic agents

Load `skills/video-production/SKILL.md` as an instruction file and keep `scripts/` plus `references/` available relative to it.
