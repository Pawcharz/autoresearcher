"""
Synthetic binary classification data with controllable class imbalance.

imbalance_ratio is majority:minority. Ratio 1 = balanced (50/50).
Ratio 10 = 10 majority samples per 1 minority sample (91% / 9%).
Ratio 100 = 99% majority, 1% minority.
"""

import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split


def generate(
    n_samples: int = 2000,
    imbalance_ratio: float = 1.0,
    n_features: int = 10,
    seed: int = 42,
):
    """Return X, y with the requested class imbalance.
    Class 0 = majority, class 1 = minority."""
    minority_frac = 1.0 / (1.0 + imbalance_ratio)
    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=5,
        n_redundant=2,
        n_repeated=0,
        weights=[1 - minority_frac, minority_frac],
        flip_y=0.01,
        random_state=seed,
    )
    return X, y


def split(X, y, test_size: float = 0.3, seed: int = 42):
    return train_test_split(X, y, test_size=test_size, random_state=seed, stratify=y)
