import logging

import numpy as np
import pandas as pd  # type: ignore

import data
import scripts.utils as utils

LOGGER = logging.getLogger(__name__)
"""Data preprocessing logger."""


def run():
    """Run the data preprocessing script."""
    LOGGER.info("Preprocessing dataset...")

    LOGGER.debug("Loading datasets...")
    attack_train = pd.read_csv(data.ATTACK_TRAIN)
    benign_train = pd.read_csv(data.BENIGN_TRAIN)
    attack_test = pd.read_csv(data.ATTACK_TEST)
    benign_test = pd.read_csv(data.BENIGN_TEST)
    capture = pd.read_csv(data.CAPTURED_DATA)

    # split captured data (80/20 split) and append to benign data
    split_index = int(len(capture) * 0.8)  # required to preserve order
    capture_train = capture.iloc[:split_index]
    capture_test = capture.iloc[split_index:]
    benign_train = pd.concat([benign_train, capture_train], ignore_index=True)
    benign_test = pd.concat([benign_test, capture_test], ignore_index=True)

    # add type column indicating attack or benign
    attack_train["Type"] = 1
    attack_test["Type"] = 1
    benign_train["Type"] = 0
    benign_test["Type"] = 0

    # combine datasets
    LOGGER.debug("Combining datasets...")
    train_dataset = pd.concat([attack_train, benign_train], ignore_index=True)
    test_dataset = pd.concat([attack_test, benign_test], ignore_index=True)

    # generate labels
    train_labels = train_dataset["Type"]
    train_dataset.drop(columns=["Type"], inplace=True)
    test_labels = test_dataset["Type"]
    test_dataset.drop(columns=["Type"], inplace=True)

    # summary statistics
    LOGGER.debug("Summarizing datasets...")
    LOGGER.warning(
        f"Training data:\n"
        f"{pd.concat([attack_train, benign_train]).describe()}"
    )
    LOGGER.warning(
        f"Testing data:\n"
        f"{pd.concat([attack_test, benign_test]).describe()}"
    )

    # write modified dataset to files
    LOGGER.debug("Writing final datasets to files...")
    train_dataset.to_csv(data.PREPROCESSED_TRAIN, index=False)
    test_dataset.to_csv(data.PREPROCESSED_TEST, index=False)
    np.save(data.LABELS_TRAIN, train_labels)
    np.save(data.LABELS_TEST, test_labels)

    LOGGER.debug("Data preprocessing complete")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Data preprocessing script.")
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
