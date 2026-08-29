from datetime import datetime


def create_execution_context(
    pipeline_name: str
) -> dict:
    """Create metadata for a new pipeline execution."""

    job_start_time = datetime.now().astimezone()

    execution_id = job_start_time.strftime(
        "%Y%m%dT%H%M%S%f"
    )

    return {
        "execution_id": execution_id,
        "pipeline_name": pipeline_name,
        "job_start_timestamp": job_start_time.isoformat()
    }