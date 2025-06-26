# unit_test_s3_download.md

## 対象コード
- tests/test_s3_download.py

## 入力条件
- list_csv_files: S3バケット名、プレフィックス、日付文字列（YYYY-MM-DD）を指定
- download_csv: S3バケット名、ファイルキー、ダウンロード先パスを指定

## 実行方法
```bash
pytest tests/test_s3_download.py
```

## 想定結果
- test_list_csv_files: 指定日付のCSVファイル一覧が正しく取得される
  - 例: ['test/2025-06-12_0900.csv', 'test1/2025-06-12_0900.csv']
- test_download_csv: S3から指定ファイルがダウンロードされ、ローカルにファイルが存在する
