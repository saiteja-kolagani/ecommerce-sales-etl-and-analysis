import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

log_file_handler = os.getenv("LOG_FILE_HANDLER", "logs/ecommerce_sales_etl.log")

def setup_logger(log_file: str = log_file_handler, level = logging.INFO):

    """Configure logging to both file and cosole."""
    try:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

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
    except Exception as e:
        print(f"Failed to set up logger: {e}")
        raise
    

logger  = setup_logger()