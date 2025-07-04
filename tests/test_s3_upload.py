import os
import tempfile
import zipfile
import pytest
from unittest import mock
from modules.s3_upload import zip_csv_files, upload_csv

# --- zip_csv_files 正常系/境界値/異常系 ---
@pytest.mark.parametrize(
    "csv_dir, zip_path, files, expected_in_zip, expected_exception", [
        # No.1 標準ケース
        ("/tmp/dir1", "/tmp/out1.zip", ["a.csv", "b.csv"], ["a.csv", "b.csv"], None),
        # No.2 非CSV除外
        ("/tmp/dir2", "/tmp/out2.zip", ["a.csv", "b.csv", "c.txt"], ["a.csv", "b.csv"], None),
        # No.3 空ディレクトリ
        ("/tmp/dir3", "/tmp/out3.zip", [], [], None),
        # No.4 1件のみ
        ("/tmp/dir4", "/tmp/out4.zip", ["a.csv"], ["a.csv"], None),
        # No.5 複数件
        ("/tmp/dir5", "/tmp/out5.zip", ["a.csv", "b.csv", "c.csv"], ["a.csv", "b.csv", "c.csv"], None),
        # No.6 ディレクトリ不存在
        ("/notfound", "/tmp/out6.zip", None, None, FileNotFoundError),
        # No.7 csv_dir空文字
        ("", "/tmp/out7.zip", None, None, ValueError),
        # No.8 csv_dir None
        (None, "/tmp/out8.zip", None, None, TypeError),
        # No.9 zip_path空文字
        ("/tmp/dir9", "", ["a.csv"], None, ValueError),
        # No.10 zip_path None
        ("/tmp/dir10", None, ["a.csv"], None, TypeError),
    ]
)
def test_zip_csv_files(csv_dir, zip_path, files, expected_in_zip, expected_exception):
    """
    @pytest.mark.parametrize # No.1-10
    """
    if expected_exception:
        with pytest.raises(expected_exception):
            zip_csv_files(csv_dir, zip_path)
        return
    with tempfile.TemporaryDirectory() as tmpdir:
        # Use tmpdir for test isolation
        test_dir = os.path.join(tmpdir, os.path.basename(csv_dir))
        os.mkdir(test_dir)
        for f in files:
            with open(os.path.join(test_dir, f), "w") as fp:
                fp.write("data")
        zip_path_full = os.path.join(tmpdir, os.path.basename(zip_path))
        result = zip_csv_files(test_dir, zip_path_full)
        assert result == zip_path_full
        with zipfile.ZipFile(zip_path_full) as z:
            names = z.namelist()
            assert sorted(names) == sorted(expected_in_zip)

# --- upload_csv 正常系/境界値/異常系 ---
@pytest.mark.parametrize(
    "bucket, key, file_path, should_raise, expected_exception", [
        # No.1 標準ケース
        ("bucket", "test/file.csv", "/tmp/file.csv", False, None),
        # No.2 空ファイル
        ("bucket", "test/file.csv", "/tmp/empty.csv", False, None),
        # No.3 大容量ファイル
        ("bucket", "test/file.csv", "/tmp/large.csv", False, None),
        # No.4 bucket空文字
        ("", "test/file.csv", "/tmp/file.csv", True, ValueError),
        # No.5 bucket None
        (None, "test/file.csv", "/tmp/file.csv", True, TypeError),
        # No.6 key空文字
        ("bucket", "", "/tmp/file.csv", True, ValueError),
        # No.7 key None
        ("bucket", None, "/tmp/file.csv", True, TypeError),
        # No.8 file_path空文字
        ("bucket", "test/file.csv", "", True, ValueError),
        # No.9 file_path None
        ("bucket", "test/file.csv", None, True, TypeError),
        # No.10 ファイル不存在
        ("bucket", "test/file.csv", "/tmp/notfound.csv", True, FileNotFoundError),
    ]
)
def test_upload_csv(bucket, key, file_path, should_raise, expected_exception):
    """
    @pytest.mark.parametrize # No.1-10
    """
    with mock.patch("boto3.client") as m:
        m.return_value.upload_file.return_value = None
        if should_raise:
            m.return_value.upload_file.side_effect = expected_exception("error") if expected_exception is not FileNotFoundError else FileNotFoundError("error")
            with pytest.raises(expected_exception):
                upload_csv(bucket, key, file_path)
        else:
            upload_csv(bucket, key, file_path)
            m.return_value.upload_file.assert_called_once_with(file_path, bucket, key)



