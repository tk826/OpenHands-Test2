import os  # OS操作用

import pandas as pd  # データ操作用
from dotenv import load_dotenv  # .envファイルから環境変数を読み込むため
from s3_download import list_csv_files, download_csv  # S3からのダウンロード用ユーティリティ
from s3_upload import zip_csv_files, upload_csv  # S3へのアップロード用ユーティリティ
from check_process import load_column_types, check_values  # データ検証用ユーティリティ


def main():
    """
    Main workflow for downloading, validating, zipping, and uploading CSV files from/to S3.
    Steps:
        1. Load environment variables.
        2. Get target date from user input.
        3. List and download CSV files from S3.
        4. Validate and clean data.
        5. Zip processed CSVs.
        6. Upload the zip file to S3.
    """
    load_dotenv()
    bucket = os.getenv('S3_BUCKET')
    prefix = os.getenv('S3_PREFIX')
    local_dir = os.getenv('LOCAL_DIR')
    columns_file = os.getenv('COLUMNS_FILE')
    date_str = input('対象日付(YYYY-MM-DD): ').strip()

    # S3からCSV一覧取得
    csv_keys = list_csv_files(bucket, prefix, date_str)
    print(f"取得CSV: {csv_keys}")
    local_files = []
    for key in csv_keys:
        local_path = download_csv(bucket, key, local_dir)
        local_files.append(local_path)

    # データ検証・加工
    column_types = load_column_types(columns_file)
    for file in local_files:
        df = pd.read_csv(file)
        df, warnings = check_values(df, column_types)
        if warnings:
            print(f"警告({file}):")
            for w in warnings:
                print('  ', w)
        df.to_csv(file, index=False)

    # ZIP圧縮
    zip_path = os.path.join(local_dir, f"csv_{date_str}.zip")
    zip_csv_files(local_dir, zip_path)

    # S3へアップロード
    upload_key = f"{prefix}csv_{date_str}.zip"
    upload_csv(bucket, upload_key, zip_path)
    print(f"アップロード完了: {upload_key}")

if __name__ == '__main__':
    main()
