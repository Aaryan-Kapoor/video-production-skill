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

## Generic agents

Load `skills/video-production/SKILL.md` as an instruction file and keep `scripts/` plus `references/` available relative to it.
