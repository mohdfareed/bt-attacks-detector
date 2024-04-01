#!/usr/bin/env python3

import logging

import scripts.evaluation
import scripts.feature_extraction
import scripts.preprocessing
import scripts.training
import scripts.utils as utils

LOGGER = logging.getLogger(__name__)
"""Main logger."""


def main(
    debug: bool, preprocess: bool, features: bool, train: bool, eval: bool
):
    """Run the specified scripts.

    Args:
        debug (bool): Whether to log debug messages.
    """

    utils.setup_logging(debug)
    try:
        scripts.preprocessing.run() if preprocess else None
        scripts.feature_extraction.run() if features else None
        scripts.training.run() if train else None
        scripts.evaluation.run() if eval else None
    except KeyboardInterrupt:
        LOGGER.warning("Execution interrupted.")
        exit(0)
    except Exception as exception:
        LOGGER.exception(exception)
        LOGGER.error(f"Execution failed.")
        exit(1)
    LOGGER.info("Exiting...")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run project script.")
    parser.add_argument(
        "-d", "--debug", action="store_true", help="enable debug mode"
    )
    parser.add_argument(
        "-p", "--preprocess", action="store_true", help="preprocess data"
    )
    parser.add_argument(
        "-f", "--features", action="store_true", help="extract features"
    )
    parser.add_argument(
        "-t", "--train", action="store_true", help="train models"
    )
    parser.add_argument(
        "-e", "--eval", action="store_true", help="run evaluation"
    )

    args = parser.parse_args()
    main(args.debug, args.preprocess, args.features, args.train, args.eval)
