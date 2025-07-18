import os  # OS操作用

import boto3  # AWS SDK for Python（AWS用SDK）


import zipfile  # ZIPアーカイブ作成用



def zip_csv_files(csv_dir, zip_path):
    """
    ディレクトリ内のすべてのCSVファイルを1つのzipアーカイブにまとめます。
    引数:
        csv_dir (str): CSVファイルが格納されているディレクトリ。
        zip_path (str): 出力するzipファイルのパス。
    戻り値:
        str: 作成されたzipファイルのパス。
    """
    if csv_dir is None:
        raise TypeError('csv_dir is None')
    if not csv_dir:
        raise ValueError('csv_dir is empty')
    if not zip_path:
        raise ValueError('zip_path is empty')
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in os.listdir(csv_dir):
            if file.endswith('.csv'):
                zipf.write(os.path.join(csv_dir, file), arcname=file)
    return zip_path

def upload_csv(bucket, key, file_path):
    """
    ファイルをS3にアップロードします。
    引数:
        bucket (str): S3バケット名。
        key (str): アップロード先のS3キー。
        file_path (str): アップロードするローカルファイルのパス。
    """
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket, key)
