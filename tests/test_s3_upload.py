import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock
from modules.s3_upload import zip_csv_files, upload_csv

@pytest.mark.parametrize("csv_files,expected_files", [
    (["a.csv", "b.csv"], ["a.csv", "b.csv"]),
    (["a.csv", "b.txt"], ["a.csv"]),
    ([], []),
])
def test_zip_csv_files(csv_files, expected_files):
    with tempfile.TemporaryDirectory() as d:
        for fname in csv_files:
            with open(os.path.join(d, fname), 'w') as f:
                f.write('data')
        zip_path = os.path.join(d, 'out.zip')
        result = zip_csv_files(d, zip_path)
        assert os.path.exists(result)
        import zipfile
        with zipfile.ZipFile(result) as z:
            names = z.namelist()
            assert sorted(names) == sorted(expected_files)

@pytest.mark.parametrize("bucket,key,file_content,raises", [
    ("bucket", "key", b"data", None),
    (None, "key", b"data", Exception),
    ("bucket", None, b"data", Exception),
])
def test_upload_csv(bucket, key, file_content, raises):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(file_content)
        fpath = f.name
    try:
        with patch('modules.s3_upload.boto3.client') as mock_client:
            mock_s3 = MagicMock()
            mock_client.return_value = mock_s3
            if raises:
                with pytest.raises(Exception):
                    upload_csv(bucket, key, fpath)
            else:
                upload_csv(bucket, key, fpath)
                mock_s3.upload_file.assert_called_once_with(fpath, bucket, key)
    finally:
        os.remove(fpath)
