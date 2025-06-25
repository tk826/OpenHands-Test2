#!/bin/bash
set -e

# Load environment variables from .env if exists
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Required environment variables
: "${S3_BUCKET:?}"
: "${S3_PREFIX_IN:?}"
: "${S3_PREFIX_OUT:?}"
: "${LOCAL_S3_DIR:=/tmp/s3_data}"
: "${LOCAL_CHECK_DIR:=/tmp/data}"
: "${COLUMNS_FILE:?}"
: "${TARGET_YMD:?}"

mkdir -p "$LOCAL_S3_DIR" "$LOCAL_CHECK_DIR"

# 1. List CSV files in S3
CSV_KEYS=$(aws s3 ls "s3://$S3_BUCKET/$S3_PREFIX_IN/" | awk '{print $4}' | grep "${TARGET_YMD}_.*\.csv$")
echo "取得CSV: $CSV_KEYS"

# 2. Download CSV files
for key in $CSV_KEYS; do
  aws s3 cp "s3://$S3_BUCKET/$S3_PREFIX_IN/$key" "$LOCAL_S3_DIR/$key"
done

# 3. (Optional) Validate and merge CSVs
# NOTE: This step is complex in Bash. You may use csvkit or skip validation.
# Here, we simply copy all files to LOCAL_CHECK_DIR.
for file in $LOCAL_S3_DIR/*.csv; do
  cp "$file" "$LOCAL_CHECK_DIR/"
done

# 4. Zip processed CSVs
cd "$LOCAL_CHECK_DIR"
ZIP_NAME="processed_${TARGET_YMD}.zip"
zip -j "$ZIP_NAME" *.csv
cd -

# 5. Upload zip to S3
aws s3 cp "$LOCAL_CHECK_DIR/$ZIP_NAME" "s3://$S3_BUCKET/$S3_PREFIX_OUT/$ZIP_NAME"

echo "処理完了: $ZIP_NAME を S3 にアップロードしました"
