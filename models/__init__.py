"""Trained models files."""

import os

models_dir = os.path.dirname(os.path.realpath(__file__))

GBM_MODEL = os.path.join(models_dir, "gbm.joblib")
RAND_FOREST_MODEL = os.path.join(models_dir, "rand_forest.joblib")
