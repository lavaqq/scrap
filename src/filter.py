import pandas as pd
import utils

data = utils.load('data/data.json')


def filter_team():
    roles = ['Administrateur', 'Gérant', 'Fondateur',
             'Président', 'Représentant', 'Directeur', 'Vice-président']
    filter_team = []
    for cities in data:
        for company in data[cities]:
            try:
                for key, value in data[cities][company]['Equipe'].items():
                    p = value.split()
                    for i in roles:
                        if i in p:
                            filter_team.append(company)
            except KeyError:
                pass
    return filter_team


def filter_situation():
    filter_situation = []
    for cities in data:
        for company in data[cities]:
            try:
                p = data[cities][company]['Situation'].split()
                if 'normale' in p:
                    filter_situation.append(company)
            except KeyError:
                pass
    return filter_situation


def get_filtered_companies():
    team = filter_team()
    situation = filter_situation()
    filtered_companies = []
    for i in team:
        if i in situation:
            filtered_companies.append(i)
    return filtered_companies


def get_data(filtered_companies):
    tmp_filtered_data = {}
    filtered_data = {}
    for cities in data:
        for company in data[cities]:
            if company in filtered_companies:
                tmp_filtered_data |= {company: data[cities][company]}
                tmp_filtered_data[company]['Ville'] = cities
    for company in tmp_filtered_data:
        if 'normale' in tmp_filtered_data[company]['Situation']:
            filtered_data |= {company: tmp_filtered_data[company]}
    return filtered_data


def getRoles():
    words_list = []
    for cities in data:
        for company in data[cities]:
            try:
                words_list.append(data[cities][company]["Situation"])
            except KeyError:
                pass
    checked_words = []
    for word in words_list:
        if word not in checked_words:
            words_list.count(word)
            checked_words.append(word)
            print(word, words_list.count(word))
        else:
            pass


def check_tmp(tmp_companies, company):
    if company in tmp_companies:
        return True
    else:
        return False


def filter():
    raw_data = utils.load('data/filtered_data.json')
    tmp_companies = {}
    for company in raw_data:
        try:
            if raw_data[company]['Numéro de TVA']:
                tmp_companies |= {company: raw_data[company]}
            else:
                if check_tmp(tmp_companies, company):
                    del tmp_companies[company]
            if raw_data[company]["Type d'entité"]:
                tmp_companies |= {company: raw_data[company]}
            else:
                if check_tmp(tmp_companies, company):
                    del tmp_companies[company]
            if raw_data[company]['Situation']:
                tmp_companies |= {company: raw_data[company]}
            else:
                if check_tmp(tmp_companies, company):
                    del tmp_companies[company]
            if raw_data[company]['Capital']:
                tmp_companies |= {company: raw_data[company]}
            else:
                if check_tmp(tmp_companies, company):
                    del tmp_companies[company]
            if raw_data[company]['Forme juridique']:
                tmp_companies |= {company: raw_data[company]}
            else:
                if check_tmp(tmp_companies, company):
                    del tmp_companies[company]
            if raw_data[company]['Effectif']:
                tmp_companies |= {company: raw_data[company]}
            else:
                if check_tmp(tmp_companies, company):
                    del tmp_companies[company]
            if raw_data[company]['Téléphone']:
                tmp_companies |= {company: raw_data[company]}
            else:
                if check_tmp(tmp_companies, company):
                    del tmp_companies[company]
        except KeyError:
            if check_tmp(tmp_companies, company):
                del tmp_companies[company]
            else:
                pass
    for company in tmp_companies:
        tmp_companies[company]['Name'] = company
        try:
            del tmp_companies[company]['Sécurité sociale']
        except KeyError:
            pass
    for company in tmp_companies:
        try:
            del tmp_companies[company]['Fax']
        except KeyError:
            pass
    utils.write('data/test.json', tmp_companies)


# utils.write('data/filtered_data.json', get_data(get_filtered_companies()))
filter()
pdObj = pd.read_json('data/test.json', orient='index')
pdObj.to_csv('data/data.csv', index=False)
