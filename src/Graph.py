import pandas as pd

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
    def __init__(self, borders, cases):
        self.edges = borders
        self.vertices = cases

    def get_neighbours(self, country):
        if country.upper() not in self.edges.keys():
            country = mapping_countries_names[country]
        if country != 'Not_a_country':
            return self.edges[country.upper()]

    def get_stats(self, country, date):
        None
