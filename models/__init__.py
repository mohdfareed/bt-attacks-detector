"""Trained models files."""

import os

models_dir = os.path.dirname(os.path.realpath(__file__))

VECTORIZER_MODEL = os.path.join(models_dir, "vectorizer.joblib")
ENCODER_MODEL = os.path.join(models_dir, "encoder.joblib")
SCALER_MODEL = os.path.join(models_dir, "scaler.joblib")
