import json
from bs4 import BeautifulSoup
import requests

base_url = "https://be.welipro.com/v?page="
data = {}

for i in range(1, 1001):
    url = base_url + str(i)
    req = requests.get(url)
    res = BeautifulSoup(req.text, 'html.parser')
    if res.find("div") is None:
        break
    else:
        list = res.find("div", class_="content")
        for item in list.find_all("a"):
            city_name = item.text
            city_url = item.get("href")
            if city_name.__len__() > 1:  # TODO: check if it's not a pagination link
                data |= {city_name.strip(' '): city_url}

print('→ Saving ' + str(data.__len__()) + " cities in data/cities.json ...")
jsonString = json.dumps(data, indent=4)
jsonFile = open('data/cities.json', 'w')
jsonFile.write(jsonString)
jsonFile.close()
print('→ All data has been saved in data/cities.json')
