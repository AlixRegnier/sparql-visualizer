from typing import Set
import networkx as nx
from graphviz import Digraph
import matplotlib.pyplot as plt

def get_tags(filename) -> Set[str]:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            tags = set()
            for line in f:
                if line.startswith("#tags:"):
                    tags |= set(map(lambda s : s.strip().replace(' ', '_'), line[len("#tags:"):-1].split(',')))
                    break
            return tags - {""}
    except IOError:
        print(f"FAILED: {filename}")

def drawGraph(g : nx.DiGraph):
    nx.draw(g, pos = nx.spring_layout(g, k = 0.5), with_labels = True, labels = { n : g.nodes[n]["label"] for n in g.nodes })
    plt.show()

def dotGraph(g : nx.DiGraph, name, nodelabel = True, edgelabel = True, format = "png", cleanup=False):
    graph = Digraph(name)
    graph.format = format

    graph.graph_attr["rankdir"] = "LR"
    for node in g.nodes:
        if nodelabel:
            graph.node(hex(hash(node)), label=g.nodes[node]["label"])
        else:
            graph.node(hex(hash(node)), label="")

    for edge in g.edges:
        if edgelabel:
            graph.edge(hex(hash(edge[0])), hex(hash(edge[1])), label=g.edges[edge]["label"])
        else:   
            graph.edge(hex(hash(edge[0])), hex(hash(edge[1])))

    graph.render(cleanup=cleanup)

def em(e1, e2) -> bool:
    """
        An arc matches another arc if they have the same label XOR both have no label
    """
    try:
        return e1["label"] == e2["label"]
    except KeyError:
        return "label" not in e1 and "label" not in e2
    
def getRelationGraph(graph : nx.DiGraph):
    """
    Returns a simplified line graph of input graph
    """

    g = nx.line_graph(graph)

    for edge in graph.edges:
        if "label" in graph.edges[edge]:
            if graph.edges[edge]["label"] in ("VALUE", "TYPE", "AS", "") and "_duplicate" not in edge[1]:
                g.remove_node(edge)
            else:
                g.nodes[edge]["label"] = graph.edges[edge]["label"]
        else:
            g.remove_node(edge)
    return g

def getSimpleGraph(graph : nx.DiGraph):
    """
    Returns a simplified graph of input graph (filter some arcs like "VALUE", "TYPE", "AS", ...)
    """
    
    g = graph.copy()
    for edge in graph.edges:
        if edge in g.edges:
            if "label" in g.edges[edge]:
                if edge[1] in g.nodes and g.edges[edge]["label"] in ("VALUE", "TYPE", "AS", "") and "_duplicate" not in edge[1]:
                    g.remove_node(edge[1])
            else:
                g.remove_node(edge[1])
    g.remove_nodes_from(set(nx.isolates(g)))

    #Remove all labels as they aren't taken into account on MCS process
    for node in g.nodes:
        g.nodes[node]["label"] = ""

    return g
    