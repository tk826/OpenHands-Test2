# test_check_process.py テスト仕様書

## テスト対象
- modules/check_process.py の load_column_types, check_values

## テストケース一覧

### test_load_column_types
- 入力条件: 'a:int\nb:float\nc:datetime\n' 形式の一時ファイル
- 実行方法: load_column_types(ファイルパス)
- 想定結果: {'a': 'int', 'b': 'float', 'c': 'datetime'} を返す
- 想定外: 不正な形式の行があっても例外発生またはエラー等の[または]は何が正しいか記載する

### test_check_values
- 入力条件: カラム型情報 {'a': 'int', 'b': 'float', 'c': 'datetime', 'd': 'str'}
  - DataFrame: a, b, c, d, e（余分なカラム）
- 実行方法: check_values(df, column_types)
- 想定結果:
  - 不正値は空文字に置換
  - 警告リストに 'Invalid int in a at row 1: x' などが含まれる
  - 余分なカラム e は削除される
- 想定外: 型未定義カラムがあっても例外発生しない

### test_grouped_output
- 入力条件: グループ/日付_時分.csv 形式の複数ファイル
- 実行方法: テスト用関数でグループ化・検証・出力
- 想定結果: グループごとに正しいファイル名・内容で出力される
- 想定外: ファイルが空でも例外発生しない

