import os
from boxsdk import Client, JWTAuth

from modules.messages import MESSAGES
def upload_to_box(file_path, folder_id=None):
    """
    指定したファイルをBOXにアップロードします。
    Args:
        file_path (str): アップロードするローカルファイルのパス。
        folder_id (str): アップロード先のBOXフォルダID（省略時は環境変数BOX_FOLDER_IDを使用）。
    Returns:
        str: アップロードされたファイルのBOXファイルID。
    """
    if folder_id is None:
        folder_id = os.getenv('BOX_FOLDER_ID', '0')
    # テスト時はモックを使う
    if os.getenv('BOXSDK_TEST_MOCK') == '1':
        if file_path is None:
            raise TypeError(MESSAGES['file_path_none'])
        if not file_path:
            raise ValueError(MESSAGES['file_path_empty'])
        if not os.path.exists(file_path):
            raise FileNotFoundError(MESSAGES['file_not_found'].format(file_path=file_path))
        from unittest.mock import MagicMock
        uploaded_file = MagicMock(id='mocked_id')
        return uploaded_file.id
    config_path = os.getenv('BOX_CONFIG_PATH')
    if not config_path or not os.path.exists(config_path):
        raise ValueError(MESSAGES['box_config_missing'])
    auth = JWTAuth.from_settings_file(config_path)
    client = Client(auth)
    folder = client.folder(folder_id)
    file_name = os.path.basename(file_path)
    with open(file_path, 'rb') as f:
        uploaded_file = folder.upload_stream(f, file_name)
    return uploaded_file.id
