# OpenHands-Test2

- `.env` ファイルのサンプル:

  ```env
  S3_BUCKET=your-bucket
  S3_PREFIX=your/prefix/
  LOCAL_DIR=/tmp/data
  COLUMNS_FILE=columns.txt
  # 必要に応じて他の変数も追加
  ```

## Dockerによる実行方法
**2025年6月13日更新: Docker実行時の環境変数指定方法を`.env`ファイル方式に変更しました。**


### 1. ビルド

```sh
docker build -t s3-batch-app .
```

### 2. 実行

```sh
docker run --rm -it \
  --env-file .env \
  -e AWS_ACCESS_KEY_ID=your-access-key \
  -e AWS_SECRET_ACCESS_KEY=your-secret-key \
  -v $(pwd):/app \
  s3-batch-app
```

- `.env` ファイルに主要な環境変数（S3_BUCKET, S3_PREFIX, LOCAL_DIR, COLUMNS_FILEなど）を記載し、`--env-file .env` で一括指定できます。
- AWS認証情報（AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY）は `.env` には含めず、`-e` オプションで個別に指定してください。
- 必要に応じて環境変数を設定してください。
- `columns.txt` などのファイルも `/app` にマウントされます。


### Dockerでテストを実行する方法

1. テストを実行します。

    ```sh
    docker run --rm -v $(pwd):/app s3-batch-app pytest
    ```

    ```cmd
    docker run --rm -v "%cd%":/app s3-batch-app pytest
    docker run --rm -v "%cd%":/app s3-batch-app pytest test_check_process.py
    ```
    - 必要に応じて `pytest` の引数を追加できます（例: `pytest test_check_process.py`）。
    - `requirements.txt` などがある場合はDockerfileにインストールコマンドを追加してください。

