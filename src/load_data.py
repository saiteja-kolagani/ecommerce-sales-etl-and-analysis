import os
from dotenv import load_dotenv
import pandas as pd
from pathlib import Path
from snowflake.connector.pandas_tools import write_pandas
from .utils.setup_logger import logger
from .utils.snowflake_connection import get_snowflake_connection
from .merge_customers import merge_customers
from .merge_transactions import merge_transactions

load_dotenv()

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

        CUSTOMERS_TABLE = os.getenv("CUSTOMERS_TABLE")
        CUSTOMERS_STG_TABLE = os.getenv("CUSTOMERS_STG_TABLE")

        TRANSACTIONS_TABLE = os.getenv("TRANSACTIONS_TABLE")
        TRANSACTIONS_STG_TABLE = os.getenv("TRANSACTIONS_STG_TABLE")

        # Processed data directory
        processed_data_dir = Path(__file__).parent.parent / "data" / "processed"

        customers_file = processed_data_dir / "customers.csv"
        transactions_file = processed_data_dir / "transactions.csv"

        # Read processed datasets
        logger.info("Reading processed customers dataset...")
        customers_df = pd.read_csv(customers_file)

        logger.info(f"Customers dataset loaded from disk. Rows: {len(customers_df)}")

        logger.info("Reading processed transactions dataset...")
        transactions_df = pd.read_csv(transactions_file)

        logger.info(f"Transactions dataset loaded from disk. Rows: {len(transactions_df)}")

        # Connection to Snowflake
        connection = get_snowflake_connection()

        # Loading customers first because transactions references customers
        logger.info("Loading customers data into Snowflake staging table...")

        truncate_table(connection, CUSTOMERS_STG_TABLE)

        success, nchunks, nrows, _ = write_pandas(
            conn = connection,
            df = customers_df,
            table_name = CUSTOMERS_STG_TABLE,
            auto_create_table = False,
            overwrite = False,
            quote_identifiers = False
        )

        if not success:
            raise RuntimeError("Failed to load customers data into Snowflake staging table.")

        logger.info(f"Customers data loaded successfully into Snowflake staging table. Rows loaded: {nrows}, chunks: {nchunks}")

        merge_customers(connection, job_start_time, CUSTOMERS_TABLE, CUSTOMERS_STG_TABLE)

        # Load transactions
        logger.info("Loading transactions data into Snowflake staging table...")

        truncate_table(connection, TRANSACTIONS_STG_TABLE)

        success, nchunks, nrows, _ = write_pandas(
            conn = connection,
            df = transactions_df,
            table_name = TRANSACTIONS_STG_TABLE,
            auto_create_table = False,
            overwrite = False,
            quote_identifiers = False
        )

        if not success:
            raise RuntimeError("Failed to load transactions data into Snowflake staging table.")

        logger.info(f"Transactions data loaded successfully into Snowflake staging table. Rows loaded: {nrows}, chunks: {nchunks}")

        merge_transactions(connection, job_start_time, TRANSACTIONS_TABLE, TRANSACTIONS_STG_TABLE)

        logger.info("Data loading into Snowflake completed successfully.")

    except Exception as error:
        raise RuntimeError(f"Failed to load data into Snowflake: {error}") from error

    finally:
        if connection:
            connection.close()
            logger.info("Snowflake connection closed.")