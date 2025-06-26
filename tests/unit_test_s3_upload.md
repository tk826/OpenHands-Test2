# unit_test_s3_upload.md

## 対象コード
- tests/test_s3_upload.py

## 入力条件
- zip_csv_files: ディレクトリパス、zipファイル出力先パスを指定
- upload_csv: S3バケット名、ファイルパス、アップロード先キーを指定

## 実行方法
```bash
pytest tests/test_s3_upload.py
```

## 想定結果
- test_zip_csv_files: 指定ディレクトリ内のCSVファイルがzip化され、zipファイルが生成される
- test_upload_csv: S3にファイルがアップロードされる（mockで確認）
