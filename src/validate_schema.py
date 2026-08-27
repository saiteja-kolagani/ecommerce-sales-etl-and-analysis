from .utils.setup_logger import logger

def validate_schema(df, expected_columns, dataset_name):
    """Validate that the DataFrame contains the expected columns."""
    
    logger.info(f"Validating schema for {dataset_name} dataset...")

    actual_columns = set(df.columns)
    expected_columns = set(expected_columns)

    missing_columns = expected_columns - actual_columns
    unexpected_columns = actual_columns - expected_columns

    if missing_columns:
         raise ValueError(f"{dataset_name} dataset is missing expected columns: {sorted(missing_columns)}")

    if unexpected_columns:
        logger.warning(f"{dataset_name} dataset has unexpected columns: {sorted(unexpected_columns)}")

    logger.info(f"{dataset_name} dataset schema validation passed.")



def validate_datasets(dataframes, schemas):
    """Validate the schemas of multiple datasets."""
    
    for dataset_name, df in dataframes.items():
        
        if dataset_name not in schemas:
            logger.warning(f"No schema defined for {dataset_name} dataset. Skipping validation.")
            continue

        validate_schema(df, schemas[dataset_name], dataset_name)