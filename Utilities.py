import json
import os


def open_file(folder_path: str, file_path: str):
    if file_path.endswith('json'):
        with open(os.path.join(folder_path, file_path), 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
    return data


def save_file(data, folder_path: str, file_path: str):
    with open(os.path.join(folder_path, file_path), 'w', encoding='utf-8') as save_f:
        json.dump(data, save_f, indent=2, ensure_ascii=False)


def check_folder(folder_path: str):
    if os.path.exists(folder_path):
        pass
    else:
        os.makedirs(folder_path)
