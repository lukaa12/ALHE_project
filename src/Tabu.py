import Graph
import Path
from datetime import date
import numpy as np
import copy

class TabuSearch:
    """Implementacja algorytmu przeszukiwania przestrzeni ścieżek z tabu"""

    def __init__(self, graph, start_date, tabu_len, goal_function):
        self.graph = graph
        self.start_date = start_date
        self.tabu_len = tabu_len
        if goal_function not in ['recovered', 'deaths']:
            raise ValueError('Unsupported goal function: ' + goal_function)
        self.goal_function = goal_function
        self.tabu = []
        self.best = None
        self.x = None

    def start_with_random(self):
        end_day = date(self.graph.get_stats('Germany')[0, 2], self.graph.get_stats('Germany')[0, 1],
                       self.graph.get_stats('Germany')[0, 0])
        path_len = (end_day - self.start_date).days
        start = np.random.randint(len(self.graph.countries))
        path = Path.Path(self.graph.countries[start], self.start_date)
        for j in range(path_len - 1):
            nexts = self.graph.get_neighbours(path.countries[-1])
            path.add(nexts[np.random.randint(len(nexts))])
        self.x = path
        self.x.eval(self.graph)
        self.best = self.x

    def step(self):
        Y = self.get_neighbours()
        if len(Y) == 0:
            return
        local_best = Y[0]
        for i in Y:
            i.eval(self.graph)
            if self.goal_function == 'recovered' and i.score > local_best.score:
                local_best = i
            elif self.goal_function == 'deaths' and i.score < local_best.score:
                local_best = i
        if self.goal_function == 'recovered' and local_best.score > self.best.score:
            self.best = local_best
        elif self.goal_function == 'deaths' and local_best.score < self.best.score:
            self.best = local_best
        self.x = local_best
        self.tabu.append(self.x)
        self.tabu = self.tabu[-self.tabu_len:]

    def find_path(self, iterations = 1000):
        self.start_with_random()
        for i in range(iterations):
            self.step()
        return self.best

    def get_neighbours(self):
        neighbours = []
        for i in range(len(self.x.countries)):
            if i == 0:
                for j in self.graph.get_neighbours(self.x.countries[i+1]):
                    new_neighbour = copy.deepcopy(self.x)
                    new_neighbour.countries[i] = j
                    not_in_tabu = True
                    for t in self.tabu:
                        if new_neighbour.countries == t.countries:
                            not_in_tabu = False
                            break
                    if not_in_tabu:
                        neighbours.append(new_neighbour)
            elif i == len(self.x.countries) - 1:
                for j in self.graph.get_neighbours(self.x.countries[i-1]):
                    new_neighbour = copy.deepcopy(self.x)
                    new_neighbour.countries[i] = j
                    not_in_tabu = True
                    for t in self.tabu:
                        if new_neighbour.countries == t.countries:
                            not_in_tabu = False
                            break
                    if not_in_tabu:
                        neighbours.append(new_neighbour)
            else:
                possibles = list(set(self.graph.get_neighbours(self.x.countries[i - 1])) & set(
                    self.graph.get_neighbours(self.x.countries[i + 1])))
                if (self.x.countries[i] in possibles):
                    possibles.remove(self.x.countries[i])
                for j in possibles:
                    new_neighbour = copy.deepcopy(self.x)
                    new_neighbour.countries[i] = j
                    not_in_tabu = True
                    for t in self.tabu:
                        if new_neighbour.countries == t.countries:
                            not_in_tabu = False
                            break
                    if not_in_tabu:
                        neighbours.append(new_neighbour)
        return neighbours

