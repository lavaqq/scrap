import requests
from bs4 import BeautifulSoup
import re
import json
import src.utils as utils
from progressbar import AnimatedMarker, ProgressBar
from os.path import exists


def get(companies):
    if not exists("data/data.json"):
        companies_data = {}
        pbar = ProgressBar(
            widgets=['→ Retrieve all data companies: ', AnimatedMarker(['.', '..', '...'])])
        for city in pbar(companies):
            companies_data[city] = {}
            for company in companies[city]:
                companies_data[city][company] = {}
                url = companies[city][company]
                req = requests.get(url)
                res = BeautifulSoup(req.text, 'html.parser')
                first_card = res.find_all(
                    "ul", class_="list-group list-group-flush")
                second_card_child = res.find_all(
                    "h2", class_="media bg-light font-weight-semibold py-2 like_li")
                second_card_parent = [
                    second_card_child.parent for second_card_child in second_card_child]
                for item in first_card:
                    li = item.find_all("li")
                    for item in li:
                        if "Numéro: " in item.text:
                            companies_data[city][company] |= {
                                "Numéro d'entreprise": item.text.replace("Numéro: ", "").strip(' ')}
                        if "Numéro de TVA  " in item.text:
                            m = re.search(r'(BE)?0[0-9]{9}', item.text)
                            if m:
                                companies_data[city][company] |= {
                                    "Numéro de TVA": m.group().strip(' ')}
                        if "Type d'entité: " in item.text:
                            companies_data[city][company] |= {
                                "Type d'entité": item.text.replace("Type d'entité: ", "").strip(' ')}
                        if "Situation: " in item.text:
                            companies_data[city][company] |= {
                                "Situation": item.text.replace("Situation: ", "").strip(' ')}
                        if "Capital: " in item.text:
                            companies_data[city][company] |= {
                                "Capital": item.text.replace("Capital: ", "").strip(' ')}
                        if "Forme juridique: " in item.text:
                            m = re.search(
                                'Forme juridique: (.+?) Depuis', item.text)
                            if m:
                                companies_data[city][company] |= {
                                    "Forme juridique": m.group(1).strip(' ')}
                        if "Sécurité sociale  " in item.text:
                            m = re.search(r'\d\d\d\d\d\d\d-\d\d', item.text)
                            if m:
                                companies_data[city][company] |= {
                                    "Sécurité sociale": m.group().strip(' ')}
                        if "Effectif: " in item.text:
                            companies_data[city][company] |= {
                                "Effectif": item.text.replace("Effectif: ", "").strip(' ')}
                        if item.find("i", class_="icon-direction mr-1"):
                            i_parent = item.find(
                                "i", class_="icon-direction mr-1").parent
                            address = ""
                            for i_child in i_parent:
                                address += i_child.text
                            companies_data[city][company] |= {
                                "Adresse": address.replace("Belgique", "").strip(' ')}
                        if "Téléphone: " in item.text:
                            companies_data[city][company] |= {
                                "Téléphone": item.text.replace("Téléphone: ", "").strip(' ')}
                        if "Fax: " in item.text:
                            companies_data[city][company] |= {
                                "Fax": item.text.replace("Fax: ", "").strip(' ')}
                for item in second_card_parent:
                    li = item.find_all("li")
                    companies_data[city][company]["Equipe"] = {}
                    for item in li:
                        m = re.search(
                            r'( Depuis le )[0-9]{2}(-)[0-9]{2}(-)[0-9]{4}', item.text)
                        if m:
                            i = item.text.split(m.group())
                            name = i[0].strip(' ')
                            position = i[1].strip(' ')
                            companies_data[city][company]["Equipe"] |= {
                                name: position}
        # TODO: make it a function and put it in utils.data
        jsonString = json.dumps(companies_data, indent=2)
        jsonFile = open('data/data.json', 'w')
        jsonFile.write(jsonString)
        jsonFile.close()
    else:
        print("→ data/data.json is already created.")
