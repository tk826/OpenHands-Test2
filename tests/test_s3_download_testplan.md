# test_s3_download.py テスト仕様書

## テスト対象
- modules/s3_download.py の list_csv_files, download_csv

## テストケース一覧

### test_list_csv_files
- 入力条件: S3バケットに複数のCSVファイルとその他ファイルが存在
- 実行方法: list_csv_files('bucket', '', '2025-06-12')
- 想定結果: 指定日付・形式のCSVファイルのみリストアップされる
- 想定外: Contentsが空でも例外発生しない

### test_download_csv
- 入力条件: S3バケットにCSVファイルが存在
- 実行方法: download_csv(bucket, key, tmpdir, prefix)
- 想定結果: 指定ディレクトリ・サブディレクトリにファイルがダウンロードされる
- 想定外: ディレクトリが存在しなくても自動作成される

