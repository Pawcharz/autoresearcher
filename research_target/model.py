"""Logistic regression classifier wrapper."""

import numpy as np
from sklearn.linear_model import LogisticRegression


def train(X_train: np.ndarray, y_train: np.ndarray) -> LogisticRegression:
    clf = LogisticRegression(random_state=42, max_iter=1000)
    clf.fit(X_train, y_train)
    return clf


def predict(clf: LogisticRegression, X: np.ndarray) -> np.ndarray:
    return clf.predict(X)


def predict_proba(clf: LogisticRegression, X: np.ndarray) -> np.ndarray:
    """Probability of the positive (minority) class. Shape: (n,)."""
    return clf.predict_proba(X)[:, 1]


def predict_at_threshold(proba: np.ndarray, threshold: float = 0.5) -> np.ndarray:
    """Apply a custom decision threshold to pre-computed probabilities."""
    return (proba >= threshold).astype(int)
