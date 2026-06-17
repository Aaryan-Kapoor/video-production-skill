# Install For Agents

You are an AI coding agent (Claude Code, OpenClaw, Gemini CLI, or similar). Read this
entire file, then follow the steps to install the `video-production` skill into your
skills directory so you can produce end-to-end educational and explainer videos.

This skill turns you into a full-stack video producer: research → script → narration
(TTS) → Manim/ffmpeg visuals → render → QC → archive → deliver.

---

## Step 0: Identify your skills directory

Pick the install target that matches your runtime. If you are unsure, prefer the
user-level Claude Code directory.

| Runtime | Skills directory |
|---|---|
| Claude Code (user-level) | `~/.claude/skills/` |
| Claude Code (project-level) | `<repo>/.claude/skills/` |
| OpenClaw | `<workspace>/skills/` |
| Gemini CLI | managed by `gemini skills install` (Step 2B) |
| Generic agent | wherever you load skill folders from |

A correctly installed skill lives as a single folder named `video-production/`
containing `SKILL.md`, `scripts/`, and `references/`.

---

## Step 1: Get the skill files

Clone the repository to a temporary location:

```bash
git clone https://github.com/Aaryan-Kapoor/video-production-skill.git /tmp/video-production-skill
```

If `git` is unavailable, download and unzip the prebuilt archive instead —
`dist/video-production.zip` already contains a single root folder named
`video-production/`.

---

## Step 2A: Copy the skill into your skills directory

Replace `<SKILLS_DIR>` with the directory you chose in Step 0.

```bash
SKILLS_DIR="$HOME/.claude/skills"   # or your runtime's skills directory from Step 0
mkdir -p "$SKILLS_DIR"
cp -R /tmp/video-production-skill/skills/video-production "$SKILLS_DIR/"
```

Verify the layout:

```bash
ls "$SKILLS_DIR/video-production"
# Expect: SKILL.md  references  scripts
```

## Step 2B: Gemini CLI (alternative to 2A)

```bash
gemini skills install /tmp/video-production-skill/skills/video-production
```

---

## Step 3: Reload so the skill registers

- **Claude Code:** the skill is discovered automatically; start a new session if it
  does not appear in the available skills list.
- **OpenClaw:** start a new session so the skill snapshot reloads.
- **Generic agent:** load `<SKILLS_DIR>/video-production/SKILL.md` as an instruction
  file and keep `scripts/` and `references/` available relative to it.

---

## Step 4: Check dependencies

The skill degrades gracefully, but check what is present and tell the user what is
missing. **Required:** Python 3.10+ and `ffmpeg`/`ffprobe`.

```bash
python3 --version          # need 3.10+
ffmpeg -version | head -1
ffprobe -version | head -1
```

**Recommended optional tools** (install only what the user's videos need):

- `manim` — animated diagrams, equations, charts, timelines
- Kokoro (or another TTS stack) — narration voiceover
- `poppler-utils` (`pdftotext`, `pdftoppm`) — paper/PDF asset extraction
- `Pillow` — image crops and compositing
- Tailscale — optional private hosting of the finished video

---

## Step 5: Wire up TTS voiceover (optional but recommended)

The skill ships a portable Kokoro helper. Either install Kokoro into the active Python
environment, or point the helper at an existing one. **Do not hardcode user-specific
install paths** — use the environment variables.

```bash
# Option A: active environment
python3 -m pip install kokoro      # install espeak-ng via your OS package manager if required

# Option B: point at a separate Kokoro environment
export KOKORO_PYTHON=/path/to/kokoro-env/bin/python
export KOKORO_TTS_DIR=/path/to/kokoro/repo   # optional local checkout
export KOKORO_VOICE=af_heart

# Validate Kokoro + ffmpeg availability:
python3 "$SKILLS_DIR/video-production/scripts/synth_kokoro.py" --check
```

If Kokoro is unavailable, fall back to any reliable TTS stack (OpenAI TTS, ElevenLabs,
platform-native), but preserve the same artifacts the skill expects: per-segment WAVs,
`audio/voice_raw.wav`, normalized `audio/voice.wav`, and `audio/timings.json`.

---

## Step 6: Confirm and report

Tell the user:

1. The skill is installed at `<SKILLS_DIR>/video-production`.
2. Required dependencies present/missing (`python3`, `ffmpeg`, `ffprobe`).
3. Which optional tools are available (Manim, TTS, poppler, Tailscale).
4. That they can now ask for things like *"make a video explaining this paper"* or
   *"turn these lecture notes into a pre-class video"*.

When a video request arrives, read `<SKILLS_DIR>/video-production/SKILL.md` and follow
its Standard Workflow. Treat a video request as a finished deliverable, not a plan.

---

## Cleanup

```bash
rm -rf /tmp/video-production-skill
```
