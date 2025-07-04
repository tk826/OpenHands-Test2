# box_upload.py 単体テスト仕様書

## 1. 対象モジュール
- modules/box_upload.py

## 2. テスト対象関数
- upload_to_box(file_path, folder_id=None)

## 3. テスト環境・前提条件
- boxsdk, pytest, unittest.mock, tempfile, os など必要なパッケージがインストール済みであること
- BOXアクセスはモックを利用し、実際のBOXリソースは使用しない
- 環境変数BOX_CONFIG_PATH, BOX_FOLDER_ID, BOXSDK_TEST_MOCKを適切に設定
- ローカルファイルは一時ファイルを利用

## 4. テスト実行方法
```sh
pytest tests/test_box_upload.py
```

## 5. テストケース一覧

### upload_to_box
| No | 正常/異常 | 入力(file_path, folder_id, 環境変数) | 期待結果 | 備考 |
|----|----------|--------------------------------------|----------|------|
| 1  | 正常系   | '/tmp/file1.csv', '12345', BOXSDK_TEST_MOCK=1 | 'mocked_id' 返却 | モック動作 |
| 2  | 正常系   | '/tmp/file2.csv', None, BOXSDK_TEST_MOCK=1, BOX_FOLDER_ID='99999' | 'mocked_id' 返却 | folder_id省略・環境変数利用 |
| 3  | 境界値   | '/tmp/empty.csv', '12345', BOXSDK_TEST_MOCK=1 | 'mocked_id' 返却 | 空ファイル |
| 4  | 境界値   | '/tmp/large.csv', '12345', BOXSDK_TEST_MOCK=1 | 'mocked_id' 返却 | 大容量ファイル |
| 5  | 異常系   | '', '12345', BOXSDK_TEST_MOCK=1 | 例外発生(ValueError) | file_path空文字 |
| 6  | 異常系   | None, '12345', BOXSDK_TEST_MOCK=1 | 例外発生(TypeError) | file_path None |
| 7  | 異常系   | '/tmp/file3.csv', '', BOXSDK_TEST_MOCK=1 | 'mocked_id' 返却 | folder_id空文字(BOX_FOLDER_ID既定値) |
| 8  | 異常系   | '/tmp/file3.csv', None, BOXSDK_TEST_MOCK=0, BOX_CONFIG_PATH未設定 | 例外発生(ValueError) | BOX_CONFIG_PATH未設定 |
| 9  | 異常系   | '/tmp/file3.csv', None, BOXSDK_TEST_MOCK=0, BOX_CONFIG_PATH='/tmp/notfound.json' | 例外発生(ValueError) | BOX_CONFIG_PATHファイル不存在 |
| 10 | 異常系   | '/tmp/notfound.csv', '12345', BOXSDK_TEST_MOCK=1 | 例外発生(FileNotFoundError) | ファイル不存在 |

## 6. 想定結果の詳細
- 正常系は返却値・BOXアップロード呼び出しが正しいことを確認
- 異常系・想定外入力は例外発生や既定値利用など、あいまいな動作がないことを確認
- すべての分岐・条件・境界値を網羅

## 7. カバレッジ計測方法
```sh
pytest --cov=modules.box_upload tests/test_box_upload.py
```
