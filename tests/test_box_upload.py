import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock
from modules.box_upload import upload_to_box

@pytest.mark.parametrize("file_content,folder_id,env_mock,config_exists,raises,expected_id", [
    (b"dummy", None, True, True, None, 'mocked_id'),  # mock mode
    (b"dummy", "12345", False, True, None, 'uploaded_id'),  # normal
    (b"dummy", None, False, False, ValueError, None),  # config missing
])
def test_upload_to_box(file_content, folder_id, env_mock, config_exists, raises, expected_id):
    # Setup temp file
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(file_content)
        fpath = f.name
    # Env setup
    old_env = dict(os.environ)
    try:
        if env_mock:
            os.environ['BOXSDK_TEST_MOCK'] = '1'
        else:
            os.environ.pop('BOXSDK_TEST_MOCK', None)
        if config_exists:
            config_path = tempfile.mktemp()
            with open(config_path, 'w') as cf:
                cf.write('{}')
            os.environ['BOX_CONFIG_PATH'] = config_path
        else:
            os.environ['BOX_CONFIG_PATH'] = '/nonexistent/path.json'
        if raises:
            with pytest.raises(raises):
                upload_to_box(fpath, folder_id)
        else:
            if env_mock:
                result = upload_to_box(fpath, folder_id)
                assert result == expected_id
            else:
                # Patch Client and JWTAuth
                with patch('modules.box_upload.JWTAuth') as mock_jwt, \
                     patch('modules.box_upload.Client') as mock_client:
                    mock_auth = MagicMock()
                    mock_jwt.from_settings_file.return_value = mock_auth
                    mock_cli = MagicMock()
                    mock_client.return_value = mock_cli
                    mock_folder = MagicMock()
                    mock_cli.folder.return_value = mock_folder
                    mock_uploaded = MagicMock(id='uploaded_id')
                    mock_folder.upload_stream.return_value = mock_uploaded
                    result = upload_to_box(fpath, folder_id)
                    assert result == expected_id
    finally:
        os.environ.clear()
        os.environ.update(old_env)
        os.remove(fpath)
        if config_exists and 'config_path' in locals():
            os.remove(config_path)
