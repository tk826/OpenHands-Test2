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

def zip_csv_files(csv_dir, zip_path):
    """
    ディレクトリ内のすべてのCSVファイルを1つのzipアーカイブにまとめます。
    引数:
        csv_dir (str): CSVファイルが格納されているディレクトリ。
        zip_path (str): 出力するzipファイルのパス。
    戻り値:
        str: 作成されたzipファイルのパス。
    """
    import zipfile
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in os.listdir(csv_dir):
            if file.endswith('.csv'):
                zipf.write(os.path.join(csv_dir, file), arcname=file)
    return zip_path

def upload_file_to_s3(bucket, key, file_path):
    """
    ファイルをS3にアップロードします。
    引数:
        bucket (str): S3バケット名。
        key (str): アップロード先のS3キー。
        file_path (str): アップロードするローカルファイルのパス。
    """
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket, key)

def main_workflow():
    """
    S3からCSVファイルをダウンロード、検証、圧縮し、再度S3にアップロードするメインワークフロー。
    手順:
        1. 環境変数の読み込み。
        2. ユーザー入力から対象日付を取得。
        3. S3からCSVファイルをリストアップ・ダウンロード。
        4. データの検証・クリーニング。
        5. 処理済みCSVをzip化。
        6. zipファイルをS3にアップロード。
    """
    pass

