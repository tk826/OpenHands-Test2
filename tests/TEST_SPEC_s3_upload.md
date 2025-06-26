# TEST SPEC: modules/s3_upload.py

## zip_csv_files
- **Input conditions:**
    - csv_dir: str (directory containing CSV files)
    - zip_path: str (output zip file path)
- **Execution method:**
    - Call zip_csv_files(csv_dir, zip_path)
- **Expected results:**
    - Creates a zip file at zip_path containing all CSV files in csv_dir.
    - Returns the zip_path.
    - If csv_dir does not exist, raises exception.
    - If no CSV files, creates empty zip.
    - If zip_path is not writable, raises exception.
    - If csv_dir contains non-CSV files, ignores them.
    - If csv_dir is empty, creates empty zip.
    - If csv_dir is not a directory, raises exception.

## upload_csv
- **Input conditions:**
    - bucket: str (S3 bucket name)
    - key: str (S3 key to upload to)
    - file_path: str (local file path to upload)
- **Execution method:**
    - Call upload_csv(bucket, key, file_path)
- **Expected results:**
    - Uploads the file at file_path to S3 at bucket/key.
    - If file_path does not exist, raises exception.
    - If bucket does not exist or permission denied, raises exception.
    - If key is empty, raises exception.
    - If file_path is not readable, raises exception.
    - If boto3 is misconfigured, raises exception.
