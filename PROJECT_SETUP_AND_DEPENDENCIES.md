# E-commerce Sales ETL — Packages, Libraries & Commands Notes

## 1. Project Architecture

The current pipeline architecture:

```text
                    Kaggle
                      │
                      ▼
                KaggleHub
                      │
                      ▼
              Temporary download
                      │
                      ▼
              ┌──────────────┐
              │  S3 BRONZE   │
              │  Raw CSV     │
              └──────┬───────┘
                     │
                     ▼
              inspect_data()
                     │
                     ▼
              Schema Validation
                     │
                     ▼
               Transformation
                     │
                     ▼
           Post Transformation
                Validation
                     │
                     ▼
              ┌──────────────┐
              │  S3 SILVER   │
              │ Processed CSV│
              └──────┬───────┘
                     │
                     ▼
             Snowflake STG
                     │
                     ▼
                  MERGE
                     │
                     ▼
          Snowflake Analytics
```

---

# 2. Python Environment

## Create Virtual Environment

From the project root:

```powershell
python -m venv .venv
```

Activate on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

You should see:

```text
(.venv) PS C:\Dev\DataEngineering\ecommerce-sales-etl-and-analysis>
```

## Verify Python

```powershell
python --version
```

## Verify pip

```powershell
pip --version
```

## Upgrade pip

```powershell
python -m pip install --upgrade pip
```

---

# 3. Pandas

Package:

```text
pandas
```

Import:

```python
import pandas as pd
```

## Purpose

Used for:

* Reading CSV files
* DataFrames
* Data cleaning
* Data transformation
* Missing-value handling
* Duplicate detection
* Data type conversion
* Aggregation
* Writing CSV files

## Installation

```powershell
pip install pandas
```

## Verify

```powershell
python -c "import pandas; print(pandas.__version__)"
```

Our Snowflake integration currently uses a compatible pandas version.

---

# 4. pathlib

Python standard library.

Import:

```python
from pathlib import Path
```

## Purpose

Used for filesystem paths.

Example:

```python
download_path = Path(
    kagglehub.dataset_download(dataset_handler)
)
```

No pip installation is required.

`pathlib` is included with Python.

---

# 5. os

Python standard library.

Import:

```python
import os
```

## Purpose

Used primarily for environment variables.

Example:

```python
BRONZE_BUCKET = os.getenv("S3_BRONZE_BUCKET")
```

No pip installation is required.

---

# 6. datetime

Python standard library.

Import:

```python
from datetime import datetime
```

Used to create the pipeline/job start timestamp:

```python
job_start_time = datetime.now().astimezone()
```

Example:

```text
2026-08-29 17:17:42+05:30
```

This timestamp is used throughout the pipeline.

It is used for:

* S3 ingestion folders
* Batch identification
* Snowflake `INSERTED_AT`
* Snowflake `MODIFIED_AT`

No pip installation is required.

---

# 7. io

Python standard library.

Import:

```python
import io
```

We use:

```python
io.BytesIO()
```

to read S3 objects into pandas without first saving them to disk.

Example:

```python
response = s3_client.get_object(
    Bucket=BRONZE_BUCKET,
    Key=s3_key
)

df = pd.read_csv(
    io.BytesIO(response["Body"].read())
)
```

This allows:

```text
S3
 ↓
Memory
 ↓
DataFrame
```

instead of:

```text
S3
 ↓
Local file
 ↓
DataFrame
```

No pip installation is required.

---

# 8. Logging

Python standard library:

```python
import logging
```

Our project has:

```text
src/
└── utils/
    └── setup_logger.py
```

Import:

```python
from .utils.setup_logger import logger
```

## Common logging levels

```python
logger.debug(...)
logger.info(...)
logger.warning(...)
logger.error(...)
logger.exception(...)
```

Example:

```python
logger.info("Starting the pipeline...")
```

The logger is used for pipeline observability, including:

* Pipeline start/end
* Dataset extraction
* S3 uploads
* Data inspection
* Validation
* Transformation
* Snowflake loading
* MERGE operations
* Errors

No pip installation is required.

---

# 9. python-dotenv

Package:

```text
python-dotenv
```

Import:

```python
from dotenv import load_dotenv
```

## Installation

```powershell
pip install python-dotenv
```

## Purpose

Loads configuration values from `.env`.

Example `.env`:

```env
AWS_REGION=ap-south-1

S3_BRONZE_BUCKET=your-bronze-bucket
S3_SILVER_BUCKET=your-silver-bucket

KAGGLE_DATASET_HANDLER=your-kaggle-dataset

CUSTOMERS_TABLE=CUSTOMERS
CUSTOMERS_STG_TABLE=CUSTOMERS_STG

TRANSACTIONS_TABLE=TRANSACTIONS
TRANSACTIONS_STG_TABLE=TRANSACTIONS_STG
```

Load the variables:

```python
load_dotenv()
```

Access a variable:

```python
bucket = os.getenv("S3_BRONZE_BUCKET")
```

## Important

Never commit `.env` to GitHub.

Add this to `.gitignore`:

```gitignore
.env
```

---

# 10. KaggleHub

Package:

```text
kagglehub
```

Import:

```python
import kagglehub
```

## Installation

```powershell
pip install kagglehub
```

## Purpose

Downloads datasets from Kaggle.

Example:

```python
download_path = Path(
    kagglehub.dataset_download(dataset_handler)
)
```

The dataset handler is configured through `.env`:

```env
KAGGLE_DATASET_HANDLER=your-kaggle-dataset
```

Current architecture:

```text
Kaggle
   ↓
KaggleHub
   ↓
Temporary local download
   ↓
S3 Bronze
```

The temporary Kaggle download is not our permanent raw-data storage.

---

# 11. Boto3

Package:

```text
boto3
```

Import:

```python
import boto3
```

## Installation

Install inside the virtual environment:

```powershell
pip install boto3
```

## Verify

```powershell
python -c "import boto3; print(boto3.__version__)"
```

## Purpose

Boto3 is the AWS SDK for Python.

Our project uses it to communicate with Amazon S3.

We created:

```text
src/
└── utils/
    └── s3_client.py
```

Example:

```python
s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION
)
```

Architecture:

```text
Python
   ↓
boto3
   ↓
AWS
   ↓
S3
```

---

# 12. AWS CLI

AWS CLI is **not a Python package**.

It is installed separately on the operating system.

## Verify installation

```powershell
aws --version
```

Example:

```text
aws-cli/2.36.34 Python/3.14.6 Windows/11
```

## Purpose

Used to interact with AWS from the terminal.

Examples:

```powershell
aws sts get-caller-identity
```

```powershell
aws s3 ls
```

```powershell
aws s3 ls s3://YOUR_BUCKET
```

---

# 13. AWS IAM

IAM is an AWS service, not a Python library.

We created a dedicated IAM user for the ETL project.

The architecture is:

```text
Python
   ↓
boto3
   ↓
AWS Credentials
   ↓
IAM User
   ↓
IAM Policy
   ↓
S3
```

The IAM policy controls what the ETL application is allowed to do.

For example, access can be restricted to the project's Bronze and Silver buckets.

---

# 14. AWS CLI Configuration

Configure AWS credentials:

```powershell
aws configure
```

It asks for:

```text
AWS Access Key ID
AWS Secret Access Key
Default region
Default output format
```

Example region:

```text
ap-south-1
```

## Verify AWS identity

```powershell
aws sts get-caller-identity
```

This confirms which AWS IAM identity is currently being used.

## Important

Do not hard-code credentials in Python:

```python
# DON'T DO THIS

AWS_ACCESS_KEY = "..."
AWS_SECRET_KEY = "..."
```

Instead, allow Boto3 to use the AWS credential configuration.

---

# 15. Amazon S3

S3 is our cloud data-lake storage layer.

We use two logical layers:

```text
Bronze
Silver
```

## Bronze

Contains raw source data.

Example:

```text
customers/
└── ingestion_date=2026-08-29/
    └── ingestion_timestamp=20260829T171742/
        └── customers.csv
```

Transactions:

```text
transactions/
└── ingestion_date=2026-08-29/
    └── ingestion_timestamp=20260829T171742/
        └── transactions.csv
```

## Silver

Contains transformed/validated data.

Example:

```text
customers/
└── ingestion_date=2026-08-29/
    └── ingestion_timestamp=20260829T171742/
        └── customers.csv
```

---

# 16. Important Boto3 S3 Functions

## Upload a local file

```python
s3_client.upload_file(
    str(file),
    BRONZE_BUCKET,
    s3_key
)
```

Used for:

```text
Kaggle temporary file
        ↓
S3 Bronze
```

---

## Upload an in-memory file

```python
s3_client.upload_fileobj(
    csv_buffer,
    SILVER_BUCKET,
    s3_key
)
```

Used for:

```text
DataFrame
   ↓
BytesIO
   ↓
S3 Silver
```

---

## Read an S3 object

```python
response = s3_client.get_object(
    Bucket=BRONZE_BUCKET,
    Key=s3_key
)
```

---

## List S3 objects

```python
response = s3_client.list_objects_v2(
    Bucket=BRONZE_BUCKET
)
```

---

# 17. Snowflake Connector

Package:

```text
snowflake-connector-python
```

For pandas integration:

```powershell
pip install "snowflake-connector-python[pandas]"
```

## Verify

```powershell
python -c "import snowflake.connector; print(snowflake.connector.__version__)"
```

Verify `write_pandas`:

```powershell
python -c "from snowflake.connector.pandas_tools import write_pandas; print('write_pandas available')"
```

Our project currently uses the Snowflake Python connector to connect Python with Snowflake.

---

# 18. Snowflake Connection

Our project contains:

```text
src/
└── utils/
    └── snowflake_connection.py
```

We use:

```python
get_snowflake_connection()
```

The Snowflake connection contains configuration such as:

```text
Account
User
Authentication
Database
Schema
Warehouse
Role
```

The connection establishes the Snowflake session.

The loading function determines which Snowflake table should receive the DataFrame.

---

# 19. Snowflake `write_pandas()`

Import:

```python
from snowflake.connector.pandas_tools import write_pandas
```

Example:

```python
success, nchunks, nrows, _ = write_pandas(
    conn=connection,
    df=customers_df,
    table_name=CUSTOMERS_STG_TABLE,
    auto_create_table=False,
    overwrite=False,
    quote_identifiers=False
)
```

## Return values

```text
success
nchunks
nrows
output
```

We check:

```python
if not success:
    raise RuntimeError(...)
```

---

# 20. Snowflake Staging Tables

We created:

```text
CUSTOMERS_STG
TRANSACTIONS_STG
```

The loading flow is:

```text
S3 Silver
   ↓
Snowflake STG
   ↓
MERGE
   ↓
Target Table
```

Before loading a new batch:

```sql
TRUNCATE TABLE CUSTOMERS_STG;
```

and:

```sql
TRUNCATE TABLE TRANSACTIONS_STG;
```

This prevents old staging data from remaining during subsequent pipeline executions.

---

# 21. Snowflake MERGE

We created separate modules:

```text
src/
├── merge_customers.py
└── merge_transactions.py
```

The general pattern is:

```sql
MERGE INTO CUSTOMERS AS target
USING CUSTOMERS_STG AS source
    ON target.ID = source.ID
```

For existing records:

```sql
WHEN MATCHED AND (...)
THEN UPDATE
```

For new records:

```sql
WHEN NOT MATCHED
THEN INSERT
```

This implements an **upsert**.

---

# 22. `IS DISTINCT FROM`

We use:

```sql
target.NAME IS DISTINCT FROM source.NAME
```

instead of:

```sql
target.NAME <> source.NAME
```

`IS DISTINCT FROM` handles `NULL` comparisons safely.

This allows the MERGE to update a record only when its actual business data has changed.

This is important for:

```text
MODIFIED_AT
```

because we don't want to change `MODIFIED_AT` every time the pipeline runs if the data itself hasn't changed.

---

# 23. Pipeline Job Timestamp

At the beginning of `main.py`:

```python
job_start_time = datetime.now().astimezone()
```

The same timestamp is passed through the pipeline:

```text
main.py
   │
   ├── extract_dataset(job_start_time)
   │
   ├── inspect_data(job_start_time)
   │
   ├── transform_data(...)
   │
   ├── save_processed_data(..., job_start_time)
   │
   └── load_data(job_start_time)
```

This gives every pipeline run a consistent timestamp.

---

# 24. S3 Ingestion Timestamp

We derive:

```python
ingestion_date = job_start_time.strftime("%Y-%m-%d")
```

and:

```python
ingestion_timestamp = job_start_time.strftime(
    "%Y%m%dT%H%M%S"
)
```

For example:

```text
2026-08-29 17:17:42+05:30
```

becomes:

```text
ingestion_date=2026-08-29
ingestion_timestamp=20260829T171742
```

This allows us to preserve multiple ingestion runs.

---

# 25. Bronze vs Silver

## Bronze

```text
Kaggle
   ↓
Bronze
```

Characteristics:

* Raw data
* Historical data
* Timestamped ingestion
* Minimal modification
* Original source representation

## Silver

```text
Bronze
   ↓
Validation
   ↓
Transformation
   ↓
Silver
```

Characteristics:

* Cleaned
* Standardized
* Validated
* Transformed
* Ready for downstream consumption

---

# 26. Pandas Operations Used in the Project

## Read CSV

```python
pd.read_csv(file)
```

## Shape

```python
df.shape
```

## Columns

```python
df.columns.tolist()
```

## Data types

```python
df.dtypes
```

## Missing values

```python
df.isnull().sum()
```

## Duplicate rows

```python
df.duplicated().sum()
```

## Remove duplicates

```python
df.drop_duplicates()
```

## Convert to datetime

```python
pd.to_datetime(
    df["signup_date"],
    errors="coerce"
)
```

## Convert to numeric

```python
pd.to_numeric(
    df["unit_price"],
    errors="coerce"
)
```

## Convert to string

```python
df["phone_number"].astype("string")
```

## Strip whitespace

```python
df["name"].str.strip()
```

## Lowercase

```python
df["email"].str.lower()
```

## Fill missing values

```python
df["review_text"].fillna(
    "No review provided"
)
```

## Group median

```python
df.groupby("subscribe")["age"].median()
```

## Group-wise transformation

```python
df.groupby("subscribe")["age"].transform("median")
```

## Fill missing values using group median

```python
df["age"] = df["age"].fillna(
    df.groupby("subscribe")["age"].transform("median")
)
```

---

# 27. Current Python Dependencies

The main direct Python dependencies used by the project are:

```text
pandas
kagglehub
python-dotenv
boto3
snowflake-connector-python[pandas]
```

Install them together:

```powershell
pip install pandas kagglehub python-dotenv boto3 "snowflake-connector-python[pandas]"
```

---

# 28. `requirements.txt`

Create a dependency file:

```text
requirements.txt
```

Generate it from the active virtual environment:

```powershell
pip freeze > requirements.txt
```

A new developer can recreate the Python environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Important

`requirements.txt` contains Python dependencies.

It does not install/configure:

* AWS CLI
* AWS IAM
* Amazon S3
* Snowflake account
* Kaggle account

Those are external tools/services.

---

# 29. Useful Python Package Commands

## List installed packages

```powershell
pip list
```

## Show package details

```powershell
pip show pandas
```

```powershell
pip show boto3
```

```powershell
pip show kagglehub
```

```powershell
pip show python-dotenv
```

## Check outdated packages

```powershell
pip list --outdated
```

## Upgrade a package

```powershell
pip install --upgrade boto3
```

## Uninstall a package

```powershell
pip uninstall boto3
```

---

# 30. AWS Useful Commands

## Check AWS CLI

```powershell
aws --version
```

## Configure AWS

```powershell
aws configure
```

## Verify IAM identity

```powershell
aws sts get-caller-identity
```

## List buckets

```powershell
aws s3 ls
```

If the IAM user doesn't have:

```text
s3:ListAllMyBuckets
```

this command can return:

```text
AccessDenied
```

That does not necessarily mean access to a specific bucket is unavailable.

## List a specific bucket

```powershell
aws s3 ls s3://YOUR_BUCKET
```

## List a folder

```powershell
aws s3 ls s3://YOUR_BUCKET/customers/
```

## Recursive listing

```powershell
aws s3 ls s3://YOUR_BUCKET --recursive
```

---

# 31. Git Commands

## Check repository status

```powershell
git status
```

## Add files

```powershell
git add .
```

## Commit

```powershell
git commit -m "Integrate S3 bronze and silver layers"
```

## Push

```powershell
git push
```

## Create feature branch

```powershell
git checkout -b feature/aws-s3-integration
```

## Switch branch

```powershell
git checkout main
```

---

# 32. `.gitignore`

At minimum:

```gitignore
.venv/
.env
__pycache__/
*.pyc
logs/
```

Since raw and processed data are now stored in S3, local data directories can also be excluded:

```gitignore
data/raw/
data/processed/
```

---

# 33. Current Project Structure

The project is moving toward this structure:

```text
ecommerce-sales-etl-and-analysis/
│
├── .venv/
├── .env
├── .gitignore
├── requirements.txt
├── main.py
│
├── config/
│   └── schema.py
│
├── src/
│   │
│   ├── data_extract.py
│   ├── inspect_data.py
│   ├── validate_schema.py
│   ├── transform_data.py
│   ├── validate_transformed_data.py
│   ├── save_processed_data.py
│   ├── load_data.py
│   ├── merge_customers.py
│   ├── merge_transactions.py
│   │
│   └── utils/
│       ├── setup_logger.py
│       ├── s3_client.py
│       └── snowflake_connection.py
│
└── logs/
```

The actual data is stored externally:

```text
AWS S3
│
├── Bronze
│   ├── customers/
│   └── transactions/
│
└── Silver
    ├── customers/
    └── transactions/

Snowflake
│
├── CUSTOMERS_STG
├── TRANSACTIONS_STG
├── CUSTOMERS
└── TRANSACTIONS
```

---

# 34. Complete Installation

If setting up the project from scratch:

## Step 1 — Create virtual environment

```powershell
python -m venv .venv
```

## Step 2 — Activate

```powershell
.venv\Scripts\Activate.ps1
```

## Step 3 — Upgrade pip

```powershell
python -m pip install --upgrade pip
```

## Step 4 — Install Python dependencies

```powershell
pip install pandas kagglehub python-dotenv boto3 "snowflake-connector-python[pandas]"
```

## Step 5 — Save dependencies

```powershell
pip freeze > requirements.txt
```

## Step 6 — Configure AWS CLI

```powershell
aws configure
```

## Step 7 — Verify AWS

```powershell
aws sts get-caller-identity
```

## Step 8 — Verify Python AWS SDK

```powershell
python -c "import boto3; print(boto3.__version__)"
```

## Step 9 — Verify pandas

```powershell
python -c "import pandas; print(pandas.__version__)"
```

## Step 10 — Verify Snowflake

```powershell
python -c "import snowflake.connector; print(snowflake.connector.__version__)"
```

## Step 11 — Verify `write_pandas`

```powershell
python -c "from snowflake.connector.pandas_tools import write_pandas; print('write_pandas available')"
```

## Step 12 — Run pipeline

```powershell
python main.py
```

---

# 35. Quick Command Cheat Sheet

## Python

```powershell
python --version
```

```powershell
python -m venv .venv
```

```powershell
.venv\Scripts\Activate.ps1
```

```powershell
python -m pip install --upgrade pip
```

---

## Packages

```powershell
pip install pandas
```

```powershell
pip install kagglehub
```

```powershell
pip install python-dotenv
```

```powershell
pip install boto3
```

```powershell
pip install "snowflake-connector-python[pandas]"
```

### Install everything

```powershell
pip install pandas kagglehub python-dotenv boto3 "snowflake-connector-python[pandas]"
```

---

## Dependencies

```powershell
pip freeze > requirements.txt
```

```powershell
pip install -r requirements.txt
```

---

## AWS

```powershell
aws --version
```

```powershell
aws configure
```

```powershell
aws sts get-caller-identity
```

```powershell
aws s3 ls
```

```powershell
aws s3 ls s3://YOUR_BUCKET
```

```powershell
aws s3 ls s3://YOUR_BUCKET --recursive
```

---

## Package Verification

```powershell
python -c "import pandas; print(pandas.__version__)"
```

```powershell
python -c "import boto3; print(boto3.__version__)"
```

```powershell
python -c "import kagglehub; print('kagglehub available')"
```

```powershell
python -c "import snowflake.connector; print(snowflake.connector.__version__)"
```

```powershell
python -c "from snowflake.connector.pandas_tools import write_pandas; print('write_pandas available')"
```

---

## Git

```powershell
git status
```

```powershell
git add .
```

```powershell
git commit -m "Your commit message"
```

```powershell
git push
```

```powershell
git checkout -b feature/branch-name
```

---

# 36. Key Concepts to Remember

Don't just memorize the package names. Understand the responsibility of each component.

| Component                    | Role                                    |
| ---------------------------- | --------------------------------------- |
| `pandas`                     | Data processing                         |
| `pathlib`                    | File/path handling                      |
| `os`                         | Environment variables and OS operations |
| `logging`                    | Pipeline observability                  |
| `datetime`                   | Job/batch timestamps                    |
| `io`                         | In-memory file handling                 |
| `python-dotenv`              | Configuration management                |
| `kagglehub`                  | Source extraction                       |
| `boto3`                      | Python → AWS                            |
| AWS CLI                      | AWS terminal interaction                |
| IAM                          | Authentication and authorization        |
| S3                           | Data Lake storage                       |
| `snowflake-connector-python` | Python → Snowflake                      |
| `write_pandas()`             | DataFrame → Snowflake                   |
| Snowflake STG                | Loading/staging layer                   |
| Snowflake `MERGE`            | Upsert/incremental loading              |
| Git                          | Source control                          |

---

# 37. Architecture Responsibilities

The most important distinction is:

```text
KaggleHub
    = EXTRACT
```

```text
Pandas
    = TRANSFORM
```

```text
S3 Bronze
    = RAW DATA
```

```text
S3 Silver
    = PROCESSED DATA
```

```text
Snowflake STG
    = LOAD BUFFER
```

```text
Snowflake Analytics
    = TARGET / SERVING LAYER
```

The overall ETL flow is therefore:

```text
EXTRACT
   ↓
KaggleHub
   ↓
S3 Bronze

TRANSFORM
   ↓
Pandas
   ↓
S3 Silver

LOAD
   ↓
Snowflake STG
   ↓
MERGE
   ↓
Snowflake Analytics
```

This separation of responsibilities is the core architecture of the **E-commerce Sales ETL project**.
