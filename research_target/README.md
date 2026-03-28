# Dummy Research Target: Evaluation Metrics Under Class Imbalance

A binary classification experiment studying when common evaluation metrics
give misleading results. Used to test the autoresearcher framework.

The setup: a logistic regression model trained on synthetic data where the
minority class (the one we care about detecting) becomes progressively rarer —
from 50/50 balanced to 100:1 imbalanced. At high imbalance, a model can
achieve 99% accuracy by simply predicting "majority" every time, while being
completely useless in practice.

The research question: **at what imbalance level does accuracy become
misleading, and which metrics remain trustworthy?**

## Setup

```bash
pip install numpy scikit-learn matplotlib
python research_target/train.py
```

Trains logistic regression at 7 imbalance ratios (1:1 to 100:1) and saves
predictions, probabilities, and a summary table to `artifacts/`.

## Files

- `data.py` — synthetic binary classification with controllable imbalance ratio
- `model.py` — logistic regression wrapper (train, predict, predict_proba)
- `evaluate.py` — accuracy, F1, AUC, precision, recall, MCC + majority baseline
- `train.py` — sweeps ratios, saves per-ratio artifacts + `artifacts/summary.json`
- `utils.py` — `load_summary()`, `load_ratio(ratio)` for use in experiments

## Imbalance ratios tested

| Ratio | Minority % | Baseline accuracy |
|-------|-----------|-------------------|
| 1:1   | 50.0%     | 50%               |
| 2:1   | 33.3%     | 67%               |
| 5:1   | 16.7%     | 83%               |
| 10:1  | 9.1%      | 91%               |
| 20:1  | 4.8%      | 95%               |
| 50:1  | 2.0%      | 98%               |
| 100:1 | 1.0%      | 99%               |
