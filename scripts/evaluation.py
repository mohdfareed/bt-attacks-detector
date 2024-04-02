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
    LOGGER.info("Running evaluation...")

    # load testing features and labels
    LOGGER.debug("Loading features and labels...")
    features = load_npz(data.FEATURES_TEST)
    labels = np.load(data.LABELS_TEST)
    # load model
    LOGGER.debug("Loading model...")
    model: GradientBoostingClassifier = load(models.GBM_MODEL)

    # evaluate model
    LOGGER.info("Evaluating model...")
    predictions = model.predict(features)
    accuracy = metrics.accuracy_score(labels, predictions)
    LOGGER.warning(f"Train accuracy: {accuracy}")
    conf_matrix = metrics.confusion_matrix(labels, predictions)
    LOGGER.warning(f"Confusion matrix:\n{conf_matrix}")
    report = metrics.classification_report(labels, predictions)
    LOGGER.warning(f"Classification report:\n{report}")

    LOGGER.info("Finished evaluation")
