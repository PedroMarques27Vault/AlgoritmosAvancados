from queue import PriorityQueue

from search_node import SearchNode


class GreedySearchTree:

        def __init__(self,graph):
            self.problem = graph
            self.achievable = {k: self.problem.actions(k) for k in self.problem.vert_coordinates}
            self.v_next = PriorityQueue()

            try:
                self.v_next.put([(self.heuristic(v), SearchNode(v, None)) for v in self.achievable if self.achievable[v] != []][0])
            except:
                pass

        def search(self):
            to_explore ={k:[x for x in v if self.achievable[x]!=[]] for k,v in self.achievable.items()}
            self.iterations = 0
            self.tim = 0
            while not self.v_next.empty():
                h,v = self.v_next.get()
                self.iterations+=1
                not_yet_explored = [x for x in to_explore[v.state] if x!=v.state ]
                if v.parent:
                    not_yet_explored = [x for x in not_yet_explored if x not in to_explore[v.initial]]

                for x in self.achievable[v.initial]+[v.initial]:
                    self.achievable[x]+=[f for f in not_yet_explored if f not in self.achievable[x]]
                    if v.state in to_explore[x]:
                        to_explore[x].remove(v.state)

                [self.v_next.put((self.heuristic(nv)+h, SearchNode(nv, v))) for nv in not_yet_explored]

                if to_explore[v.initial]==[]:
                    return v.initial, self.achievable[v.initial], sum([self.problem.cost(x) for x in self.achievable[v.initial]])

            return self.problem.vert_coordinates, self.achievable, 0

        def heuristic(self, vert):
            return -(len(self.achievable[vert]) + sum([self.problem.cost(x) for x in self.achievable[vert]]))

