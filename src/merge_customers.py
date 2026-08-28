
from .utils.setup_logger import logger

def merge_customers(connection, job_start_time, CUSTOMERS_TABLE, CUSTOMERS_STG_TABLE):
    """Merge staged customer records into the customers table."""

    logger.info("Merging customers staging data...")

    merge_sql = f"""
        MERGE INTO {CUSTOMERS_TABLE} AS target
        USING {CUSTOMERS_STG_TABLE} AS source
            ON target.ID = source.ID

        WHEN MATCHED AND (
                target.NAME IS DISTINCT FROM source.NAME
                OR target.AGE IS DISTINCT FROM source.AGE
                OR target.GENDER IS DISTINCT FROM source.GENDER
                OR target.STATE IS DISTINCT FROM source.STATE
                OR target.SIGNUP_DATE IS DISTINCT FROM source.SIGNUP_DATE
                OR target.EMAIL IS DISTINCT FROM source.EMAIL
                OR target.PHONE_NUMBER IS DISTINCT FROM source.PHONE_NUMBER
                OR target.SUBSCRIBE IS DISTINCT FROM source.SUBSCRIBE 
            )
            THEN UPDATE SET
                target.NAME = source.NAME,
                target.AGE = source.AGE,
                target.GENDER = source.GENDER,
                target.STATE = source.STATE,
                target.SIGNUP_DATE = source.SIGNUP_DATE,
                target.EMAIL = source.EMAIL,
                target.PHONE_NUMBER = source.PHONE_NUMBER,
                target.SUBSCRIBE = source.SUBSCRIBE,
                target.MODIFIED_AT = '{job_start_time}'

        WHEN NOT MATCHED THEN
            INSERT (
                ID,
                NAME,
                AGE,
                GENDER,
                STATE,
                SIGNUP_DATE,
                EMAIL,
                PHONE_NUMBER,
                SUBSCRIBE,
                INSERTED_AT,
                MODIFIED_AT
            )
            VALUES (
                source.ID,
                source.NAME,
                source.AGE,
                source.GENDER,
                source.STATE,
                source.SIGNUP_DATE,
                source.EMAIL,
                source.PHONE_NUMBER,
                source.SUBSCRIBE,
                '{job_start_time}',
                '{job_start_time}'
            )
    """

    cursor = connection.cursor()

    try:
        logger.info("Starting customers MERGE...")
        cursor.execute(merge_sql)

        logger.info(
            f"Customers merge completed. "
            f"Rows affected: {cursor.rowcount}"
        )

    except Exception as error:
        raise RuntimeError(
            f"Failed to merge customers data: {error}"
        ) from error

    finally:
        cursor.close()