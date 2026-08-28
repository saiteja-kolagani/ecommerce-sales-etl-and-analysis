from src.utils.setup_logger import logger
from src.data_extract import extract_dataset
from src.inspect_data import inspect_data
from src.validate_schema import validate_datasets
from config.schema import EXPECTED_SCHEMAS
from src.transform_data import transform_data

def main():
    try:
        logger.info("Starting the pipeline...")

        # Step 1: Extract datasets
        logger.info("Calling extract_dataset() to extract datasets...")
        extract_dataset()
        logger.info("extract_dataset() completed successfully.")

        # Step 2: Inspect and validate datasets
        logger.info("Calling inspect_data() to inspect datasets...")
        dataframes = inspect_data()
        logger.info("inspect_data() completed successfully.")
        logger.info("Calling validate_datasets() to validate datasets...")
        validate_datasets(dataframes, EXPECTED_SCHEMAS)
        logger.info("validate_datasets() completed successfully.")

        # Step 3: Transform datasets
        logger.info("Calling transform_data() to transform datasets...")
        transformed_data = transform_data(dataframes)
        logger.info("transform_data() completed successfully.")

        logger.info("Pipeline completed successfully without errors.")

    except Exception:
        logger.exception("Pipeline failed due to an error.")

    finally:
        logger.info("Pipeline execution completed.")

if __name__ == '__main__':
    main()