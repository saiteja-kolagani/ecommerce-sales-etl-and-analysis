import kagglehub
from pathlib import Path
import shutil

# Download latest version
download_path = kagglehub.dataset_download("saidnizam/messy-e-commerce-dataset")

# Project's raw data directory
raw_data_dir = Path(__file__).parent.parent / "data" / "raw"
raw_data_dir.mkdir(parents=True, exist_ok=True)

# Copy downloaded files to the raw data directory
for file in Path(download_path).iterdir():
    if file.is_file():
        shutil.copy(file, raw_data_dir / file.name)

print(f"Dataset downloaded to:, {raw_data_dir.resolve()}")