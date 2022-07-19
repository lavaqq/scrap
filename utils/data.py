from os.path import exists
import json


def load(file_name):
    if exists(file_name):
        with open(file_name, 'r') as f:
            data = json.load(f)
    else:
        data = {}
    return data
