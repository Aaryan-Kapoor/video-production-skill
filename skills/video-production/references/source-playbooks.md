# Source Playbooks for Video Production

## Research paper / arXiv / Hugging Face paper
1. Fetch metadata and PDF/source page. Use official paper page when possible.
2. Extract text (`pdftotext -layout`) and page images (`pdftoppm`) for figures/tables.
3. Identify must-show figures, tables, equations, and results.
4. Ask a sub-agent to produce a video brief when the paper is long or technical.
5. Build source-grounded charts from reported numbers instead of relying only on screenshots.
6. Include caveats: version/peer-review state, assumptions, scope limits, implementation constraints.

## Product / project walkthrough
1. Gather the product page, repository, docs, changelog, screenshots, or demo data the user wants covered.
2. Identify the audience, promise, workflow, differentiators, limitations, and concrete proof points.
3. Prefer showing real UI, diagrams, traces, charts, or before/after examples over generic stock visuals.
4. Keep claims source-grounded and record source provenance in the manifest.

## General topic video
1. Decide whether the facts are stable. Browse for current/unstable topics.
2. Build an outline from first principles and add concrete examples.
3. Prefer original diagrams/animations over generic web images.
4. Cite or mention sources in the video only when it helps credibility; keep full source list in the job manifest/notes.

## Daily summary video
1. Create a scheduled/durable job if the user wants recurrence.
2. Pull data from first-party tools, workspace sources, and web sources as appropriate for the requested briefing.
3. Keep the video short unless the user asks for depth: usually 2-5 minutes.
4. Archive every daily output in backups by date.
