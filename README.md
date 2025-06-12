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
