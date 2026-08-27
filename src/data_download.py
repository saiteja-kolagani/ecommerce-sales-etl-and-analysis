import os
import kagglehub
from pathlib import Path
import shutil
from .utils.setup_logger import logger
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


def download_dataset():
    try:
        logger.info("Started downloading the dataset from Kaggle...")

        # Download latest version
        dataset_handler = os.getenv("KAGGLE_DATASET_HANDLER")

        if not dataset_handler:
            raise ValueError("KAGGLE_DATASET_HANDLER environment variable is not set.")

        download_path = kagglehub.dataset_download(dataset_handler)

        # Project's raw data directory
        raw_data_dir = Path(__file__).parent.parent / "data" / "raw"
        raw_data_dir.mkdir(parents=True, exist_ok=True)

        # Copy downloaded files to the raw data directory
        for file in Path(download_path).iterdir():
            if file.is_file():
                shutil.copy(file, raw_data_dir / file.name)

        logger.info(f"Dataset downloaded to: {raw_data_dir.resolve()}")

    except Exception as error:
        raise RuntimeError(f"Failed to download the dataset: {error}") from error
        