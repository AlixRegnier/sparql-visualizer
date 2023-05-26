from __future__ import annotations
import networkx as nx
from networkx.algorithms.isomorphism import *
import matplotlib.pyplot as plt
from graphviz import Digraph
from typing import List, Dict, Set, Iterable
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
    return {**d1, **d2 } == d1

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

class Module:
    def __init__(self, graph : nx.DiGraph, n : int, tags : Set[str], queries : Iterable[str]):
        self.graph = graph.copy()
        self.n = n
        self.tags = set(tags)
        self.queries = set(queries)
    
    def getGraph(self) -> nx.DiGraph:
        return self.graph
    
    def getOccurrence(self) -> int:
        return self.n
    
    def increaseOccurrence(self):
        self.n += 1
    
    def getTags(self) -> Set[str]:
        return set(self.tags)
    
    def getQueries(self) -> Set[str]:
        return set(self.queries)
    
    def addTags(self, tags):
        if len(self.tags) == 0:
            self.tags = set(tags)
        else:
            self.tags &= tags

    def addQueries(self, *queries):
        self.queries |= set(queries)

    @staticmethod
    def __edgematch(e1, e2) -> bool:
        try:
            return e1["label"] == e2["label"]
        except KeyError:
            return "label" not in e1 and "label" not in e2
        
    def __eq__(self, o : Module | nx.DiGraph ) -> bool:
        if isinstance(o, Module):
            return nx.is_isomorphic(self.graph, o.graph, edge_match=Module.__edgematch)
        return nx.is_isomorphic(self.graph, o, edge_match=Module.__edgematch)

    

