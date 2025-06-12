import os
import tempfile
from s3_upload import zip_csv_files, upload_csv
from unittest.mock import patch, MagicMock

def test_zip_csv_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        csv1 = os.path.join(tmpdir, 'a.csv')
        csv2 = os.path.join(tmpdir, 'b.csv')
        with open(csv1, 'w') as f:
            f.write('a,b\n1,2')
        with open(csv2, 'w') as f:
            f.write('c,d\n3,4')
        zip_path = os.path.join(tmpdir, 'test.zip')
        zip_csv_files(tmpdir, zip_path)
        assert os.path.exists(zip_path)

def test_upload_csv():
    with patch('boto3.client') as mock_client:
        mock_s3 = MagicMock()
        mock_client.return_value = mock_s3
        upload_csv('bucket', 'key', '/tmp/file.zip')
        mock_s3.upload_file.assert_called_once()
