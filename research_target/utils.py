"""
Utilities for loading artifacts in experiments.

Usage:
    import sys
    sys.path.insert(0, 'research_target')
    from utils import load_summary, load_ratio, RATIOS
"""

import json
import os
import pickle
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), 'artifacts')
RATIOS = [1, 2, 5, 10, 20, 50, 100]


def load_summary() -> list[dict]:
    """Load summary.json — list of per-ratio dicts with all metrics.
    Each entry: {ratio, minority_pct, model: {accuracy, f1, auc, ...},
                 baseline: {accuracy, f1, auc, ...}}"""
    path = os.path.join(ARTIFACTS_DIR, 'summary.json')
    if not os.path.exists(path):
        raise FileNotFoundError(
            'Artifacts not found. Run `python research_target/train.py` first.'
        )
    with open(path) as f:
        return json.load(f)


def load_ratio(ratio: int) -> dict:
    """Load per-ratio arrays for threshold and detailed analysis.
    Returns: {y_test, y_pred, y_prob, model (LogisticRegression)}"""
    ratio_dir = os.path.join(ARTIFACTS_DIR, f'ratio_{ratio:03d}')
    if not os.path.exists(ratio_dir):
        raise FileNotFoundError(f'No artifacts for ratio {ratio}. Run train.py first.')
    with open(os.path.join(ratio_dir, 'model.pkl'), 'rb') as f:
        clf = pickle.load(f)
    return {
        'y_test': np.load(os.path.join(ratio_dir, 'y_test.npy')),
        'y_pred': np.load(os.path.join(ratio_dir, 'y_pred.npy')),
        'y_prob': np.load(os.path.join(ratio_dir, 'y_prob.npy')),
        'model':  clf,
    }
