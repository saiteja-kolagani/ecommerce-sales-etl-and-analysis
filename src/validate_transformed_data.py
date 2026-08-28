from .utils.setup_logger import logger


def validate_customers(df):
    """Validate the transformed customers dataset."""

    logger.info("Validating transformed customers dataset...")

    # Check duplicate rows
    duplicate_rows = df.duplicated().sum()

    if duplicate_rows > 0:
        raise ValueError(f"Customers dataset contains {duplicate_rows} duplicate rows.")

    # Check customer IDs
    duplicate_ids = df["id"].duplicated().sum()

    if duplicate_ids > 0:
        raise ValueError(f"Customers dataset contains {duplicate_ids} duplicate IDs.")

    if df["id"].isna().any():
        raise ValueError("Customers dataset contains null IDs.")

    # Check age
    if df["age"].isna().any():
        raise ValueError("Customers dataset contains null age values.")

    if not df["age"].between(18, 65).all():
        raise ValueError("Customers dataset contains age values outside 18-65.")

    # Check state
    if df["state"].isna().any():
        raise ValueError("Customers dataset contains null state values.")

    # Check signup date
    if df["signup_date"].isna().any():
        raise ValueError("Customers dataset contains invalid signup dates.")

    logger.info("Transformed customers dataset validation passed.")


def validate_transactions(df):
    """Validate the transformed transactions dataset."""

    logger.info("Validating transformed transactions dataset...")

    # Check duplicate rows
    duplicate_rows = df.duplicated().sum()

    if duplicate_rows > 0:
        raise ValueError(
            f"Transactions dataset contains "
            f"{duplicate_rows} duplicate rows."
        )

    # Check transaction IDs
    duplicate_ids = df["id"].duplicated().sum()

    if duplicate_ids > 0:
        raise ValueError(
            f"Transactions dataset contains "
            f"{duplicate_ids} duplicate IDs."
        )

    if df["id"].isna().any():
        raise ValueError("Transactions dataset contains null IDs.")

    # Check customer IDs
    if df["customer_id"].isna().any():
        raise ValueError("Transactions dataset contains null customer IDs.")

    # Check transaction date
    if df["transaction_date"].isna().any():
        raise ValueError("Transactions dataset contains invalid transaction dates.")

    # Check quantity
    if (df["quantity"] <= 0).any():
        raise ValueError(
            "Transactions dataset contains "
            "quantity values less than or equal to zero."
        )

    # Check unit price
    if (df["unit_price"] < 0).any():
        raise ValueError("Transactions dataset contains negative unit prices.")

    # Check discount
    if not df["discount_applied"].between(0, 50).all():
        raise ValueError(
            "Transactions dataset contains "
            "discount values outside 0-50."
        )

    # Check review
    if df["review_text"].isna().any():
        raise ValueError("Transactions dataset contains null review values.")

    logger.info("Transformed transactions dataset validation passed.")


def validate_transformed_data(dataframes):
    """Validate all transformed datasets."""

    logger.info("Starting post-transformation data validation...")

    for dataset_name, df in dataframes.items():

        if dataset_name == "customers":
            validate_customers(df)

        elif dataset_name == "transactions":
            validate_transactions(df)

        else:
            logger.warning(
                f"No post-transformation validation defined "
                f"for {dataset_name}. Skipping."
            )

    logger.info("Post-transformation data validation completed successfully.")