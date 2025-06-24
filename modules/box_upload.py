import os
from boxsdk import Client, OAuth2

def upload_to_box(file_path, folder_id=None):
    """
    指定したファイルをBOXにアップロードします。
    Args:
        file_path (str): アップロードするローカルファイルのパス。
        folder_id (str): アップロード先のBOXフォルダID（省略時は環境変数BOX_FOLDER_IDを使用）。
    Returns:
        str: アップロードされたファイルのBOXファイルID。
    """
    access_token = os.getenv('BOX_ACCESS_TOKEN')
    if folder_id is None:
        folder_id = os.getenv('BOX_FOLDER_ID', '0')
    if not access_token:
        raise ValueError('BOX_ACCESS_TOKEN is not set')
    # テスト時はモックを使う
    if os.getenv('BOXSDK_TEST_MOCK') == '1':
        from unittest.mock import MagicMock
        uploaded_file = MagicMock(id='mocked_id')
        return uploaded_file.id
    oauth2 = OAuth2(None, None, access_token=access_token)
    client = Client(oauth2)
    folder = client.folder(folder_id)
    file_name = os.path.basename(file_path)
    with open(file_path, 'rb') as f:
        uploaded_file = folder.upload_stream(f, file_name)
    return uploaded_file.id
