from .utils.setup_logger import logger

def merge_transactions(connection, job_start_time, TRANSACTIONS_TABLE, TRANSACTIONS_STG_TABLE):
    """Merge staged transaction records into the transactions table."""

    logger.info("Merging transactions staging data...")

    merge_sql = f"""
        MERGE INTO {TRANSACTIONS_TABLE} AS target
        USING {TRANSACTIONS_STG_TABLE} AS source
            ON target.ID = source.ID

        WHEN MATCHED  AND (
                target.CUSTOMER_ID IS DISTINCT FROM source.CUSTOMER_ID
                OR target.TRANSACTION_DATE IS DISTINCT FROM source.TRANSACTION_DATE
                OR target.PRODUCT_ID IS DISTINCT FROM source.PRODUCT_ID
                OR target.QUANTITY IS DISTINCT FROM source.QUANTITY
                OR target.UNIT_PRICE IS DISTINCT FROM source.UNIT_PRICE
                OR target.PAYMENT_METHOD IS DISTINCT FROM source.PAYMENT_METHOD
                OR target.DISCOUNT_APPLIED IS DISTINCT FROM source.DISCOUNT_APPLIED
                OR target.TRANSACTION_STATUS IS DISTINCT FROM source.TRANSACTION_STATUS
                OR target.REVIEW_TEXT IS DISTINCT FROM source.REVIEW_TEXT
                OR target.GROSS_AMOUNT IS DISTINCT FROM source.GROSS_AMOUNT
                OR target.DISCOUNT_AMOUNT IS DISTINCT FROM source.DISCOUNT_AMOUNT
                OR target.NET_AMOUNT IS DISTINCT FROM source.NET_AMOUNT
            )
            THEN UPDATE SET
                target.CUSTOMER_ID = source.CUSTOMER_ID,
                target.TRANSACTION_DATE = source.TRANSACTION_DATE,
                target.PRODUCT_ID = source.PRODUCT_ID,
                target.QUANTITY = source.QUANTITY,
                target.UNIT_PRICE = source.UNIT_PRICE,
                target.PAYMENT_METHOD = source.PAYMENT_METHOD,
                target.DISCOUNT_APPLIED = source.DISCOUNT_APPLIED,
                target.TRANSACTION_STATUS = source.TRANSACTION_STATUS,
                target.REVIEW_TEXT = source.REVIEW_TEXT,
                target.GROSS_AMOUNT = source.GROSS_AMOUNT,
                target.DISCOUNT_AMOUNT = source.DISCOUNT_AMOUNT,
                target.NET_AMOUNT = source.NET_AMOUNT,
                target.MODIFIED_AT = '{job_start_time}'

        WHEN NOT MATCHED THEN
            INSERT (
                ID,
                CUSTOMER_ID,
                TRANSACTION_DATE,
                PRODUCT_ID,
                QUANTITY,
                UNIT_PRICE,
                PAYMENT_METHOD,
                DISCOUNT_APPLIED,
                TRANSACTION_STATUS,
                REVIEW_TEXT,
                GROSS_AMOUNT,
                DISCOUNT_AMOUNT,
                NET_AMOUNT,
                INSERTED_AT,
                MODIFIED_AT
            )
            VALUES (
                source.ID,
                source.CUSTOMER_ID,
                source.TRANSACTION_DATE,
                source.PRODUCT_ID,
                source.QUANTITY,
                source.UNIT_PRICE,
                source.PAYMENT_METHOD,
                source.DISCOUNT_APPLIED,
                source.TRANSACTION_STATUS,
                source.REVIEW_TEXT,
                source.GROSS_AMOUNT,
                source.DISCOUNT_AMOUNT,
                source.NET_AMOUNT,
                '{job_start_time}',
                '{job_start_time}'
            )
    """

    cursor = connection.cursor()

    try:
        logger.info("Starting transactions MERGE...")
        cursor.execute(merge_sql)

        logger.info(
            f"Transactions merge completed. "
            f"Rows affected: {cursor.rowcount}"
        )

    except Exception as error:
        raise RuntimeError(
            f"Failed to merge customers data: {error}"
        ) from error

    finally:
        cursor.close()