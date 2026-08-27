from src.utils.setup_logger import logger
from src.data_extract import extract_dataset
from src.inspect_data import inspect_data
from src.validate_schema import validate_datasets
from config.schema import EXPECTED_SCHEMAS

def main():
    try:
        logger.info("Starting the pipeline...")
        extract_dataset()
        dataframes = inspect_data()
        validate_datasets(dataframes, EXPECTED_SCHEMAS)
        logger.info("Pipeline completed successfully without errors.")

    except Exception:
        logger.exception("Pipeline failed due to an error.")

    finally:
        logger.info("Pipeline execution completed.")

if __name__ == '__main__':
    main()