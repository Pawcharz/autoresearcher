# autoresearcher

experiment progression

A framework for autonomous experiment execution on ML research codebases. Define research directions, point it at your code, and let it run. Workers explore the codebase, write and execute experiments, self-score results against your rubric, and iterate until they find something significant. Output: a findings report with quantified results, counterarguments, and prioritized follow-ups.

Works with Claude Code, Cursor, and Codex — any subscription, zero extra cost.

---

## How it works

architecture diagram

You define research directions — specific, falsifiable questions about your codebase. autoresearcher spawns one worker agent per direction. Each worker explores the code, writes and runs experiments, self-scores results against a rubric you provide, and keeps iterating until a finding clears the significance threshold or the experiment budget runs out. Everything is coordinated through plain markdown files. No Python orchestrator, no API calls — the markdown files *are* the program.

### Papers pipeline

Drop PDFs into `papers/raw/`, run `Read papers/ingest.md and begin`, and each paper gets distilled into three tiers that workers reference during experiments — from a one-liner index loaded at startup, to a condensed full-text loaded when directly relevant.

papers pipeline

---

## Example output

> **Does accuracy become misleading under class imbalance?**
>
> **Key finding:** Accuracy becomes misleading at ratio 5:1, where model accuracy (82.67%) converges with the majority-class baseline (83%). At ratio 10:1, F1 collapses below 0.1 while accuracy remains above 90% — complete decoupling between accuracy and minority-class detection.
>
> **Actionable insight:** Switch to AUC or threshold-optimized F1 above ratio 5:1. For ratios 10–20, threshold tuning recovers F1 (6.6× gain at ratio 10) but always trades accuracy. Above 50:1, threshold tuning alone is insufficient (max F1 < 0.15).
>
> Score: 8/10  ·  exp_001 replicated by exp_002

> **Can threshold tuning recover performance at high imbalance?**
>
> **Key finding:** At ratio 20:1, lowering threshold 0.5 → 0.10 recovers F1 from 0 to 0.31. Optimal threshold correlates with minority fraction (r=0.71) but ultimately depends on probability distribution overlap — at 100:1, distributions overlap so heavily that no threshold recovers F1 above 0.04.
>
> Score: 8/10  ·  exp_001 replicated by exp_004

*Example output from the included demo. Your run produces* `runs/{timestamp}/findings.md`*.*

---

## Try it in 5 minutes

```bash
git clone https://github.com/YOUR_USERNAME/autoresearcher
cd autoresearcher
pip install numpy scikit-learn matplotlib
python research_target/train.py      # precompute demo artifacts (~2 sec)
```

Open Claude Code (or Cursor, or Codex) in this directory and say:

```
Read program.md and begin.
```

The demo has 3 research directions exploring class imbalance — a problem with a known answer, so you can judge whether the agent's findings are correct.

---

## Use it on your own research

**1. Point it at your codebase**

```bash
ln -s /path/to/your/codebase research_target
# or set research_target_path in config/config.yaml
```

**2. Define research directions** — `config/directions.yaml`

```yaml
directions:
  - id: my_direction
    title: "Does X cause Y?"
    question: >
      Specific, falsifiable question. What would a positive result look like?
    context: >
      What data exists. Which functions to call. Known baselines to beat.
```

**3. Set your scoring rubric** — `config/scoring_rubric.md`

Describe what a publishable finding looks like for your paper and venue. Workers use this to self-score every experiment and decide when to stop.

**4. (Optional) Add papers** — drop PDFs into `papers/raw/`, then:

```
Read papers/ingest.md and begin.
```

Workers reference the paper database when designing experiments.

**5. Run experimentation pipeline**

```
In new session: "Read program.md and begin."
```

---

## Design notes

**No API credits.** The markdown files drive the built-in tool loop of your coding assistant. No `anthropic.Anthropic()`, no separate billing.

**Isolated context per direction.** Each worker runs in a fresh context window. Parallel directions don't share context or inflate each other's cost.

**Mandatory skepticism.** Every experiment requires a counterargument section before a score is assigned. The worker argues against its own findings — generic objections are rejected by the rubric.

**Safe by default.** Experiments are tiered: read-only (default) → runtime monkey-patching → file copies in `patches/`. `research_target/` is never modified unless you allow it in config.

**Paper-agnostic.** All domain knowledge lives in `config/` and `papers/`. Clone and reconfigure for a different project.

---

## Compatibility


| Tool        | Parallel workers | Method                  |
| ----------- | ---------------- | ----------------------- |
| Claude Code | ✓                | Agent Teams / Task tool |
| Cursor      | ✓                | Background agents       |
| Codex       | ✓                | Explicit spawning       |


Works on Linux, macOS, and Windows. Project-scoped command allowlists included for all three tools (`.claude/settings.json`, `.cursor/cli.json`, `.codex/rules/default.rules`).

---

## Inspiration

Andrej Karpathy's [autoresearch](https://github.com/karpathy/autoresearch) demonstrated the idea of running an AI coding tool autonomously on a research codebase. autoresearcher extends this to multi-direction parallel research on any codebase, with structured output and no additional API costs.

---

## License

MIT