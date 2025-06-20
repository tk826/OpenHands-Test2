#!/bin/bash
set -e

# Test folders:upload mock
export MOCK_BOX_RTESULT=0
output=$("$(dirname "$0")/../bin/box" folders:upload folder_id file.txt)
status=$?
if [[ "$output" != *"[MOCK] box folders:upload folder_id file.txt"* ]]; then
  echo "FAIL: Expected mock output for folders:upload" >&2
  exit 1
fi
if [[ $status -ne 0 ]]; then
  echo "FAIL: Expected exit code 0 for folders:upload, got $status" >&2
  exit 1
fi

echo "PASS: folders:upload mock"

# Test passthrough error
set +e
output=$("$(dirname "$0")/../bin/box" folders:list folder_id 2>&1)
status=$?
set -e
if [[ "$output" != *"box CLI not found for passthrough"* ]]; then
  echo "FAIL: Expected passthrough error output" >&2
  exit 1
fi
if [[ $status -ne 127 ]]; then
  echo "FAIL: Expected exit code 127 for passthrough error, got $status" >&2
  exit 1
fi

echo "PASS: passthrough error"
