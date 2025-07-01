# check_process.py 単体テスト仕様書

## 1. 対象モジュール
- modules/check_process.py

## 2. テスト対象関数
- load_column_types(columns_file)
- check_values(df, column_types)

## 3. テスト環境・前提条件
- pandas, numpy, pytest, tempfile など必要なパッケージがインストール済みであること
- ファイル入出力は一時ファイル・ディレクトリを利用
- DataFrameはpandasで作成

## 4. テスト実行方法
```sh
pytest tests/test_check_process.py
```

## 5. テストケース一覧

### load_column_types
| No | 正常/異常 | 入力(columns_file内容) | 期待結果 | 備考 |
|----|----------|----------------------|----------|------|
| 1  | 正常系   | 'a:int\nb:float\nc:datetime\n' | {'a': 'int', 'b': 'float', 'c': 'datetime'} | 標準ケース |
| 2  | 異常系   | 'a:int\nb\nc:datetime\n' | 例外発生(ValueError: invalid format in columns_file) | フォーマット不正 |
| 3  | 境界値   | '' | 例外発生(ValueError: columns_file is empty) | 空ファイル |
| 4  | 想定外   | None | 例外発生(ValueError: columns_file is None) | None入力 |

### check_values
| No | 正常/異常 | 入力DataFrame | column_types | 期待結果 | 備考 |
|----|----------|--------------|--------------|----------|------|
| 1  | 正常系   | a: ['1'], b: ['1.1'], c: ['2020-01-01 12:00:00'], d: ['x'] | {'a': 'int', 'b': 'float', 'c': 'datetime', 'd': 'str'} | 結果値: [{'a': 1, 'b': 1.1, 'c': '2020-01-01 12:00:00', 'd': 'x'}]<br> ワーニング: [] | 標準ケース(1件) |
| 2  | 正常系   | a: ['1', '2'], b: ['1.1', '2.2'], c: ['2020-01-01 12:00:00', '2020-01-02 00:00:00'], d: ['x', 'y'] | {'a': 'int', 'b': 'float', 'c': 'datetime', 'd': 'str'} | 結果値: [{'a': 1, 'b': 1.1, 'c': '2020-01-01 12:00:00', 'd': 'x'}, {'a': 2, 'b': 2.2, 'c': '2020-01-02 00:00:00', 'd': 'y'}]<br> ワーニング: [] | 標準ケース(複数件) |
| 3  | 正常系   | a: ['1', '3'], b: ['1.1', '3.3'], c: ['2020-01-01 12:00:00', '2020-01-02 00:00:00'], d: ['x', 'y'], e: [1,2] | {'a': 'int', 'b': 'float', 'c': 'datetime', 'd': 'str'} | 結果値: [{'a': 1, 'b': 1.1, 'c': '2020-01-01 12:00:00', 'd': 'x'}, {'a': 3, 'b': 3.3, 'c': '2020-01-02 00:00:00', 'd': 'y'}]<br> ワーニング: [] | 余分なカラム |
| 4  | 異常系   | a: ['1', 'x'], b: ['1.1', 'bad'], c: ['2020-01-01 12:00:00', '2020-13-01 00:00:00'], d: [None, 'abc'] | {'a': 'int', 'b': 'float', 'c': 'datetime', 'd': 'str'} | 結果値: [{'a': 1, 'b': 1.1, 'c': '2020-01-01 12:00:00', 'd': ''}, {'a': '', 'b': '', 'c': '', 'd': 'abc'}]<br> ワーニング: [{'col': 'a', 'row': 1, 'value': 'x', 'error': 'invalid int'}, {'col': 'b', 'row': 1, 'value': 'bad', 'error': 'invalid float'}, {'col': 'c', 'row': 1, 'value': '2020-13-01 00:00:00', 'error': 'invalid datetime'}] | 型不正値 |
| 5  | 境界値   | a: ['', None], b: ['', None], c: ['', None], d: ['', None] | {'a': 'int', 'b': 'float', 'c': 'datetime', 'd': 'str'} | 結果値: [{'a': '', 'b': '', 'c': '', 'd': ''}, {'a': '', 'b': '', 'c': '', 'd': ''}]<br> ワーニング: [] | 欠損値 |
| 6  | 境界値   | a: ['0', '-1'], b: ['0.0', '-1.1'], c: ['1999-12-31 23:59:59', '2100-01-01 00:00:00'], d: ['',''] | {'a': 'int', 'b': 'float', 'c': 'datetime', 'd': 'str'} | 結果値: [{'a': 0, 'b': 0.0, 'c': '1999-12-31 23:59:59', 'd': ''}, {'a': -1, 'b': -1.1, 'c': '2100-01-01 00:00:00', 'd': ''}]<br> ワーニング: [] | 境界値 |
| 7  | 複数件   | a: ['1', '2'], b: ['1.1', '2.2'], c: ['2020-01-01 12:00:00', '2020-01-02 00:00:00'], d: ['x', 'y'] | {'a': 'int', 'b': 'float', 'c': 'datetime', 'd': 'str'} | 結果値: [{'a': 1, 'b': 1.1, 'c': '2020-01-01 12:00:00', 'd': 'x'}, {'a': 2, 'b': 2.2, 'c': '2020-01-02 00:00:00', 'd': 'y'}] | 複数件 |
| 8  | 想定外   | a: ['a', 'b'], b: ['b', 'c'], c: ['c', 'd'], d: [None, None] | {'a': 'int', 'b': 'float', 'c': 'datetime', 'd': 'str'} | 結果値: [{'a': '', 'b': '', 'c': '', 'd': ''}, {'a': '', 'b': '', 'c': '', 'd': ''}]<br> ワーニング: [{'col': 'a', 'row': 0, 'value': 'a', 'error': 'invalid int'}, {'col': 'a', 'row': 1, 'value': 'b', 'error': 'invalid int'}, {'col': 'b', 'row': 0, 'value': 'b', 'error': 'invalid float'}, {'col': 'b', 'row': 1, 'value': 'c', 'error': 'invalid float'}, {'col': 'c', 'row': 0, 'value': 'c', 'error': 'invalid datetime'}, {'col': 'c', 'row': 1, 'value': 'd', 'error': 'invalid datetime'}] | 全不正値 |
| 9  | 想定外   | 空DataFrame | {'a': 'int'} | 結果値: []<br> ワーニング: [] | カラムなし |
| 10  | 想定外   | a: [1,2] | {} | 結果値: []<br> ワーニング: [] | column_types空 |

## 6. 想定結果の詳細
- 正常系は返却値・警告リスト・DataFrame内容が正しいことを確認
- 異常系・想定外入力は例外発生や空文字・空DataFrame返却など、あいまいな動作がないことを確認
- すべての分岐・条件・境界値を網羅

## 7. カバレッジ計測方法
```sh
pytest --cov=modules.check_process tests/test_check_process.py
```
