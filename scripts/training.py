import logging

import numpy as np
from joblib import dump
from scipy.sparse import load_npz
from sklearn.ensemble import GradientBoostingClassifier

import data
import models

LOGGER = logging.getLogger(__name__)
"""Model training logger."""


def run():
    """Run the model training script."""
    LOGGER.info("Running model training...")

    # load features and labels
    LOGGER.debug("Loading features and labels...")
    features = load_npz(data.FEATURES_TRAIN)
    labels = np.load(data.LABELS_TRAIN)

    # train model
    LOGGER.info("Training model...")
    model = GradientBoostingClassifier(verbose=2)
    model.fit(features, labels)

    # write model to file
    LOGGER.info("Saving model...")
    dump(model, models.GBM_MODEL)

    LOGGER.info("Finished model training")
