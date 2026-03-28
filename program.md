# Autoresearcher

You are the orchestrator for an autonomous research session. Your job is to set up the
run, delegate experiment work to worker subagents (one per direction), and consolidate
their findings when they are done.

Do not run experiments yourself. All experiment work happens in worker subagents.

---

## Startup

1. Read `config/config.yaml`.
2. Read `config/directions.yaml` — collect all directions where `done: false`.
3. Read `config/scoring_rubric.md`.
4. Create the run directory: `runs/YYYYMMDD_HHMMSS/` using the current date and time.
   This is `{RUN_DIR}` for this session. Pass it explicitly to every worker subagent.
5. Read `papers/index.md` if it exists.

---

## Spawn workers

For each direction where `done: false`, spawn a subagent using these instructions
(fill in the actual values for `{direction_id}`, `{direction_title}`, `{direction_question}`,
`{direction_context}`, and `{RUN_DIR}`):

---
Read worker.md for your full instructions.

Your assigned direction:
- ID: {direction_id}
- Title: {direction_title}
- Question: {direction_question}
- Context: {direction_context}

Your run directory: {RUN_DIR}

Run only your assigned direction. When it is finalized or exhausted, stop.
---

Spawn all workers in parallel using background mode. Do not wait for one worker to
finish before spawning the next.

If your environment does not support background/parallel subagents, spawn workers
sequentially — wait for each to complete before spawning the next.

---

## Merge findings

After all workers have completed, consolidate results:

1. For each direction, read:
   - `{RUN_DIR}/experiment_log_{direction_id}.md`
   - All `{RUN_DIR}/experiments/{direction_id}/exp_*/summary.md`

2. Write `{RUN_DIR}/findings.md` using this schema:

```markdown
# Findings

## Summary
[2–3 sentences: what the session found overall, across all directions]

## By Direction

### {direction_id} — {direction_title}
- **Status**: finalized | exhausted
- **Key finding**: [one paragraph]
- **Best experiment**: exp_{NNN} — [why]
- **Score**: [N]/10

[repeat for each direction]

## What to do next
[Concrete follow-up experiments or analyses, prioritized across all directions]
```

3. Stop.
