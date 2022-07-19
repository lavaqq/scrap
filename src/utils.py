from os.path import exists
from progressbar import AnimatedMarker, ProgressBar
import json


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


# jsonString = json.dumps(companies_data, indent=2)
# jsonFile = open('data/data.json', 'w')
# jsonFile.write(jsonString)
# jsonFile.close()
