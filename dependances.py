import networkx as nx
from networkx.algorithms.isomorphism import DiGraphMatcher
from module import Module
from utils import em
from os.path import basename
import pickle
import sys
import statistics

modules = []
QUERYINDEX = -1

#Load pickle files to retrieve modules/queries as graph
for i in range(1,len(sys.argv)):
    if "simple" in sys.argv[i]: #Marche mais moche, ça permet juste de différencier si c'est une requête ou un module
        QUERYINDEX = i
        break
    with open(sys.argv[i], "rb") as f:
        modules.append(pickle.load(f))
    
modules = sorted(modules, key=lambda e: e.getName())

def isXsubgraphOfY(x, y):
    """
    Return True if X is a subgraph of Y

    If a graph X is isomorphic with a subgraph Y' of Y then, we can consider X being a subgraph of Y
    """

    return DiGraphMatcher(y, x, edge_match=em).subgraph_is_isomorphic()

#Composition indirecte
subgraphs = [[] for _ in range(len(modules))]

#Composition directe
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

#Graphe de composition indirecte
compoindirect = nx.DiGraph()

#Graphe de composition directe
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

#Calcul min, max et médiane du nombre de sous-modules
m = sorted([len(k) for k in directSubgraph])
if len(m) > 0:
    print(f"Composition: Minimum={min(m)}, Mediane={statistics.median(m)}, Maximum={max(m)}")
else:
    print("Composition: empty")


s = set()

#On ajoute dans un ensemble toutes les requêtes qui ont servi à annoter toutes les feuilles
for m in feuilles:
    s |= m.getQueries().keys()

print("\nLes feuilles couvrent au plus:", len(s), "/", 777)

#On itère sur les requêtes
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

def inversedict(dictionnaire : dict):
    """
    Return dictionary with key-value pairs reversed
    Dict<K,V> => Dict<V,K>
    """
    return { dictionnaire[k] : k for k in dictionnaire}

#Save module-module mapping (how to connect them)
for i in range(len(modules)):
    # j starting at i+1 will avoid checking self-module mapping but this check can be interesting for modules that maps itself not totally
    # to check self mapping, j should start to i in next line
    for j in range(i+1, len(modules)):
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

#Graphe d'association
association = nx.Graph()

#Graphe d'association des modules en enlevant les associations avec des modules interdépendants
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

