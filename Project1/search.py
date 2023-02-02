# – Find a maximum weighted closure for a given vertex-weighted directed graph G(V, E), with n
# vertices and m edges. A closure of G is a set of vertices C, such that no edges leave C. The weight
# of a closure is the sum of its vertices’ weights. A maximum weight closure is a closure whose total
# weight is as large as possible
import sys
import time
from queue import Queue, PriorityQueue

class BruteSearchTree:

    def __init__(self,graph):
        self.problem = graph

    # procurar a solucao
    def search(self):
        self.iterations = 0
        self.achievable = {k: self.problem.actions(k) for k in self.problem.vert_coordinates}

        for _v in self.problem.vert_coordinates:
            v_next = self.problem.actions(_v)
            while v_next != []:
                self.iterations += 1
                new_vertex = v_next.pop(0)
                new_achievable = [x for x  in self.achievable[new_vertex] if x not in self.achievable[_v]]
                self.achievable[_v]+=new_achievable
                _v = new_vertex
                v_next[:0] = new_achievable

        results = {k: sum([self.problem.cost(x) for x in self.achievable[k]]) for k in self.achievable}
        _max = max(results.values())

        return [(k,self.achievable[k],_max) for k in self.achievable if results[k]==_max ]