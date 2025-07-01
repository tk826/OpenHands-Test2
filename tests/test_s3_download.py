import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock
from modules.s3_download import list_csv_files, download_csv

def test_list_csv_files():
    with patch('boto3.client') as mock_client:
        mock_s3 = MagicMock()
        mock_client.return_value = mock_s3
        # 新形式: グループ名/日付_時分.csv
        mock_s3.get_paginator.return_value.paginate.return_value = [
            {'Contents': [
                {'Key': 'test/2025-06-12_0900.csv'},
                {'Key': 'test/2025-06-11_0900.csv'},
                {'Key': 'test1/2025-06-12_0900.csv'},
                {'Key': 'test/other.txt'}
            ]}
        ]
        files = list_csv_files('bucket', '', '2025-06-12')
        assert set(files) == {'test/2025-06-12_0900.csv', 'test1/2025-06-12_0900.csv'}


@pytest.mark.parametrize("objects,date_str,expected", [
    # No.1: 日付一致CSVのみ抽出
    ([{'Key': 'test/2025-06-12_0900.csv'}, {'Key': 'test/2025-06-11_0900.csv'}, {'Key': 'test1/2025-06-12_0900.csv'}, {'Key': 'test/other.txt'}], '2025-06-12', ['test/2025-06-12_0900.csv', 'test1/2025-06-12_0900.csv']),
    # No.2: 一致なし
    ([{'Key': 'test/2025-06-12_0900.csv'}, {'Key': 'test/2025-06-11_0900.csv'}], '2025-06-13', []),
    # No.3: S3にファイルなし
    ([], '2025-06-12', []),
    # No.4: 拡張子不一致
    ([{'Key': 'test/2025-06-12_0900.txt'}], '2025-06-12', []),
    # No.5: date_str空文字
    ([{'Key': 'test/2025-06-12_0900.csv'}], '', ['test/2025-06-12_0900.csv']),
    # No.6: 同一ファイル複数
    ([{'Key': 'test/2025-06-12_0900.csv'}, {'Key': 'test/2025-06-12_0900.csv'}], '2025-06-12', ['test/2025-06-12_0900.csv', 'test/2025-06-12_0900.csv']),
    # No.7: KeyがNone
    ([{'Key': None}], '2025-06-12', []),
])
def test_list_csv_files_cases(objects, date_str, expected):
    with patch('boto3.client') as mock_client:
        mock_s3 = MagicMock()
        mock_client.return_value = mock_s3
        mock_s3.get_paginator.return_value.paginate.return_value = [
            {'Contents': objects} if objects else {}
        ]
        files = list_csv_files('bucket', '', date_str)
        assert files == expected


@pytest.mark.parametrize("bucket,key,local_s3_dir,prefix,should_raise", [
    # 正常系
    ('bucket', 'test/2025-06-12_0900.csv', 'tmpdir', 'test/', False),
    ('bucket', 'test/2025-06-12_0900.csv', 'tmpdir', None, False),
    # ディレクトリ自動作成
    ('bucket', 'test/2025-06-12_0900.csv', 'tmpdir2', 'test/', False),
    # サブディレクトリも作成
    ('bucket', 'test/subdir/2025-06-12_0900.csv', 'tmpdir3', 'test/', False),
    # 想定外入力
    ('bucket', '', 'tmpdir', 'test/', True),
    ('bucket', None, 'tmpdir', 'test/', True),
    ('', 'test/2025-06-12_0900.csv', 'tmpdir', 'test/', True),
    (None, 'test/2025-06-12_0900.csv', 'tmpdir', 'test/', True),
    ('bucket', 'test/2025-06-12_0900.csv', '', 'test/', True),
    ('bucket', 'test/2025-06-12_0900.csv', None, 'test/', True),
])
def test_download_csv_cases(bucket, key, local_s3_dir, prefix, should_raise):
    with patch('boto3.client') as mock_client:
        mock_s3 = MagicMock()
        mock_client.return_value = mock_s3
        # Use a real temp dir for valid cases
        if local_s3_dir and local_s3_dir.startswith('tmpdir'):
            with tempfile.TemporaryDirectory() as tmpdir:
                local_dir = tmpdir if local_s3_dir == 'tmpdir' else os.path.join(tmpdir, local_s3_dir)
                if not should_raise:
                    # Should not raise
                    result = download_csv(bucket, key, local_dir, prefix)
                    mock_s3.download_file.assert_called_once()
                    assert os.path.exists(os.path.dirname(result))
                    assert result.endswith(os.path.basename(key))
                else:
                    with pytest.raises((ValueError, TypeError, FileNotFoundError, Exception)):
                        download_csv(bucket, key, local_dir, prefix)
        else:
            # For invalid local_s3_dir (empty/None)
            if should_raise:
                with pytest.raises((ValueError, TypeError, FileNotFoundError, Exception)):
                    download_csv(bucket, key, local_s3_dir, prefix)
            else:
                # Should not happen in this param set
                assert False, "Unexpected non-raise case"

