import os
import tempfile
from unittest.mock import patch, MagicMock
import pytest
from modules.box_upload import upload_to_box

def test_upload_to_box_success():
    with tempfile.NamedTemporaryFile(suffix='.zip') as tmpfile:
        tmpfile.write(b'zipdata')
        tmpfile.flush()
        os.environ['BOX_ACCESS_TOKEN'] = 'dummy_token'
        os.environ['BOX_FOLDER_ID'] = '999'
        os.environ['BOXSDK_TEST_MOCK'] = '1'
        file_id = upload_to_box(tmpfile.name)
        assert file_id == 'mocked_id'
        del os.environ['BOXSDK_TEST_MOCK']

def test_upload_to_box_no_token():
    with tempfile.NamedTemporaryFile(suffix='.zip') as tmpfile:
        if 'BOX_ACCESS_TOKEN' in os.environ:
            del os.environ['BOX_ACCESS_TOKEN']
        with pytest.raises(ValueError):
            upload_to_box(tmpfile.name)
