import os
import boto3

from aws.utils.logger import logger
from aws.config import AWS_REGION
from aws.config import DYNAMODB_EXECUTIONS_TABLE


AWS_REGION = os.getenv("AWS_REGION")
DYNAMODB_EXECUTIONS_TABLE = os.getenv(
    "DYNAMODB_EXECUTIONS_TABLE"
)


dynamodb_client = boto3.client(
    "dynamodb",
    region_name=AWS_REGION
)


def create_execution(
    execution_id: str,
    pipeline_name: str,
    job_start_timestamp: str
) -> None:
    """Create a new pipeline execution record in DynamoDB."""

    if not DYNAMODB_EXECUTIONS_TABLE:
        raise ValueError(
            "DYNAMODB_EXECUTIONS_TABLE environment variable "
            "is not configured."
        )

    logger.info(
        f"Creating pipeline execution: {execution_id}"
    )

    try:
        dynamodb_client.put_item(
            TableName=DYNAMODB_EXECUTIONS_TABLE,
            Item={
                "execution_id": {
                    "S": execution_id
                },
                "pipeline_name": {
                    "S": pipeline_name
                },
                "job_start_timestamp": {
                    "S": job_start_timestamp
                },
                "status": {
                    "S": "RUNNING"
                }
            },
            ConditionExpression=(
                "attribute_not_exists(execution_id)"
            )
        )

        logger.info(
            f"Pipeline execution created successfully: "
            f"{execution_id}"
        )

    except Exception as error:
        logger.exception(
            f"Failed to create pipeline execution: "
            f"{execution_id}"
        )
        raise RuntimeError(
            f"Failed to create pipeline execution: {error}"
        ) from error


def update_execution_status(
    execution_id: str,
    status: str,
    completed_timestamp: str | None = None
) -> None:
    """Update the status of a pipeline execution."""

    if not DYNAMODB_EXECUTIONS_TABLE:
        raise ValueError(
            "DYNAMODB_EXECUTIONS_TABLE environment variable "
            "is not configured."
        )

    logger.info(
        f"Updating execution {execution_id} "
        f"to status: {status}"
    )

    try:
        update_expression = "SET #status = :status"

        expression_attribute_names = {
            "#status": "status"
        }

        expression_attribute_values = {
            ":status": {
                "S": status
            }
        }

        if completed_timestamp:

            update_expression += (
                ", completed_timestamp = :completed_timestamp"
            )

            expression_attribute_values[
                ":completed_timestamp"
            ] = {
                "S": completed_timestamp
            }

        dynamodb_client.update_item(
            TableName=DYNAMODB_EXECUTIONS_TABLE,
            Key={
                "execution_id": {
                    "S": execution_id
                }
            },
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values
        )

        logger.info(
            f"Execution updated successfully: {execution_id}"
        )

    except Exception as error:
        logger.exception(
            f"Failed to update execution: {execution_id}"
        )

        raise RuntimeError(
            f"Failed to update execution status: {error}"
        ) from error