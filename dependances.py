import networkx as nx
from networkx.algorithms.isomorphism import DiGraphMatcher
from MCS import Module
import pickle
import sys

modules = []
for file in sys.argv[1:]:
    with open(file, "rb") as f:
        modules.append(pickle.load(f))


def em(e1, e2) -> bool:
    try:
        return e1["label"] == e2["label"]
    except KeyError:
        return "label" not in e1 and "label" not in e2
    
modules = sorted(modules, key=lambda e: e.getOccurrence(), reverse=True)

def isXsubgraphOfY(x, y):
    return DiGraphMatcher(y, x, edge_match=em).subgraph_is_isomorphic()

print("moduleX is subgraph of moduleY")
subgraphs = [[] for _ in range(len(modules))]

for i in range(len(modules)):
    for j in range(len(modules)):
        if i != j:
            if isXsubgraphOfY(modules[i].getGraph(), modules[j].getGraph()):
                print(f"module{i+1:03}\tmodule{j+1:03}")
                rm = []
                for k in subgraphs[j]:
                    if isXsubgraphOfY(modules[i].getGraph(), modules[k].getGraph()):
                        break
                    elif isXsubgraphOfY(modules[k].getGraph(), modules[i].getGraph()):
                        rm.append(k)
                else:
                    subgraphs[j].append(i)

                for k in rm:
                    subgraphs[j].remove(k)

with open("dependances.txt", "w") as f:
    f.write("Submodules of moduleXXX:\n\n")
    for i in range(len(subgraphs)):
        f.write(f"\nmodule{i+1:03}: ")
        for k in subgraphs[i]:
            f.write(f"module{k+1:03} ")

graphcompo = nx.DiGraph()
with open("feuilles.txt", "w") as f:
    for i in range(len(subgraphs)):
        graphcompo.add_node(i+1, label=f"module{i+1:03}")
        if len(subgraphs[i]) == 0: #Feuille
            f.write(f"module{i+1:03}\n")
        for j in subgraphs[i]:
            graphcompo.add_edge(j+1, i+1)
nx.write_gexf(graphcompo, "composition.gexf")

s = input("modules:")
while s != "":
    s = list(map(lambda e: int(e)-1, s.split()))
    queries = set(modules[s[0]].getQueries().keys())
    for m in s[1:]:
        queries &= modules[m].getQueries().keys()
    print(queries)
    s = input("modules:")




