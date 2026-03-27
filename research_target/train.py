"""
Train a small MLP on synthetic 2D data and save artifacts.

Run from repo root:
    python research_target/train.py
"""

import os
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "artifacts")
RANDOM_SEED = 42


def generate_data():
    X, y = make_classification(
        n_samples=1000,
        n_features=2,
        n_informative=2,
        n_redundant=0,
        n_clusters_per_class=2,
        class_sep=0.8,
        random_state=RANDOM_SEED,
    )
    return X, y


def train_model(X_train, y_train):
    model = MLPClassifier(
        hidden_layer_sizes=(16, 8),
        activation="relu",
        max_iter=500,
        random_state=RANDOM_SEED,
    )
    model.fit(X_train, y_train)
    return model


def extract_activations(model, X):
    """Extract hidden layer activations for all samples."""
    activations = {}
    layer_input = X
    for i, (weights, biases) in enumerate(zip(model.coefs_[:-1], model.intercepts_[:-1])):
        pre_activation = layer_input @ weights + biases
        layer_output = np.maximum(0, pre_activation)  # ReLU
        activations[f"layer_{i+1}"] = layer_output
        layer_input = layer_output
    return activations


def main():
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    X, y = generate_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_SEED
    )

    model = train_model(X_train, y_train)

    train_acc = accuracy_score(y_train, model.predict(X_train))
    test_acc = accuracy_score(y_test, model.predict(X_test))
    print(f"Train accuracy: {train_acc:.3f}")
    print(f"Test accuracy:  {test_acc:.3f}")

    train_activations = extract_activations(model, X_train)
    test_activations = extract_activations(model, X_test)

    # Save everything
    with open(os.path.join(ARTIFACTS_DIR, "model.pkl"), "wb") as f:
        pickle.dump(model, f)

    np.save(os.path.join(ARTIFACTS_DIR, "X_train.npy"), X_train)
    np.save(os.path.join(ARTIFACTS_DIR, "X_test.npy"), X_test)
    np.save(os.path.join(ARTIFACTS_DIR, "y_train.npy"), y_train)
    np.save(os.path.join(ARTIFACTS_DIR, "y_test.npy"), y_test)

    np.save(os.path.join(ARTIFACTS_DIR, "train_layer1.npy"), train_activations["layer_1"])
    np.save(os.path.join(ARTIFACTS_DIR, "train_layer2.npy"), train_activations["layer_2"])
    np.save(os.path.join(ARTIFACTS_DIR, "test_layer1.npy"), test_activations["layer_1"])
    np.save(os.path.join(ARTIFACTS_DIR, "test_layer2.npy"), test_activations["layer_2"])

    print(f"Artifacts saved to {ARTIFACTS_DIR}/")
    print(f"  Layer 1 activations shape: {train_activations['layer_1'].shape}")
    print(f"  Layer 2 activations shape: {train_activations['layer_2'].shape}")


if __name__ == "__main__":
    main()
