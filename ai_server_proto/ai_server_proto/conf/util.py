import os
import json


def get_server_info_value(key: str):
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_dir = os.path.join(root_dir, '.config_secret')
    server_info = os.path.join(config_dir, 'server_info.json')

    with open(server_info, mode='rt', encoding='utf-8') as file:
        data = json.load(file)
        for k, v in data.items():
            if k == key:
                return v

        raise ValueError("Cannot check server information")
