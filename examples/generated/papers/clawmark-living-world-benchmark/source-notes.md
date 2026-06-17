# Source Notes: ClawMark technical showcase remake

Selected paper: **ClawMark: A Living-World Benchmark for Multi-Turn, Multi-Day, Multimodal Coworker Agents** (`arXiv:2604.23781v1`, submitted 2026-04-26).

Primary/official sources used:
- arXiv abstract/PDF: https://arxiv.org/abs/2604.23781 and https://arxiv.org/pdf/2604.23781
- Official project site: https://claw-mark.com/
- Official GitHub repository archive: https://github.com/evolvent-ai/ClawMark

Grounded claims used in the video:
- ClawMark evaluates persistent coworker agents in multi-turn, multi-day workflows where environment state changes independently between turns.
- The release reports 100 tasks across 13 professional scenarios, 87 in-task roles, five sandboxed services, 1,072 raw multimodal artifacts, and 1,537 deterministic Python checkers.
- Scoring uses deterministic post-turn service-state checkers, not LLM-as-judge; weighted score and strict Task Success answer different questions.
- Leaderboard values are recreated from Table 3: Sonnet 4.6 75.8 weighted / 14.0 strict; Opus 4.6 74.6 / 20.0; GPT-5.4 high 72.0 / 9.0; Kimi K2.6 68.4 / 7.0; Gemini 3.1 Pro Preview 68.2 / 8.0; Qwen 3.6 Plus 57.2 / 5.0; Kimi K2.5 56.0 / 0.0.
- Failure-mode chart is recreated from Table 5: silent-change detection 56.5%, backend writeback 53.6%, cross-source consistency 34.0%, deliverable correctness 31.4%, evidence extraction 23.6%, compliance guardrail 21.5%.
- Actual task example is grounded in the public repository file `tasks/insurance/task5/task.py`: enterprise property fire claim assessment, staged Monday-Friday, with filesystem/email/Notion/Sheets/calendar services, two red-line checkers, and payout-checker details.

Caveats preserved in narration:
- Main leaderboard is a single full sweep per model; narrow ranking gaps should be read cautiously.
- Stability reruns are reported for Kimi K2.6 and GPT-5.4, not every model.
- EDA has one task, so that scenario row is case-level evidence rather than a stable domain trend.
- The benchmark is best treated as a diagnostic stress test for state refresh, backend writeback, multimodal evidence handling, and compliance constraints, not as a final universal model ranking.

Production notes:
- Narration generated with real Kokoro TTS via `/home/cbak/clawd/projects/archived_projects/ai-podcast/tts-kokoro/.venv/bin/python` and the repo `synth_kokoro.py` script.
- Visuals are recreated charts/diagrams/source-code callouts from the paper and public repository, not promotional headline cards.
