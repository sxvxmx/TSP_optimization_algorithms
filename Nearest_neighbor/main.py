import networkx as nx
import GUI

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
        if len(visited) == graph.nodes():
            break
    if len(s) == graph.number_of_nodes()+1:
        return s
    else:
        return None
    
def fnei(graph:nx.Graph):
    minlen = float('inf')
    minway = []
    for node in graph.nodes():
        waylen = 0
        way = nearn(graph,node)
        s = node
        for n in way:
            if n != s:
                waylen += graph[n][s]["weight"]
                s = n
        if minlen > waylen:
            minlen = waylen
            minway = way
    return (minway,minlen)



if __name__ == '__main__':
    w = GUI.Window(fnei, 0)
    w.run()