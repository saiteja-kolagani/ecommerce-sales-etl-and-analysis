import os
import snowflake.connector
from dotenv import load_dotenv
from .setup_logger import logger

load_dotenv() 

def get_snowflake_connection():
    """Create and return a Snowflake connection using credentials from environment variables."""

    try:
        logger.info("Creating Snowflake connection...")

        # Retrieve Snowflake credentials from environment variables
        account = os.getenv("SNOWFLAKE_ACCOUNT")
        user = os.getenv("SNOWFLAKE_USER")
        password = os.getenv("SNWOFLAKE_PASSWORD")
        warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
        database = os.getenv("SNWOFLAKE_DATABASE")
        schema = os.getenv("SANOWFLAKE_SCHEMA")

        # Create a Snowflake connection
        connection = snowflake.connector.connect(
            user = user,
            password = password,
            account = account,
            warehouse = warehouse,
            database = database,
            schema = schema
        )

        logger.info("Snowflake connection created successfully.")

        return connection
    
    except Exception as error:
        raise RuntimeError(f"Failed to create Snowflake connection: {error}") from error