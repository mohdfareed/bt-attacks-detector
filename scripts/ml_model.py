import logging

import numpy as np
import pandas as pd  # type: ignore
import sklearn.metrics as metrics  # type: ignore
from joblib import dump, load  # type: ignore
from scipy.sparse import load_npz  # type: ignore
from sklearn.ensemble import (  # type: ignore
    GradientBoostingClassifier,
    RandomForestClassifier,
)

import data
import models
import scripts.utils as utils
from scripts.feature_extraction import create_feature_extractor

LOGGER = logging.getLogger(__name__)
"""Model training logger."""

# classifier = models.GBM_MODEL
classifier = models.RAND_FOREST_MODEL
model_name = (
    "Gradient Boosting" if classifier == models.GBM_MODEL else "Random Forest"
)


def run():
    """Run the model training script."""
    LOGGER.info("Training model (%s)...", model_name)

    LOGGER.debug("Loading features and labels...")
    training_features = load_npz(data.FEATURES_TRAIN)
    training_labels = np.load(data.LABELS_TRAIN)
    testing_features = load_npz(data.FEATURES_TEST)
    testing_labels = np.load(data.LABELS_TEST)

    # train model
    LOGGER.debug("Training model...")
    if classifier == models.GBM_MODEL:
        model = GradientBoostingClassifier(verbose=1)
    else:
        model = RandomForestClassifier(n_jobs=-1, verbose=1)
    model.fit(training_features, training_labels)

    # evaluate model
    LOGGER.debug("Evaluating model...")
    predictions = model.predict(testing_features)
    accuracy = metrics.accuracy_score(testing_labels, predictions)
    LOGGER.warning(f"Train accuracy: {accuracy}")
    conf_matrix = metrics.confusion_matrix(testing_labels, predictions)
    LOGGER.warning(f"Confusion matrix:\n{conf_matrix}")
    report = metrics.classification_report(testing_labels, predictions)
    LOGGER.warning(f"Classification report:\n{report}")

    # write model to file
    LOGGER.debug("Saving model...")
    if classifier == models.GBM_MODEL:
        dump(model, models.GBM_MODEL)
    else:
        dump(model, models.RAND_FOREST_MODEL)

    LOGGER.debug("Model training complete")


def create_predictor(classifier):
    """Create a model predictor."""

    LOGGER.debug("Loading prediction model...")
    model: GradientBoostingClassifier | RandomForestClassifier
    if classifier == models.GBM_MODEL:
        model = load(models.GBM_MODEL)
    else:
        model = load(models.RAND_FOREST_MODEL)
    model.verbose = 0  # type: ignore
    extract_features = create_feature_extractor()

    def predict(data: pd.DataFrame) -> int:
        """Generate the features for the given dataset row."""
        nonlocal model
        # extract features and combine
        features = extract_features(data)
        # make prediction
        return int(model.predict(features))

    return predict


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
