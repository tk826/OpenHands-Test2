import json
from boxsdk import JWTAuth, Client


def get_box_client(config_json_path):
    """
    JWT認証でBoxクライアントを取得する
    :param config_json_path: Boxアプリの構成ファイル(JSON)のパス
    :return: boxsdk.Client インスタンス
    """
    with open(config_json_path, 'r') as f:
        config = json.load(f)
    auth = JWTAuth.from_settings_dictionary(config)
    client = Client(auth)
    return client
