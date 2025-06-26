# unit_test.md

本ドキュメントは、作成した各主要モジュール・関数ごとに100%カバレッジを目指した単体テスト仕様書です。

---

## modules/s3_download.py

### list_csv_files
- **入力条件:**
    - bucket: str (S3バケット名)
    - prefix: str (S3キーのプレフィックス)
    - date_str: str (ファイル名に含まれる日付文字列)
- **実行方法:**
    - list_csv_files(bucket, prefix, date_str) を呼び出す
- **想定結果:**
    - prefix配下でdate_strを含むCSVファイルのS3キーリストを返す
    - 一致するファイルがなければ空リスト
    - バケットが存在しない/権限なしなら例外
    - paginatorの'Contents'がなければ空リスト
    - prefixが空ならルートから検索
    - date_strが空ならprefix配下の全CSVを返す
    - boto3設定不備なら例外
- **想定外ケース:**
    - bucketが空文字列
    - date_strが空文字列
    - 一致するファイルがない
    - S3クライアントの例外
    - 'Contents'が存在しない

### download_csv
- **入力条件:**
    - bucket: str (S3バケット名)
    - key: str (ダウンロード対象S3キー)
    - local_s3_dir: str (保存先ローカルディレクトリ)
    - prefix: str or None (任意)
- **実行方法:**
    - download_csv(bucket, key, local_s3_dir, prefix) を呼び出す
- **想定結果:**
    - S3からローカルにファイルをダウンロードしパスを返す
    - バケット/キーが存在しない場合は例外
    - local_s3_dirがなければ作成
    - 権限エラー時は例外
    - boto3設定不備なら例外
    - keyがCSVでなくてもダウンロード
    - local_s3_dirが書き込み不可なら例外
    - key/bucketが空なら例外
- **想定外ケース:**
    - keyが空文字列
    - bucketが空文字列
    - local_s3_dirが書き込み不可
    - S3クライアントの例外

---

## modules/s3_upload.py

### zip_csv_files
- **入力条件:**
    - csv_dir: str (CSVファイル格納ディレクトリ)
    - zip_path: str (出力zipファイルパス)
- **実行方法:**
    - zip_csv_files(csv_dir, zip_path) を呼び出す
- **想定結果:**
    - csv_dir内の全CSVをzip_pathにzip化
    - zip_pathを返す
    - csv_dirが存在しなければ例外
    - CSVがなければ空zip
    - zip_pathが書き込み不可なら例外
    - 非CSVファイルは無視
    - csv_dirが空なら空zip
    - csv_dirがディレクトリでなければ例外
- **想定外ケース:**
    - csv_dirが存在しない
    - csv_dirが空
    - zip_pathが書き込み不可
    - csv_dirがディレクトリでない

### upload_csv
- **入力条件:**
    - bucket: str (S3バケット名)
    - key: str (アップロード先S3キー)
    - file_path: str (アップロードするローカルファイルパス)
- **実行方法:**
    - upload_csv(bucket, key, file_path) を呼び出す
- **想定結果:**
    - file_pathをS3のbucket/keyにアップロード
    - file_pathがなければ例外
    - バケットが存在しない/権限なしなら例外
    - keyが空なら例外
    - file_pathが読込不可なら例外
    - boto3設定不備なら例外
- **想定外ケース:**
    - file_pathが存在しない
    - bucketが空
    - keyが空
    - file_pathが読込不可
    - S3クライアントの例外

---

## modules/check_process.py

### load_column_types
- **入力条件:**
    - columns.txt形式のファイルパス
- **実行方法:**
    - load_column_types(path) を呼び出す
- **想定結果:**
    - 正常な場合: カラム名→型のdictを返す
    - 空ファイル: 空dict
    - 不正な行: ValueError
- **想定外ケース:**
    - 空ファイル
    - 不正な行

### check_values
- **入力条件:**
    - DataFrame, カラム型dict
- **実行方法:**
    - check_values(df, column_types) を呼び出す
- **想定結果:**
    - 型変換・不正値は空文字列に変換、警告リスト返却
    - 余分なカラムは除外
- **想定外ケース:**
    - 存在しないカラムがDataFrameに含まれる
    - 型が全く異なる値（例: intカラムに"abc"や空リスト）
    - 欠損値（None, NaN, 空文字列, 空リスト, 空dict, 0, False, Trueなど）
    - 日付型カラムに不正な日付
    - float/intカラムに極端な値（inf, nan, 1e1000など）
    - strカラムに数値やNone
    - DataFrame自体が空、カラムが空、全値が空文字/None/NaN
    - columns.txtが空または不正な形式
    - 入力ファイルが壊れている/パース不能（上位層で例外）

---

# テストカバレッジ

- 上記の全仕様・想定外ケースは tests/test_s3_download.py, tests/test_s3_upload.py, tests/test_check_process.py で網羅的に自動テストされています。
- pytestで全ケース自動検証され、例外・エラーも含めて100%カバレッジを目指しています。
