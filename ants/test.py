import networkx as nx
from matplotlib import pyplot as plt
import random
import math

def nearn(graph:nx.Graph, point):
    s = [point]
    visited = set([point])
    while len(s) < graph.number_of_nodes()+1 and s:
        sor = sorted(graph[s[-1]].items(), key=lambda q: list(q[-1].items())[-1])
        for nei in sor:
            if nei[0] not in visited:
                s.append(nei[0])
                visited.add(nei[0])
                break
            if nei[0] == point and len(s) == graph.number_of_nodes():
                    s.append(nei[0])
    if len(s) == graph.number_of_nodes()+1:
        return(s)
    else:
        return None

def fnei(graph:nx.Graph):
    waylen = 0
    minlen = float('inf')
    minway = []
    for node in graph.nodes():
        way = nearn(graph,node)
        for n in way:
            if n != node:
                waylen += graph[node][n]["weight"]
        if minlen > waylen:
            minlen = waylen
            minway = way
    return (minway,minlen)

def ant(graph:nx.Graph, psize:int, node:tuple, pherom):
    ants = []
    pgraph = graph.copy()
    for i in range(psize):
        ants.append([set(),0])
        findway(graph, pgraph , ants[-1], node)
        s = node
        for n in ants[-1][0]:
            if n != s:
                pgraph[n][s]["weight"] += pherom/ants[-1][1]
                s = n
    return sorted(ants[0][0])
    


def findway(graph:nx.Graph, pgraph:nx.Graph, ant, node):
    s = [node]
    visited = set([node])
    while len(s) < graph.number_of_nodes() and s:
        sm = 0
        for nei in graph[s[-1]].items():
            if nei[0] not in visited:
                sm += pgraph[s[-1]][nei[0]]["weight"]+nei[1]["weight"]
        c = random.uniform(0,1)
        p = 0
        for nei in graph[s[-1]].items():
            if nei[0] not in visited:
                p += pgraph[s[-1]][nei[0]]["weight"]+nei[1]["weight"]
                if c <= p/sm:
                    s.append(nei[0])
                    visited.add(nei[0])
                    ant[1] += nei[1]["weight"]
                    break
    if len(s) == graph.number_of_nodes():
        ant[0] = s
    else:
        ant[0] = None

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
    if target(graph, tway) >= target(graph, way):
        return way
    else:
        if  random.uniform(0,1) >= math.exp((target(graph,way)-target(graph,tway))/temp):
            return tway
        return way

def annealing(graph:nx.Graph, temp, iter):
    way = list(graph.nodes())
    for i in range(iter):
        way = uway(graph, way, temp)
        temp *= 0.99
    way.append(way[0])    
    return way

if __name__ == '__main__':
    g = nx.Graph()
    g.add_nodes_from([0,1,2,3,4,5])
    g.add_weighted_edges_from([(0,1,10),(0,2,30),(0,3,30),(0,4,5),(0,5,1),(1,2,3),(1,3,6),(1,4,3),(1,5,3),(2,3,1),(2,4,9),(2,5,1),(3,4,1),(3,5,2),(4,5,1)])
    nx.draw_networkx(g)
    plt.show()
    
    print(annealing(g,1,50))