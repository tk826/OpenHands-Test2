# s3_download.py 単体テスト仕様書

## 1. 対象モジュール
- modules/s3_download.py

## 2. テスト対象関数
- list_csv_files(bucket, prefix, date_str)
- download_csv(bucket, key, local_s3_dir, prefix=None)

## 3. テスト環境・前提条件
- boto3, pytest, unittest.mock, tempfile など必要なパッケージがインストール済みであること
- S3アクセスはモックを利用し、実際のAWSリソースは使用しない
- ローカルディレクトリは一時ディレクトリを利用

## 4. テスト実行方法
```sh
pytest tests/test_s3_download.py
```

## 5. テストケース一覧

### list_csv_files
| No | 正常/異常 | 入力(bucket, prefix, date_str) | S3オブジェクト一覧 | 期待結果 | 備考 |
|----|----------|-------------------------------|--------------------|----------|------|
| 1  | 正常系   | 'bucket', '', '2025-06-12'    | ['test/2025-06-12_0900.csv', 'test/2025-06-11_0900.csv', 'test/other.txt'] | ['test/2025-06-12_0900.csv'] | 日付一致CSVのみ抽出 |
| 2  | 正常系   | 'bucket', '', '2025-06-12'    | ['test/2025-06-12_0900.csv', 'test/2025-06-11_0900.csv', 'test1/2025-06-12_1210.csv', 'test/other.txt'] | ['test/2025-06-12_0900.csv', 'test1/2025-06-12_1210.csv'] | 日付一致CSVのみ抽出 |
| 3  | 正常系   | 'bucket', '', '2025-06-12'    | ['test/2025-06-12_0900.csv', 'test/2025-06-12_0915.csv', 'test/2025-06-12_2359.csv', 'test/2025-06-11_0900.csv', 'test1/2025-06-12_1210.csv', 'test/other.txt'] | ['test/2025-06-12_0900.csv', 'test/2025-06-12_0915.csv', 'test/2025-06-12_2359.csv', 'test1/2025-06-12_1210.csv'] | 日付一致CSVのみ抽出 |
| 4  | 正常系   | 'bucket', '', '2025-06-13'    | ['test/2025-06-12_0900.csv', 'test/2025-06-11_0900.csv'] | [] | 一致なし |
| 5  | 異常系   | 'bucket', '', '2025-06-12'    | [] | [] | S3にファイルなし |
| 6  | 異常系   | 'bucket', '', '2025-06-12'    | ['test/2025-06-12_0900.txt'] | [] | 拡張子不一致 |
| 7  | 境界値   | 'bucket', '', ''              | ['test/2025-06-12_0900.csv'] | [] | date_str空文字 |
| 8  | 境界値   | 'bucket', '', '2025-06-12'    | ['test/2025-06-12_0900.csv', 'test/2025-06-12_0900.csv'] | ['test/2025-06-12_0900.csv', 'test/2025-06-12_0900.csv'] | 同一ファイル複数 |
| 9  | 想定外   | 'bucket', '', '2025-06-12'    | [{'Key': None}] | [], warnings: [] | KeyがNone |

### download_csv
| No | 正常/異常 | 入力(bucket, key, local_s3_dir, prefix) | 事前状態 | 期待結果 | 備考 |
|----|----------|-----------------------------------------|----------|----------|------|
| 1  | 正常系   | 'bucket', 'test/2025-06-12_0900.csv', tmpdir, 'test/' | tmpdir存在 | '/tmp/tmpdir/test/2025-06-12_0900.csv' |  |
| 2  | 正常系   | 'bucket', 'test/2025-06-12_0900.csv', tmpdir, None | tmpdir存在 | '/tmp/tmpdir/2025-06-12_0900.csv' | prefix省略 |
| 3  | 正常系   | 'bucket', 'test/2025-06-12_0900.csv', tmpdir, 'test/' | tmpdir未作成 | '/tmp/tmpdir/test/2025-06-12_0900.csv' | ディレクトリ自動作成 |
| 4  | 正常系   | 'bucket', 'test/2025-06-12_0900.csv', tmpdir, 'test/' | keyがサブディレクトリ含む | '/tmp/tmpdir/test/2025-06-12_0900.csv' | 階層保存 |
| 5  | 想定外   | 'bucket', '', tmpdir, 'test/' | key空文字 | 例外発生(ValueError: key is empty) | 想定外入力 |
| 6  | 想定外   | 'bucket', None, tmpdir, 'test/' | key=None | 例外発生(ValueError: key is None) | 想定外入力 |
| 7  | 想定外   | '', 'test/2025-06-12_0900.csv', tmpdir, 'test/' | bucket空文字 | 例外発生(ValueError: bucket is empty) | 想定外入力 |
| 8  | 想定外   | None, 'test/2025-06-12_0900.csv', tmpdir, 'test/' | bucket=None | 例外発生(ValueError: bucket is None) | 想定外入力 |
| 9  | 想定外   | 'bucket', 'test/2025-06-12_0900.csv', '', 'test/' | local_s3_dir空文字 | 例外発生(ValueError: local_s3_dir is empty) | 想定外入力 |
| 10 | 想定外   | 'bucket', 'test/2025-06-12_0900.csv', None, 'test/' | local_s3_dir=None | 例外発生(ValueError: local_s3_dir is None) | 想定外入力 |

## 6. 想定結果の詳細
- 正常系は返却値・ファイルパス・ディレクトリ構造が正しいことを確認
- 異常系・想定外入力は例外発生や空リスト返却など、あいまいな動作がないことを確認
- すべての分岐・条件・境界値を網羅

## 7. カバレッジ計測方法
```sh
pytest --cov=modules.s3_download tests/test_s3_download.py
```
