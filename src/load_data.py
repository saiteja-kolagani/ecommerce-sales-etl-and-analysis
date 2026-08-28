import pandas as pd
from pathlib import Path
from snowflake.connector.pandas_tools import write_pandas
from .utils.setup_logger import logger
from .utils.snowflake_connection import get_snowflake_connection

def load_data():
    """Load processed datasets into Snowflake"""

    connection = None

    try:
        logger.info("Starting data loading phase...")

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
        logger.info("Loading customers data into Snowflake...")

        success, nchunks, nrows, _ = write_pandas(
            conn = connection,
            df = customers_df,
            table_name = "CUSTOMERS",
            database = "ECOMMERCE_DB",
            schema = "ANALYTICS",
            auto_create_table = False,
            overwrite = False,
            quote_identifiers = False
        )

        if not success:
            raise RuntimeError("Failed to load customers data into Snowflake.")

        logger.info(f"Customers data loaded successfully into Snowflake. Rows loaded: {nrows}, chunks: {nchunks}")

        # Load transactions
        logger.info("Loading transactions data into Snowflake...")

        success, nchunks, nrows, _ = write_pandas(
            conn = connection,
            df = transactions_df,
            table_name = "TRANSACTIONS",
            database = "ECOMMERCE_DB",
            schema = "ANALYTICS",
            auto_create_table = False,
            overwrite = False,
            quote_identifiers = False
        )

        if not success:
            raise RuntimeError("Failed to load transactions data.")

        logger.info(f"Transactions data loaded successfully into Snowflake. Rows loaded: {nrows}, chunks: {nchunks}")

        logger.info("Data loading into Snowflake completed successfully.")

    except Exception as error:
        raise RuntimeError(f"Failed to load data into Snowflake: {error}") from error

    finally:
        if connection:
            connection.close()
            logger.info("Snowflake connection closed.")