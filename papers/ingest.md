# Paper Ingestion

Run this in a **separate agent session** from the main research loop to avoid contaminating
the experiment context with full paper content.

**How to invoke**: open a new Claude Code / Cursor session in this repo and say:
"Read papers/ingest.md and begin."

Do not ask which papers to process. Do not stop between papers. Process all unprocessed
papers and stop only when none remain.

---

## Startup

1. List all files in `papers/raw/` (ignore dotfiles and non-paper files).
2. For each file, check whether both `papers/overview/{paper_id}.md` and
   `papers/condensed/{paper_id}.md` already exist (where `paper_id` is the filename
   without extension).
3. Build the list of unprocessed papers: those missing either output file.
4. If the list is empty, report "All papers already processed." and stop.
5. Otherwise, process each paper sequentially. Do not ask for confirmation.

---

## Per-paper task

For each unprocessed paper, complete all four steps before moving to the next paper.

### Step 1 — Overview: `papers/overview/{paper_id}.md`

Use the template at `papers/overview/_template.md`. Hard limits:

- **Problem**: 1 sentence.
- **Method**: 2 sentences maximum. Name what is specifically novel — not "a transformer-based
  approach" but what it does differently.
- **Key results**: 1 sentence with numbers.
- **Useful for**: comma-separated keywords only, no prose (e.g. "neuron ablation, linear probe,
  activation patching" — not "interpretability research").
- **Total length**: ≤15 lines including frontmatter.

### Step 2 — Condensed version: `papers/condensed/{paper_id}.md`

Use the template at `papers/condensed/_template.md`.

- Target length: 10–20% of the original.
- Preserve verbatim: all algorithms, pseudocode, equations, implementation details,
  hyperparameter tables, and result tables. Never paraphrase these.
- Compress to 1–2 sentences or drop entirely: abstract, introduction, related work,
  motivation paragraphs, discussion, conclusion, acknowledgements.
- The condensed version must be sufficient for someone to implement the method
  without referring back to the original.

### Step 3 — Index entry: `papers/index.md`

Append exactly one line to `papers/index.md`, after the `<!-- entries will appear below this line -->` comment:

```
- {paper_id} | {title} ({venue} {year}) | {useful_for keywords, copied verbatim from the overview}
```

This step is mandatory. Do not proceed to the next paper until the index entry is written.

### Step 4 — Verification

Before moving to the next paper, confirm:

- [ ] `paper_id` matches across overview filename, condensed filename, index entry, and raw filename.
- [ ] Overview is ≤15 lines including frontmatter.
- [ ] Each overview field respects its length limit.
- [ ] `useful_for` in the index entry is copied verbatim from the overview (not rewritten).
- [ ] Index entry has been written to `papers/index.md`.
- [ ] Condensed version contains no paraphrased equations or pseudocode.

---

## Completion

After all papers are processed, print:
- How many papers were processed this session.
- List of paper IDs processed.
- Any papers skipped (e.g. unreadable file) — list them with the reason.
