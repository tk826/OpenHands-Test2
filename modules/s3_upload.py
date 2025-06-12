import os  # OS操作用

import boto3  # AWS SDK for Python（AWS用SDK）


import zipfile  # ZIPアーカイブ作成用



def zip_csv_files(csv_dir, zip_path):
    """
    Zip all CSV files in a directory into a single zip archive.
    Args:
        csv_dir (str): Directory containing CSV files.
        zip_path (str): Output path for the zip file.
    Returns:
        str: Path to the created zip file.
    """
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in os.listdir(csv_dir):
            if file.endswith('.csv'):
                zipf.write(os.path.join(csv_dir, file), arcname=file)
    return zip_path

def upload_csv(bucket, key, file_path):
    """
    Upload a file to S3.
    Args:
        bucket (str): S3 bucket name.
        key (str): S3 key for the uploaded file.
        file_path (str): Local path to the file to upload.
    """
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket, key)
