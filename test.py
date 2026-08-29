import os
from dotenv import load_dotenv

from src.utils.s3_client import s3_client

load_dotenv()

bronze_bucket = os.getenv("S3_BRONZE_BUCKET")

try:
    s3_client.head_bucket(Bucket=bronze_bucket)
    print(f"Successfully connected to: {bronze_bucket}")

except Exception as error:
    print(f"S3 connection failed: {error}")