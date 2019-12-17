import math
from copy import deepcopy

class Vertex(object):
    def __init__(self):
        self.edges = dict()
        self.revedges = dict()
        self.required = 0
        self.rxn_produced = 0

    def add_edge(self, vname, cost):
        self.edges[vname] = cost

    def add_back_edge(self, vname, prod):
        self.revedges[vname] = prod

    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return 'Vertex(r='+str(self.required)+', p='+str(self.rxn_produced)+', e='+str(self.edges)+', re='+str(self.revedges)+')'

def read_data(filename):
    with open(filename, "r") as f:
        lines = [x.strip() for x in f.readlines()]
    graph = {}
    for line in lines:
        reactants, product = line.split(' => ')
        p, pname = product.split(" ")
        if pname not in graph:
            vertex = Vertex()
            vertex.rxn_produced = int(p)
            graph[pname] = vertex
        else:
            graph[pname].rxn_produced = int(p)

        for reactant in reactants.split(", "):
            r, rname = reactant.split(" ")
            if rname not in graph:
                reactVert = Vertex()
                graph[rname] = reactVert
            graph[pname].add_edge(rname, int(r))
            graph[rname].add_back_edge(pname, int(r))
    graph['FUEL'].required = 1
    graph['ORE'].rxn_produced = 1
    return graph

def get_topological_order(graph, startname):
    topo_order = []
    visited = set()

    def toposort(vertex, name):
        if not vertex.edges: # the vertex has no outgoing edges
            topo_order.append(name)
            return
        for childname in vertex.edges:
            if childname in visited:
                continue
            visited.add(childname)
            toposort(graph[childname], childname)
        topo_order.append(name)
    
    toposort(graph[startname], startname)
    return topo_order

def part1(graph):
    order = get_topological_order(graph, "FUEL")
    order.reverse()
    for name in order:
        vertex = graph[name]
        if vertex.rxn_produced == 0:
            print(name + str(vertex))
        its = max(1, math.ceil(vertex.required / vertex.rxn_produced))
        for reactant_name, cost in vertex.edges.items():
            graph[reactant_name].required += its*cost
    return graph["ORE"].required

def part2(graph):
    #binary search for how many that can be produced using part1
    best = 0
    ores = 1000000000000
    high = 1000000000000
    low = 1
    while low <= high:
        guess = (low+high) // 2
        graph["FUEL"].required = guess
        needed_ores = part1(deepcopy(graph))
        print(f"need {needed_ores}: ", end="")
        if needed_ores < ores:
            best = max(best, guess)
            low = guess + 1
            print(f"new low: {low}")
        elif needed_ores > ores:
            high = guess - 1
            print(f"new high: {high}")
        else:
            return guess
    return best


if __name__ == '__main__':
    filename = "input14.txt"
    graph = read_data(filename)
    print(part1(deepcopy(graph)))
    print(part2(deepcopy(graph)))


