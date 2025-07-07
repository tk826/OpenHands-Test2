# デシジョンテーブル作成方法

このドキュメントでは、`modules/check_process.py` のデシジョンテーブルを作成します。

## デシジョンテーブルとは
ある処理や関数の入力条件と出力・動作を表形式で整理したものです。条件ごとにどのような結果になるかを明確にします。

---

## check_process.py の主な関数
- `load_column_types(columns_file)`
- `check_values(df, column_types)`

---

## デシジョンテーブル: load_column_types
| 条件 (columns_file)         | 結果・動作                                      |
|----------------------------|------------------------------------------------|
| None                       | ValueError("columns_file is None") を発生させる |
| 空ファイル                 | ValueError("columns_file is empty") を発生させる|
| フォーマット不正な行あり    | ValueError("invalid format in columns_file") を発生させる|
| 正常なファイル              | カラム名と型の辞書を返す                        |

---

## デシジョンテーブル: check_values
| 条件 (df, column_types)         | 結果・動作                                      |
|---------------------------------|------------------------------------------------|
| dfにcolumn_typesのカラムがない   | そのカラムのチェック・クリーニングをスキップ     |
| datetime型で不正な値            | 警告リストに追加し、その値を空文字にする         |
| float型で不正な値               | 警告リストに追加し、その値を空文字にする         |
| int型で不正な値                 | 警告リストに追加し、その値を空文字にする         |
| str型でNoneやNaN                | 空文字に変換                                    |
| column_typesにないカラム         | DataFrameから削除                               |
| 欠損値（NaNなど）               | 空文字に変換                                    |

---

## 備考
- デシジョンテーブルは仕様変更時の影響範囲確認やテストケース作成にも活用できます。
