import Graph
import Path
from datetime import date
import numpy as np

class EvolutionaryAlgorithm:
    """Implementacja algorytmu ewolucyjnego
    Na wejściu przyjmuje argumentu:
    -graf na którym ma działać
    -dzień w którym naukowiec zaczyna podróż,
    -liczność populacji początkowej (μ)
    -liczność zbioru do reprodukcji (λ)
    -prawdopodobieństwo mutacji pojedynczej ścieżki
    -sposób wyboru osobników do następnego pokolenia
        -'best' μ najlepszych
        -'roulette' metoda koła ruletki
        -'ranking' selekcja rankingowa
    -liczba pokoleń przez które będzie działać algorytm
    """
    def __init__(self, graph, start_date, popul_q, repr_q, mutation, selection, generations, goal_function):
        self.graph = graph
        self.start_date = start_date
        self.ni = popul_q
        self.lambd = repr_q
        self.mutation_p = mutation
        if selection not in ['best', 'roulette', 'ranking']:
            raise ValueError('Unsupported selection method: ' + selection)
        self.selection_method = selection
        self.generations = generations
        if goal_function not in ['recovered', 'deaths']:
            raise ValueError('Unsupported goal function: ' + goal_function)
        self.goal_function = goal_function
        self.active_generation = []
        self.best = None

    def find_path(self):
        self.start_generation()
        for i in range(self.generations):
            self.active_generation = self.select_next_generation(self.reproduce(self.random_lambda()))
        return self.best

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
        self.active_generation.sort(reverse=True, key=lambda x: x.score)
        self.best = self.active_generation[0]

    def random_lambda(self):
        popul = []
        choices = np.random.randint(0, len(self.active_generation), self.lambd)
        for i in choices:
            popul.append(self.active_generation[i])
        return popul

    def reproduce(self, temp_popul):
        offspring = []
        for i in range(len(temp_popul)):
            for j in range(i + 1, len(temp_popul),1):
                if(i < len(temp_popul) and self.can_be_mixed(temp_popul[i],temp_popul[j])):
                    k , l = self.cross_paths(temp_popul[i], temp_popul[j])
                    temp_popul.remove(temp_popul[j])
                    offspring.append(k)
                    offspring.append(l)
                    break
        for i in range(len(offspring)):
            if (np.random.random_sample() < self.mutation_p):
                offspring[i] = self.mutate(offspring[i])
        return offspring


    def select_next_generation(self, reproduced):
        candidats = self.active_generation + reproduced
        new_generation = []
        for i in candidats:
            i.eval(self.graph, self.goal_function)
        for candidat in candidats:
            if self.goal_function == 'recovered' and candidat.score > self.best.score:
                self.best = candidat
            elif self.goal_function == 'deaths' and candidat.score < self.best.score:
                self.best = candidat

        if self.selection_method == 'best':
            if self.goal_function == 'recovered':
                candidats.sort(reverse= True, key= lambda x : x.score)
            elif self.goal_function == 'deaths':
                candidats.sort(reverse=False, key=lambda x: x.score)
            new_generation = candidats[:self.ni]

        if self.selection_method == 'roulette':
            scores_sum = 0.0
            for i in candidats:
                scores_sum += i.score
            shots = np.random.random(self.ni)
            for shot in shots:
                for i in range(len(candidats)):
                    if self.goal_function =='recovered':
                        if shot < candidats[i].score / scores_sum:
                            new_generation.append(candidats[i])
                            scores_sum -= candidats[i].score
                            candidats.pop(i)
                            break
                        else:
                            shot -= candidats[i].score / scores_sum
                    elif self.goal_function == 'deaths':
                        if shot < (scores_sum - candidats[i].score) / scores_sum:
                            new_generation.append(candidats[i])
                            scores_sum -= candidats[i].score
                            candidats.pop(i)
                            break
                        else:
                            shot -= (scores_sum - candidats[i].score) / scores_sum

        if self.selection_method == 'ranking':
            if self.goal_function == 'recovered':
                candidats.sort(reverse=True, key=lambda x: x.score)
            elif self.goal_function == 'deaths':
                candidats.sort(reverse=False, key=lambda x: x.score)
            while(len(new_generation) != self.ni):
                for i in new_generation:
                    candidats.remove(i)
                for i in range(len(candidats)):
                    if np.random.random() < (len(candidats) - i) / len(candidats):
                        new_generation.append(candidats[i])
                    if len(new_generation) == self.ni:
                        break

        return new_generation

    def cross_paths(self, path1, path2):
        itrsct = [value for value in path1.countries if value in path2.countries]
        point1, point2 = path1.countries.index(itrsct[len(itrsct) // 2]), path2.countries.index(itrsct[len(itrsct) // 2])
        need_len = len(path2.countries)
        if (point1 == point2):
            ch1 = path1.countries[:point1] + path2.countries[point2:]
            ch2 = path2.countries[:point2] + path1.countries[point1:]
            child1, child2 = path1, path2
            child1.countries, child2.countries = ch1, ch2
            return child1, child2
        if (point1 < point2):
            tmp, tmpp = path1, point1
            path1, point1 = path2, point2
            path2, point2 = tmp, tmpp
        path = path1.countries[:point1] + path2.countries[point2:]
        ch1 = path[:need_len]
        ch2 = path[-need_len:]
        child1, child2 = path1, path2
        child1.countries, child2.countries = ch1, ch2
        return child1, child2

    def mutate(self, path):
        for i in range(1,len(path.countries)-1, 1):
            possibles = list(set(self.graph.get_neighbours(path.countries[i-1])) & set(self.graph.get_neighbours(path.countries[i+1])))
            if(len(possibles) > 1):
                if(path.countries[i] in possibles):
                    possibles.remove(path.countries[i])
                path.countries[i] = possibles[np.random.randint(len(possibles))]
                return path
        possibles = self.graph.get_neighbours(path.countries[-2])
        path.countries[-1] = possibles[np.random.randint(len(possibles))]
        return path



    def can_be_mixed(self, path1, path2):
        for i in path1.countries[1:-1]:
            if i in path2.countries[1:-1]:
                return True
        return False


# graf = Graph.get_graph()
# start_day = date(2020, 4, 24)
# algorytm = EvolutionaryAlgorithm(graf, start_day, 100, 150, 0.5, 'best', 50, 'deaths')
# najlepszy = algorytm.find_path()
#
# print(najlepszy.countries)
# print(najlepszy.score)