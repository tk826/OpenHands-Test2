import os
import boto3
import zipfile

def zip_csv_files(csv_dir, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in os.listdir(csv_dir):
            if file.endswith('.csv'):
                zipf.write(os.path.join(csv_dir, file), arcname=file)
    return zip_path

def upload_csv(bucket, key, file_path):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket, key)
