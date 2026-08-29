import os
import io
import pandas as pd
from dotenv import load_dotenv
from .utils.setup_logger import logger 
from .utils.s3_client import s3_client

load_dotenv()

SILVER_BUCKET = os.getenv("S3_SILVER_BUCKET")


def save_processed_data(dataframes, job_start_time):
    """Upload transformed datasets to the S3 Silver layer."""

    try:
        logger.info("Saving processed datasets to S3 Silver...")

        if not SILVER_BUCKET:
            raise ValueError(
                "S3_SILVER_BUCKET environment variable is not set."
            )

        ingestion_date = job_start_time.strftime("%Y-%m-%d")
        ingestion_timestamp = job_start_time.strftime("%Y%m%dT%H%M%S")

        # Save each DataFrame to a CSV file
        for dataset_name, df in dataframes.items():
            file_name = f"{dataset_name}.csv"

            s3_key = (
                f"{dataset_name}/"
                f"ingestion_date={ingestion_date}/"
                f"ingestion_timestamp={ingestion_timestamp}/"
                f"{file_name}"
            )
            
            logger.info(f"Uploading {dataset_name} dataset to Silver S3...")

            # Convert DataFrame to CSV in memory
            csv_buffer = io.BytesIO()

            df.to_csv(
                csv_buffer,
                index=False
            )

            csv_buffer.seek(0)

            # Upload CSV directly to S3
            s3_client.upload_fileobj(
                csv_buffer,
                SILVER_BUCKET,
                s3_key
            )

            logger.info(
                f"Uploaded {dataset_name} dataset to "
                f"s3://{SILVER_BUCKET}/{s3_key}"
            )

        logger.info("All processed datasets saved successfully.")

    except Exception as error:
        raise RuntimeError(f"Failed to save processed datasets: {error}") from error