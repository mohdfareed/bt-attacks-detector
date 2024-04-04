import logging
import os
import queue
import threading
import time

import keyboard
import pandas as pd
from rich import print

import data
import scripts.utils as utils
from scripts.ml_model import create_predictor as create_ml_predicator
from scripts.rule_based import create_predictor as create_rule_predicator

LOGGER = logging.getLogger(__name__)
"""Evaluation logger."""

data_queue: queue.Queue[pd.DataFrame | None] = queue.Queue()  # rows data queue
cancellation_event = threading.Event()  # token to stop data reader
unpause_event = threading.Event()  # pause reading data
unpause_event.set()  # pause when NOT set, start unpause


def run():
    """Run the evaluation script."""
    LOGGER.info("Running demonstration...")

    # check for sudo permissions
    if os.geteuid() != 0:
        LOGGER.error(
            "This script requires sudo permissions to listen to keyboard "
            "events for pausing/unpausing execution"
        )
        exit(1)

    # load prediction models
    LOGGER.debug("Loading models...")
    predict_ml = create_ml_predicator()
    predict_rules = create_rule_predicator()

    # start background thread to read data
    LOGGER.debug("Reading data...")
    data_thread = threading.Thread(target=read_captured_data)
    data_thread.start()
    # start background thread to check for keypress
    LOGGER.debug("Listening to commands...")
    keyboard_thread = threading.Thread(target=check_keypress)
    keyboard_thread.start()

    try:  # process data and make predictions
        while True:  # loop until cancelled
            if (row := data_queue.get()) is None:
                break  # stop processing data when finished
            ml_prediction = predict_ml(row)
            rule_prediction = predict_rules(row)
            display(row, ml_prediction, rule_prediction)
        LOGGER.info("Finished reading captured data")

    finally:  # wait for threads to finish
        cancellation_event.set()
        data_thread.join()
        keyboard_thread.join()
    LOGGER.debug("Demonstration complete")


def read_captured_data():
    """Read the captured data."""
    global data_queue, cancellation_event
    dataset = pd.read_csv(data.DATA_CAPTURE)

    for i, _ in dataset.iterrows():
        while not unpause_event.is_set() and not cancellation_event.is_set():
            time.sleep(0.1)
            continue  # pause reading data
        if cancellation_event.is_set():
            break  # stop reading data when cancelled

        # queue row data
        row: pd.DataFrame = dataset.iloc[[i]]  # type: ignore
        data_queue.put(row)
        LOGGER.debug(f"Read row {i}")
        time.sleep(0.5)  # simulate real-time data

    # signal end of data
    data_queue.put(None)


def check_keypress():
    """Check for pause signal."""
    global unpause_event, cancellation_event
    print("Press [yellow]ESC[/] to pause/unpause")

    while True:  # reading event without blocking
        while not keyboard.is_pressed("esc"):
            if cancellation_event.is_set():
                return
            time.sleep(0.1)

        # pause/unpause data reading
        if unpause_event.is_set():
            unpause_event.clear()
            print("[yellow]Paused[/]")
        else:
            unpause_event.set()
        time.sleep(0.5)  # debounce keypress


def display(row: pd.DataFrame, ml_pred, rule_pred):
    """Display the data row and predictions."""
    ml_pred = "[bold red]Attack[/]" if ml_pred else "[bold green]Benign[/]"
    rule_pred = "[bold red]Attack[/]" if rule_pred else "[bold green]Benign[/]"

    print()
    print(row.to_string(index=False))
    print(f"[bold]ML Prediction:[/]         {ml_pred}")
    print(f"[bold]Rule-Based Prediction:[/] {rule_pred}")


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
