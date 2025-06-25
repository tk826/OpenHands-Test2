#!/bin/bash
# box_upload.sh: Upload a file to Box using the Box CLI
# Usage: ./box_upload.sh <local_file_path> <box_folder_id>

set -e

if [ $# -ne 2 ]; then
  echo "Usage: $0 <local_file_path> <box_folder_id>"
  exit 1
fi

LOCAL_FILE="$1"
BOX_FOLDER_ID="$2"

if [ ! -f "$LOCAL_FILE" ]; then
  echo "Error: File $LOCAL_FILE does not exist."
  exit 3
fi

if ! command -v box &> /dev/null; then
  echo "Error: Box CLI (box) is not installed or not in PATH."
  exit 2
fi

# Upload the file to Box
box files upload "$LOCAL_FILE" "$BOX_FOLDER_ID"

if [ $? -eq 0 ]; then
  echo "Upload successful: $LOCAL_FILE to Box folder $BOX_FOLDER_ID"
else
  echo "Upload failed."
  exit 4
fi
