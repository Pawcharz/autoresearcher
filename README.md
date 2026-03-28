# Autoresearcher

A framework for autonomous overnight experiment execution on ML research codebases.
Works with Claude Code, Cursor, and Codex — no API credits required.

The user opens their AI coding tool, says "Read program.md and begin", and leaves it
running. The orchestrator spawns one worker subagent per research direction (in parallel
where supported, sequentially otherwise), each running in its own fresh context window.
Results are consolidated into a findings report at the end.

---

## How to use

**1. Point it at your research codebase**

Symlink your codebase into `research_target/`:
```bash
ln -s /path/to/your/codebase research_target
```
Or set `research_target_path` in `config/config.yaml` to an absolute path.

**2. Define your research directions**

Edit `config/directions.yaml`. Each direction is a focused research question.
Workers run in parallel — one worker per direction.

**3. Define your scoring rubric**

Edit `config/scoring_rubric.md` to describe what a publishable finding looks like
for your paper and target venue.

**4. (Optional) Add papers**

Drop PDFs into `papers/raw/`, then run a separate ingestion session:
```
Read papers/ingest.md and begin.
```
The ingestion session builds a searchable paper database workers can reference when
designing experiments.

**5. Open Claude Code (or Cursor, or Codex) and say:**
```
Read program.md and begin.
```

Leave it running. Workers explore the codebase, write and run experiments, score
findings, and log results. When all directions are done, the orchestrator writes
`runs/{timestamp}/findings.md`.

---

## Directory structure

```
autoresearcher/
├── program.md               ← entry point; read this to begin (orchestrator)
├── worker.md                ← worker instructions; spawned per direction
├── config/
│   ├── config.yaml          ← research target path, timeout, thresholds
│   ├── directions.yaml      ← research directions (one worker per direction)
│   └── scoring_rubric.md    ← what "interesting" means for your paper
├── papers/
│   ├── ingest.md            ← ingestion entry point (orchestrator)
│   ├── ingest_worker.md     ← per-paper worker; spawned by ingest.md
│   ├── index.md             ← one-liner per paper; loaded by workers at startup
│   ├── raw/                 ← original PDFs (gitignored)
│   ├── overview/            ← short structured overview per paper (gitignored)
│   └── condensed/           ← ~10-20% length distillation per paper (gitignored)
├── research_target/         ← symlink to your codebase (gitignored)
└── runs/                    ← auto-created; one subdir per session (gitignored)
    └── YYYYMMDD_HHMMSS/
        ├── experiment_log_{direction_id}.md
        ├── findings.md
        └── experiments/
            └── {direction_id}/
                └── exp_001/
                    ├── experiment.py
                    ├── outputs/
                    └── summary.md
```

---

## Design principles

**No API credits.** Uses the built-in tools of Claude Code, Cursor, or Codex — works
with any subscription. No `anthropic.Anthropic()` calls, no separate billing.

**Parallel workers, isolated context.** Each research direction runs in its own subagent
with a fresh context window. No quadratic context growth across directions.

**Filesystem coordination.** Workers write to their own `experiments/{direction_id}/`
subdirectory. No shared state, no write conflicts. The orchestrator reads results after
workers finish.

**Compact memory.** Each worker maintains a compact `experiment_log_{direction_id}.md`
(~100–200 tokens per entry, rolling 10-entry window) instead of relying on full
conversation history.

**Mandatory skepticism.** Every experiment summary requires a counterargument section
where the worker argues against its own findings before assigning a score.

**Paper-agnostic core.** All paper-specific knowledge lives in `config/` and `papers/`.
Clone and reconfigure to use on a different research project.

**1:1 mapping.** One repo instance = one research codebase = one config.
