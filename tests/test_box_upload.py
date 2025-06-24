import os
import tempfile
from unittest.mock import patch, MagicMock
import pytest
from modules.box_upload import upload_to_box

def test_upload_to_box_success():
    with tempfile.NamedTemporaryFile(suffix='.zip') as tmpfile:
        tmpfile.write(b'zipdata')
        tmpfile.flush()
        os.environ['BOX_FOLDER_ID'] = '999'
        os.environ['BOXSDK_TEST_MOCK'] = '1'
        file_id = upload_to_box(tmpfile.name)
        assert file_id == 'mocked_id'
        del os.environ['BOXSDK_TEST_MOCK']

def test_upload_to_box_no_config():
    with tempfile.NamedTemporaryFile(suffix='.zip') as tmpfile:
        if 'BOX_CONFIG_PATH' in os.environ:
            del os.environ['BOX_CONFIG_PATH']
        if 'BOXSDK_TEST_MOCK' in os.environ:
            del os.environ['BOXSDK_TEST_MOCK']
        with pytest.raises(ValueError):
            upload_to_box(tmpfile.name)
