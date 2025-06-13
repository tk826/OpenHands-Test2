import os  # OS操作用

import pandas as pd  # データ操作用
from dotenv import load_dotenv  # .envファイルから環境変数を読み込むため
from modules.s3_download import list_csv_files, download_csv  # S3からのダウンロード用ユーティリティ
from modules.s3_upload import zip_csv_files, upload_csv  # S3へのアップロード用ユーティリティ
from modules.check_process import load_column_types, check_values  # データ検証用ユーティリティ


import re
from collections import defaultdict
def main():
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

    # ファイル名からグループ化: { (date, group): [(time, filepath), ...] }
    pattern = re.compile(r'(\d{4}-\d{2}-\d{2})_(\d+)_([^.]+)\.csv$')
    grouped = defaultdict(list)
    for file in local_files:
        m = pattern.search(os.path.basename(file))
        if m:
            date, time, group = m.group(1), m.group(2), m.group(3)
            grouped[(date, group)].append((int(time), file))
        else:
            print(f"ファイル名形式不正: {file}")

    column_types = load_column_types(columns_file)
    output_files = []
    for (date, group), filelist in grouped.items():
        # 時分でソート
        filelist.sort()
        dfs = []
        for _, file in filelist:
            df = pd.read_csv(file)
            df, warnings = check_values(df, column_types)
            if warnings:
                print(f"警告({file}):")
                for w in warnings:
                    print('  ', w)
            dfs.append(df)
        if dfs:
            merged = pd.concat(dfs, ignore_index=True)
            outname = f"{date}_{group}.csv"
            outpath = os.path.join(local_dir, outname)
            merged.to_csv(outpath, index=False)
            output_files.append(outpath)
            print(f"出力: {outpath}")

    # 必要ならZIP圧縮やS3アップロード処理をここでoutput_filesに対して行う
    # 例: zip_path = os.path.join(local_dir, f"csv_{date_str}.zip")
    #     zip_csv_files(local_dir, zip_path)
    #     upload_key = f"{prefix}csv_{date_str}.zip"
    #     upload_csv(bucket, upload_key, zip_path)

if __name__ == '__main__':
    main()
