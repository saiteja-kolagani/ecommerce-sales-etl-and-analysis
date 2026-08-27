from src.utils.setup_logger import logger
from src.data_download import download_dataset

def main():
    try:
        logger.info("Starting the pipeline...")
        download_dataset()
        logger.info("Pipeline completed successfully.")
    except Exception:
        logger.exception("Pipeline failed due to an error.")
    finally:
        logger.info("Pipeline execution completed.")

if __name__ == '__main__':
    main()