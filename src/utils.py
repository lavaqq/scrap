import json
from os.path import exists
from progressbar import AnimatedMarker, ProgressBar


def load(file_name):
    if exists(file_name):
        with open(file_name, 'r') as f:
            data = json.load(f)
    else:
        data = {}
    return data


def write(file_name, data):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=2)
