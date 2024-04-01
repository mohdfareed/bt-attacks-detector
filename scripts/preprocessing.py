import logging

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

    # summary statistics
    LOGGER.info("Summarizing datasets...")
    LOGGER.info(f"Attack training data:\n{attack_train.describe()}")
    LOGGER.info(f"Benign training data:\n{benign_train.describe()}")
    LOGGER.info(f"Attack testing data:\n{attack_test.describe()}")
    LOGGER.info(f"Benign testing data:\n{benign_test.describe()}")

    # write data to files
    LOGGER.info("Writing data to files...")
    attack_train.to_csv(data.PREPROCESSED_ATTACK_TRAIN, index=False)
    benign_train.to_csv(data.PREPROCESSED_BENIGN_TRAIN, index=False)
    attack_test.to_csv(data.PREPROCESSED_ATTACK_TEST, index=False)
    benign_test.to_csv(data.PREPROCESSED_BENIGN_TEST, index=False)

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
