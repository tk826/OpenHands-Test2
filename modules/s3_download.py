import os
import boto3
from datetime import datetime

def list_csv_files(bucket, prefix, date_str):
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
    s3 = boto3.client('s3')
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    local_path = os.path.join(local_dir, os.path.basename(key))
    s3.download_file(bucket, key, local_path)
    return local_path
