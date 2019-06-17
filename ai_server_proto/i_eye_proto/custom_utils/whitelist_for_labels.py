import os
import json


def get_whitelist_value(key: str):
    required = get_list_value("required")
    return required[key]


def get_refusal_value(key: str):
    refusal = get_list_value("refusal")
    return refusal[key]


def get_whitelist_score_value():
    score = get_list_value("score")
    return score


def get_list_value(key: str):
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ref_dir = os.path.join(root_dir, 'references')
    whitelist = os.path.join(ref_dir, 'whitelist_for_labels.json')

    with open(whitelist, mode='rt', encoding='utf-8') as file:
        data = json.load(file)
        for k, v in data.items():
            if k == key:
                return v

        raise ValueError("Cannot check key in white list")

