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
directSubgraph = [[] for _ in range(len(modules))]
MAX = len(modules) * len(modules)
x = 0
print("Calcul de la composition:")
for i in range(len(modules)):
    for j in range(len(modules)):
        if i != j:
            if isXsubgraphOfY(modules[i].getGraph(), modules[j].getGraph()):

                directSubgraph[j].append(i)
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

#Write module indirect composition
with open("compositionIndirect.txt", "w") as f:
    for i in range(len(subgraphs)):
        f.write(f"\nmodule{i+1:03}: ")
        for k in subgraphs[i]:
            f.write(f"module{k+1:03} ")


#Write module direct composition
with open("compositionDirect.txt", "w") as f:
    for i in range(len(directSubgraph)):
        f.write(f"\nmodule{i+1:03}: ")
        for k in directSubgraph[i]:
            f.write(f"module{k+1:03} ")

#Write module -> queries entries
with open("module-query.txt", "w") as ff:
    for i in range(len(modules)):
        ff.write(f"\nmodule{i+1:03}: ")
        for q in modules[i].getQueries():
            ff.write(q + " ")

compoindirect = nx.DiGraph()
compodirect = nx.DiGraph()
feuilles = []
with open("feuilles.txt", "w") as f:
    for i in range(len(subgraphs)):
        compoindirect.add_node(f"module{i+1:03}")
        if len(subgraphs[i]) == 0: #Feuille
            f.write(f"module{i+1:03}\n")
            feuilles.append(modules[i])
        for j in subgraphs[i]:
            compoindirect.add_edge(f"module{j+1:03}", f"module{i+1:03}")

for i in range(len(directSubgraph)):
    compodirect.add_node(f"module{i+1:03}")
    for j in directSubgraph[i]:
        compodirect.add_edge(f"module{j+1:03}", f"module{i+1:03}")

nx.write_gexf(compoindirect, "compositionIndirect.gexf")
nx.write_gexf(compodirect, "compositionDirect.gexf")

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

    print("\nRevérification des requêtes dans lesquelles les modules sont inclus")

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

"""
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

def inversedict(dictionnaire : dict):
    return { dictionnaire[k] : k for k in dictionnaire}

#Save module mapping (how to connect them)
for i in range(len(modules)):
    for j in range(i+1, len(modules)): #i+1 won't check self-mapping /!\
        for query in modules[i].getQueries().keys() & modules[j].getQueries().keys():
            for mappingi in modules[i].getQueries()[query][1]:
                for mappingj in modules[j].getQueries()[query][1]:
                    #Query nodes as key
                    di = inversedict(mappingi)
                    dj = inversedict(mappingj)
                    intersection = di.keys() & dj.keys()
                    if intersection:
                        modules[i].addMappingModule(f"module{j+1:03}", { di[k] : dj[k] for k in intersection})
                        modules[j].addMappingModule(f"module{i+1:03}", { dj[k] : di[k] for k in intersection})

association = nx.Graph()
associationFiltered = nx.Graph()
for i in range(len(modules)):
    association.add_node(f"module{i+1:03}")
    associationFiltered.add_node(f"module{i+1:03}")
    for modulej in modules[i].getMappingModules().keys():
        if (f"module{i+1:03}", modulej) not in compodirect.edges and (modulej, f"module{i+1:03}") not in compodirect.edges:
            associationFiltered.add_edge(f"module{i+1:03}", modulej)
        association.add_edge(f"module{i+1:03}", modulej)

nx.write_gexf(association, "association.gexf")
nx.write_gexf(associationFiltered, "associationFiltered.gexf")
print("Modules qui ne mappent aucun autre module (normal):\n", list(nx.isolates(association)))
print("Modules qui ne mappent aucun autre module (filtered):\n", list(nx.isolates(associationFiltered)))


            