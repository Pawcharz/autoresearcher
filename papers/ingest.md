# Paper Ingestion Orchestrator

You are the ingestion orchestrator. Your job is to identify unprocessed papers, spawn
one worker subagent per paper, and update the index after all workers finish.

Do not process papers yourself. All per-paper work happens in worker subagents.

---

## Startup

1. Use your directory listing tool to list `papers/raw/`. Output the result explicitly
   before doing anything else. Do not infer or recall from memory — run the tool.

2. If `papers/raw/` contains no files: output "papers/raw/ is empty. Nothing to do."
   and stop.

3. For each file found, check whether both `papers/overview/{paper_id}.md` and
   `papers/condensed/{paper_id}.md` exist (`paper_id` = filename without extension).
   Output the full checklist — one line per paper showing which files exist and which
   are missing — before proceeding.

4. If all papers already have both output files: output "All papers already processed."
   and stop.

---

## Spawn workers

For each unprocessed paper, spawn a subagent using these instructions
(fill in the actual `{filename}` and `{paper_id}`):

---
Read papers/ingest_worker.md for your full instructions.

Your assigned paper:
- Filename: {filename}
- Full path to raw file: {absolute_path_to_raw_file}
- Paper ID: {paper_id} (filename without extension)
- Write overview to: {absolute_path_to_repo}/papers/overview/{paper_id}.md
- Write condensed to: {absolute_path_to_repo}/papers/condensed/{paper_id}.md
- Templates are at: {absolute_path_to_repo}/papers/overview/_template.md
  and {absolute_path_to_repo}/papers/condensed/_template.md
- Do NOT modify papers/index.md

Process only this paper. When done, stop.
---

Spawn all workers in parallel using background mode.

If your environment does not support background/parallel subagents, spawn workers
sequentially.

---

## Update index

After all workers have completed:

1. For each paper that was processed this session, read its
   `papers/overview/{paper_id}.md` and extract the `useful_for` field.

2. For each, append one line to `papers/index.md` after the
   `<!-- entries will appear below this line -->` comment:
   ```
   - {paper_id} | {title} ({venue} {year}) | {useful_for, copied verbatim from overview}
   ```
   Skip any paper that already has an entry in `papers/index.md`.

3. Report:
   - How many papers were processed this session.
   - List of paper IDs added to the index.
   - Any papers skipped (unreadable file, worker failed) — list with reason.
