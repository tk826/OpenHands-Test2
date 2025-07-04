# check_process.py デシジョンテーブル

## 1. load_column_types 関数

| No | 条件                         | 入力値                | 判定内容・分岐                           | 出力・例外                      |
|----|------------------------------|-------------------------|------------------------------------------|----------------------------------|
| 1  | columns_file is None         | None                    | columns_fileがNone                       | ValueError("columns_file is None")|
| 2  | 空ファイル                   | （空ファイル）           | ファイルが空                             | ValueError("columns_file is empty")|
| 3  | フォーマット不正             | a:int\nb\nc:datetime   | ':'が含まれない行がある                  | ValueError("invalid format in columns_file")|
| 4  | 正常                         | a:int\nb:float          | すべての行が'カラム:型'形式               | {'a': 'int', 'b': 'float'}       |


## 2. check_values 関数

| No | カラム型      | 値の内容         | 判定内容・分岐                                   | DataFrame変換後の値 | ワーニング内容                                 |
|----|--------------|------------------|--------------------------------------------------|--------------------|-----------------------------------------------|
| 1  | datetime     | 2024-01-01 12:00:00 | '%Y-%m-%d %H:%M:%S'でパース可能                  | そのまま           | なし                                          |
| 2  | datetime     | 2024-13-01 12:00:00 | パース不可                                        | ''                 | Invalid datetime in {col} at row {i}: 2024-13-01 12:00:00 |
| 3  | datetime     | ''               | 空文字                                            | ''                 | Invalid datetime in {col} at row {i}: '' |
| 4  | datetime     | None             | None                                              | ''                 | Invalid datetime in {col} at row {i}: None    |
| 5  | float        | 1.23             | float変換可能                                    | 1.23           | なし                                          |
| 6  | float        | abc              | float変換不可                                    | ''                 | Invalid float in {col} at row {i}: abc        |
| 7  | float        | ''               | 空文字                                            | ''                 | Invalid float in {col} at row {i}: '' |
| 8  | float        | None             | None                                              | ''                 | Invalid float in {col} at row {i}: None       |
| 9  | int          | 123              | int(float(v))変換可能                            | 123           | なし                                          |
|10  | int          | abc              | int(float(v))変換不可                            | ''                 | Invalid int in {col} at row {i}: abc          |
|11  | int          | ''               | 空文字                                            | ''                 | Invalid int in {col} at row {i}: '' |
|12  | int          | None             | None                                              | ''                 | Invalid int in {col} at row {i}: None         |
|13  | str          | None             | None→''、str変換                                 | ''                 | なし                                          |
|14  | str          | ''               | 空文字                                            | ''                 | なし                                          |
|15  | str          | test             | str変換                                           | test             | なし                                          |
|16  | 不要カラム    | -                | column_typesに含まれないカラムは削除              | 削除               | なし                                          |
|17  | 欠損値       | NaN              | fillna('')で空文字に補完                         | ''                 | なし                                          |
|18  | 欠損値       | None             | fillna('')で空文字に補完                         | ''                 | なし                                          |

- ワーニングはリスト形式で返却される。
- すべてのカラム・行で上記判定を実施。
- 返却値は(クリーニング済みDataFrame, ワーニングリスト)
