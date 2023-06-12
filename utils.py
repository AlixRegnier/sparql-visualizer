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