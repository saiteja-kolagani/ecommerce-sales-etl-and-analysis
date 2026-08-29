import logging
import sys 

LOGGER_NAME = "ecommerce_sales_etl"

def get_logger(name: str = LOGGER_NAME) -> logging.Logger:
    """Create and return the application logger."""

    # Obtain the root logger
    logger = logging.getLogger(name)

    # Removes existinf handlers to avoid duplicate log messages.
    for handler in logger.handlers:
        logger.removeHandler(handler)


    if not logger.handlers:
        # Create Stream Handler
        handler = logging.StreamHandler(sys.stdout)

        # Define the log format
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        )

        # Attach formatter to handler
        handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(handler)

    # Set logger level
    logger.setLevel(logging.INFO)

    # Stops a logger from passing its log messages up to its parent or ancestor loggers in Python
    logger.propagate = False

    return logger

logger = get_logger()