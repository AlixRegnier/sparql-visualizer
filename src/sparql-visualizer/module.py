from __future__ import annotations
import networkx as nx
from typing import Dict, Set, List

class Module:
    """
    Class that represents a module (a subgraph of a query that may have a real meaning)
    """
    def __init__(self, graph : nx.DiGraph, n : int):
        self.graph = graph.copy()
        self.n = n
        self.name = ""
        self.tags = set()
        self.alltags = set()
        self.queries = dict()
        self.associations = dict()
        self.mappingModules = dict()
    
    def getGraph(self) -> nx.DiGraph:
        return self.graph

    def getName(self) -> str:
        return self.name
    
    def getOccurence(self) -> int:
        return self.n
    
    def increaseOccurence(self):
        self.n += 1

    def addAssociation(self, query : str, a:  Dict[str, str]):
        if query not in self.associations:
            self.associations[query] = [a.copy()]
        elif a not in self.associations[query]:
            self.associations[query].append(a.copy())

    def getAlltags(self) -> Set[str]:
        return self.alltags
    
    def getTags(self) -> Set[str]:
        return self.tags
    
    def getQueries(self) -> Dict[str, int]:
        return self.queries
    
    def setName(self, name):
        self.name = name

    def addMappingModule(self, moduleName, mapping : dict):
        if moduleName in self.mappingModules:
            if mapping not in self.mappingModules[moduleName]:
                self.mappingModules[moduleName].append(mapping)
        else:
            self.mappingModules[moduleName] = [mapping]
        
    def getMappingModules(self) -> Dict[str, List[Dict]]:
        return self.mappingModules

    def addTags(self, tags):
        if len(self.tags) == 0:
            self.tags = set(tags)
        else:
            self.tags &= tags

        self.alltags |= tags

    def addQuery(self, query, mapping): # [OccurenceInQuery, List<Set>]
        if query in self.queries:
            self.queries[query][0] += 1
            if mapping not in self.queries[query][1]:
                self.queries[query][1].append(mapping)
        else:
            self.queries[query] = [1, [mapping]]

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
    
    def __str__(self) -> str:
        s = f"Nombre d'occurrences:\n{self.getOccurence()}\n\nCommon tags:\n"

        if self.getTags():
            s += '\n'.join(sorted(self.getTags()))
        else:
            s += "NONE"
        s += "\n\nAll tags:\n"
        s += '\n'.join(sorted(self.getAlltags()))
        s += "\n\nQueries:\n"
        for k in sorted(self.queries.keys()):
            s += f"{k}\t{self.queries[k][0]}\n"
    
        return s