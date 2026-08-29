import os
import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")

s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION
)