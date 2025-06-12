import os  # OS操作用

import boto3  # AWS SDK for Python（AWS用SDK）


from datetime import datetime  # 日付操作用


def list_csv_files(bucket, prefix, date_str):
    """
    List CSV files in an S3 bucket with a specific prefix and date string.
    Args:
        bucket (str): S3 bucket name.
        prefix (str): Prefix for S3 keys.
        date_str (str): Date string to filter files.
    Returns:
        list: List of matching CSV file keys.
    """
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    files = []
    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']
            if key.endswith('.csv') and date_str in key:
                files.append(key)
    return files

def download_csv(bucket, key, local_dir):
    """
    Download a CSV file from S3 to a local directory.
    Args:
        bucket (str): S3 bucket name.
        key (str): S3 key of the file.
        local_dir (str): Local directory to save the file.
    Returns:
        str: Local file path of the downloaded CSV.
    """
    s3 = boto3.client('s3')
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    local_path = os.path.join(local_dir, os.path.basename(key))
    s3.download_file(bucket, key, local_path)
    return local_path
