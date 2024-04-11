#!/usr/bin/env python3

import logging

import scripts.demo
import scripts.feature_extraction
import scripts.ml_model
import scripts.preprocessing
import scripts.utils as utils

LOGGER = logging.getLogger(__name__)
"""Main logger."""


def main(
    verbose: bool,
    preprocess: bool,
    features: bool,
    train: bool,
    demo: bool,
    cleanup: bool,
):
    """Run the specified scripts.

    Args:
        debug (bool): Whether to log debug messages.
    """

    utils.setup_logging(verbose, cleanup)
    try:

        scripts.preprocessing.run() if preprocess else None
        scripts.feature_extraction.run() if features else None
        scripts.ml_model.run() if train else None
        scripts.demo.run() if demo else None
    except KeyboardInterrupt:
        print()
        LOGGER.warning("Execution interrupted")
        exit(0)
    except Exception as exception:
        LOGGER.exception(exception)
        LOGGER.error(f"Execution failed")
        exit(1)
    LOGGER.info("Exiting...")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run project script.")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="enable verbose mode"
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
        "-d", "--demo", action="store_true", help="run demo (requires admin)"
    )
    parser.add_argument(
        "-c", "--cleanup", action="store_true", help="clean up previous logs"
    )

    args = parser.parse_args()
    main(
        args.verbose,
        args.preprocess,
        args.features,
        args.train,
        args.demo,
        args.cleanup,
    )
