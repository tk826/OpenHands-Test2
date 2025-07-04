import os
import tempfile
import zipfile
import pytest
from unittest import mock
from modules.s3_upload import zip_csv_files, upload_csv

@pytest.mark.parametrize("csv_files", [
    ["a.csv", "b.csv"],
    ["a.csv", "b.csv", "c.txt"],
    [],
    ["a.csv"],
    ["a.csv", "b.csv", "c.csv"],
])
def test_zip_csv_files(csv_files):
    with tempfile.TemporaryDirectory() as d:
        for f in csv_files:
            with open(os.path.join(d, f), "w") as fp:
                fp.write("data")
        zip_path = os.path.join(d, "out.zip")
        result = zip_csv_files(d, zip_path)
        assert result == zip_path
        with zipfile.ZipFile(zip_path) as z:
            names = z.namelist()
            assert all(n.endswith('.csv') for n in names)
            for f in csv_files:
                if f.endswith('.csv'):
                    assert f in names

@pytest.mark.parametrize("csv_dir, zip_path, exc", [
    ("/notfound", "/tmp/out.zip", FileNotFoundError),
    ("", "/tmp/out.zip", ValueError),
    (None, "/tmp/out.zip", TypeError),
    ("/tmp", "", ValueError),
    ("/tmp", None, TypeError),
])
def test_zip_csv_files_exceptions(csv_dir, zip_path, exc):
    if csv_dir == "/notfound":
        with pytest.raises(exc):
            zip_csv_files(csv_dir, zip_path)
    else:
        with pytest.raises(exc):
            zip_csv_files(csv_dir, zip_path)

@pytest.mark.parametrize("bucket, key, file_path", [
    ("bucket", "test/file.csv", "/tmp/file.csv"),
    ("bucket", "test/file.csv", "/tmp/empty.csv"),
])
def test_upload_csv(bucket, key, file_path):
    with mock.patch("boto3.client") as m:
        m.return_value.upload_file.return_value = None
        upload_csv(bucket, key, file_path)
        m.return_value.upload_file.assert_called_once_with(file_path, bucket, key)

@pytest.mark.parametrize("bucket, key, file_path, exc", [
    ("", "test/file.csv", "/tmp/file.csv", ValueError),
    (None, "test/file.csv", "/tmp/file.csv", TypeError),
    ("bucket", "", "/tmp/file.csv", ValueError),
    ("bucket", None, "/tmp/file.csv", TypeError),
    ("bucket", "test/file.csv", "", ValueError),
    ("bucket", "test/file.csv", None, TypeError),
    ("bucket", "test/file.csv", "/tmp/notfound.csv", FileNotFoundError),
])
def test_upload_csv_exceptions(bucket, key, file_path, exc):
    with mock.patch("boto3.client") as m:
        m.return_value.upload_file.side_effect = exc("error") if exc not in (FileNotFoundError,) else FileNotFoundError("error")
        with pytest.raises(exc):
            upload_csv(bucket, key, file_path)

