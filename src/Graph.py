import pandas as pd
import requests

# some names of countries are diffrent in covid dataset and in borders data
mapping_countries_names = {
    'Bonaire, Saint Eustatius and Saba' : 'Netherlands',
    'Brunei_Darussalam' : 'Brunei',
    'Cases_on_an_international_conveyance_Japan' : 'Not_a_country',
    'Congo' : 'Republic_of_the_Congo',
    'Cote_dIvoire' : "Côte_d'Ivoire",
    'Czechia' : 'Czech_Republic',
    'Eswatini' : 'Eswatini_(Swaziland)',
    'Falkland_Islands_(Malvinas)' : 'Falkland_Islands',
    'Gambia' : 'The_Gambia',
    'Guinea_Bissau' : 'Guinea-Bissau',
    'Holy_See' : 'Vatican_City',
    'Sao_Tome_and_Principe' : 'São_Tomé_and_Príncipe',
    'Timor_Leste' : 'East_Timor',
    'United_Republic_of_Tanzania' : 'Tanzania',
    'United_States_of_America' : 'United_States',
}

class Graph:
    """Represents structure of Countries with borders and data about COVID in regions"""

    def __init__(self, borders, cases):
        self.edges = borders
        self.vertices = cases

    def get_neighbours(self, country):
        if country.upper() not in self.edges.keys():
            country = mapping_countries_names[country]
        if country != 'Not_a_country':
            return self.edges[country.upper()]

    def get_stats(self, country, date):
        return self.vertices.loc[country.upper(), date.strftime('%d/%m/%Y')]


def refresh_covid_data():
    """Updates data about covid in local repository"""

    COVID_URL = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv"
    r = requests.get(COVID_URL, allow_redirects=True)
    open("../data/covid_data.csv", "wb").write(r.content)

def get_graph():
    """Returns graph containing borders between countries and covid data"""

    cases = pd.read_csv("../data/covid_data.csv")
    cases['countriesAndTerritories'] = cases['countriesAndTerritories'].map(str.upper)
    cases = cases.set_index(['countriesAndTerritories', 'dateRep'])

    with open("../data/borders.csv", mode="r", encoding="utf-8-sig") as file:
        borders = {}
        for line in file:
            neighbours = line.replace('\n', '').replace(' ', '_').upper().split(',')
            borders[neighbours[0]] = neighbours[1:]
        file.close()

    graph = Graph(borders, cases)
    return graph