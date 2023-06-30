from __future__ import annotations
import networkx as nx
from networkx.algorithms.isomorphism import *
from typing import List, Dict
from itertools import permutations, product, filterfalse, chain
from functools import reduce

class NodeEdgeDict:
    """
    Class that stores in and out arcs labels for each vertices and vertice that can be found by following arcs
    """
    def __init__(self, g : nx.DiGraph):
        #verticeId -> in/out arcs
        self.inEdges = {}
        self.outEdges = {}

        for e in g.edges:
            #First init of dicts
            if e[0] not in self.inEdges:
                self.inEdges[e[0]] = dict()
            if e[1] not in self.outEdges:
                self.outEdges[e[1]] = dict()

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
    
    #Edges that are going to node n
    def getInEdges(self, n) -> dict:
        return self.inEdges[n] if n in self.inEdges else dict()
    
    #Edges that can be followed from node n
    def getOutEdges(self, n) -> dict:
        return self.outEdges[n] if n in self.outEdges else dict()

    def __str__(self) -> str:
        return f"InEdges: {self.inEdges}\n\nOutEdges: {self.outEdges}\n"
    
def unique_permutations(l1, l2):
    """
    Retourne l'arrangement des paires d'éléments entre l1 et l2
    Soit toutes les paires (a, b) avec a et b appartenant respectivement à l1 et l2
    """

    if len(l1) >= len(l2):
        for p in (tuple(zip(x, l2)) for x in permutations(l1, len(l2))):
            yield p[0]
    else:
        for p in (tuple(zip(l1, x)) for x in permutations(l2, len(l1))):
            yield p[0]

#WARNING: Doesn't remind the existing edge for have been used, all edges between any MCS will be kept
def search(g1 : nx.DiGraph, g2 : nx.DiGraph, g1dicts : NodeEdgeDict, g2dicts : NodeEdgeDict, n1, n2, visited1, visited2) -> List[Dict[str, str]]:
    """
    Recursive function of MCS algorithm
    """
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

def isSubdict(d1, d2):
    """
    Return True if d2 is a subdict of d1
    (True if overwriting d1's datas with d2's datas won't change values of d1)
    """
    return { **d1, **d2 } == d1

def MCS(g1 : nx.DiGraph, g2 : nx.DiGraph):
    """
    Retourne tout les MCS (plusieurs fois le même si le mapping diffère)
    """
    g1dicts = NodeEdgeDict(g1)
    g2dicts = NodeEdgeDict(g2)

    mcss = [] #list<dict<node1,node2>>
    for n1 in g1.nodes:
        for n2 in g2.nodes:
            s = search(g1, g2, g1dicts, g2dicts, n1, n2, set(), set())
            
            #Remove results that are a subset of a wider result
            for p in s:
                if len(p) > 2: #Module shall have at least 3 vertices
                    for d in mcss:
                        if isSubdict(d, p):
                            break
                    else: #If there weren't any subdict in previous loop then check list before adding new result
                        mcss = list(filterfalse(lambda e: isSubdict(p, e), mcss))
                        mcss.append(p)

    return mcss

def extractMapping(g1 : nx.DiGraph, g2 : nx.DiGraph, mapping : Dict[str, str]) -> nx.DiGraph:
    """
    Extract perfectly the mapping vertices (and arcs) specified between g1 and g2
    """

    g1dicts = NodeEdgeDict(g1)
    g2dicts = NodeEdgeDict(g2)
    _g1 = g1.subgraph(mapping.keys()).copy()
    remove = set() #to store wrong arcs

    for n1 in _g1.nodes:
        #Store wrong mapping arcs from result (in arcs)
        for diff in g1dicts.getInEdges(n1).keys() - g2dicts.getInEdges(mapping[n1]).keys():
            for x in g1dicts.getInEdges(n1)[diff]:
                remove.add((x, n1))
        
        #Store wrong mapping arcs from result (out arcs)
        for diff in g1dicts.getOutEdges(n1).keys() - g2dicts.getOutEdges(mapping[n1]).keys():
            for x in g1dicts.getOutEdges(n1)[diff]:
                remove.add((n1, x))
    
    _g1.remove_edges_from(remove) #Remove all arcs  
    return _g1
