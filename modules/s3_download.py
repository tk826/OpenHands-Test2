import os  # OS操作用

import boto3  # AWS SDK for Python（AWS用SDK）


from datetime import datetime  # 日付操作用


def list_csv_files(bucket, prefix, date_str):
    """
    指定したプレフィックスと日付文字列でS3バケット内のCSVファイルをリストアップします。
    引数:
        bucket (str): S3バケット名。
        prefix (str): S3キーのプレフィックス。
        date_str (str): ファイルをフィルタリングする日付文字列。
    戻り値:
        list: 条件に一致するCSVファイルキーのリスト。
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
    S3からCSVファイルをローカルディレクトリにダウンロードします。
    引数:
        bucket (str): S3バケット名。
        key (str): ダウンロードするファイルのS3キー。
        local_dir (str): ファイルを保存するローカルディレクトリ。
    戻り値:
        str: ダウンロードしたCSVファイルのローカルパス。
    """
    s3 = boto3.client('s3')
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    local_path = os.path.join(local_dir, os.path.basename(key))
    s3.download_file(bucket, key, local_path)
    return local_path
