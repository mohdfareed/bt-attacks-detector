import logging
import os

import numpy as np
import sklearn.metrics as metrics
from joblib import dump
from scipy.sparse import load_npz
from sklearn.ensemble import GradientBoostingClassifier

import data
import models
import scripts.utils as utils

LOGGER = logging.getLogger(__name__)
"""Model training logger."""


def run():
    """Run the model training script."""
    LOGGER.info("Running model training...")

    LOGGER.debug("Loading features and labels...")
    try:  # load features and labels
        training_features = load_npz(data.FEATURES_TRAIN)
        training_labels = np.load(data.LABELS_TRAIN)
        testing_features = load_npz(data.FEATURES_TEST)
        testing_labels = np.load(data.LABELS_TEST)
    except FileNotFoundError as exception:
        raise FileNotFoundError(
            "Feature and/or label files not found"
        ) from exception

    # train model
    LOGGER.debug("Training model...")
    model = GradientBoostingClassifier(verbose=2)
    model.fit(training_features, training_labels)

    # evaluate model
    LOGGER.info("Evaluating model...")
    predictions = model.predict(testing_features)
    accuracy = metrics.accuracy_score(testing_labels, predictions)
    LOGGER.warning(f"Train accuracy: {accuracy}")
    conf_matrix = metrics.confusion_matrix(testing_labels, predictions)
    LOGGER.warning(f"Confusion matrix:\n{conf_matrix}")
    report = metrics.classification_report(testing_labels, predictions)
    LOGGER.warning(f"Classification report:\n{report}")

    # write model to file
    LOGGER.info("Saving model...")
    dump(model, models.GBM_MODEL)
    # write evaluation metrics to file
    eval_file = os.path.join(utils.root_dir, "evaluation.txt")
    with open(eval_file, "w") as file:
        file.write(f"Train accuracy: {accuracy}\n\n")
        file.write(f"Confusion matrix:\n{conf_matrix}\n\n")
        file.write(f"Classification report:\n{report}\n")

    LOGGER.info("Model training complete")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Model training script.")
    args = parser.parse_args()

    utils.setup_logging(debug=True)
    try:
        run()
    except KeyboardInterrupt:
        LOGGER.warning("Execution interrupted")
        exit(0)
    except Exception as exception:
        LOGGER.exception(exception)
        LOGGER.error(f"Execution failed")
        exit(1)
