# test_s3_upload.py テスト仕様書

## テスト対象
- modules/s3_upload.py の zip_csv_files, upload_csv

## テストケース一覧

### test_zip_csv_files
- 入力条件: ディレクトリ内に複数のCSVファイルが存在
- 実行方法: zip_csv_files(tmpdir, zip_path)
- 想定結果: 指定パスにZIPファイルが作成される
- 想定外: CSVが1つでも例外発生しない

### test_upload_csv
- 入力条件: S3バケット・キー・ローカルファイルパスが指定されている
- 実行方法: upload_csv('bucket', 'key', '/tmp/file.zip')
- 想定結果: boto3のupload_fileが1回呼ばれる
- 想定外: ファイルが存在しない場合は例外発生

