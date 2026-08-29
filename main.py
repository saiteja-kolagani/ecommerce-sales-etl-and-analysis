from datetime import datetime
from src.utils.setup_logger import logger
from src.data_extract import extract_dataset
from src.inspect_data import inspect_data
from src.validate_schema import validate_datasets
from config.schema import EXPECTED_SCHEMAS
from src.transform_data import transform_data
from src.validate_transformed_data import validate_transformed_data
from src.save_processed_data import save_processed_data
from src.load_data import load_data

def main():
    job_start_time = datetime.now().astimezone()

    try:
        logger.info("Starting the pipeline...")
        logger.info(f"Pipeline started at: {job_start_time}")

        # Step 1: Extract datasets
        logger.info("Calling extract_dataset() to extract datasets...")
        extract_dataset(job_start_time)
        logger.info("extract_dataset() completed successfully.")

        # Step 2: Inspect and validate datasets
        logger.info("Calling inspect_data() to inspect datasets...")
        dataframes = inspect_data(job_start_time)
        logger.info("inspect_data() completed successfully.")
        logger.info("Calling validate_datasets() to validate datasets...")
        validate_datasets(dataframes, EXPECTED_SCHEMAS)
        logger.info("validate_datasets() completed successfully.")

        # Step 3: Transform datasets
        logger.info("Calling transform_data() to transform datasets...")
        transformed_data = transform_data(dataframes)
        logger.info("transform_data() completed successfully.")

        # Step 4: Validate transformed datasets
        logger.info("Calling validate_transformed_data() to validate transformed datasets...")
        validate_transformed_data(transformed_data)
        logger.info("validate_transformed_data() completed successfully.")

        # Step 5: Save processed datasets
        logger.info("Calling save_processed_data() to save processed datasets...")
        save_processed_data(transformed_data, job_start_time)
        logger.info("save_processed_data() completed successfully.")

        # Step 6: Load processed data into Snowflake
        logger.info("Calling load_data() to save processed datasets...")
        load_data(job_start_time)
        logger.info("load_data() completed successfully.")

        logger.info("Pipeline completed successfully without errors.")

    except Exception:
        logger.exception("Pipeline failed due to an error.")

    finally:
        logger.info("Pipeline execution completed.")

if __name__ == '__main__':
    main()