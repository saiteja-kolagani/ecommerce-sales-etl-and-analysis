import os
import io
from dotenv import load_dotenv
import pandas as pd
from pathlib import Path
from snowflake.connector.pandas_tools import write_pandas
from .utils.setup_logger import logger
from .utils.s3_client import s3_client
from .utils.snowflake_connection import get_snowflake_connection
from .merge_customers import merge_customers
from .merge_transactions import merge_transactions

load_dotenv()

SILVER_BUCKET = os.getenv("S3_SILVER_BUCKET")

def truncate_table(connection, table_name):
    """Truncate a Snowflake staging table."""

    cursor = connection.cursor()

    try:
        logger.info(f"Truncating staging table: {table_name}")
        cursor.execute(f"TRUNCATE TABLE {table_name}")

    except Exception as error:
        raise RuntimeError(
            f"Failed to truncate {table_name}: {error}"
        ) from error

    finally:
        cursor.close()

def load_data(job_start_time):
    """Load processed datasets into Snowflake"""

    connection = None

    try:
        logger.info("Starting data loading phase...")

        if not SILVER_BUCKET:
            raise ValueError(
                "S3_SILVER_BUCKET environment variable is not set."
            )

        CUSTOMERS_TABLE = os.getenv("CUSTOMERS_TABLE")
        CUSTOMERS_STG_TABLE = os.getenv("CUSTOMERS_STG_TABLE")

        TRANSACTIONS_TABLE = os.getenv("TRANSACTIONS_TABLE")
        TRANSACTIONS_STG_TABLE = os.getenv("TRANSACTIONS_STG_TABLE")

        # Current pipeline ingestion
        ingestion_date = job_start_time.strftime("%Y-%m-%d")
        ingestion_timestamp = job_start_time.strftime("%Y%m%dT%H%M%S")

        current_ingestion_path = (
            f"ingestion_date={ingestion_date}/"
            f"ingestion_timestamp={ingestion_timestamp}/"
        )

        logger.info(f"Loading Silver ingestion: {current_ingestion_path}")

        # List objects in Silver bucket
        response = s3_client.list_objects_v2(
            Bucket=SILVER_BUCKET
        )

        objects = response.get("Contents", [])

        # Select only CSV files from current ingestion
        csv_objects = [
            obj
            for obj in objects
            if obj["Key"].lower().endswith(".csv")
            and current_ingestion_path in obj["Key"]
        ]

        if not csv_objects:
            raise FileNotFoundError(
                f"No CSV files found for ingestion "
                f"{ingestion_timestamp} in Silver bucket."
            )

        dataframes = {}

        # Read datasets from S3 Silver
        for obj in csv_objects:

            s3_key = obj["Key"]

            logger.info(
                f"Reading dataset from Silver S3: "
                f"s3://{SILVER_BUCKET}/{s3_key}"
            )

            response = s3_client.get_object(
                Bucket=SILVER_BUCKET,
                Key=s3_key
            )

            df = pd.read_csv(
                io.BytesIO(response["Body"].read())
            )

            dataset_name = Path(s3_key).stem

            dataframes[dataset_name] = df

            logger.info(
                f"{dataset_name} dataset loaded from Silver. "
                f"Rows: {len(df)}"
            )

        # Snowflake connection
        connection = get_snowflake_connection()

        # ---------------------------------------------------------
        # Customers
        # ---------------------------------------------------------

        if "customers" not in dataframes:
            raise FileNotFoundError(
                "Customers dataset not found in current Silver ingestion."
            )

        customers_df = dataframes["customers"]

        logger.info(
            "Loading customers data into Snowflake staging table..."
        )

        truncate_table(
            connection,
            CUSTOMERS_STG_TABLE
        )

        success, nchunks, nrows, _ = write_pandas(
            conn=connection,
            df=customers_df,
            table_name=CUSTOMERS_STG_TABLE,
            auto_create_table=False,
            overwrite=False,
            quote_identifiers=False
        )

        if not success:
            raise RuntimeError(
                "Failed to load customers data into "
                "Snowflake staging table."
            )

        logger.info(
            f"Customers data loaded successfully into Snowflake "
            f"staging table. Rows loaded: {nrows}, chunks: {nchunks}"
        )

        merge_customers(
            connection,
            job_start_time,
            CUSTOMERS_TABLE,
            CUSTOMERS_STG_TABLE
        )

        # ---------------------------------------------------------
        # Transactions
        # ---------------------------------------------------------

        if "transactions" not in dataframes:
            raise FileNotFoundError(
                "Transactions dataset not found in current Silver ingestion."
            )

        transactions_df = dataframes["transactions"]

        logger.info(
            "Loading transactions data into Snowflake staging table..."
        )

        truncate_table(
            connection,
            TRANSACTIONS_STG_TABLE
        )

        success, nchunks, nrows, _ = write_pandas(
            conn=connection,
            df=transactions_df,
            table_name=TRANSACTIONS_STG_TABLE,
            auto_create_table=False,
            overwrite=False,
            quote_identifiers=False
        )

        if not success:
            raise RuntimeError(
                "Failed to load transactions data into "
                "Snowflake staging table."
            )

        logger.info(
            f"Transactions data loaded successfully into Snowflake "
            f"staging table. Rows loaded: {nrows}, chunks: {nchunks}"
        )

        merge_transactions(
            connection,
            job_start_time,
            TRANSACTIONS_TABLE,
            TRANSACTIONS_STG_TABLE
        )

        logger.info(
            "Data loading into Snowflake completed successfully."
        )

    except Exception as error:
        raise RuntimeError(
            f"Failed to load data into Snowflake: {error}"
        ) from error

    finally:
        if connection:
            connection.close()
            logger.info("Snowflake connection closed.")