# TEST SPEC: modules/s3_download.py

## list_csv_files
- **Input conditions:**
    - bucket: str (S3 bucket name)
    - prefix: str (S3 key prefix)
    - date_str: str (date string to filter files)
- **Execution method:**
    - Call list_csv_files(bucket, prefix, date_str)
- **Expected results:**
    - Returns a list of S3 keys for CSV files matching the prefix and containing date_str in the filename.
    - If no files match, returns an empty list.
    - If bucket does not exist or permission denied, raises an exception.
    - If paginator returns no 'Contents', returns an empty list.
    - If prefix is empty, searches from root.
    - If date_str is empty, returns all CSV files under prefix.
    - If boto3 is misconfigured, raises exception.

## download_csv
- **Input conditions:**
    - bucket: str (S3 bucket name)
    - key: str (S3 key to download)
    - local_s3_dir: str (local directory to save file)
    - prefix: str or None (optional, not used in logic)
- **Execution method:**
    - Call download_csv(bucket, key, local_s3_dir, prefix)
- **Expected results:**
    - Downloads the file from S3 to the specified local directory, preserving subdirectory structure.
    - Returns the local file path.
    - If the bucket/key does not exist, raises an exception.
    - If local_s3_dir does not exist, creates it.
    - If permission denied (S3 or local), raises an exception.
    - If boto3 is misconfigured, raises exception.
    - If key is not a CSV file, still downloads (no check).
    - If local_s3_dir is not writable, raises exception.
    - If key is empty, raises exception.
    - If bucket is empty, raises exception.
