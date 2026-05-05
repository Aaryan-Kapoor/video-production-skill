# Source Playbooks for Video Production

## Research paper / arXiv / Hugging Face paper
1. Fetch metadata and PDF/source page. Use official paper page when possible.
2. Extract text (`pdftotext -layout`) and page images (`pdftoppm`) for figures/tables.
3. Identify must-show figures, tables, equations, and results.
4. Ask a sub-agent to produce a video brief when the paper is long or technical.
5. Build source-grounded charts from reported numbers instead of relying only on screenshots.
6. Include caveats: version/peer-review state, assumptions, scope limits, implementation constraints.

## KSU / D2L class video
1. Load the `d2l` skill first; never scrape D2L with browser/Playwright.
2. Read the course `notes.md` and `sop.md` before course work.
3. For Calc II schedule/due-date questions, pull the latest weekly PDF from D2L first.
4. Save generated class artifacts under `ksu/courses/<course>/{assignments}/<assignment>/` when tied to an assignment; otherwise use the video-production workspace and link the course source in manifest.
5. For pre-class videos: extract learning objectives, definitions, examples, and likely pitfalls.

## General topic video
1. Decide whether the facts are stable. Browse for current/unstable topics.
2. Build an outline from first principles and add concrete examples.
3. Prefer original diagrams/animations over generic web images.
4. Cite or mention sources in the video only when it helps credibility; keep full source list in the job manifest/notes.

## Daily summary video
1. Create a scheduled/durable job if the user wants recurrence.
2. Pull data from first-party tools: D2L for courses, Google Workspace for calendar/email/docs when relevant, web for news/current events.
3. Keep the video short unless the user asks for depth: usually 2-5 minutes.
4. Archive every daily output in backups by date.
