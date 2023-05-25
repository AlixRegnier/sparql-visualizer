import networkx as nx
from networkx.algorithms.isomorphism import *
import matplotlib.pyplot as plt
from graphviz import Digraph
from typing import List, Dict
from itertools import permutations, product, filterfalse, chain
from functools import reduce

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
            if g.edges[e]["label"] not in self.inNodes:
                self.inNodes[g.edges[e]["label"]] = dict()
                self.outNodes[g.edges[e]["label"]] = dict()
            if e[0] not in self.inEdges:
                self.inEdges[e[0]] = dict()
            if e[1] not in self.outEdges:
                self.outEdges[e[1]] = dict()

            #InNodes
            if e[0] in self.inNodes[g.edges[e]["label"]]:
                self.inNodes[g.edges[e]["label"]][e[0]].append(e[1])
            else:
                self.inNodes[g.edges[e]["label"]][e[0]] = [e[1]]

            #OutNodes
            if e[1] in self.outNodes[g.edges[e]["label"]]:
                self.outNodes[g.edges[e]["label"]][e[1]].append(e[0])
            else:
                self.outNodes[g.edges[e]["label"]][e[1]] = [e[0]]

            #InEdges
            if g.edges[e]["label"] in self.inEdges[e[0]]:
                self.inEdges[e[0]][g.edges[e]["label"]].append(e[1])
            else:
                self.inEdges[e[0]][g.edges[e]["label"]] = [e[1]]

            #OutEdges
            if g.edges[e]["label"] in self.outEdges[e[1]]:
                self.outEdges[e[1]][g.edges[e]["label"]].append(e[0])
            else:
                self.outEdges[e[1]][g.edges[e]["label"]] = [e[0]]
            
    #Nodes that can follow a labelled rule
    def getInNodes(self, label) -> dict:
        return self.inNodes[label] if label in self.inNodes else dict()

    #Nodes that can be reached by following 
    def getOutNodes(self, label) -> dict:
        return self.outNodes[label] if label in self.outNodes else dict()
    
    #Edges that are going to node n
    def getInEdges(self, n) -> dict:
        return self.inEdges[n] if n in self.inEdges else dict()
    
    #Edges that can be followed from node n
    def getOutEdges(self, n) -> dict:
        return self.outEdges[n] if n in self.outEdges else dict()

    def __str__(self) -> str:
        return f"InNodes: {self.inNodes}\n\nOutNodes: {self.outNodes}\n\nInEdges: {self.inEdges}\n\nOutEdges: {self.outEdges}\n"
    
def unique_permutations(l1, l2):
    if len(l1) >= len(l2):
        for p in (tuple(zip(x, l2)) for x in permutations(l1, len(l2))):
            yield p[0]
    else:
        for p in (tuple(zip(l1, x)) for x in permutations(l2, len(l1))):
            yield p[0]

#WARNING: Doesn't remind the existing edge for have been used, all edges between any MCS will be kept
def search(g1 : nx.DiGraph, g2 : nx.DiGraph, g1dicts : NodeEdgeDict, g2dicts : NodeEdgeDict, n1, n2, visited1, visited2) -> List[Dict[str, str]]:
    if n1 in visited1 or n2 in visited2:
        return []
    
    visited1.add(n1)
    visited2.add(n2)

    _in = g1dicts.getInEdges(n1).keys() & g2dicts.getInEdges(n2).keys()
    _out = g1dicts.getOutEdges(n1).keys() & g2dicts.getOutEdges(n2).keys()

    #No compatibility => Nodes cannot be parallely reached 
    if len(_in) == 0 and len(_out) == 0:
        return []

    x = [{n1:n2}]
    #For each matches from outcoming edges make a recursive call for each possibilities, a list of dicts by match
    for i in _in:
        _x = tuple(chain.from_iterable(search(g1, g2, g1dicts, g2dicts, a, b, visited1.copy(), visited2.copy()) for (a, b) in unique_permutations(g1dicts.getInEdges(n1)[i], g2dicts.getInEdges(n2)[i])))
        if _x:
            x = [reduce(lambda a, b: {**a, **b}, e) for e in product(x, _x)] #Foreach list, merge their dictionaries

    for o in _out:
        _x = tuple(chain.from_iterable(search(g1, g2, g1dicts, g2dicts, a, b, visited1.copy(), visited2.copy()) for (a, b) in unique_permutations(g1dicts.getOutEdges(n1)[o], g2dicts.getOutEdges(n2)[o])))
        if _x:
            x = [reduce(lambda a, b: {**a, **b}, e) for e in product(x, _x)] #Foreach list, merge their dictionaries
    return x

#Check if d2 is a subdict of d1
def isSubdict(d1, d2):
    if d1 | d2 == d1:
        return True
    return False

def MCS(g1 : nx.DiGraph, g2 : nx.DiGraph):
    g1dicts = NodeEdgeDict(g1)
    g2dicts = NodeEdgeDict(g2)

    mcss = [] #list<dict<node1,node2>>
    for n1 in g1.nodes:
        for n2 in g2.nodes:
            s = search(g1, g2, g1dicts, g2dicts, n1, n2, set(), set())
            #Filter results if subset of a wider solution
            #Filter previous results
            for p in s:
                if len(p) > 2:
                    for d in mcss:
                        if isSubdict(d, p):
                            break
                    else:
                        mcss = list(filterfalse(lambda e: isSubdict(p, e), mcss))
                        mcss.append(p)
    """
    if len(mcss) == 0:
        print("No isomorphisms found")
    else:
        print(f"{len(mcss)} isomorphisms found")
    """
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
