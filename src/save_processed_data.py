from pathlib import Path
from .utils.setup_logger import logger 

def save_processed_data(dataframes):
    """Save the processed datasets to the processed data directory."""

    try:
        logger.info("Saving processed datasets...")

        # Define the processed data directory
        processed_data_dir = Path(__file__).parent.parent / "data" / "processed"
        processed_data_dir.mkdir(parents=True, exist_ok=True)

        # Save each DataFrame to a CSV file
        for dataset_name, df in dataframes.items():
            file_path = processed_data_dir / f"{dataset_name}.csv"
            df.to_csv(file_path, index=False)
            
            logger.info(f"Saved {dataset_name} dataset to: {file_path.resolve()}")

        logger.info("All processed datasets saved successfully.")

    except Exception as error:
        raise RuntimeError(f"Failed to save processed datasets: {error}") from error