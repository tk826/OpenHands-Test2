import os
import tempfile
import pytest
from unittest import mock
from modules.box_upload import upload_to_box

@pytest.mark.parametrize("file_path, folder_id, env, expected, exc", [  # No 1-4,7
    ("/tmp/file1.csv", "12345", {"BOXSDK_TEST_MOCK": "1"}, "mocked_id", None),
    ("/tmp/file2.csv", None, {"BOXSDK_TEST_MOCK": "1", "BOX_FOLDER_ID": "99999"}, "mocked_id", None),
    ("/tmp/empty.csv", "12345", {"BOXSDK_TEST_MOCK": "1"}, "mocked_id", None),
    ("/tmp/large.csv", "12345", {"BOXSDK_TEST_MOCK": "1"}, "mocked_id", None),
    ("/tmp/file3.csv", "", {"BOXSDK_TEST_MOCK": "1", "BOX_FOLDER_ID": "99999"}, "mocked_id", None),
])
def test_upload_to_box_mock(file_path, folder_id, env, expected, exc):
    with mock.patch.dict(os.environ, env, clear=True):
        with mock.patch("builtins.open", mock.mock_open(read_data="data")):
            with mock.patch("os.path.exists", return_value=True):
                if exc:
                    with pytest.raises(exc):
                        upload_to_box(file_path, folder_id)
                else:
                    assert upload_to_box(file_path, folder_id) == expected

@pytest.mark.parametrize("file_path, folder_id, env, exc", [  # No 5-6,10
    ("", "12345", {"BOXSDK_TEST_MOCK": "1"}, ValueError),
    (None, "12345", {"BOXSDK_TEST_MOCK": "1"}, TypeError),
    ("/tmp/notfound.csv", "12345", {"BOXSDK_TEST_MOCK": "1"}, FileNotFoundError),
])
def test_upload_to_box_mock_exceptions(file_path, folder_id, env, exc):
    with mock.patch.dict(os.environ, env, clear=True):
        if file_path == "/tmp/notfound.csv":
            with mock.patch("builtins.open", side_effect=FileNotFoundError):
                with pytest.raises(exc):
                    upload_to_box(file_path, folder_id)
        else:
            with pytest.raises(exc):
                upload_to_box(file_path, folder_id)

@pytest.mark.parametrize("file_path, folder_id, env, exc", [  # No 8-9
    ("/tmp/file3.csv", None, {"BOXSDK_TEST_MOCK": "0"}, ValueError),
    ("/tmp/file3.csv", None, {"BOXSDK_TEST_MOCK": "0", "BOX_CONFIG_PATH": "/tmp/notfound.json"}, ValueError),
])
def test_upload_to_box_real_exceptions(file_path, folder_id, env, exc):
    with mock.patch.dict(os.environ, env, clear=True):
        with pytest.raises(exc):
            upload_to_box(file_path, folder_id)
