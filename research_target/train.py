"""
Train logistic regression across imbalance ratios and save artifacts.

Run from repo root:
    python research_target/train.py

For each ratio, saves:
  artifacts/ratio_{R}/y_test.npy    — true labels
  artifacts/ratio_{R}/y_pred.npy    — hard predictions (threshold=0.5)
  artifacts/ratio_{R}/y_prob.npy    — predicted probabilities (minority class)
  artifacts/ratio_{R}/model.pkl     — fitted LogisticRegression

Also saves artifacts/summary.json with all metrics for every ratio,
for experiments that only need the summary table.
"""

import json
import os
import pickle
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from data import generate, split
from evaluate import compute_metrics, majority_baseline, minority_fraction
from model import predict, predict_proba, train

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), 'artifacts')

IMBALANCE_RATIOS = [1, 2, 5, 10, 20, 50, 100]


def run_ratio(ratio: float) -> dict:
    X, y = generate(imbalance_ratio=ratio)
    X_train, X_test, y_train, y_test = split(X, y)

    clf = train(X_train, y_train)
    y_pred = predict(clf, X_test)
    y_prob = predict_proba(clf, X_test)

    return {
        'clf': clf,
        'y_test': y_test,
        'y_pred': y_pred,
        'y_prob': y_prob,
        'model_metrics': compute_metrics(y_test, y_pred, y_prob),
        'baseline_metrics': majority_baseline(y_test),
        'minority_frac': minority_fraction(y_test),
    }


def main():
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    summary = []

    print(f'Training across {len(IMBALANCE_RATIOS)} imbalance ratios...')

    for ratio in IMBALANCE_RATIOS:
        result = run_ratio(ratio)

        # Per-ratio directory
        ratio_dir = os.path.join(ARTIFACTS_DIR, f'ratio_{ratio:03d}')
        os.makedirs(ratio_dir, exist_ok=True)
        np.save(os.path.join(ratio_dir, 'y_test.npy'), result['y_test'])
        np.save(os.path.join(ratio_dir, 'y_pred.npy'), result['y_pred'])
        np.save(os.path.join(ratio_dir, 'y_prob.npy'), result['y_prob'])
        with open(os.path.join(ratio_dir, 'model.pkl'), 'wb') as f:
            pickle.dump(result['clf'], f)

        summary.append({
            'ratio': ratio,
            'minority_pct': round(result['minority_frac'] * 100, 1),
            'model': {k: round(v, 4) for k, v in result['model_metrics'].items()},
            'baseline': {k: round(v, 4) for k, v in result['baseline_metrics'].items()},
        })

        m = result['model_metrics']
        print(f'  ratio {ratio:>3}:1  minority={result["minority_frac"]*100:4.1f}%  '
              f'acc={m["accuracy"]:.3f}  auc={m["auc"]:.3f}  '
              f'f1={m["f1"]:.3f}  mcc={m["mcc"]:.3f}')

    with open(os.path.join(ARTIFACTS_DIR, 'summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    print(f'\nArtifacts saved to {ARTIFACTS_DIR}/')


if __name__ == '__main__':
    main()
