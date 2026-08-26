import sys
import logging
from pathlib import Path

def setup_logger(log_file: str = 'logs/ecommerce_sales_etl.log', level = logging.INFO):

    """Configure logging to both file and cosole."""

    log_path = Path(log_file)
    log_path.parent.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level = level,
        format = "%(asctime)s | %(funcName)s | %(levelname)s | %(message)s",
        handlers = [
            logging.FileHandler(log_path),
            logging.StreamHandler(sys.stdout)
        ],
        force = True
    )

    return logging.getLogger(__name__)
    

logger  = setup_logger()