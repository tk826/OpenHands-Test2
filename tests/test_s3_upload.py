import os
import tempfile
from modules.s3_upload import zip_csv_files, upload_csv
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

def test_zip_csv_files_edge():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Directory does not exist
        with pytest.raises(Exception):
            zip_csv_files('/not/exist/dir', os.path.join(tmpdir, 'out.zip'))
        # Directory is not a directory
        file_path = os.path.join(tmpdir, 'notadir')
        with open(file_path, 'w') as f:
            f.write('not a dir')
        with pytest.raises(Exception):
            zip_csv_files(file_path, os.path.join(tmpdir, 'out2.zip'))
        # Directory is empty
        empty_dir = os.path.join(tmpdir, 'empty')
        os.mkdir(empty_dir)
        zip_path = os.path.join(tmpdir, 'empty.zip')
        result = zip_csv_files(empty_dir, zip_path)
        assert os.path.exists(result)
        # Output path not writable
        unwritable_dir = os.path.join(tmpdir, 'unwritable')
        os.mkdir(unwritable_dir, 0o400)
        with pytest.raises(Exception):
            zip_csv_files(empty_dir, os.path.join(unwritable_dir, 'fail.zip'))

def test_upload_csv_edge():
    with patch('boto3.client') as mock_client:
        mock_s3 = MagicMock()
        mock_client.return_value = mock_s3
        # file_path does not exist
        with pytest.raises(Exception):
            upload_csv('bucket', 'key', '/not/exist/file.zip')
        # bucket is empty
        with pytest.raises(Exception):
            upload_csv('', 'key', '/tmp/file.zip')
        # key is empty
        with pytest.raises(Exception):
            upload_csv('bucket', '', '/tmp/file.zip')
        # file_path is not readable
        with tempfile.NamedTemporaryFile(delete=False) as f:
            path = f.name
        os.chmod(path, 0o000)
        try:
            with pytest.raises(Exception):
                upload_csv('bucket', 'key', path)
        finally:
            os.chmod(path, 0o600)
            os.unlink(path)

