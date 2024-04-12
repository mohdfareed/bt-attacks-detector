"""Trained models files."""

import os

models_dir = os.path.dirname(os.path.realpath(__file__))

VECTORIZER_MODEL = os.path.join(models_dir, "vectorizer.joblib")
ENCODER_MODEL = os.path.join(models_dir, "encoder.joblib")
SCALER_MODEL = os.path.join(models_dir, "scaler.joblib")
HASHER_MODEL = os.path.join(models_dir, "hasher.joblib")
GBM_MODEL = os.path.join(models_dir, "gbm.joblib")
RAND_FOREST_MODEL = os.path.join(models_dir, "rand_forest.joblib")
