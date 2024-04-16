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

    # load prediction models and dataset
    LOGGER.debug("Loading models and dataset...")
    predict_gbm = create_ml_predicator(models.GBM_MODEL)
    predict_rand = create_ml_predicator(models.RAND_FOREST_MODEL)
    predict_rules = create_rule_predicator()
    dataset = pd.read_csv(data.DEMO_DATA)

    try:
        LOGGER.debug("Running demonstration...")
        run_demo(dataset, predict_gbm, predict_rand, predict_rules)
    except KeyboardInterrupt:
        print()
        # evaluate on entire dataset
        LOGGER.info("Evaluating...")
        evaluate(dataset, predict_gbm, predict_rand, predict_rules)
        exit(0)

    LOGGER.debug("Demonstration complete")


def run_demo(dataset, gbm, rand, rule):
    for i, _ in dataset.iterrows():
        time.sleep(0.5)  # simulate real-time data
        row: pd.DataFrame = dataset.iloc[[i]]  # type: ignore

        # make predictions
        gbm_prediction = gbm(row)
        rand_prediction = rand(row)
        rule_prediction = rule(row)

        # create prediction string
        gbm_str = (
            "[bold red]Attack[/]"
            if gbm_prediction
            else "[bold green]Benign[/]"
        )
        rand_str = (
            "[bold red]Attack[/]"
            if rand_prediction
            else "[bold green]Benign[/]"
        )
        rule_str = (
            "[bold red]Attack[/]"
            if rule_prediction
            else "[bold green]Benign[/]"
        )

        # display results
        print()
        print(row.to_string(index=False))
        print(f"[bold]Gradient Boosting Machine:[/]\t{gbm_str}")
        print(f"[bold]Random Forest:[/]\t\t\t{rand_str}")
        print(f"[bold]Rule-Based Prediction:[/]\t\t{rule_str}")


def evaluate(dataset, gbm, rand, rule):
    # accuracy tracking
    gbm_misclassifications = 0
    rand_misclassifications = 0
    rule_misclassifications = 0

    for i, _ in dataset.iterrows():
        row: pd.DataFrame = dataset.iloc[[i]]  # type: ignore
        # make predictions
        gbm_prediction = gbm(row)
        rand_prediction = rand(row)
        rule_prediction = rule(row)
        # update accuracy
        gbm_misclassifications += gbm_prediction
        rand_misclassifications += rand_prediction
        rule_misclassifications += rule_prediction

    # calculate final accuracy
    gbm_accuracy = 1 - (gbm_misclassifications / len(dataset))
    rand_accuracy = 1 - (rand_misclassifications / len(dataset))
    rule_accuracy = 1 - (rule_misclassifications / len(dataset))

    # display results
    LOGGER.warning("Complete demo evaluation results:")
    LOGGER.warning(
        f"Gradient Boosting Machine: {gbm_accuracy * 100:.2f}% accuracy"
    )
    LOGGER.warning(f"Random Forest: {rand_accuracy * 100:.2f}% accuracy")
    LOGGER.warning(
        f"Rule-Based Prediction: {rule_accuracy * 100:.2f}% accuracy"
    )


def display(
    row: pd.DataFrame,
    gbm_prediction: int,
    rand_prediction: int,
    rule_prediction: int,
):
    """Display the results of the given row."""
    print()
    print(row.to_string(index=False))
    print(
        f"[bold]Gradient Boosting Machine:[/]\t"
        f"{'[bold red]Attack[/]' if gbm_prediction else '[bold green]Benign[/]'}\t"
    )
    print(
        f"[bold]Random Forest:[/]\t\t\t"
        f"{'[bold red]Attack[/]' if rand_prediction else '[bold green]Benign[/]'}\t"
    )
    print(
        f"[bold]Rule-Based Prediction:[/]\t\t"
        f"{'[bold red]Attack[/]' if rule_prediction else '[bold green]Benign[/]'}\t"
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
