import os  # OS操作用

import boto3  # AWS SDK for Python（AWS用SDK）


from datetime import datetime  # 日付操作用


def list_csv_files(bucket, prefix, date_str):
    """
    指定したプレフィックスと日付文字列でS3バケット内のCSVファイルをリストアップします。
    新形式: prefix/グループ名/YYYY-MM-DD_hhmm.csv
    引数:
        bucket (str): S3バケット名。
        prefix (str): S3キーのプレフィックス。
        date_str (str): ファイルをフィルタリングする日付文字列。
    戻り値:
        list: 条件に一致するCSVファイルキーのリスト。
    """
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    files = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        if 'Contents' in page:
            for obj in page['Contents']:
                key = obj['Key']
                # 例: test/2025-06-12_0900.csv
                base = os.path.basename(key)
                # フォーマット: YYYY-MM-DD_hhmm.csv
                if (
                    key.endswith('.csv')
                    and date_str in base
                    and len(base.split('_')) == 2
                    and base.split('_')[1].endswith('.csv')
                ):
                    files.append(key)
    return files

def download_csv(bucket, key, local_s3_dir, prefix=None):
    """
    S3からCSVファイルをローカルディレクトリにダウンロードします。
    引数:
        bucket (str): S3バケット名。
        key (str): ダウンロードするファイルのS3キー。
        local_s3_dir (str): ファイルを保存するローカルディレクトリ。
    戻り値:
        str: ダウンロードしたCSVファイルのローカルパス。
    """
    s3 = boto3.client('s3')
    if not os.path.exists(local_s3_dir):
        os.makedirs(local_s3_dir)
    # 新形式: グループ名/ファイル名で保存
    rel_path = key
    local_path = os.path.join(local_s3_dir, rel_path)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    s3.download_file(bucket, key, local_path)
    return local_path
