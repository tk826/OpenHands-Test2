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

@pytest.mark.parametrize("bucket,prefix,date_str,expected,exception", [
    ("", "", "2025-06-12", None, Exception),  # empty bucket
    ("bucket", "", "", ["test/2025-06-12_0900.csv", "test/2025-06-11_0900.csv", "test1/2025-06-12_0900.csv"], None),  # empty date_str returns all csv
    ("bucket", "", "notfound", [], None),  # no matching date
])
def test_list_csv_files_edge(bucket, prefix, date_str, expected, exception):
    with patch('boto3.client') as mock_client:
        mock_s3 = MagicMock()
        mock_client.return_value = mock_s3
        mock_s3.get_paginator.return_value.paginate.return_value = [
            {'Contents': [
                {'Key': 'test/2025-06-12_0900.csv'},
                {'Key': 'test/2025-06-11_0900.csv'},
                {'Key': 'test1/2025-06-12_0900.csv'},
                {'Key': 'test/other.txt'}
            ]}
        ]
        if exception:
            with pytest.raises(Exception):
                list_csv_files(bucket, prefix, date_str)
        else:
            files = list_csv_files(bucket, prefix, date_str)
            assert set(files) == set(expected)


def test_list_csv_files_no_contents():
    with patch('boto3.client') as mock_client:
        mock_s3 = MagicMock()
        mock_client.return_value = mock_s3
        mock_s3.get_paginator.return_value.paginate.return_value = [{}]
        files = list_csv_files('bucket', '', '2025-06-12')
        assert files == []


def test_download_csv_edge():
    with patch('boto3.client') as mock_client, tempfile.TemporaryDirectory() as tmpdir:
        mock_s3 = MagicMock()
        mock_client.return_value = mock_s3
        # key does not exist
        mock_s3.download_file.side_effect = Exception("Not found")
        with pytest.raises(Exception):
            download_csv('bucket', 'notfound.csv', tmpdir)
        # bucket is empty
        with pytest.raises(Exception):
            download_csv('', 'test.csv', tmpdir)
        # key is empty
        with pytest.raises(Exception):
            download_csv('bucket', '', tmpdir)
        # local_s3_dir is not writable
        unwritable_dir = os.path.join(tmpdir, 'unwritable')
        os.mkdir(unwritable_dir, 0o400)
        with pytest.raises(Exception):
            download_csv('bucket', 'test.csv', unwritable_dir)

