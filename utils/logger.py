import logging
import sys


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Function to set up a simple logger for terminal output."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    logger.addHandler(console_handler)

    return logger
