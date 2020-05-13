import Graph
import Path
from datetime import date
import numpy as np

class EvolutionaryAlgorithm:
    """Implementacja algorytmu ewolucyjnego
    Na wejściu przyjmuje argumentu:
    -dzień w którym naukowiec zaczyna podróż,
    -liczność populacji początkowej (μ)
    -liczność zbioru do reprodukcji (λ)
    -prawdopodobieństwo mutacji pojedynczego węzła ścieżki
    -sposób wyboru osobników do następnego pokolenia
        -'best' μ najlepszych
        -'roulette' metoda koła ruletki
        -'ranking' selekcja rankingowa
    """
    def __init__(self, graph, start_date, popul_q, repr_q, mutation, selection, generations):
        self.graph = graph
        self.start_date = start_date
        self.ni = popul_q
        self.lambd = repr_q
        self.mutation_p = mutation
        self.selection_method = selection
        self.generations = generations
        self.active_generation = []
        self.best = None

    def find_path(self):
        None

    def start_generation(self):
        end_day = date(self.graph.get_stats('Germany')[0,2], self.graph.get_stats('Germany')[0,1],
                       self.graph.get_stats('Germany')[0,0])
        path_len = (end_day - self.start_date).days
        start = np.random.randint(0, len(self.graph.countries), self.ni)
        for i in range(self.ni):
            path = Path.Path(self.graph.countries[start[i]], self.start_date)
            for j in range(path_len-1):
                nexts = self.graph.get_neighbours(path.countries[-1])
                path.add(nexts[np.random.randint(len(nexts))])
            self.active_generation.append(path)

    def random_lambda(self):
        None

    def reproduce(self, temp_popul):
        None

    def select_next_popul(self, reproduced):
        None

    def cross_paths(self, path1, path2):
        None

    def mutate(self, path):
        None

