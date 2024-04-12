import logging
import time

import pandas as pd  # type: ignore
from rich import print

import data
import scripts.utils as utils
from scripts.ml_model import create_predictor as create_ml_predicator
from scripts.rule_based import create_predictor as create_rule_predicator

LOGGER = logging.getLogger(__name__)
"""Evaluation logger."""


def run():
    """Run the evaluation script."""
    LOGGER.info("Running demonstration...")

    # load prediction models
    LOGGER.debug("Loading models...")
    predict_ml = create_ml_predicator()
    predict_rules = create_rule_predicator()

    # accuracy tracking
    ml_misclassifications = 0
    rule_misclassifications = 0

    # load demo data
    dataset = pd.read_csv(data.DEMO_DATA)
    for i, _ in dataset.iterrows():
        time.sleep(0.5)  # simulate real-time data
        row: pd.DataFrame = dataset.iloc[[i]]  # type: ignore

        # make predictions
        ml_prediction = predict_ml(row)
        rule_prediction = predict_rules(row)

        # update accuracy
        ml_misclassifications += int(ml_prediction)  # type: ignore
        ml_accuracy = 1 - (ml_misclassifications / (int(i) + 1))  # type: ignore
        rule_misclassifications += int(rule_prediction)
        rule_accuracy = 1 - (rule_misclassifications / (int(i) + 1))  # type: ignore

        # display results
        display(
            row,
            ml_prediction,
            ml_accuracy,
            rule_prediction,
            rule_accuracy,
        )

    LOGGER.debug("Demonstration complete")


def display(
    row: pd.DataFrame,
    ml_prediction: int,
    ml_accuracy: float,
    rule_prediction: int,
    rule_accuracy: float,
):
    """Display the results of the given row."""
    print()
    print(row.to_string(index=False))
    print(
        f"[bold]ML Prediction:[/]\t\t"
        f"{'[bold red]Attack[/]' if ml_prediction else '[bold green]Benign[/]'}\t"
        f"Accuracy: {ml_accuracy * 100:.2f}%"
    )
    print(
        f"[bold]Rule-Based Prediction:[/]\t"
        f"{'[bold red]Attack[/]' if rule_prediction else '[bold green]Benign[/]'}\t"
        f"Accuracy: {rule_accuracy * 100:.2f}%"
    )


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
