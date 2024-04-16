import logging
from calendar import c

import pandas as pd  # type: ignore
from joblib import dump, load  # type: ignore
from scipy.sparse import csr_matrix, hstack, save_npz  # type: ignore
from sklearn.feature_extraction import FeatureHasher  # type: ignore
from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
from sklearn.preprocessing import OneHotEncoder, StandardScaler  # type: ignore

import data
import models
import scripts.utils as utils

LOGGER = logging.getLogger(__name__)
"""Feature extraction logger."""


def run():
    """Run the feature extraction script."""
    LOGGER.info("Performing feature extraction...")
    LOGGER.debug("Loading datasets...")
    train_dataset = pd.read_csv(data.PREPROCESSED_TRAIN)
    test_dataset = pd.read_csv(data.PREPROCESSED_TEST)

    # apply time delta encoding to Time column
    train_time = csr_matrix(train_dataset[["Time"]].diff().fillna(0))
    test_time = csr_matrix(test_dataset[["Time"]].diff().fillna(0))
    # keep Length column as is
    train_length = csr_matrix(train_dataset[["Length"]])
    test_length = csr_matrix(test_dataset[["Length"]])
    # combine features
    train_features = hstack([train_time, train_length])
    test_features = hstack([test_time, test_length])

    # report feature extraction results
    LOGGER.debug("Feature extraction results:")
    LOGGER.warning(f"Total number of features: {train_features.shape[1]}")

    # write features to files
    LOGGER.debug("Writing features data to files...")
    save_npz(data.FEATURES_TRAIN, train_features)
    save_npz(data.FEATURES_TEST, test_features)
    LOGGER.debug("Feature extraction complete")


def create_feature_extractor():
    """Create a feature extractor."""
    prev_time = 0

    def extract_features(data: pd.DataFrame) -> csr_matrix:
        """Generate the features for the given dataset row."""
        nonlocal prev_time

        # extract features and combine
        time = csr_matrix(data[["Time"]].diff().fillna(prev_time))
        length = csr_matrix(data[["Length"]])
        # combine features
        features = hstack([time, length])

        # update previous time and return features
        prev_time = data["Time"].values[0]
        return features  # type: ignore

    return extract_features


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Feature extraction script.")
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
