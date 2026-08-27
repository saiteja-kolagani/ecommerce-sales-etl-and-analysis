import pandas as pd
from pathlib import Path
from .utils.setup_logger import logger

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

def inspect_data():
    try:
        logger.info("Started inspecting the dataset...")

        raw_data_dir = Path(__file__).parent.parent / "data" / "raw"
        csv_files = list(raw_data_dir.glob("*.csv"))

        if not csv_files:
            raise FileNotFoundError(f"No CSV files found in the raw data directory: {raw_data_dir.resolve()}")

        dataframes = {}

        for file in csv_files:
            logger.info(f"Loading dataset: {file.name}")
            df = pd.read_csv(file)
            dataframes[file.stem] = df
            inspect_dataframe(df, file.stem)

        logger.info("Dataset inspection completed successfully.")

        return dataframes
        
    except Exception as error:
        raise RuntimeError(f"Failed to inspect the dataset: {error}") from error