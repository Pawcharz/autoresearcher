# Autoresearcher

A framework for autonomous overnight experiment execution on ML research codebases,
driven by Claude Code.

No API credits required. No Python orchestrator. The entry point is a single `program.md`
that instructs Claude to explore your codebase, run experiments, score findings, and
keep going until all research directions are exhausted.

---

## How to use

**1. Point it at your research codebase**

Symlink or copy your codebase into `research_target/`:
```bash
ln -s /path/to/your/codebase research_target
```
Or set `research_target_path` in `config/config.yaml` to an absolute path.

**2. Define your research directions**

Edit `config/directions.yaml`. Each direction is a focused research question Claude
will design and run experiments for.

**3. Define your scoring rubric**

Edit `config/scoring_rubric.md` to describe what a "good finding" looks like for
your paper and target venue.

**4. Open Claude Code and say:**
```
Read program.md and begin.
```

Leave it running. Claude will explore the codebase, write experiments, run them,
score findings, and log everything to `experiment_log.md`. When done, it writes
`findings.md`.

---

## Directory structure

```
autoresearcher/
├── program.md               ← Claude reads this and follows it
├── config/
│   ├── config.yaml          ← research target path and settings
│   ├── directions.yaml      ← your research directions
│   └── scoring_rubric.md    ← what "interesting" means for your paper
├── research_target/         ← symlink to your codebase (gitignored)
├── experiments/             ← auto-created per direction (gitignored)
│   └── {direction_id}/
│       └── exp_001/
│           ├── experiment.py
│           ├── outputs/
│           └── summary.md
├── experiment_log.md        ← compact running log Claude maintains (gitignored)
└── findings.md              ← consolidated findings written at the end (gitignored)
```

---

## Design principles

**No API credits.** Uses Claude Code's built-in tools — works with any Claude Code
or Cursor subscription.

**Compact memory.** Claude maintains `experiment_log.md` (~100–200 tokens per entry)
instead of relying on full message history. After 10 experiments the log is ~1,500
tokens flat.

**Mandatory skepticism.** Every experiment summary requires a counterargument section
where Claude argues against its own findings before assigning a score.

**Paper-agnostic core.** All paper-specific knowledge lives in `config/` only.
To use on a different project, clone and reconfigure — don't modify `program.md`.

**1:1 mapping.** One repo instance = one research codebase = one config.
