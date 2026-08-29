import json
import boto3

from aws.utils.logger import logger
from aws.config import AWS_REGION


secrets_manager_client = boto3.client(
    "secretsmanager",
    region_name=AWS_REGION
)


def get_secret(secret_name: str) -> dict:
    """Retrieve and return a JSON secret from AWS Secrets Manager."""

    logger.info(
        f"Retrieving secret: {secret_name}"
    )

    try:
        response = secrets_manager_client.get_secret_value(
            SecretId=secret_name
        )

        secret_string = response.get("SecretString")

        if not secret_string:
            raise ValueError(
                f"Secret {secret_name} does not contain SecretString."
            )

        secret = json.loads(secret_string)

        logger.info(
            f"Secret retrieved successfully: {secret_name}"
        )

        return secret

    except Exception as error:
        logger.exception(
            f"Failed to retrieve secret: {secret_name}"
        )

        raise RuntimeError(
            f"Failed to retrieve secret {secret_name}: {error}"
        ) from error