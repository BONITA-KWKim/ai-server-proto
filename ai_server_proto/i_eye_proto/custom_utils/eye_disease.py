import os
import json


def get_disease_value(key: str):
    diseases = get_disease_list_value("disease")
    return diseases[key]


def get_disease_score_value():
    score = get_disease_list_value("score")
    return score


def get_disease_list_value(key: str):
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ref_dir = os.path.join(root_dir, 'references')
    disease = os.path.join(ref_dir, 'eye_diseases.json')

    with open(disease, mode='rt', encoding='utf-8') as file:
        data = json.load(file)
        for k, v in data.items():
            if k == key:
                return v

        raise ValueError("Cannot check key in white list")

