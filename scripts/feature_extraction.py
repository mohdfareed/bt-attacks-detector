import logging

import pandas as pd
from joblib import dump
from scipy.sparse import csr_matrix, hstack, save_npz
from sklearn.feature_extraction import FeatureHasher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

import data
import models
import scripts.utils as utils

LOGGER = logging.getLogger(__name__)
"""Feature extraction logger."""


def run():
    """Run the feature extraction script."""
    LOGGER.info("Running feature extraction...")

    LOGGER.debug("Loading datasets...")
    try:  # load preprocessed datasets
        train_dataset = pd.read_csv(data.PREPROCESSED_TRAIN)
        test_dataset = pd.read_csv(data.PREPROCESSED_TEST)
    except FileNotFoundError as exception:
        raise FileNotFoundError(
            "Preprocessed dataset files not found"
        ) from exception

    # apply tf-idf vectorization to Info column
    LOGGER.info("Applying TF-IDF vectorization...")
    vectorizer = TfidfVectorizer()
    train_info = vectorizer.fit_transform(train_dataset["Info"])
    test_info = vectorizer.transform(test_dataset["Info"])

    # apply one-hot encoding to Protocol column
    LOGGER.info("Applying one-hot encoding...")
    encoder = OneHotEncoder()
    train_protocol = encoder.fit_transform(train_dataset[["Protocol"]])
    test_protocol = encoder.transform(test_dataset[["Protocol"]])

    # apply standard scaling to Length column
    LOGGER.info("Applying standard scaling...")
    scaler = StandardScaler()
    train_length = scaler.fit_transform(train_dataset[["Length"]])
    test_length = scaler.transform(test_dataset[["Length"]])

    # apply feature hashing to Source and Destination columns
    LOGGER.info("Applying feature hashing...")
    train_source = apply_feature_hashing(train_dataset, "Source")
    test_source = apply_feature_hashing(test_dataset, "Source")
    train_destination = apply_feature_hashing(train_dataset, "Destination")
    test_destination = apply_feature_hashing(test_dataset, "Destination")

    # combine features
    LOGGER.debug("Combining features...")
    train_features = hstack(
        [
            csr_matrix(train_dataset[["Time"]]),
            train_source,
            train_destination,
            train_protocol,
            csr_matrix(train_length),
            train_info,
        ]
    )
    test_features = hstack(
        [
            csr_matrix(test_dataset[["Time"]]),
            test_source,
            test_destination,
            test_protocol,
            csr_matrix(test_length),
            test_info,
        ]
    )

    # write features and models to files
    LOGGER.info("Writing data and models to files...")
    save_npz(data.FEATURES_TRAIN, train_features)
    save_npz(data.FEATURES_TEST, test_features)
    dump(vectorizer, models.VECTORIZER_MODEL)
    dump(scaler, models.SCALER_MODEL)
    dump(encoder, models.ENCODER_MODEL)

    LOGGER.debug("Feature extraction complete")


def apply_feature_hashing(dataset, column, n_features=20):
    """Applies feature hashing to a specified column of the dataset."""
    hasher = FeatureHasher(n_features=n_features, input_type="string")
    hashed_features = hasher.transform(
        dataset[column].apply(lambda x: [str(x)])
    )
    return hashed_features


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
