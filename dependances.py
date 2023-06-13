import networkx as nx
from networkx.algorithms.isomorphism import DiGraphMatcher
from MCS import Module
from os.path import basename
import pickle
import sys

modules = []
QUERYINDEX = -1
for i in range(1,len(sys.argv)):
    if "simple" in sys.argv[i]:
        QUERYINDEX = i
        break
    with open(sys.argv[i], "rb") as f:
        modules.append(pickle.load(f))


def em(e1, e2) -> bool:
    try:
        return e1["label"] == e2["label"]
    except KeyError:
        return "label" not in e1 and "label" not in e2
    
modules = sorted(modules, key=lambda e: e.getName()) #Safer way to retrieve modules order than reverse sorting by occurrencies

def isXsubgraphOfY(x, y):
    return DiGraphMatcher(y, x, edge_match=em).subgraph_is_isomorphic()

subgraphs = [[] for _ in range(len(modules))]

nbSousmodules = [[] for _ in range(len(modules))]
MAX = len(modules) * len(modules)
x = 0
print("Calcul de la composition:")
for i in range(len(modules)):
    for j in range(len(modules)):
        if i != j:
            if isXsubgraphOfY(modules[i].getGraph(), modules[j].getGraph()):
                nbSousmodules[j].append(f"module{i+1:03}")
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
        x += 1
        print(f"\r{x} / {MAX}", end="")


###############Plus grand module###############
maxIndex = []
maxLength = 0
for i in range(len(nbSousmodules)):
    if len(nbSousmodules[i]) > maxLength:
        maxLength = len(nbSousmodules[i])
        maxIndex = [i]
    elif len(nbSousmodules[i]) == maxLength:
        maxIndex.append(i)

for i in maxIndex:
    print(f"\nmodule{i+1:03}:", nbSousmodules[i], end="")
###############################################

with open("dependances.txt", "w") as f:
    f.write("Submodules of moduleXXX:\n\n")
    for i in range(len(subgraphs)):
        f.write(f"\nmodule{i+1:03}: ")
        for k in subgraphs[i]:
            f.write(f"module{k+1:03} ")

"""
with open("module-query.txt", "w") as ff:
    for i in range(len(modules)):
        ff.write(f"\nmodule{i+1:03}: ")
        for q in modules[i].getQueries():
            ff.write(q + " ")
"""

graphcompo = nx.DiGraph()
feuilles = []
with open("feuilles.txt", "w") as f:
    for i in range(len(subgraphs)):
        graphcompo.add_node(i+1, label=f"module{i+1:03}")
        if len(subgraphs[i]) == 0: #Feuille
            f.write(f"module{i+1:03}\n")
            feuilles.append(modules[i])
        for j in subgraphs[i]:
            graphcompo.add_edge(j+1, i+1)
nx.write_gexf(graphcompo, "dependances.gexf")

s = set()

for m in feuilles:
    s |= m.getQueries().keys()

print("\nLes feuilles couvrent au plus:", len(s), "/", 777)

if QUERYINDEX > 0:
    queries = {}
    for i in range(QUERYINDEX, len(sys.argv)):
        with open(sys.argv[i], "rb") as f:
            queries[basename(sys.argv[i]).rstrip("rq.simple.dat")] = pickle.load(f)
    print("Requêtes non couvertes:", queries.keys() - s)

    print("Vérification des requêtes dans lesquelles les modules sont inclus")

    MAX = len(queries) * len(modules)
    print()
    i = 0
    j = 0
    for q in queries:
        for m in modules:
            if q not in m.getQueries() and isXsubgraphOfY(m.getGraph(), queries[q]):
                for mapping in DiGraphMatcher(queries[q], m.getGraph(), edge_match=em).subgraph_isomorphisms_iter():
                    m.addQuery(q, { mapping[k] : k for k in mapping })
                j += 1
            i += 1
            print(f"\r{i} / {MAX}", end="")

    s = set()

    for m in feuilles:
        s |= m.getQueries().keys()

    print("\nLes feuilles avec vérification sur toutes les requêtes couvrent au plus:", len(s), "/", 777)
    print(f"{j} ajouts d'appartenance à une requête")
    print("Requêtes non couvertes:", queries.keys() - s)


setfeuilles = { f.getName() for f in feuilles }
s = input("query:")
while s != "":
    r = set()
    for m in modules:
        if s in m.getQueries():
            r.add(m.getName())

    print("Modules:")
    print(r)
    print("Feuilles:")
    print(r & setfeuilles)
    s = input("\nquery:")


"""
for i in range(len(modules)):
    for j in range(i+1, len(modules)):
        for query in modules[i].getQueries().keys() & modules[j].getQueries.keys():
            #CALCULATE WHERE EACH MODULES OVERLAP ON <QUERY>
            #THEN INTERSECTION OF OVERLAPS IS THE WAY HOW TO CONNECT BOTH MODULES TO EACH OTHER
"""