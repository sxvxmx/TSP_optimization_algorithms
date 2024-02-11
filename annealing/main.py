import Gui
import networkx as nx
import random
import math


def target(graph:nx.Graph,way) -> int:
    s = 0
    node = None
    for i in way:
        if node != None:
            s += graph[i][node]["weight"]
        node = i
    return s

def uway(graph:nx.Graph ,way:list, temp):
    a = random.randint(0,len(way)-1)
    b = random.randint(0,len(way)-1)
    tway = way.copy()
    q = tway[a]
    tway[a] = tway[b]
    tway[b] = q
    if target(graph, tway) <= target(graph, way):
        return tway
    else:
        if  random.uniform(0,1) >= math.exp((target(graph, way)-target(graph, tway))/temp):
            print(target(graph, way),temp)
            return tway
        return way

def annealing(graph:nx.Graph, temp, iter):
    way = list(graph.nodes())
    for i in range(iter):
        way = uway(graph, way, temp)
        temp *= 0.99
    way.append(way[0])    
    return way, target(graph, way)


if __name__ == '__main__':
    w = Gui.Window(annealing)
    w.run()