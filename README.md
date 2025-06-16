# OpenHands-Test2

## Dockerによる実行方法

### 1. ビルド

```sh
docker build -t s3-batch-app .
```

### 2. 実行

```sh
docker run --rm -it -e S3_BUCKET=your-bucket -e S3_PREFIX_IN=test_data -e S3_PREFIX_OUT=zip -e LOCAL_S3_DIR=/tmp/s3_data -e LOCAL_CHECK_DIR=/tmp/data -e COLUMNS_FILE=columns.txt -e TARGET_YMD=2025-06-13   -v "%cd%":/app   -v "%cd%"/tmp/s3_data:/tmp/s3_data   -v "%cd%"/tmp/data:/tmp/data s3-batch-app

```

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

