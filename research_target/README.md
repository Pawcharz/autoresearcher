# Dummy Research Target: Synthetic Classifier

A small MLP trained on 2D synthetic data. Used to test the autoresearcher framework.

## Setup

```bash
pip install numpy scikit-learn matplotlib
python research_target/train.py
```

This generates `research_target/artifacts/` with saved model weights and activations.

## Structure

- `train.py` — trains the model and saves artifacts
- `utils.py` — shared utilities (load model, load data, extract activations)
- `artifacts/` — saved after running train.py (gitignored)
