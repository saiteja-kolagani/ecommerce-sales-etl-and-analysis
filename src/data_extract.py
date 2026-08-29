import os
import kagglehub
from pathlib import Path
from .utils.setup_logger import logger
from dotenv import load_dotenv
from .utils.s3_client import s3_client

load_dotenv() 

BRONZE_BUCKET = os.getenv("S3_BRONZE_BUCKET")


def extract_dataset(job_start_time):
    """Download the dataset from Kaggle and upload it to S3 Bronze."""

    try:
        logger.info("Started extracting the dataset from Kaggle...")

        ingestion_date = job_start_time.strftime("%Y-%m-%d")
        ingestion_timestamp = job_start_time.strftime("%Y%m%dT%H%M%S")

        # Download latest version
        dataset_handler = os.getenv("KAGGLE_DATASET_HANDLER")

        if not dataset_handler:
            raise ValueError("KAGGLE_DATASET_HANDLER environment variable is not set.")

        download_path = Path(kagglehub.dataset_download(dataset_handler))

        logger.info(f"Kaggle dataset downloaded to temporary location: {download_path}")

        files = list(download_path.glob("*.csv"))

        if not files:
            raise FileNotFoundError(f"No CSV file found in kaggle download directory: {download_path}")

        for file in files:
            dataset_name = file.stem
            s3_key = (
                f"{dataset_name}/"
                f"ingestion_date={ingestion_date}/"
                f"ingestion_timestamp={ingestion_timestamp}/"
                f"{file.name}"
            )

            logger.info(f"Uploading {file.name} to Bronze S3...")

            s3_client.upload_file(
                str(file),
                BRONZE_BUCKET,
                s3_key
            )

            logger.info(f"Uploaded {file.name} to s3://{BRONZE_BUCKET}/{s3_key}")

            logger.info("Dataset extraction and Bronze upload completed successfully.")

    except Exception as error:
        raise RuntimeError(f"Failed to extract the dataset: {error}") from error
        