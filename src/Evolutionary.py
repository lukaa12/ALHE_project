import Graph
import Path

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
        None

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

