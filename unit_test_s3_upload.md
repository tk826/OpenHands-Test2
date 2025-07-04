# s3_upload.py 単体テスト仕様書

## 1. 対象モジュール
- modules/s3_upload.py

## 2. テスト対象関数
- zip_csv_files(csv_dir, zip_path)
- upload_csv(bucket, key, file_path)

## 3. テスト環境・前提条件
- boto3, pytest, unittest.mock, tempfile, zipfile, os など必要なパッケージがインストール済みであること
- S3アクセスはモックを利用し、実際のAWSリソースは使用しない
- ローカルディレクトリ・ファイルは一時ディレクトリ・ファイルを利用

## 4. テスト実行方法
```sh
pytest tests/test_s3_upload.py
```

## 5. テストケース一覧

### zip_csv_files
| No | 正常/異常 | 入力(csv_dir, zip_path, ディレクトリ内容) | 期待結果 | 備考 |
|----|----------|------------------------------------------|----------|------|
| 1  | 正常系   | '/tmp/dir1', '/tmp/out1.zip', ['a.csv', 'b.csv'] | '/tmp/out1.zip' 作成、zip内: ['a.csv', 'b.csv'] | 標準ケース |
| 2  | 正常系   | '/tmp/dir2', '/tmp/out2.zip', ['a.csv', 'b.csv', 'c.txt'] | '/tmp/out2.zip' 作成、zip内: ['a.csv', 'b.csv'] | 非CSV除外 |
| 3  | 正常系   | '/tmp/dir3', '/tmp/out3.zip', [] | '/tmp/out3.zip' 作成、zip内: [] | 空ディレクトリ |
| 4  | 境界値   | '/tmp/dir4', '/tmp/out4.zip', ['a.csv'] | '/tmp/out4.zip' 作成、zip内: ['a.csv'] | 1件のみ |
| 5  | 境界値   | '/tmp/dir5', '/tmp/out5.zip', ['a.csv', 'b.csv', 'c.csv'] | '/tmp/out5.zip' 作成、zip内: ['a.csv', 'b.csv', 'c.csv'] | 複数件 |
| 6  | 異常系   | '/tmp/dir6', '/tmp/out6.zip', ディレクトリなし | 例外発生(FileNotFoundError) | ディレクトリ不存在 |
| 7  | 異常系   | '', '/tmp/out7.zip', [] | 例外発生(ValueError) | csv_dir空文字 |
| 8  | 異常系   | None, '/tmp/out8.zip', [] | 例外発生(TypeError) | csv_dir None |
| 9  | 異常系   | '/tmp/dir9', '', ['a.csv'] | 例外発生(ValueError) | zip_path空文字 |
| 10 | 異常系   | '/tmp/dir10', None, ['a.csv'] | 例外発生(TypeError) | zip_path None |

### upload_csv
| No | 正常/異常 | 入力(bucket, key, file_path) | 期待結果 | 備考 |
|----|----------|-----------------------------|----------|------|
| 1  | 正常系   | 'bucket', 'test/file.csv', '/tmp/file.csv' | S3アップロード正常終了 | 標準ケース |
| 2  | 境界値   | 'bucket', 'test/file.csv', '/tmp/empty.csv' | S3アップロード正常終了 | 空ファイル |
| 3  | 境界値   | 'bucket', 'test/file.csv', '/tmp/large.csv' | S3アップロード正常終了 | 大容量ファイル |
| 4  | 異常系   | '', 'test/file.csv', '/tmp/file.csv' | 例外発生(ValueError) | bucket空文字 |
| 5  | 異常系   | None, 'test/file.csv', '/tmp/file.csv' | 例外発生(TypeError) | bucket None |
| 6  | 異常系   | 'bucket', '', '/tmp/file.csv' | 例外発生(ValueError) | key空文字 |
| 7  | 異常系   | 'bucket', None, '/tmp/file.csv' | 例外発生(TypeError) | key None |
| 8  | 異常系   | 'bucket', 'test/file.csv', '' | 例外発生(ValueError) | file_path空文字 |
| 9  | 異常系   | 'bucket', 'test/file.csv', None | 例外発生(TypeError) | file_path None |
| 10 | 異常系   | 'bucket', 'test/file.csv', '/tmp/notfound.csv' | 例外発生(FileNotFoundError) | ファイル不存在 |

## 6. 想定結果の詳細
- 正常系は返却値・ファイル内容・S3アップロード呼び出しが正しいことを確認
- 異常系・想定外入力は例外発生や空zip作成など、あいまいな動作がないことを確認
- すべての分岐・条件・境界値を網羅

## 7. カバレッジ計測方法
```sh
pytest --cov=modules.s3_upload tests/test_s3_upload.py
```
