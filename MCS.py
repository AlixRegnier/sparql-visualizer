import networkx as nx
from networkx.algorithms.isomorphism import *
import matplotlib.pyplot as plt
from graphviz import Digraph
from typing import List, Dict

#Citations
"""
#Good approach
G. Levi, A note on the derivation of maximal common subgraphs of two directed or undirected graphs, CALCOLO 9 (1973) 341–352. 

#Clique
McCreesh, C., Ndiaye, S.N., Prosser, P., Solnon, C. (2016). Clique and Constraint Models for Maximum Common (Connected) Subgraph Problems. In: Rueher, M. (eds) Principles and Practice of Constraint Programming. CP 2016. Lecture Notes in Computer Science(), vol 9892. Springer, Cham. https://doi.org/10.1007/978-3-319-44953-1_23

#McSplit
McCreesh, Ciaran & Prosser, Patrick & Trimble, James. (2017). A Partitioning Algorithm for Maximum Common Subgraph Problems. 712-719. 10.24963/ijcai.2017/99. 
"""

#
#VF2
#https://networkx.org/documentation/stable/reference/algorithms/isomorphism.vf2.html
#https://doi.org/10.1016/j.dam.2018.02.018
"""
vf2pp_is_isomorphic(G1, G2, node_label = "label")
    Boolean if G1 and G2 are isomorphic /!\ not subgraph isomorphisms /!\

vf2pp_all_isomorphisms(G1, G2, node_label = "label")
    Yields all the possible mappings between G1 and G2 (all subgraphs isomorphisms)

vf2pp_isomorphism(G1, G2, node_label = "label")
    Return first isomorphisms found by vf2pp_all_isomorphisms()

"""

#ISMAGS
#https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.isomorphism.ISMAGS.html
#https://doi.org/10.1371/journal.pone.0097896

"""
find_isomorphisms()
    Find all subgraph isomorphisms between subgraph and graph

is_isomorphic()
    Returns True if graph is isomorphic to subgraph and False otherwise.

isomorphisms_iter()
    Does the same as find_isomorphisms() if graph and subgraph have the same number of nodes.

largest_common_subgraph()
    Find the largest common induced subgraphs between subgraph and graph.

subgraph_is_isomorphic()
    Returns True if a subgraph of graph is isomorphic to subgraph and False otherwise.
"""

def drawGraph(g : nx.DiGraph):
    nx.draw(g, pos = nx.spring_layout(g, k = 0.5), with_labels = True, labels = { n : g.nodes[n]["label"] for n in g.nodes })
    plt.show()

def dotGraph(g : nx.DiGraph, name, format = "png"):
    graph = Digraph(name)
    graph.format = format

    graph.graph_attr["rankdir"] = "LR"
    for node in g.nodes:
        graph.node(hex(hash(node)), label=g.nodes[node]["label"])
    for edge in g.edges:
        graph.edge(hex(hash(edge[0])), hex(hash(edge[1])))
    graph.render(cleanup=True)

def equality(n1, n2) -> bool:
        try:
            return n1["label"] == n2["label"]
        except KeyError:
            #print("WARNING: A node wasn't labelled !")
            return False
    
#TODO: Implement a little function for getting MCS from g1 and g2
def most_common_subgraph(g1 : nx.DiGraph, g2 : nx.DiGraph) -> Dict[nx.DiGraph]:
    pass

#Inputs must be NetworkX DiGraph
def MCS(g1 : nx.DiGraph, g2 : nx.DiGraph) -> List[nx.DiGraph]:
    matcher = ISMAGS(g1, g2, equality)
    matchs = []
    best = 2 #Need at least 2 nodes
    for iso in matcher.largest_common_subgraph():
        f = g1.copy().subgraph(iso.keys())
        subiso = f.subgraph(max(nx.weakly_connected_components(f), key=len))
        
        if subiso.number_of_nodes() > best:
            best = subiso.number_of_nodes()
            matchs = [subiso]
        elif subiso.number_of_nodes() == best:
            for i in range(len(matchs)):
                if set(matchs[i].nodes) == set(subiso.nodes):
                    break
            else:
                matchs.append(subiso)

    return matchs