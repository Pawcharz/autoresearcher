"""
Shared utilities for loading model artifacts.

Usage in experiments:
    import sys
    sys.path.insert(0, 'research_target')
    from utils import load_model, load_data, load_activations
"""

import os
import pickle
import numpy as np

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "artifacts")


def load_model():
    path = os.path.join(ARTIFACTS_DIR, "model.pkl")
    if not os.path.exists(path):
        raise FileNotFoundError(
            "Model not found. Run `python research_target/train.py` first."
        )
    with open(path, "rb") as f:
        return pickle.load(f)


def load_data(split="test"):
    """Load X and y for 'train' or 'test' split."""
    X = np.load(os.path.join(ARTIFACTS_DIR, f"X_{split}.npy"))
    y = np.load(os.path.join(ARTIFACTS_DIR, f"y_{split}.npy"))
    return X, y


def load_activations(layer, split="test"):
    """
    Load saved activations.
    layer: 1 or 2
    split: 'train' or 'test'
    Returns array of shape (n_samples, n_neurons)
    """
    path = os.path.join(ARTIFACTS_DIR, f"{split}_layer{layer}.npy")
    return np.load(path)


def extract_activations_live(model, X):
    """Re-extract activations from a model on arbitrary input X."""
    activations = {}
    layer_input = X
    for i, (weights, biases) in enumerate(zip(model.coefs_[:-1], model.intercepts_[:-1])):
        pre_activation = layer_input @ weights + biases
        layer_output = np.maximum(0, pre_activation)
        activations[f"layer_{i+1}"] = layer_output
        layer_input = layer_output
    return activations
