from datetime import date

class Path:
    """Represents path by travel start daye, list of countries, and score"""
    def __init__(self, country, date):
        self.countries = [country]
        self.start_date = date
        self.score = 0

    def add(self, country):
        self.countries.append(country)