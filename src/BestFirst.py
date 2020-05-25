import Graph
from Path import Path
import datetime


class BestFirst:
    """Class representing Best First algorithm
    It returns a path depending on which country has the highest number of cases on the next day"""
    def __init__(self, starting_country, starting_date, alg_graph, goal_function):
        """Initializes BestFirst Algorithm object
        You specify the country and date you start with and a graph to work with"""
        self.path = Path(starting_country, starting_date)
        self.graph = alg_graph
        self.goal_function = goal_function


    def finding_path(self):
        """Main function to find a path according to BestFirst algorithm
            It returns a path object"""
        start_country, start_date = self.path.countries[0], self.path.start_date
        stats = self.graph.get_stats(start_country) # Here is a country which has latest data
        last_date = datetime.date(stats[0, 2], stats[0, 1], stats[0, 0])
        current_country_neighbors = self.graph.get_neighbours(start_country)
        current_country, current_date = start_country, start_date
        while current_date != last_date:
            current_country = self.choose_neighbor_with_max_cases(current_country_neighbors)
            current_country_neighbors = self.graph.get_neighbours(current_country)
            current_date += datetime.timedelta(days=1)
            self.path.add(current_country)
        self.path.eval(self.graph, self.goal_function)

    def choose_neighbor_with_max_cases(self, countries_list=None):
        """Function which chooses the best country to go to next
        It looks for the biggest number of cases from countries list"""
        countries_list = countries_list if countries_list else []
        try:
            if not countries_list:
                raise Exception
        except Exception as e:
            print("There are no neighbors to choose from: {0}".format(e))
        max_cases = -1
        country_with_max_cases = ''
        for country in countries_list:
            if self.path.get_profit(self.graph, country, self.goal_function) > max_cases:
                max_cases = self.path.get_profit(self.graph, country, self.goal_function)
                country_with_max_cases = country
        return country_with_max_cases

    def work(self):
        """Method which initializes every method essential to find a path"""
        self.finding_path()