# check_process.py デシジョンテーブル

## 1. load_column_types 関数

| No | 条件                         | 入力値例                | 判定内容・分岐                           | 出力・例外                      |
|----|------------------------------|-------------------------|------------------------------------------|----------------------------------|
| 1  | columns_file is None         | None                    | columns_fileがNoneか                     | ValueError("columns_file is None")|
| 2  | 空ファイル                   | ''                      | ファイルが空か                           | ValueError("columns_file is empty")|
| 3  | フォーマット不正             | 'a:int\nb\nc:datetime' | ':'が含まれない行があるか                | ValueError("invalid format in columns_file")|
| 4  | 正常                         | 'a:int\nb:float'        | すべての行が'カラム:型'形式か             | {'a': 'int', 'b': 'float'}       |


## 2. check_values 関数

| No | カラム型      | 値の内容         | 判定内容・分岐                                   | DataFrame変換後の値 | ワーニング内容例                                 |
|----|--------------|------------------|--------------------------------------------------|--------------------|-----------------------------------------------|
| 1  | datetime     | 正常日付         | '%Y-%m-%d %H:%M:%S'でパース可能                  | そのまま           | なし                                          |
| 2  | datetime     | 不正日付/空/None | パース不可/空/None                               | ''                 | Invalid datetime in {col} at row {i}: {v}     |
| 3  | float        | 数値文字列       | float変換可能                                    | そのまま           | なし                                          |
| 4  | float        | 不正値/空/None   | float変換不可/空/None                            | ''                 | Invalid float in {col} at row {i}: {v}        |
| 5  | int          | 数値文字列       | int(float(v))変換可能                            | そのまま           | なし                                          |
| 6  | int          | 不正値/空/None   | int(float(v))変換不可/空/None                    | ''                 | Invalid int in {col} at row {i}: {v}          |
| 7  | str          | None/空/その他   | None→''、str変換                                 | ''またはstr(v)     | なし                                          |
| 8  | 不要カラム    | -                | column_typesに含まれないカラムは削除              | 削除               | なし                                          |
| 9  | 欠損値       | NaN/None         | fillna('')で空文字に補完                         | ''                 | なし                                          |

- ワーニングはリスト形式で返却される。
- すべてのカラム・行で上記判定を実施。
- 返却値は(クリーニング済みDataFrame, ワーニングリスト)
