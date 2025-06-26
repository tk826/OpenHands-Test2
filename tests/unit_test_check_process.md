# unit_test_check_process.md

## 対象コード
- tests/test_check_process.py

## 入力条件
- load_column_types: カラム名:型 の形式で1行ずつ記載されたテキストファイルのパスを指定
- check_values: カラム名と型情報のdict、pandas.DataFrame（各カラムに値が入ったもの）を指定

## 実行方法
```bash
pytest tests/test_check_process.py
```

## 想定結果
- test_load_column_types: ファイルから正しく型情報がdictで読み込まれる
  - 例: {'a': 'int', 'b': 'float', 'c': 'datetime'}
- test_check_values: 型変換できない値や不正な値が検出される
  - 例: 'x'はint型に変換できない、'bad'はfloat型に変換できない、'2020-13-01 00:00:00'はdatetime型として不正
