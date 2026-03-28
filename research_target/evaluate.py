"""
Evaluation metrics for binary classification.

Computes accuracy, F1, AUC-ROC, precision, recall, and MCC.
Also provides a majority-class baseline for comparison.

The core question this module supports: when does accuracy give a false sense
of model quality, and which other metrics remain informative?
"""

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    matthews_corrcoef,
    precision_score,
    recall_score,
    roc_auc_score,
)


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray) -> dict:
    """All six metrics for a model with both hard predictions and probabilities."""
    return {
        'accuracy':  accuracy_score(y_true, y_pred),
        'f1':        f1_score(y_true, y_pred, zero_division=0),
        'auc':       roc_auc_score(y_true, y_prob),
        'precision': precision_score(y_true, y_pred, zero_division=0),
        'recall':    recall_score(y_true, y_pred, zero_division=0),
        'mcc':       matthews_corrcoef(y_true, y_pred),
    }


def majority_baseline(y_true: np.ndarray) -> dict:
    """Metrics for always predicting the majority class (a naive baseline).
    AUC is 0.5 by definition (random ranking). MCC is 0 (no information).
    High accuracy here signals the imbalance problem."""
    majority_class = int(np.bincount(y_true).argmax())
    y_pred = np.full_like(y_true, majority_class)
    y_prob = np.full(len(y_true), float(majority_class))
    return compute_metrics(y_true, y_pred, y_prob)


def minority_fraction(y: np.ndarray) -> float:
    """Fraction of samples belonging to the minority (positive) class."""
    return float(y.mean())
