import logging

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

    # apply tf-idf vectorization to Info column
    LOGGER.debug("Applying TF-IDF vectorization...")
    vectorizer = TfidfVectorizer(max_features=1000)
    train_info = vectorizer.fit_transform(train_dataset["Info"])
    test_info = vectorizer.transform(test_dataset["Info"])

    # apply one-hot encoding to Protocol column
    LOGGER.debug("Applying one-hot encoding...")
    encoder = OneHotEncoder()
    train_protocol = encoder.fit_transform(train_dataset[["Protocol"]])
    test_protocol = encoder.transform(test_dataset[["Protocol"]])

    # apply time delta encoding to Time column
    LOGGER.debug("Applying time delta encoding...")
    train_time = csr_matrix(train_dataset[["Time"]].diff().fillna(0))
    test_time = csr_matrix(test_dataset[["Time"]].diff().fillna(0))

    # apply standard scaling to Length column
    LOGGER.debug("Applying standard scaling...")
    scaler = StandardScaler()
    train_length = scaler.fit_transform(train_dataset[["Length"]])
    test_length = scaler.transform(test_dataset[["Length"]])

    # apply feature hashing to Source and Destination columns
    LOGGER.debug("Applying feature hashing...")
    hasher = FeatureHasher(n_features=20, input_type="string")
    train_source = hasher.transform(train_dataset["Source"].apply(lambda x: [x]))  # type: ignore
    test_source = hasher.transform(test_dataset["Source"].apply(lambda x: [x]))  # type: ignore
    train_dest = hasher.transform(train_dataset["Destination"].apply(lambda x: [x]))  # type: ignore
    test_dest = hasher.transform(test_dataset["Destination"].apply(lambda x: [x]))  # type: ignore

    # combine features
    LOGGER.debug("Combining features...")
    train_features = hstack(
        [
            train_time,
            train_source,
            train_dest,
            train_protocol,
            train_length,
            train_info,
        ]
    )
    test_features = hstack(
        [
            test_time,
            test_source,
            test_dest,
            test_protocol,
            test_length,
            test_info,
        ]
    )

    # report feature extraction results
    LOGGER.debug("Feature extraction results:")
    LOGGER.warning(f"TF-IDF Vocabulary size: {len(vectorizer.vocabulary_)}")
    LOGGER.warning(f"One-Hot Encoding unique categories: {len(encoder.categories_[0])}")  # type: ignore
    LOGGER.warning(f"Time Delta features count: {train_time.shape[1]}")
    LOGGER.warning(f"Standard Scaling features count: {train_length.shape[1]}")
    LOGGER.warning(f"Feature Hashing features count: {train_source.shape[1]}")
    LOGGER.warning(f"Total number of features: {train_features.shape[1]}")

    # write features and models to files
    LOGGER.debug("Writing data and models to files...")
    save_npz(data.FEATURES_TRAIN, train_features)
    save_npz(data.FEATURES_TEST, test_features)
    dump(vectorizer, models.VECTORIZER_MODEL)
    dump(encoder, models.ENCODER_MODEL)
    dump(scaler, models.SCALER_MODEL)
    dump(hasher, models.HASHER_MODEL)

    LOGGER.debug("Feature extraction complete")


def create_feature_extractor():
    """Create a feature extractor."""

    LOGGER.debug("Loading feature extraction models...")
    vectorizer: TfidfVectorizer = load(models.VECTORIZER_MODEL)
    encoder: OneHotEncoder = load(models.ENCODER_MODEL)
    hasher: FeatureHasher = load(models.HASHER_MODEL)
    scalar: StandardScaler = load(models.SCALER_MODEL)
    prev_time = 0

    def extract_features(data: pd.DataFrame) -> csr_matrix:
        """Generate the features for the given dataset row."""
        nonlocal vectorizer, encoder, hasher, scalar, prev_time

        # extract features and combine
        info = vectorizer.transform(data["Info"])
        protocol = encoder.transform(data[["Protocol"]])
        time = csr_matrix(data[["Time"]].diff().fillna(prev_time))
        length = scalar.transform(data[["Length"]])
        source = hasher.transform(data["Source"].apply(lambda x: [x]))  # type: ignore
        dest = hasher.transform(data["Destination"].apply(lambda x: [x]))  # type: ignore

        # combine features
        features = hstack(
            [
                time,
                source,
                dest,
                protocol,
                length,
                info,
            ]
        )

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
