import datetime
import numpy as np
import Graph

class Path:
    """Represents path by travel start daye, list of countries, and score"""
    def __init__(self, country, date):
        self.countries = [country]
        self.start_date = date
        self.score = 0

    def add(self, country):
        """Dodaje kraj do ścieżki"""
        self.countries.append(country)

    def eval(self, graph, function = "recovered"):
        """Oblicza wartość ścieżki"""
        if function == "recovered":
            checked = []
            self.score = 0
            for i in range(len(self.countries)-1,-1,-1):
                if(self.countries[i] not in checked):
                    self.score += graph.get_active_cases(self.countries[i], self.start_date + datetime.timedelta(days=i))
                    checked.append(self.countries[i])
        if function == "deaths":
            self.score = 0
            for country in graph.countries:
                if country not in self.countries:
                    self.score += np.sum(graph.get_stats(country)[:,-1])
                else:
                    for i in range(graph.get_stats(country).shape[0]):
                        to_day = self.start_date + datetime.timedelta(days=self.countries.index(country))
                        if (datetime.date(graph.get_stats(country)[i, 2], graph.get_stats(country)[i, 1], graph.get_stats(country)[i, 0]) < to_day):
                            self.score += graph.get_stats(country)[i, 4]

    def get_profit(self, graph, country, function='recovered'):
        """Zwraca potencjalny zysk po dodaniu kraju na koniec ścieżki"""
        profit = 0
        if function == 'recovered':
            for i in range(len(self.countries)):
                if(self.countries[i] == country):
                    profit -= graph.get_active_cases(self.countries[i], self.start_date + datetime.timedelta(days=i))

            profit += graph.get_active_cases(country, self.start_date + datetime.timedelta(days=len(self.countries)))

        elif function == 'deaths':
            if country not in self.countries:
                to_day = self.start_date + datetime.timedelta(days=len(self.countries))
                for i in range(graph.get_stats(country).shape[0]):
                    if datetime.date(graph.get_stats(country)[i, 2], graph.get_stats(country)[i, 1], graph.get_stats(country)[i, 0]) >= to_day:
                        profit += graph.get_stats(country)[i, 4]
        return profit
