from datetime import datetime

from aws.utils.dynamodb_client import create_execution
from aws.utils.execution_context import create_execution_context
from aws.utils.logger import logger


PIPELINE_NAME = "ecommerce-sales-etl"


def lambda_handler(event, context):
    """
    AWS Lambda entry point.

    Handles Lambda-specific configuration and
    delegates execution to scheduled_handler().
    """

    logger.info(
        "Pipeline Start Lambda execution started."
    )

    return scheduled_handler(event, context)


def scheduled_handler(event, context):
    """
    Prepare execution metadata for the pipeline.
    """

    logger.info(
        "Preparing pipeline execution context..."
    )

    job_context = create_execution_context(
        PIPELINE_NAME
    )

    create_execution(
        execution_id=job_context["execution_id"],
        pipeline_name=job_context["pipeline_name"],
        job_start_timestamp=job_context["job_start_timestamp"]
    )

    return process_handler(job_context)


def process_handler(job_context):
    """
    Return the execution context to Step Functions.
    """

    logger.info(
        "Pipeline execution context created successfully."
    )

    logger.info(
        f"Execution ID: {job_context['execution_id']}"
    )

    logger.info(
        f"Job start timestamp: "
        f"{job_context['job_start_timestamp']}"
    )

    return {
        "status": "RUNNING",
        "execution_id": job_context["execution_id"],
        "pipeline_name": job_context["pipeline_name"],
        "job_start_timestamp": job_context[
            "job_start_timestamp"
        ]
    }