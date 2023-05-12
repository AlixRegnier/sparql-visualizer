import networkx as nx
from networkx.algorithms.isomorphism import *
import sys

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



#Input must be GEXF files
def main(file1, file2):
    g1 = nx.read_gexf(file1)
    g2 = nx.read_gexf(file2)

    #Remove exclusives labels from graphs
    forbiddenLabels = set(nx.get_node_attributes(g1, "label").values()) ^ set(nx.get_node_attributes(g2, "label").values())
    g1.remove_nodes_from([n for n in g1.nodes if g1.nodes[n]["label"] in forbiddenLabels])
    g2.remove_nodes_from([n for n in g2.nodes if g2.nodes[n]["label"] in forbiddenLabels])

    def equality(n1, n2):
        try:
            return n1["label"] == n2["label"]
        except KeyError:
            print("WARNING: A node wasn't labelled !")
            return False
        
    matcher = DiGraphMatcher(g1, g2, node_match = equality)

    i = 0
    for iso in matcher.subgraph_isomorphisms_iter():
        i += 1
        f = g1.copy().remove_nodes_from(g1.nodes - iso.keys())
        nx.write_gexf(f, "result{i}.gexf")
    print(i)
    print("No isomorphisms found")



main(sys.argv[1], sys.argv[2])