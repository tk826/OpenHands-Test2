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
| 2  | 異常系   | 'a:int\nb\nc:datetime\n' | 例外発生 | フォーマット不正 |
| 3  | 境界値   | '' | 空dict返却 or 例外 | 空ファイル |
| 4  | 想定外   | None | 例外発生 | None入力 |

### check_values
| No | 正常/異常 | 入力DataFrame | column_types | 期待結果 | 備考 |
|----|----------|--------------|--------------|----------|------|
| 1  | 正常系   | a: ['1', '2'], b: ['1.1', '2.2'], c: ['2020-01-01 12:00:00', '2020-01-02 00:00:00'], d: ['x', 'y'] | {'a': 'int', 'b': 'float', 'c': 'datetime', 'd': 'str'} | 変換・警告なし | 標準ケース |
| 2  | 正常系   | a: ['1', '3'], b: ['1.1', '3.3'], c: ['2020-01-01 12:00:00', '2020-01-02 00:00:00'], d: ['x', 'y'], e: [1,2] | {'a': 'int', 'b': 'float', 'c': 'datetime', 'd': 'str'} | e列削除 | 余分なカラム |
| 3  | 異常系   | a: ['1', 'x'], b: ['1.1', 'bad'], c: ['2020-01-01 12:00:00', '2020-13-01 00:00:00'], d: [None, 'abc'] | {'a': 'int', 'b': 'float', 'c': 'datetime', 'd': 'str'} | 警告3件, 不正値空文字 | 型不正値 |
| 4  | 境界値   | a: ['', None], b: ['', None], c: ['', None], d: ['', None] | {'a': 'int', 'b': 'float', 'c': 'datetime', 'd': 'str'} | 全て空文字, 警告なし | 欠損値 |
| 5  | 境界値   | a: ['0', '-1'], b: ['0.0', '-1.1'], c: ['1999-12-31 23:59:59', '2100-01-01 00:00:00'], d: ['',''] | {'a': 'int', 'b': 'float', 'c': 'datetime', 'd': 'str'} | 変換・警告なし | 境界値 |
| 6  | 複数件   | a: ['1', '2'], b: ['1.1', '2.2'], c: ['2020-01-01 12:00:00', '2020-01-02 00:00:00'], d: ['x', 'y'] | {'a': 'int', 'b': 'float', 'c': 'datetime', 'd': 'str'} | 2件返却 | 複数件 |
| 7  | 想定外   | a: ['a', 'b'], b: ['b', 'c'], c: ['c', 'd'], d: [None, None] | {'a': 'int', 'b': 'float', 'c': 'datetime', 'd': 'str'} | 全て警告・空文字 | 全不正値 |
| 8  | 想定外   | 空DataFrame | {'a': 'int'} | 空DataFrame返却 | カラムなし |
| 9  | 想定外   | a: [1,2] | {} | a列削除 | column_types空 |

## 6. 想定結果の詳細
- 正常系は返却値・警告リスト・DataFrame内容が正しいことを確認
- 異常系・想定外入力は例外発生や空文字・空DataFrame返却など、あいまいな動作がないことを確認
- すべての分岐・条件・境界値を網羅

## 7. カバレッジ計測方法
```sh
pytest --cov=modules.check_process tests/test_check_process.py
```
