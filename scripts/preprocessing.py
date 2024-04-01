import logging

import numpy as np
import pandas as pd

import data
import scripts.utils as utils

LOGGER = logging.getLogger(__name__)
"""Data preprocessing logger."""

_data_types = {
    "No.": int,
    "Time": float,
    "Source": object,
    "Destination": object,
    "Protocol": object,
    "Length": int,
    "Info": object,
}


def run():
    """Run the data preprocessing script."""
    LOGGER.info("Running data preprocessing...")

    LOGGER.debug("Loading datasets...")
    attack_train = pd.read_csv(data.ATTACK_TRAIN)
    benign_train = pd.read_csv(data.BENIGN_TRAIN)
    attack_test = pd.read_csv(data.ATTACK_TEST)
    benign_test = pd.read_csv(data.BENIGN_TEST)

    # data types check
    LOGGER.debug("Checking data types...")
    for dataset in [attack_train, benign_train, attack_test, benign_test]:
        for column, data_type in _data_types.items():
            assert (
                dataset[column].dtype == data_type
            ), f"Invalid data type for {column}"

    # data shape check
    LOGGER.debug("Checking data shapes...")
    assert attack_train.shape[1] == 7, "Invalid attack training data shape"
    assert benign_train.shape[1] == 7, "Invalid benign training data shape"
    assert attack_test.shape[1] == 7, "Invalid attack testing data shape"
    assert benign_test.shape[1] == 7, "Invalid benign testing data shape"

    # add type column indicating attack or benign
    attack_train["Type"] = 1
    attack_test["Type"] = 1
    benign_train["Type"] = 0
    benign_test["Type"] = 0

    # combine datasets
    LOGGER.info("Combining datasets...")
    train_dataset = pd.concat([attack_train, benign_train], ignore_index=True)
    test_dataset = pd.concat([attack_test, benign_test], ignore_index=True)
    # generate labels
    train_labels = train_dataset["Type"]
    test_labels = test_dataset["Type"]

    # summary statistics
    LOGGER.info("Summarizing datasets...")
    LOGGER.info(f"Training data:\n{attack_train.describe()}")
    LOGGER.info(f"Testing data:\n{attack_test.describe()}")

    # write data to files
    LOGGER.info("Writing data to files...")
    train_dataset.to_csv(data.PREPROCESSED_TRAIN)
    test_dataset.to_csv(data.PREPROCESSED_TEST)
    np.save(data.LABELS_TRAIN, train_labels)
    np.save(data.LABELS_TEST, test_labels)

    LOGGER.debug("Finished data preprocessing")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Data preprocessing script.")
    args = parser.parse_args()

    utils.setup_logging(debug=True)
    try:
        run()
    except KeyboardInterrupt:
        LOGGER.warning("Execution interrupted.")
        exit(0)
    except Exception as exception:
        LOGGER.exception(exception)
        LOGGER.error(f"Execution failed.")
        exit(1)
