import requests
from bs4 import BeautifulSoup
import json
import utils.data as data
from progressbar import AnimatedMarker, ProgressBar
from os.path import exists


def get(cities):
    if not exists("data/companies.json"):
        companies = {}
        pbar = ProgressBar(
            widgets=['→ Retrieve all companies: ', AnimatedMarker(['.', '..', '...'])])
        for city in cities:
            companies[city] = {}
            counter = 0
            base_url = cities[city]
            for i in pbar(range(1, 1001)):
                url = base_url + str(i)
                req = requests.get(url)
                res = BeautifulSoup(req.text, 'html.parser')
                if res.find("div") is None:
                    break
                else:
                    rows = res.find_all("tr")
                    for row in rows:
                        anchors = row.find_all("a")
                        for anchor in anchors:
                            href = anchor.get("href")
                            compagny_name = anchor.text
                            companies[city] |= {compagny_name: href}
            counter += companies[city].__len__()
        # TODO: make it a function and put it in utils.data
        jsonString = json.dumps(companies, indent=4)
        jsonFile = open('data/companies.json', 'w')
        jsonFile.write(jsonString)
        jsonFile.close()
        print("→ " + str(counter) +
              " companies saved in data/companies.json.")
        return data.load("data/companies.json")
    else:
        print("→ data/companies.json is already created.")
        return data.load("data/companies.json")
