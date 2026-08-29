import os

from dotenv import load_dotenv


load_dotenv()


AWS_REGION = os.getenv("AWS_REGION")

DYNAMODB_EXECUTIONS_TABLE = os.getenv(
    "DYNAMODB_EXECUTIONS_TABLE"
)

S3_BRONZE_BUCKET = os.getenv(
    "S3_BRONZE_BUCKET"
)

S3_SILVER_BUCKET = os.getenv(
    "S3_SILVER_BUCKET"
)