import os
import tempfile
import json
import pytest
from modules.box_utils import get_box_client
from unittest.mock import patch, MagicMock

def make_fake_jwt_config():
    return {
        "boxAppSettings": {
            "clientID": "fake_client_id",
            "clientSecret": "fake_client_secret",
            "appAuth": {
                "publicKeyID": "fake_key_id",
                "privateKey": "-----BEGIN ENCRYPTED PRIVATE KEY-----\nfake\n-----END ENCRYPTED PRIVATE KEY-----",
                "passphrase": "fake_passphrase"
            }
        },
        "enterpriseID": "fake_enterprise_id"
    }

def test_get_box_client():
    config = make_fake_jwt_config()
    with tempfile.NamedTemporaryFile('w+', delete=False) as tf:
        json.dump(config, tf)
        tf.flush()
        with patch('modules.box_utils.JWTAuth.from_settings_dictionary') as mock_jwt, \
             patch('modules.box_utils.Client') as mock_client:
            mock_auth = MagicMock()
            mock_jwt.return_value = mock_auth
            mock_client.return_value = 'client_instance'
            client = get_box_client(tf.name)
            assert client == 'client_instance'
            mock_jwt.assert_called_once_with(config)
            mock_client.assert_called_once_with(mock_auth)
    os.unlink(tf.name)
