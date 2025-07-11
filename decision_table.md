# デシジョンテーブル: script.py の処理フロー

このデシジョンテーブルは、script.py の主要な分岐・動作条件を整理したものです。

| 条件 | 規則1 | 規則2 | 規則3 | 規則4 | 規則5 | 規則6 | 規則7 | 規則8 | 規則9 | 規則10 | 規則11 |
|:--------------------------|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|
| S3バケット指定 | Y | Y | Y | Y | N | N | N | N | Y | Y | Y |
| S3入力プレフィックス指定 | Y | Y | N | N | Y | Y | N | N | Y | N | N |
| S3出力プレフィックス指定 | Y | N | Y | N | Y | N | Y | N | Y | N | N |
| 対象日付指定 | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| CSVファイル取得成功 | Y | Y | Y | Y | Y | Y | N | N | Y | Y | Y |
| データ検証で警告 | N | Y | N | Y | N | Y | - | - | N | N | N |
| データ検証でエラー | N | N | Y | Y | N | N | - | - | N | N | N |
| BOXアップロード成功 | Y | Y | - | - | Y | Y | - | - | Y | N | N |
| S3アップロード成功 | Y | Y | - | - | Y | Y | - | - | N | Y | N |
| 動作: 正常処理 | X | - | - | - | X | - | - | - | - | - | - |
| 動作: ワーニング出力 | - | W | - | W | - | W | - | - | - | W | - |
| 動作: エラー終了 | - | - | E | E | - | - | E | E | E | - | E |

- 「Y」は条件が真、「N」は偽、「-」はその動作のスキップで「X」はその動作が実行されること、「W」はワーニング出力、「E」はエラー終了を示します。
- 条件が複数該当する場合、最も重大な動作（E > W > X）が優先されます。
- 主要な分岐・異常系も網羅しています。

## 補足
- S3/BOXアップロードやデータ検証での異常時は print による警告・エラー出力あり。
- 例外発生時は except でエラー終了（E）となります。
