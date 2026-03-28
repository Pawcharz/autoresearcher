# Paper Ingestion

This is a one-shot task. Run it in a **separate agent session** from the main research loop
to avoid contaminating the experiment context with full paper content.

**How to invoke**: open a new Claude Code / Cursor session in this repo and say:
"Read papers/ingest.md and ingest [filename in papers/raw/]"

---

## Task

Given a paper in `papers/raw/`, produce two output files:

### 1. Overview — `papers/overview/{paper_id}.md`

Use the template at `papers/overview/_template.md`.

Rules:
- `paper_id` must match the raw filename without extension (e.g. `attention_2017`).
- The **Method** field must be specific enough to judge relevance without reading more.
  Avoid generic descriptions like "a transformer-based approach." Name what is novel.
- The **Useful for** field should name concrete experiment types, not broad topics.
- Total length: 10–15 lines maximum.

### 2. Condensed version — `papers/condensed/{paper_id}.md`

Use the template at `papers/condensed/_template.md`.

Rules:
- Target length: 10–20% of the original. For a 10-page paper, aim for ~1–2 pages.
- Preserve verbatim: all algorithms, pseudocode, equations, implementation details,
  hyperparameter tables, and result tables. Never paraphrase these.
- Compress to a few sentences or drop entirely: abstract, introduction, related work,
  motivation paragraphs, discussion, conclusion, acknowledgements.
- The condensed version must be sufficient for someone to implement the method
  without referring back to the original.

---

## Verification

Before finishing, check:
- [ ] `paper_id` matches across both files and the raw filename.
- [ ] Overview is ≤15 lines.
- [ ] Condensed version contains no paraphrased equations or pseudocode.
- [ ] "Useful for" in the overview is specific, not generic.
