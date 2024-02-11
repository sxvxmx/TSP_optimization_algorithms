import Gui
import networkx as nx
import random

def ant(graph:nx.Graph, psize:int, node:tuple, pgraph, pherom, pheromcoef, update):
    ants = []
    for i in range(psize):
        ants.append([set(),0])
        findway(graph, pgraph , ants[-1], node, pheromcoef)
        update()
        s = node
        for n in ants[-1][0]:
            if n != s:
                pgraph[n][s]["weight"] += float(pherom)/ants[-1][1]
                s = n
    ants = sorted(ants,key=lambda q: q[1])
    return ants[0][0],ants[0][1]
    
def findway(graph:nx.Graph, pgraph:nx.Graph, ant, node, pheromcoef):
    s = [node]
    visited = set([node])
    while len(s) < graph.number_of_nodes()+1 and s:
        sm = 0
        for nei in graph[s[-1]].items():
            if nei[0] not in visited:
                sm += float(pheromcoef)*pgraph[s[-1]][nei[0]]["weight"]+nei[1]["weight"]
        c = random.uniform(0,1)
        p = 0
        for nei in graph[s[-1]].items():
            if nei[0] not in visited:
                p += float(pheromcoef)*pgraph[s[-1]][nei[0]]["weight"]+nei[1]["weight"]
                if c <= p/sm:
                    s.append(nei[0])
                    visited.add(nei[0])
                    ant[1] += nei[1]["weight"]
                    break
            if nei[0] == node and len(s) == graph.number_of_nodes():
                s.append(nei[0])
    if len(s) == graph.number_of_nodes()+1:
        ant[0] = s
    else:
        ant[0] = None


if __name__ == '__main__':
    w = Gui.Window(ant, 0)
    w.run()