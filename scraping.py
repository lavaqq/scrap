import requests
from bs4 import BeautifulSoup
from progressbar import ProgressBar, SimpleProgress
import re
import json

asked_base_url = input(
    "\nEnter the base URL: ")
base_url = asked_base_url
asked_number_of_page = input('Enter the max number of page : ')
number_of_page = int(asked_number_of_page)
data = {}
pbar_list = ProgressBar(
    widgets=['\nRetrieve compagny page in list: ', SimpleProgress()], maxval=number_of_page)
for i in pbar_list(range(1, number_of_page + 1)):
    url = base_url + str(i)
    req = requests.get(url)
    res = BeautifulSoup(req.text, 'html.parser')
    results = res.find_all("a")
    table_rows = res.find_all("tr")
    for table_row in table_rows:
        anchors = table_row.find_all("a")
        for anchor in anchors:
            href = anchor.get("href")
            compagny_name = anchor.text
            data[compagny_name] = {"welipro_url": href, "Numéro d'entrprise": "", "Numéro de TVA": "", "Type d'entité": "", "Situation": "",
                                   "Capital": "", "Forme juridique": "", "Sécurité sociale": "", "Effectif": "", "Adresse": "", "Téléphone": "", "Fax": "", "Equipe": {}}
print('→ Company list scraping is finished')
pbarCompagny = ProgressBar(
    widgets=['\nRetrieve compagny data: ', SimpleProgress()], maxval=data.__len__())
for compagny in pbarCompagny(data):
    url = data[compagny]["welipro_url"]
    req = requests.get(url)
    res = BeautifulSoup(req.text, 'html.parser')
    first_card = res.find_all("ul", class_="list-group list-group-flush")
    second_card_child = res.find_all(
        "h2", class_="media bg-light font-weight-semibold py-2 like_li")
    second_card_parent = [
        second_card_child.parent for second_card_child in second_card_child]
    for item in first_card:
        li = item.find_all("li")
        for item in li:
            if "Numéro: " in item.text:
                data[compagny]["Numéro d'entrprise"] = item.text.replace(
                    "Numéro: ", "")
            if "Numéro de TVA  " in item.text:
                m = re.search(r'(BE)?0[0-9]{9}', item.text)
                if m:
                    data[compagny]["Numéro de TVA"] = m.group()
            if "Type d'entité: " in item.text:
                data[compagny]["Type d'entité"] = item.text.replace(
                    "Type d'entité: ", "")
            if "Situation: " in item.text:
                data[compagny]["Situation"] = item.text.replace(
                    "Situation: ", "")
            if "Capital: " in item.text:
                data[compagny]["Capital"] = item.text.replace("Capital: ", "")
            if "Forme juridique: " in item.text:
                m = re.search('Forme juridique: (.+?) Depuis', item.text)
                if m:
                    data[compagny]["Forme juridique"] = m.group(1)
            if "Sécurité sociale  " in item.text:
                m = re.search(r'\d\d\d\d\d\d\d-\d\d', item.text)
                if m:
                    data[compagny]["Sécurité sociale"] = m.group()
            if "Effectif: " in item.text:
                data[compagny]["Effectif"] = item.text.replace(
                    "Effectif: ", "")
            if item.find("i", class_="icon-direction mr-1"):
                i_parent = item.find("i", class_="icon-direction mr-1").parent
                address = ""
                for i_child in i_parent:
                    address += i_child.text
                data[compagny]["Adresse"] = address
            if "Téléphone: " in item.text:
                data[compagny]["Téléphone"] = item.text.replace(
                    "Téléphone: ", "")
            if "Fax: " in item.text:
                data[compagny]["Fax"] = item.text.replace("Fax: ", "")
    for item in second_card_parent:
        li = item.find_all("li")
        for item in li:
            m = re.search(
                r'( Depuis le )[0-9]{2}(-)[0-9]{2}(-)[0-9]{4}', item.text)
            if m:
                i = item.text.split(m.group())
                name = i[0].lstrip(' ')
                position = i[1]
                data[compagny]["Equipe"][name] = position
print('→ Company data scraping is finished')
asked_name_file = input('\nEnter the name of the file : ')
name_file = asked_name_file
print('→ Saving data to ' + name_file + '.json ...')
jsonString = json.dumps(data)
jsonFile = open(name_file + '.json', 'w')
jsonFile.write(jsonString)
jsonFile.close()
print('→ Data saved to ' + name_file + '.json')
