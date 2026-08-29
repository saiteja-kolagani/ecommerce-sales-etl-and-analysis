import io
import os
import pandas as pd
from pathlib import Path
from .utils.setup_logger import logger
from dotenv import load_dotenv
from .utils.s3_client import s3_client

load_dotenv()

BRONZE_BUCKET = os.getenv("S3_BRONZE_BUCKET")

def inspect_dataframe(df, dataset_name):
    """Inspect the given DataFrame and log its details."""
    logger.info(f"Inspecting {dataset_name} dataset...")
    logger.info(f"{dataset_name} dataset shape: {df.shape}")
    logger.info(f"{dataset_name} dataset columns: {df.columns.tolist()}")
    logger.info(f"{dataset_name} dataset data types:\n{df.dtypes}")
    logger.info(f"{dataset_name} dataset missing values:\n{df.isnull().sum()}")
    logger.info(f"{dataset_name} dataset duplicate rows: {df.duplicated().sum()}")
    logger.info(f"{dataset_name} dataset summary statistics:\n{df.describe(include='all')}")
    logger.info(f"{dataset_name} dataset head:\n{df.head()}")

def inspect_data(job_start_time):
    """Discover and inspect CSV datasets from S3 Bronze."""

    try:
        logger.info("Started inspecting the datasets from S3 Bronze...")

        if not BRONZE_BUCKET:
            raise ValueError(
                "S3_BRONZE_BUCKET environment variable is not set."
            )

        ingestion_date = job_start_time.strftime("%Y-%m-%d")
        ingestion_timestamp = job_start_time.strftime("%Y%m%dT%H%M%S")

        current_ingestion_prefix = (
            f"ingestion_date={ingestion_date}/"
            f"ingestion_timestamp={ingestion_timestamp}/"
        )

        logger.info(
            f"Looking for current ingestion: "
            f"{current_ingestion_prefix}"
        )
        
        # List objects in Bronze bucket
        response = s3_client.list_objects_v2(
            Bucket=BRONZE_BUCKET
        )

        objects = response.get("Contents", [])

        csv_objects = [
            obj for obj in objects
            if obj["Key"].lower().endswith(".csv")
            and current_ingestion_prefix in obj["Key"]
        ]

        if not csv_objects:
            raise FileNotFoundError(
                f"No CSV files found for ingestion: "
                f"{ingestion_timestamp}"
            )

        dataframes = {}

        for obj in csv_objects:

            s3_key = obj["Key"]

            logger.info(f"Loading dataset from S3: s3://{BRONZE_BUCKET}/{s3_key}")

            response = s3_client.get_object(
                Bucket = BRONZE_BUCKET,
                Key = s3_key
            )

            df = pd.read_csv(io.BytesIO(response["Body"].read()))

            dataset_name = Path(s3_key).stem

            dataframes[dataset_name] = df

            inspect_dataframe(df, dataset_name)

        logger.info(f"Successfully inspected {len(dataframes)} datasets from current Bronze ingestion.")

        return dataframes
        
    except Exception as error:
        raise RuntimeError(f"Failed to inspect the dataset: {error}") from error