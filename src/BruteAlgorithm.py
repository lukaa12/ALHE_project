from Path import Path
import datetime


class BruteAlgorithm:
    """Class representing Brute Algorithm
    It takes every possible path in the graph and finds the one,
    on which the doctor cures the highest number of people"""
    def __init__(self, starting_country, starting_date, alg_graph, goal_function):
        """Method which initializes BruteAlgorithm object
            It takes start country and date plus the graph on which it should work on"""
        self.path = Path(starting_country, starting_date)
        self.graph = alg_graph
        self.possible_paths = [tuple([starting_country])]
        stats = self.graph.get_stats(starting_country)  # Here is a country which has latest data
        self.last_date = datetime.date(stats[0, 2], stats[0, 1], stats[0, 0])
        self.days_difference = int((self.last_date - starting_date).days)
        self.goal_function = goal_function

    def generate_paths(self):
        """Method which generates all available paths"""
        for path_list in self.possible_paths:
            if int(self.days_difference) < len(path_list):
                break
            for neighbor in self.graph.get_neighbours(path_list[len(path_list)-1]):
                new_path = list(path_list)
                new_path.append(neighbor)
                self.possible_paths.append(tuple(new_path))

    def choose_best_path(self):
        """Method chooses the best possible path (which has the highest number of cured poeple)"""
        longest_paths = [path for path in self.possible_paths if len(path) == self.days_difference + 1]
        best_path = []
        if self.goal_function == 'recovered':
            best_score = -1
        elif self.goal_function == 'deaths':
            best_score = 1000000000
        for path in longest_paths:
            self.clear_path()
            self.add_whole_path(path)
            self.path.eval(self.graph, self.goal_function)
            if self.goal_function == 'recovered' and self.path.score > best_score:
                best_score = self.path.score
                best_path = path
            elif self.goal_function == 'deaths' and self.path.score < best_score:
                best_score = self.path.score
                best_path = path
        self.clear_path()
        self.add_whole_path(best_path)
        self.path.eval(self.graph, self.goal_function)

    def clear_path(self):
        """Method clears the variable self.path leaving only the starting country"""
        for i in range(len(self.path.countries)-1):
            self.path.countries.pop()
        self.path.score = 0

    def add_whole_path(self, path):
        """Method adds countries which are in the argument 'path'
        (execpt the first one which is already in the variable self.path"""
        for country_index in range(len(path)):
            if country_index == 0:
                continue
            self.path.add(path[country_index])

    def work(self):
        """Method which initializes every method essential to find a path"""
        self.generate_paths()
        self.choose_best_path()