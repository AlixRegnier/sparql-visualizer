import networkx as nx
from networkx.algorithms.isomorphism import *
import matplotlib.pyplot as plt
from graphviz import Digraph
from typing import List, Dict, Set, Callable
from math import factorial
#Citations
"""
#Kind of first approach
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

def dotGraph(g : nx.DiGraph, name, nodelabel = True, edgelabel = True, format = "png"):
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

    graph.render(cleanup=True)

def equality(e1, e2) -> bool:
    try:
        return e1["label"] == e2["label"]
    except KeyError:
        print("### Ohayou")
        return "label" not in e1 and "label" not in e2

class NodeEdgeDict:
    def __init__(self, g : nx.DiGraph):
        #Edge -> in/out nodes
        self.inNodes = {}
        self.outNodes = {}

        #Node -> in/out edges
        self.inEdges = {}
        self.outEdges = {}

        for e in g.edges:
            #First init of dicts
            if e["label"] not in self.inNodes:
                self.inNodes[e["label"]] = dict()
                self.outNodes[e["label"]] = dict()
            if e[0] not in self.inEdges:
                self.inEdges[e[0]] = dict()
            if e[1] not in self.outEdges:
                self.outEdges[e[1]] = dict()

            #InNodes
            if e[0] in self.inNodes[e["label"]]:
                self.inNodes[e["label"]][e[0]] += 1
            else:
                self.inNodes[e["label"]][e[0]] = 1

            #OutNodes
            if e[1] in self.outNodes[e["label"]]:
                self.outNodes[e["label"]][e[1]] += 1
            else:
                self.outNodes[e["label"]][e[1]] = 1

            #InEdges
            if e["label"] in self.inEdges[e[0]]:
                self.inEdges[e[0]][e["label"]] += 1
            else:
                self.inEdges[e[0]][e["label"]] = 1
            #OutEdges
            if e["label"] in self.outEdges[e[1]]:
                self.outEdges[e[1]][e["label"]] += 1
            else:
                self.outEdges[e[1]][e["label"]] = 1
            
    #Nodes that can follow a labelled rule
    def getInNodes(self, label) -> dict:
        return self.inNodes[label]

    #Nodes that can be reached by following 
    def getOutNodes(self, label) -> dict:
        return self.outNodes[label]
    
    #Edges that are going to node n
    def getInEdges(self, n) -> dict:
        return self.inEdges[n]
    
    #Edges that can be followed from node n
    def getOutEdges(self, n) -> dict:
        return self.outEdges[n]
    
#TODO: Implement a little function for getting MCS from g1 and g2
#WARNING: Doesn't remind the existing edge for have been used, all edges between any MCS will be kept
def search(g1 : nx.DiGraph, g2 : nx.DiGraph, g1dicts : NodeEdgeDict, g2dicts : NodeEdgeDict, n1, n2, visited = set()) -> List[Set]:
    if n1 in visited or n2 in visited:
        return []
    
    _in = g1dicts.getInEdges(n1) & g2dicts.getInEdges(n2)
    _out = g1dicts.getOutEdges(n1) & g2dicts.getOutEdges(n2)

    #No compatibility
    if len(_in) == 0 and len(_out) == 0:
        return []
    
    #Get how many possibilities there are
    x = 1
    for i in _in:
        n = max(g1dicts.getInEdges(n1)[i], g2dicts.getInEdges(n2)[i])
        k = min(g1dicts.getInEdges(n1)[i], g2dicts.getInEdges(n2)[i])
        x *= factorial(n)/factorial(n-k)

    for o in _out:
        n = max(g1dicts.getOutEdges(n1)[o], g2dicts.getOutEdges(n2)[o])
        k = min(g1dicts.getOutEdges(n1)[o], g2dicts.getOutEdges(n2)[o])
        x *= factorial(n)/factorial(n-k)

    print(x)

def MCS(g1 : nx.DiGraph, g2 : nx.DiGraph):
    g1dicts = NodeEdgeDict(g1)
    g2dicts = NodeEdgeDict(g2)
    
    mcss = {} #All MCS found, dict [int -> List<set<node>>], int as mcs length
    for n1 in g1.nodes:
        for n2 in g2.nodes:
            s = search(g1, g2, g1dicts, g2dicts, n1, n2)
            for p in s:
                if len(p) > 0 and len(p) in mcss and p not in mcss[len(p)]:
                    mcss[len(p)].append(p)
                else:
                    mcss[len(p)] = [p]
    print(mcss)
    return mcss
            
    
#Weird code
"""
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
"""
