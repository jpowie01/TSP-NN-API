import random
import math
import itertools
import sys


class Graph:
    def __init__(self, n):
        self.shortest_tsp = sys.float_info.max
        self.order_tsp = []
        self.order_tsp_list = []
        self.n = n
        self.graph = []
        for i in range(n):
            x = random.random()
            y = random.random()
            self.graph.append((x, y))
        self.each_to_each = [[0 for x in range(self.n)] for y in range(self.n)]
        self.compute_each_to_each()

    def compute_each_to_each(self):
        for i in range(self.n):
            for j in range(i, self.n):
                if i == j:
                    self.each_to_each[i][j] = 0
                else:
                    diff_x = self.graph[i][0] - self.graph[j][0]
                    diff_y = self.graph[i][1] - self.graph[j][1]
                    self.each_to_each[i][j] = self.each_to_each[j][i] = math.sqrt(diff_x * diff_x + diff_y * diff_y)

    def compute_tsp(self):
        elements = [i for i in range(self.n)]
        for permutation in itertools.permutations(elements):
            new_length = 0
            for i in range(self.n - 1):
                new_length += self.each_to_each[permutation[i]][permutation[i+1]]
            new_length += self.each_to_each[permutation[self.n - 1]][permutation[0]]
            if new_length < self.shortest_tsp:
                self.shortest_tsp = new_length
                self.order_tsp = permutation
        self.order_tsp_list = list(self.order_tsp)
        self.order_tsp = tuple(self.order_tsp_list)


def convert_output(output, N):
    # Prepare result
    result = []
    for i in range(N):
        result_tmp = []
        for t in range(N):
            result_tmp.append(0)
        result.append(result_tmp)

    # Default values
    tab = list(output)
    best_value = -100
    best_x = -1
    best_y = -1

    # Iteration through whole output
    for i in range(1, N*N + 1):
        for y in range(N):
            for x in range(N):
                if tab[N*y + x] > best_value:
                    best_value = tab[N*y + x]
                    best_x = x
                    best_y = y
        result[best_x][best_y] = i
        tab[N*best_y + best_x] = -100
        best_value = -100

    order = []
    for i in range(N*N+1):
        for x in range(N):
            best_y = None
            for y in range(N):
                if result[x][y] == i:
                    best_y = y
            if best_y is not None and best_y not in order:
                order.append(best_y)
    # MAYBE DFS THROUGH THE GENERATED TREE?
    return order
