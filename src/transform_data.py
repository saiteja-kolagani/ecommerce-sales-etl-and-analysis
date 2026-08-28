import pandas as pd
from .utils.setup_logger import logger

def transform_customers(df):
    """Transform the customers DataFrame."""
    
    logger.info("Transforming customers dataset...")
    logger.info(f"Initial rows in customers dataset: {len(df)}")

    # Rename columns
    logger.info(f"Columns before renaming: {df.columns.tolist()}")
    df = df.rename(columns={
        'customer_id': 'id'
    })
    logger.info(f"Columns after renaming: {df.columns.tolist()}")

    # Remove duplicates
    original_df = len(df)
    df = df.drop_duplicates().copy()
    logger.info(f"Count of duplicates removed: {original_df - len(df)}")

    # Convert signup_date to datetime
    df['signup_date'] = pd.to_datetime(df['signup_date'], errors='coerce')

    invalid_dates = df["signup_date"].isna().sum()
    logger.info(f"Found {invalid_dates} invalid signup dates.")

    if invalid_dates > 0:
        raise ValueError(
            f"Found {invalid_dates} invalid signup dates."
        )

    # Convert phone number to string
    df['phone_number'] = df['phone_number'].astype('string')

     # Standardize text fields
    df["name"] = df["name"].str.strip()
    df["gender"] = df["gender"].str.strip()
    df["state"] = df["state"].str.strip()
    df["email"] = df["email"].str.strip().str.lower()
    df["subscribe"] = df["subscribe"].str.strip()

    # State missing values handling
    df["state"] = df["state"].fillna("Unknown")

    missing_age = df["age"].isna().sum()

    if missing_age > 0:
        logger.info(f"Found {missing_age} missing age values. Filling using subscription-group median...")

        age_group_medians = df.groupby("subscribe")["age"].transform("median")

        logger.info(
            f"Median age by subscription status: "
            f"{df.groupby('subscribe')['age'].median().to_dict()}"
        )

        # Fill using subscription-group median
        df["age"] = df["age"].fillna(age_group_medians)

        # Check if any missing values remain
        remaining_missing_age = df["age"].isna().sum()

        if remaining_missing_age > 0:
            overall_median = df["age"].median()
            df["age"] = df["age"].fillna(overall_median)

            logger.info(
                f"Filled {remaining_missing_age} remaining missing age values "
                f"using overall median: {overall_median}"
            )

        # Final validation
        remaining_missing_age = df["age"].isna().sum()

        if remaining_missing_age > 0:
            raise ValueError(
                f"Age transformation failed. "
                f"{remaining_missing_age} missing values remain."
            )

    logger.info(
        f"Customers transformation completed. "
        f"Rows after transformation: {len(df)}"
    )

    return df


def transform_transactions(df):
    """Transform the transactions DataFrame."""
    
    logger.info("Transforming transactions dataset...")
    logger.info(f"Initial rows in transactions dataset: {len(df)}")

    # Rename columns
    logger.info(f"Columns before renaming: {df.columns.tolist()}")
    df = df.rename(columns={
        'transaction_id': 'id',
        'customer_id': 'customer_id'
    })
    logger.info(f"Columns after renaming: {df.columns.tolist()}")

    # Remove duplicates
    original_df = len(df)
    df = df.drop_duplicates().copy()
    logger.info(f"Count of duplicates removed: {original_df - len(df)}")

    # Convert transaction_date to datetime
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')

    invalid_dates = df["transaction_date"].isna().sum()
    logger.info(f"Found {invalid_dates} invalid transaction dates.")

    if invalid_dates > 0:
        raise ValueError(
            f"Found {invalid_dates} invalid transaction dates."
        )

    # Convert unit_price to float
    df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')

    # Standardize text fields
    df["payment_method"] = df["payment_method"].str.strip()
    df["transaction_status"] = df["transaction_status"].str.strip()

    # Handle missing reviews
    df["review_text"] = df["review_text"].fillna("No review provided").str.strip()

    # Haandling missing discount_applied values
    df["discount_applied"] = df["discount_applied"].fillna(0)

    # Calulate transaction amounts
    df["gross_amount"] = df["quantity"] * df["unit_price"]

    df["discount_amount"] = df["gross_amount"] * (df["discount_applied"] / 100)

    df["net_amount"] = df["gross_amount"] - df["discount_amount"]

    # Resulting columns after transformation
    logger.info(f"Columns after transformation: {df.columns.tolist()}")
    

    logger.info(
        f"Transactions transformation completed. "
        f"Rows after transformation: {len(df)}"
    )

    return df


def transform_data(dataframes):
    """Transform the input dataframes."""

    try:
        logger.info("Starting data transformation...")

        transformed_data = {}

        for name, df in dataframes.items():
            if name == 'customers':
                transformed_data[name] = transform_customers(df)
            elif name == 'transactions':
                transformed_data[name] = transform_transactions(df)
            else:
                logger.warning(f"No transformation function defined for {name}. Skipping.")

        logger.info("Data transformation completed.")

        return transformed_data

    except Exception as error:
        raise RuntimeError(f"Error during data transformation: {error}") from error