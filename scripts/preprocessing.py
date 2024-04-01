import logging

import scripts.utils as utils

LOGGER = logging.getLogger(__name__)
"""Data preprocessing logger."""


def run():
    """Run the data preprocessing script."""
    LOGGER.info("Running data preprocessing...")
    # evaluation code here
    LOGGER.info("Finished data preprocessing")


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
