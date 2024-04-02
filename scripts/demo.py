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
data_type = 0  # 0: all, 1: attack, 2: benign


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
            prediction = predict(row, model, vectorizer, encoder, scaler)
            display(row, label, prediction)

    except:  # stop thread on error
        cancellation_event.set()
        raise
    finally:  # wait for thread to finish
        data_thread.join()

    LOGGER.info("Demonstration complete")


def predict(
    data: pd.DataFrame,
    model: GradientBoostingClassifier,
    vectorizer: TfidfVectorizer,
    encoder: OneHotEncoder,
    scaler: StandardScaler,
) -> int:
    """Generate the features for the given dataset row."""

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

    # make prediction
    return model.predict(features)  # type: ignore


def read_data():
    """Read the testing data."""
    global data_type
    dataset = pd.read_csv(data.PREPROCESSED_TEST)
    labels = np.load(data.LABELS_TEST)

    # shuffle data
    permutation = np.random.permutation(dataset.shape[0])
    dataset = dataset.iloc[permutation]
    labels = labels[permutation]
    # TODO: remove if part of preprocessing

    for (i, _), label in zip(dataset.iterrows(), labels):
        if cancellation_event.is_set():
            break  # stop reading data when cancelled
        if not pause_event.is_set():
            pause_event.wait()  # pause reading data

        # check data type
        if data_type == 0 and label == 1 and np.random.rand() < 0.66:
            continue  # skip 2/3 of attack data
        if data_type == 1 and label == 0:
            continue  # only show attack data
        if data_type == 2 and label == 1:
            continue  # only show benign data

        row = dataset.iloc[[i]]  # type: ignore
        data_queue.put((row, label))
        time.sleep(0.5)  # simulate real-time data
    # signal end of data
    data_queue.put(None)  # type: ignore


def display(row: pd.DataFrame, label, pred):
    """Display the data row and prediction."""
    label = "[bold red]Attack[/]" if label else "[bold green]Benign[/]"
    pred = "[bold red]Attack[/]" if pred else "[bold green]Benign[/]"

    print()
    print(row.to_string(index=False))
    print(f"[bold]Label:[/]      {label}")
    print(f"[bold]Prediction:[/] {pred}")


def check_keypress():
    """Check for pause signal."""

    print("Press [yellow]ESC[/] to pause/unpause")
    print("Press [blue]TAB[/] to cycle data type")
    while True:
        if cancellation_event.is_set():
            break
        event = keyboard.read_event()

        if event.event_type != keyboard.KEY_DOWN:
            continue

        if event.name == "esc":
            toggle_pause()
        elif event.name == "tab":
            cycle_data_type()


def toggle_pause():
    if pause_event.is_set():
        pause_event.clear()
        print("[yellow]Paused[/]")
    else:
        pause_event.set()


def cycle_data_type():
    global data_type
    data_type = (data_type + 1) % 3

    if data_type == 0:
        print("[blue]Showing [bold white]ALL[/] data[/]")
    elif data_type == 1:
        print("[blue]Showing [red bold]ATTACK[/] data only[/]")
    else:
        print("[blue]Showing [green bold]BENIGN[/] data only[/]")


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
