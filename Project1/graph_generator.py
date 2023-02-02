import random
import json
import time

from greedy_search import GreedySearchTree
from search import BruteSearchTree

class Graph:
    def __init__(self):
        random.seed(92926)
        self.FILE_PATH = 'graphs/'
        self.MAX_COST = 100
        self.inc_matrix = []
        self.vert_coordinates = []
        self.weights = {}
        self.n_edges = 0

    def generate(self, n):
        self.n = n
        self.inc_matrix.clear()
        self.vert_coordinates.clear()
        self.weights.clear()
        self.graph_generator()
        self.generate_coordinates()
        self.generate_weights()
        self.write_to_file()

    def actions(self, state):
        if state not in self.vert_coordinates:
            return None
        if type(state) is tuple:
            state = self.vert_coordinates.index(state)

        return [self.vert_coordinates[one] for one in range(self.n) if self.inc_matrix[state][one] == 1]

    def cost(self, action):
        return self.weights[(action)]

    def load_graph_from_file(self, n):
        self.n = n
        file_path = f'{self.FILE_PATH}graph_{self.n}.txt'

        f = open(file_path, 'r')
        lines = f.readlines()
        self.inc_matrix = [[int(y) for y in x.split(':')] for x in lines[0].replace('\n', '').split('|')]
        self.n_edges = sum([sum(n) for n in self.inc_matrix])
        self.weights.clear()
        self.weights = {(int(_assoc.split(':')[0]), int(_assoc.split(':')[1])): int(_assoc.split(':')[2]) for _assoc in
                        lines[1].replace('\n', '').split('|') if len(_assoc) > 1}
        self.vert_coordinates = sorted(list(self.weights.keys()))
    def write_to_file(self):
        filename = f'{self.FILE_PATH}graph_{self.n}.txt'
        open(filename, 'w')
        output = open(filename, 'a+')

        _str_inc_arr = [':'.join(str(x) for x in row) for row in self.inc_matrix]
        output.write('|'.join(_str_inc_arr) + '\n')
        _str_weight_arr = [f'{_tuple[0]}:{_tuple[1]}:{self.weights[_tuple]}' for _tuple in self.vert_coordinates]
        output.write('|'.join(_str_weight_arr) + '\n')

    def generate_coordinates(self):
        coord_array = set()
        while len(coord_array) != self.n:
            _tuple = (random.randint(1, 9), random.randint(1, 9))
            coord_array.add(_tuple)
        self.vert_coordinates = sorted(coord_array)

    def generate_weights(self):
        self.weights.clear()

        for v in self.vert_coordinates:
            self.weights[v] = random.randint(1, self.MAX_COST)

    def graph_generator(self):
        self.inc_matrix.clear()
        while len(self.inc_matrix)!=self.n:
            gen_array = [random.randint(0,1) for _ in range(self.n)]
            gen_array[len(self.inc_matrix)]=0

            self.inc_matrix.append(gen_array)

    def print_graph(self):

        print('\t'.join(['Vert'] + [str(x) for x in self.vert_coordinates]))
        for i in range((len(self.vert_coordinates))):
            print(str(self.vert_coordinates[i]) + '\t\t' + '\t\t'.join([str(x) for x in self.inc_matrix[i]]))


if __name__ == "__main__":
    g = Graph()




    experiments = 10

    greedy_dat = {k:{v:0 for v in ['iterations','weight','no_vertices','time','n_edges']} for k in range(2,82)}

    brute_dat = {k:{v:0 for v in ['iterations','weight','no_vertices','time','n_edges']} for k in range(2,82)}
    for n in range(2,82):
        print(n)
        for i in range(experiments):
            g = Graph()
            g.generate(n)
            g.load_graph_from_file(n)


            _init2 = time.time()
            st2 = GreedySearchTree(g)
            results2 = st2.search()
            final2 = time.time() - _init2

            greedy_dat[n]['iterations'] += st2.iterations/experiments
            greedy_dat[n]['weight'] += results2[2]/experiments
            greedy_dat[n]['no_vertices'] += len(results2[1])/experiments
            greedy_dat[n]['time'] += final2/experiments
            greedy_dat[n]['n_edges'] += g.n_edges/experiments
            g.load_graph_from_file(n)

            _init = time.time()
            st = BruteSearchTree(g)
            results = st.search()
            final = time.time() - _init

            brute_dat[n]['iterations'] += st.iterations/experiments
            brute_dat[n]['weight'] += results[0][2]/experiments
            brute_dat[n]['no_vertices'] +=max([len(x[1]) for x in results])/experiments
            brute_dat[n]['time'] += final/experiments
            brute_dat[n]['n_edges'] += g.n_edges/experiments

    open('gr_results.csv', 'w')
    f = open('gr_results.csv', 'a+')
    f.write(f'n,iterations,weight,no_vertices,time,n_edges\n')
    for i in greedy_dat:
        f.write(
            f'{i},{greedy_dat[i]["iterations"]},{greedy_dat[i]["weight"]},{greedy_dat[i]["no_vertices"]},{greedy_dat[i]["time"]},{greedy_dat[i]["n_edges"]}\n')

    open('brt_results.csv', 'w')
    f = open('brt_results.csv', 'a+')
    f.write(f'n,iterations,weight,no_vertices,time,n_edges\n')
    for i in brute_dat:

        f.write(f'{i},{brute_dat[i]["iterations"]},{brute_dat[i]["weight"]},{brute_dat[i]["no_vertices"]},{brute_dat[i]["time"]},{brute_dat[i]["n_edges"]}\n')


    
