import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock
from modules.s3_download import list_csv_files, download_csv

def test_list_csv_files():
    with patch('boto3.client') as mock_client:
        mock_s3 = MagicMock()
        mock_client.return_value = mock_s3
        mock_s3.list_objects_v2.return_value = {
            'Contents': [
                {'Key': 'csv/2025-06-12_test.csv'},
                {'Key': 'csv/2025-06-11_test.csv'},
                {'Key': 'csv/other.txt'}
            ]
        }
        files = list_csv_files('bucket', 'csv/', '2025-06-12')
        assert files == ['csv/2025-06-12_test.csv']

def test_download_csv():
    with patch('boto3.client') as mock_client, tempfile.TemporaryDirectory() as tmpdir:
        mock_s3 = MagicMock()
        mock_client.return_value = mock_s3
        key = 'csv/2025-06-12_test.csv'
        bucket = 'bucket'
        local_path = download_csv(bucket, key, tmpdir)
        mock_s3.download_file.assert_called_once()
        assert os.path.exists(tmpdir)
