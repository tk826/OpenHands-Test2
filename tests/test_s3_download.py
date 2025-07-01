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


def test_list_csv_files_cases():
    with patch('boto3.client') as mock_client:
        mock_s3 = MagicMock()
        mock_client.return_value = mock_s3
        # 様々なパターンのファイルを用意
        mock_s3.get_paginator.return_value.paginate.return_value = [
            {'Contents': [
                {'Key': 'test/2025-06-12_0900.csv'},  # マッチ
                {'Key': 'test/2025-06-12_1000.csv'},  # マッチ
                {'Key': 'test/2025-06-11_0900.csv'},  # 別日付
                {'Key': 'test1/2025-06-12_0900.csv'}, # マッチ
                {'Key': 'test/2025-06-12_0900.txt'},  # 拡張子違い
                {'Key': 'test/2025-06-12.csv'},       # フォーマット違い
                {'Key': 'test/other.txt'},            # 無関係
                {'Key': 'test2/2025-06-12_0900.csv'}, # マッチ
                {'Key': 'test/2025-06-12_0900_foo.csv'}, # フォーマット違い
            ]}
        ]
        # 2025-06-12でフィルタ
        files = list_csv_files('bucket', '', '2025-06-12')
        # 正しいものだけが返る
        assert set(files) == {
            'test/2025-06-12_0900.csv',
            'test/2025-06-12_1000.csv',
            'test1/2025-06-12_0900.csv',
            'test2/2025-06-12_0900.csv',
        }
        # 別日付や拡張子違い、フォーマット違いは含まれない
        assert 'test/2025-06-11_0900.csv' not in files
        assert 'test/2025-06-12_0900.txt' not in files
        assert 'test/2025-06-12.csv' not in files
        assert 'test/other.txt' not in files
        assert 'test/2025-06-12_0900_foo.csv' not in files
        # 日付にマッチしない場合は空
        mock_s3.get_paginator.return_value.paginate.return_value = [
            {'Contents': [
                {'Key': 'test/2025-06-11_0900.csv'},
                {'Key': 'test/2025-06-11_1000.csv'},
            ]}
        ]
        files = list_csv_files('bucket', '', '2025-06-12')
        assert files == []

def test_download_csv():
    with patch('boto3.client') as mock_client, tempfile.TemporaryDirectory() as tmpdir:
        mock_s3 = MagicMock()
        mock_client.return_value = mock_s3
        prefix = 'test/'
        key = 'test/2025-06-12_0900.csv'
        bucket = 'bucket'
        local_path = download_csv(bucket, key, tmpdir, prefix)
        mock_s3.download_file.assert_called_once()
        assert os.path.exists(tmpdir)
        # local_path should be in tmpdir and subdir
        assert local_path.startswith(tmpdir)
        assert os.path.basename(local_path) == '2025-06-12_0900.csv'
        assert os.path.basename(os.path.dirname(local_path)) == 'test'
