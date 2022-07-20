import requests
import src.utils as utils
from bs4 import BeautifulSoup
from os.path import exists


def get(cities):
    if not exists("data/companies.json"):
        print("→ data/companies.json does not exist, creating it ...")
        companies = {}
        for city in cities:
            companies[city] = {}
            counter = 0
            base_url = cities[city]
            for i in range(1, 1001):
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
        utils.write("data/companies.json", companies)
        print("→ " + str(counter) +
              " companies saved in data/companies.json.")
        return utils.load("data/companies.json")
    else:
        print("→ data/companies.json is already created.")
        return utils.load("data/companies.json")
