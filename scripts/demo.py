import logging

import numpy as np
import sklearn.metrics as metrics
from joblib import load
from scipy.sparse import load_npz
from sklearn.ensemble import GradientBoostingClassifier

import data
import models

LOGGER = logging.getLogger(__name__)
"""Evaluation logger."""


def run():
    """Run the evaluation script."""
    LOGGER.info("Running demonstration...")

    # demo code

    LOGGER.info("Demonstration complete")
