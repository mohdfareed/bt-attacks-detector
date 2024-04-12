import logging
import time

import pandas as pd  # type: ignore
from rich import print

import data
import models
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
    predict_gbm = create_ml_predicator(models.GBM_MODEL)
    predict_rand = create_ml_predicator(models.RAND_FOREST_MODEL)
    predict_rules = create_rule_predicator()

    # accuracy tracking
    gbm_misclassifications = 0
    rand_misclassifications = 0
    rule_misclassifications = 0

    # load demo data
    dataset = pd.read_csv(data.DEMO_DATA)
    for i, _ in dataset.iterrows():
        time.sleep(0.05)  # simulate real-time data
        row: pd.DataFrame = dataset.iloc[[i]]  # type: ignore

        # make predictions
        gbm_prediction = predict_gbm(row)
        rand_prediction = predict_rand(row)
        rule_prediction = predict_rules(row)

        # update accuracy
        gbm_misclassifications += gbm_prediction
        gbm_accuracy = 1 - (gbm_misclassifications / (int(i) + 1))  # type: ignore
        rand_misclassifications += rand_prediction
        rand_accuracy = 1 - (rand_misclassifications / (int(i) + 1))  # type: ignore
        rule_misclassifications += rule_prediction
        rule_accuracy = 1 - (rule_misclassifications / (int(i) + 1))  # type: ignore

        # display results
        display(
            row,
            gbm_prediction,
            gbm_accuracy,
            rand_prediction,
            rand_accuracy,
            rule_prediction,
            rule_accuracy,
        )

    LOGGER.debug("Demonstration complete")


def display(
    row: pd.DataFrame,
    gbm_prediction: int,
    gbm_accuracy: float,
    rand_prediction: int,
    rand_accuracy: float,
    rule_prediction: int,
    rule_accuracy: float,
):
    """Display the results of the given row."""
    print()
    print(row.to_string(index=False))
    print(
        f"[bold]Gradient Boosting Machine:[/]\t"
        f"{'[bold red]Attack[/]' if gbm_prediction else '[bold green]Benign[/]'}\t"
        f"Accuracy: {gbm_accuracy * 100:.2f}%"
    )
    print(
        f"[bold]Random Forest:[/]\t\t\t"
        f"{'[bold red]Attack[/]' if rand_prediction else '[bold green]Benign[/]'}\t"
        f"Accuracy: {rand_accuracy * 100:.2f}%"
    )
    print(
        f"[bold]Rule-Based Prediction:[/]\t\t"
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
