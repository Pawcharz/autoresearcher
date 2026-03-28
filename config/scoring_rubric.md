# Scoring Rubric — Class Imbalance Demo

Calibrates self-scores for experiments on the class imbalance research target.
Replace with your own rubric when using autoresearcher on a real project.

---

## High (7–10)

- A finding that pinpoints a specific transition: e.g. "accuracy diverges from AUC
  at ratio 10:1 — model accuracy (90%) matches baseline (91%) while AUC is still 0.83".
- A result that contradicts a common assumption with numbers, e.g. "F1 drops to 0
  at ratio 20:1 while AUC stays above 0.8 — they are not interchangeable".
- A threshold-tuning result showing a specific optimal threshold and the F1 gain
  it produces vs the default 0.5 threshold (e.g. "threshold 0.15 recovers F1 from
  0.00 to 0.41 at ratio 20:1").
- A finding that holds consistently across multiple ratios tested in the same experiment.

## Medium (5–6)

- A directional result without precise quantification, e.g. "lower threshold improves
  recall but we only tested two ratios".
- A correct visualization of metric trajectories that makes divergence visible but
  doesn't identify the specific crossover point.
- A correlation analysis that ranks metrics by imbalance-robustness without testing
  whether the ranking is stable.

## Low (1–4)

- A result that only restates what summary.json already shows without analysis or
  interpretation (e.g. "accuracy increases with imbalance ratio").
- A null result with no hypothesis for why.
- An experiment that fails to run or produces uninterpretable output.
