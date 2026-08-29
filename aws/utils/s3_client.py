import boto3

from aws.utils.logger import logger
from aws.config import AWS_REGION


s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION
)


def upload_file(
    file_path: str,
    bucket_name: str,
    s3_key: str
) -> None:
    """Upload a local file to an S3 bucket."""

    logger.info(
        f"Uploading file to S3: "
        f"s3://{bucket_name}/{s3_key}"
    )

    try:

        s3_client.upload_file(
            Filename=file_path,
            Bucket=bucket_name,
            Key=s3_key
        )

        logger.info(
            f"File uploaded successfully: "
            f"s3://{bucket_name}/{s3_key}"
        )

    except Exception as error:

        logger.exception(
            f"Failed to upload file to S3: "
            f"s3://{bucket_name}/{s3_key}"
        )

        raise RuntimeError(
            f"Failed to upload file to S3: {error}"
        ) from error


def get_object(
    bucket_name: str,
    s3_key: str
):
    """Retrieve an object from S3."""

    logger.info(
        f"Reading object from S3: "
        f"s3://{bucket_name}/{s3_key}"
    )

    try:

        response = s3_client.get_object(
            Bucket=bucket_name,
            Key=s3_key
        )

        logger.info(
            f"Object retrieved successfully: "
            f"s3://{bucket_name}/{s3_key}"
        )

        return response

    except Exception as error:

        logger.exception(
            f"Failed to retrieve object from S3: "
            f"s3://{bucket_name}/{s3_key}"
        )

        raise RuntimeError(
            f"Failed to retrieve object from S3: {error}"
        ) from error


def list_objects(
    bucket_name: str,
    prefix: str = ""
) -> list:
    """List objects in an S3 bucket under a prefix."""

    logger.info(
        f"Listing S3 objects: "
        f"s3://{bucket_name}/{prefix}"
    )

    try:

        response = s3_client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix
        )

        objects = response.get(
            "Contents",
            []
        )

        logger.info(
            f"Found {len(objects)} objects in "
            f"s3://{bucket_name}/{prefix}"
        )

        return objects

    except Exception as error:

        logger.exception(
            f"Failed to list S3 objects: "
            f"s3://{bucket_name}/{prefix}"
        )

        raise RuntimeError(
            f"Failed to list S3 objects: {error}"
        ) from error