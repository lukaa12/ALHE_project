import pandas as pd
import requests
import datetime

# some names of countries are diffrent in covid dataset and in borders data
mapping_countries_names = {
    'BONAIRE, SAINT EUSTATIUS AND SABA': 'NETHERLANDS',
    'BRUNEI_DARUSSALAM': 'BRUNEI',
    'CASES_ON_AN_INTERNATIONAL_CONVEYANCE_JAPAN': 'NOT_A_COUNTRY',
    'CONGO': 'REPUBLIC_OF_THE_CONGO',
    'COTE_DIVOIRE': "CÔTE_D'IVOIRE",
    'CZECHIA': 'CZECH_REPUBLIC',
    'ESWATINI': 'ESWATINI_(SWAZILAND)',
    'FALKLAND_ISLANDS_(MALVINAS)': 'FALKLAND_ISLANDS',
    'GAMBIA': 'THE_GAMBIA',
    'GUINEA_BISSAU': 'GUINEA-BISSAU',
    'HOLY_SEE': 'VATICAN_CITY',
    'SAO_TOME_AND_PRINCIPE': 'SÃO_TOMÉ_AND_PRÍNCIPE',
    'TIMOR_LESTE': 'EAST_TIMOR',
    'UNITED_REPUBLIC_OF_TANZANIA': 'TANZANIA',
    'UNITED_STATES_OF_AMERICA': 'UNITED_STATES',
}

reverse_mapping_countries_names = {
    'BRUNEI': 'BRUNEI_DARUSSALAM',
    'REPUBLIC_OF_THE_CONGO': 'CONGO',
    "CÔTE_D'IVOIRE": 'COTE_DIVOIRE',
    'CZECH_REPUBLIC': 'CZECHIA',
    'ESWATINI_(SWAZILAND)': 'ESWATINI',
    'FALKLAND_ISLANDS': 'FALKLAND_ISLANDS_(MALVINAS)',
    'THE_GAMBIA': 'GAMBIA',
    'GUINEA-BISSAU': 'GUINEA_BISSAU',
    'VATICAN_CITY': 'HOLY_SEE',
    'SÃO_TOMÉ_AND_PRÍNCIPE': 'SAO_TOME_AND_PRINCIPE',
    'EAST_TIMOR': 'TIMOR_LESTE',
    'TANZANIA': 'UNITED_REPUBLIC_OF_TANZANIA',
    'UNITED_STATES': 'UNITED_STATES_OF_AMERICA',
}


class Graph:
    """Represents structure of Countries with borders and data about COVID in regions"""

    def __init__(self, borders, cases):
        self.edges = borders
        self.vertices = {}
        self.countries = list(borders.keys())

        cases['countriesAndTerritories'] = cases['countriesAndTerritories'].map(str.upper)
        cases = cases[['day', 'month', 'year', 'cases', 'deaths', 'countriesAndTerritories']]
        cases = cases.set_index('countriesAndTerritories')

        for country in list(borders.keys()):
            country_data = None
            try:
                country_data = cases.loc[country.upper()].to_numpy()
            except KeyError as error:
                try:
                    country_data = cases.loc[reverse_mapping_countries_names[country].upper()].to_numpy()
                except KeyError as error:
                    None
            self.vertices[country] = country_data

    def get_neighbours(self, country):
        country = self.parse_country(country)
        if country != 'Not_a_country':
            return self.edges[country]

    def get_stats(self, country):
        country = self.parse_country(country)
        return self.vertices[country]

    def get_active_cases(self, country, to_day):
        country = self.parse_country(country)
        stats = self.get_stats(country)

        cases = 0
        for i in range(stats.shape[0]):
            if (datetime.date(stats[i, 2], stats[i, 1], stats[i, 0]) <= to_day):
                cases += stats[i, 3]
            if (datetime.date(stats[i, 2], stats[i, 1], stats[i, 0]) < to_day):
                cases -= stats[i, 4]
        return cases

    def parse_country(self, country):
        if type(country) == int:
            country = self.countries[country.upper()]
        if country.upper() not in self.edges.keys():
            country = mapping_countries_names[country.upper()]
        return country.upper()


def refresh_covid_data():
    """Updates data about covid in local repository"""

    COVID_URL = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv"
    r = requests.get(COVID_URL, allow_redirects=True)
    open("../data/covid_data.csv", "wb").write(r.content)


def get_graph():
    """Returns graph containing borders between countries and covid data"""

    cases = pd.read_csv("../data/covid_data.csv")

    with open("../data/borders.csv", mode="r", encoding="utf-8-sig") as file:
        borders = {}
        for line in file:
            neighbours = line.replace('\n', '').replace(' ', '_').upper().split(',')
            borders[neighbours[0]] = neighbours[1:]
        file.close()

    graph = Graph(borders, cases)
    return graph
