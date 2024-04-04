import logging

import pandas as pd
from joblib import dump, load
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
    LOGGER.info("Performing feature extraction...")

    LOGGER.debug("Loading datasets...")
    train_dataset = pd.read_csv(data.PREPROCESSED_TRAIN)
    test_dataset = pd.read_csv(data.PREPROCESSED_TEST)

    # apply tf-idf vectorization to Info column
    LOGGER.debug("Applying TF-IDF vectorization...")
    vectorizer = TfidfVectorizer()
    train_info = vectorizer.fit_transform(train_dataset["Info"])
    test_info = vectorizer.transform(test_dataset["Info"])

    # apply one-hot encoding to Protocol column
    LOGGER.debug("Applying one-hot encoding...")
    encoder = OneHotEncoder()
    train_protocol = encoder.fit_transform(train_dataset[["Protocol"]])
    test_protocol = encoder.transform(test_dataset[["Protocol"]])

    # apply standard scaling to Length column
    LOGGER.debug("Applying standard scaling...")
    scaler = StandardScaler()
    train_length = scaler.fit_transform(train_dataset[["Length"]])
    test_length = scaler.transform(test_dataset[["Length"]])

    # apply feature hashing to Source and Destination columns
    LOGGER.debug("Applying feature hashing...")
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

    # report feature extraction results
    LOGGER.debug("Feature extraction results:")
    LOGGER.warning(f"TF-IDF Vocabulary size: {len(vectorizer.vocabulary_)}")
    LOGGER.warning(f"One-Hot Encoding unique categories: {len(encoder.categories_[0])}")  # type: ignore
    LOGGER.warning(f"Standard Scaling mean: {scaler.mean_[0]:.4f}")  # type: ignore
    LOGGER.warning(f"Standard Scaling std: {scaler.scale_[0]:.4f}")  # type: ignore
    LOGGER.warning(f"Feature Hashing features count: {train_source.shape[1]}")
    LOGGER.warning(f"Total number of features: {train_features.shape[1]}")

    # write features and models to files
    LOGGER.debug("Writing data and models to files...")
    save_npz(data.FEATURES_TRAIN, train_features)
    save_npz(data.FEATURES_TEST, test_features)
    dump(vectorizer, models.VECTORIZER_MODEL)
    dump(encoder, models.ENCODER_MODEL)
    dump(scaler, models.SCALER_MODEL)

    LOGGER.debug("Feature extraction complete")


def apply_feature_hashing(dataset, column, n_features=20):
    """Applies feature hashing to a specified column of the dataset."""
    hasher = FeatureHasher(n_features=n_features, input_type="string")
    hashed_features = hasher.transform(
        dataset[column].apply(lambda x: [str(x)])
    )
    return hashed_features


def create_feature_extractor():
    """Create a feature extractor."""

    LOGGER.debug("Loading feature extraction models...")
    vectorizer: TfidfVectorizer = load(models.VECTORIZER_MODEL)
    encoder: OneHotEncoder = load(models.ENCODER_MODEL)
    scaler: StandardScaler = load(models.SCALER_MODEL)

    def extract_features(data: pd.DataFrame) -> csr_matrix:
        """Generate the features for the given dataset row."""
        nonlocal vectorizer, encoder
        # extract features and combine
        info = vectorizer.transform(data["Info"])
        protocol = encoder.transform(data[["Protocol"]])
        length = scaler.transform(data[["Length"]])
        source = apply_feature_hashing(data, "Source")
        destination = apply_feature_hashing(data, "Destination")
        features = hstack(
            [
                csr_matrix(data[["Time"]]),
                source,
                destination,
                protocol,
                csr_matrix(length),
                info,
            ]
        )
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
