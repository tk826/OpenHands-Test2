# OpenHands-Test2

## Dockerによる実行方法

### 1. ビルド

```sh
docker build -t s3-batch-app .
```

### 2. 実行

```sh
docker run --rm -it \
  -e AWS_ACCESS_KEY_ID=your-access-key \
  -e AWS_SECRET_ACCESS_KEY=your-secret-key \
  -e S3_BUCKET=your-bucket \
  -e S3_PREFIX=your/prefix/ \
  -e LOCAL_DIR=/tmp/data \
  -e COLUMNS_FILE=columns.txt \
  -v $(pwd):/app \
  s3-batch-app
```

- 必要に応じて環境変数を設定してください。
- `columns.txt` などのファイルも `/app` にマウントされます。


### Dockerでテストを実行する方法

1. Dockerイメージをビルドします。

    ```sh
    docker build -t s3-batch-app .
    ```

2. テストを実行します。

    ```sh
    docker run --rm -v $(pwd):/app s3-batch-app pytest
    ```

    - 必要に応じて `pytest` の引数を追加できます（例: `pytest tests/test_check_process.py`）。
    - `requirements.txt` などがある場合はDockerfileにインストールコマンドを追加してください。

## テストの実行方法

このリポジトリにはユニットテストが `tests/` ディレクトリに含まれています。

### 1. 必要なパッケージのインストール

`pytest` と必要な依存パッケージをインストールしてください。

```
pip install pytest pandas boto3
```

### 2. テストの実行

以下のコマンドで全テストを実行できます。

```
pytest
```

または個別のテストファイルを指定して実行することもできます。

```
pytest tests/test_check_process.py
```

