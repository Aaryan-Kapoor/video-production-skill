# Security

This skill can instruct agents to run local scripts and media tooling. Treat any third-party skill as code:

- Review `SKILL.md` and `scripts/` before enabling.
- Do not place secrets, API keys, private source material, or personal data in the skill folder.
- Use `VIDEO_PRODUCTION_ROOT` to keep generated jobs outside sensitive repositories.
- Only host final files you intend to share.
- Prefer sandboxed/isolated agent runs for untrusted prompts or source material.
