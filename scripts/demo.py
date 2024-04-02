import logging
import queue
import threading
import time

import keyboard
import numpy as np
import pandas as pd
from joblib import load
from rich import print
from scipy.sparse import csr_matrix, hstack
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

import data
import models
import scripts.utils as utils
from scripts.feature_extraction import apply_feature_hashing

LOGGER = logging.getLogger(__name__)
"""Evaluation logger."""

data_queue: queue.Queue[tuple[pd.DataFrame, int]] = queue.Queue()  # data queue
cancellation_event = threading.Event()  # token to stop data reader
pause_event = threading.Event()  # pause reading data
pause_event.set()  # pause when NOT set, start unpause


def run():
    """Run the evaluation script."""
    LOGGER.info("Running demonstration...")

    # load models
    LOGGER.info("Loading models...")
    vectorizer: TfidfVectorizer = load(models.VECTORIZER_MODEL)
    encoder: OneHotEncoder = load(models.ENCODER_MODEL)
    scaler: StandardScaler = load(models.SCALER_MODEL)
    model: GradientBoostingClassifier = load(models.GBM_MODEL)

    # start background thread to read data
    LOGGER.info("Reading data...")
    data_thread = threading.Thread(target=read_data)
    data_thread.start()
    # start background thread to check for keypress
    keyboard_thread = threading.Thread(target=check_keypress)
    keyboard_thread.start()

    try:  # process data and make predictions
        while True:
            row, label = data_queue.get()
            if row is None:
                break  # stop processing data when finished
            features = extract_features(row, vectorizer, encoder, scaler)
            prediction = model.predict(features)
            display(row, label, prediction)

    except:  # stop thread on error
        cancellation_event.set()
        raise
    finally:  # wait for thread to finish
        data_thread.join()

    LOGGER.info("Demonstration complete")


def extract_features(
    data: pd.DataFrame,
    vectorizer: TfidfVectorizer,
    encoder: OneHotEncoder,
    scaler: StandardScaler,
) -> csr_matrix:
    """Generate the features for the given dataset row."""

    # apply tf-idf vectorization to Info column
    info = vectorizer.transform(data["Info"])
    # apply one-hot encoding to Protocol column
    protocol = encoder.transform(data[["Protocol"]])
    # apply standard scaling to Length column
    length = scaler.transform(data[["Length"]])
    # apply feature hashing to Source and Destination columns
    source = apply_feature_hashing(data, "Source")
    destination = apply_feature_hashing(data, "Destination")

    # combine features
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


def read_data():
    """Read the testing data."""
    dataset = pd.read_csv(data.PREPROCESSED_TEST)
    labels = np.load(data.LABELS_TEST)

    # shuffle data
    permutation = np.random.permutation(dataset.shape[0])
    dataset = dataset.iloc[permutation]
    labels = labels[permutation]

    for (i, _), label in zip(dataset.iterrows(), labels):
        if cancellation_event.is_set():
            break  # stop reading data when cancelled
        if not pause_event.is_set():
            pause_event.wait()  # pause reading data

        row = dataset.iloc[[i]]  # type: ignore
        data_queue.put((row, label))
        time.sleep(1)  # simulate real-time data
    # signal end of data
    data_queue.put(None)  # type: ignore


def display(row: pd.DataFrame, label, prediction):
    """Display the data row and prediction."""
    label = "[red]Attack[/]" if label else "[green]Benign[/]"
    prediction = (
        "[bold red]Attack[/]" if prediction else "[bold green]Benign[/]"
    )

    print(f"\n<{label}>\n{row.to_string(index=False)}")
    print(f"[bold]Prediction:[/] {prediction}")


def check_keypress():
    """Check for pause signal."""

    while True:
        if cancellation_event.is_set():
            break
        event = keyboard.read_event()
        if event.event_type != keyboard.KEY_DOWN or event.name != "esc":
            continue

        if pause_event.is_set():
            pause_event.clear()
            print("[yellow]Paused[/]")
        else:
            pause_event.set()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Demonstration script.")
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
