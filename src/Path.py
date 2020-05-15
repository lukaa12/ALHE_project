import datetime
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

    def eval(self, graph):
        """Oblicza wartość ścieżki"""
        checked = []
        self.score = 0
        for i in range(len(self.countries)-1,-1,-1):
            if(self.countries[i] not in checked):
                self.score += graph.get_active_cases(self.countries[i], self.start_date + datetime.timedelta(days=i))
                checked.append(self.countries[i])

    def get_profit(self, graph, country):
        """Zwraca potencjalny zysk po dodaniu kraju na koniec ścieżki"""
        profit = 0
        for i in range(len(self.countries)):
            if(self.countries[i] == country):
                profit -= graph.get_active_cases(self.countries[i], self.start_date + datetime.timedelta(days=i))

        profit += graph.get_active_cases(country, self.start_date + datetime.timedelta(days=len(self.countries)))
        return profit
