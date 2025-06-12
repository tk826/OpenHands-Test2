#!/bin/bash
set -e

# Load environment variables from .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo ".env file not found. Exiting."
    exit 1
fi

# Check required environment variables
REQUIRED_VARS=(SRC_BUCKET SRC_PREFIX DATE DOWNLOAD_DIR COLUMNS_FILE CHECKED_DIR DST_BUCKET DST_KEY)
for VAR in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!VAR}" ]; then
        echo "Environment variable $VAR is not set. Exiting."
        exit 1
    fi
done

# Step 1: S3からCSVファイル一覧取得・ダウンロード
python3 s3_download.py --bucket "$SRC_BUCKET" --prefix "$SRC_PREFIX" --date "$DATE" --download_dir "$DOWNLOAD_DIR"

# Step 2: データ検証・警告出力・データ加工
for csv in "$DOWNLOAD_DIR"/*.csv; do
    python3 check_process.py --input "$csv" --columns "$COLUMNS_FILE" --output "$CHECKED_DIR/$(basename "$csv")"
done

# Step 3: ZIP圧縮・S3アップロード
ZIP_FILE="checked_csvs.zip"
python3 s3_upload.py --zip_dir "$CHECKED_DIR" --zip_file "$ZIP_FILE"
python3 s3_upload.py --upload_file "$ZIP_FILE" --bucket "$DST_BUCKET" --key "$DST_KEY"

echo "バッチ処理が正常に完了しました。"
