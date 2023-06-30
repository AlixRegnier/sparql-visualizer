#Parser and graph renderers
from SAL import parse_file, SubDigraph, Cluster

#Most Common Subgraph
from MCS import MCS, extractMapping
from module import Module

from utils import dotGraph, get_tags, getSimpleGraph, getRelationGraph
import argparse
from networkx.algorithms.isomorphism import DiGraphMatcher
from pathlib import Path
from os.path import basename
import sys
import pickle

def process(files, render_query = True, render_simple = False, render_relation = False, render_output=None, verbose=False):
    """
    Return 2 dictionaries G, T

    G contains [query -> graph]
    T contains [query -> tags]

    Flags can be set from command line if you went to render some graphs in PNG or if you need to use parser in verbose mode
    """

    pfiles = dict()
    tfiles = dict()
    if render_output is not None:
        render_output = render_output.rstrip('/')

    for i in range(len(files)):
        try:
            #Parse file
            maincluster = parse_file(str(files[i]), verbose)

            #Determine output filename
            if render_output is None:
                name = str(files[i])
            else:
                name = f"{render_output}/{basename(files[i])}"
            
            #Retrieve parser results
            maincluster.generateGraph()
            if render_query:
                SubDigraph.allSubgraphsToDot(name) #TODO: Replace all static stuff by dynamic ones

            fullgraph = maincluster.getFullGraph()
            simplegraph = getSimpleGraph(fullgraph)
            with open(name + ".simple.dat", "wb") as f:
                pickle.dump(simplegraph, f)

            if render_simple:
                dotGraph(simplegraph, name + ".simple", nodelabel=False)

            if render_relation:
                dotGraph(getRelationGraph(fullgraph), name + ".relation", edgelabel=False)

            #Merge all subdigraphes and simplify it
            k = basename(files[i].stem)
            pfiles[k] = simplegraph
            tfiles[k] = get_tags(files[i])
            print(f"\r{i+1} / {len(files)}", end=' ')
        except Exception as e:
            print("\rFAILED:", files[i], end="\n\n")
            print(e, file=sys.stderr)
        finally:
            #Reset static values for next iteration
            SubDigraph.reset()
            Cluster.reset()
    return pfiles, tfiles


def main(flag_graph, flag_mcs, flag_relation, flag_simple, flag_verbose, extension, render_output, mcs_output ):
    try:
        files = []
        for i in range(1, len(sys.argv)):
            p = Path(sys.argv[i])
            if p.is_dir():
                for file in Path.iterdir(p):
                    if file.suffix == extension:
                        files.append(file)
            elif p.is_file() and p.suffix == extension:
                files.append(p)
        
        if len(files) == 0:
            print("No queries were found. Exit")
            exit(0)

        graphs, tags = process(files, flag_graph, flag_simple, flag_relation, render_output, flag_verbose)
        modules = []

        if flag_mcs:
            mcs_output = mcs_output.rstrip('/')
            print("\nCalculating all MCS:\n")
            total = (len(graphs) * len(graphs) - len(graphs)) // 2
            x = 0
            key_graph = sorted(graphs.keys())
            for i in range(len(key_graph)):
                for j in range(i+1, len(key_graph)):
                    for mcs in MCS(graphs[key_graph[i]], graphs[key_graph[j]]):
                        #CHECK ISOMORPHISM
                        isomorph = extractMapping(graphs[key_graph[i]], graphs[key_graph[j]], mcs)
                        for m in modules:
                            if m == isomorph:
                                match = next(DiGraphMatcher(m.getGraph(), isomorph, edge_match=em).match())
                                m.addQuery(key_graph[i], match) 
                                m.addQuery(key_graph[j], { k : mcs[match[k]] for k in match } )
                                m.addTags(tags[key_graph[i]])
                                m.addTags(tags[key_graph[j]])
                                m.increaseOccurence()
                                break
                        else:
                            module = Module(isomorph, 1)
                            module.addQuery(key_graph[i], { k : k for k in mcs }) #Seems stupid but it is actually very smart
                            module.addQuery(key_graph[j], mcs)
                            module.addTags(tags[key_graph[i]])
                            module.addTags(tags[key_graph[j]])
                            modules.append(module)
                    x += 1
                    print(f"\r{x} / {total} {key_graph[i]} {key_graph[j]}", end="")
            padding=len(str(len(modules)))

            for i, m in enumerate(sorted(modules, key=lambda e: e.getOccurence(), reverse=True)):
                with open(f"{mcs_output}/module{i+1:0{padding}}.txt", "w") as f:
                    f.write(str(m))   
                print(f"module{i+1:0{padding}} : {m.getOccurence()} occurences")
                dotGraph(m.getGraph(), f"{mcs_output}/module{i+1:0{padding}}", False, True)
                with open(f"{mcs_output}/module{i+1:0{padding}}.dat", "wb") as f:
                    m.setName(f"module{i+1:0{padding}}")
                    pickle.dump(m, f)
    except KeyboardInterrupt:
        print("\nAborted by user")

if __name__ == "__main__":
    #####################PARSING ARGUMENT###############################
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-a", "--all", action="store_true", help="Alias using -g -m -r -s")
    argparser.add_argument("-g", "--graph", action="store_true", help="Render graph")
    argparser.add_argument("-m", "--mcs", action="store_true", help="Calculate all MCS")
    argparser.add_argument("-r", "--relation", action="store_true",  help="Render relation graph")
    argparser.add_argument("-s", "--simple", action="store_true",  help="Render simplified graph")
    argparser.add_argument("-e", metavar="E", nargs=1, default=".rq", help="Read files in directory suffixed with <E> (default: \".rq\")")
    argparser.add_argument("files", nargs=argparse.ONE_OR_MORE, help=argparse.SUPPRESS)

    g1 = argparser.add_argument_group()
    g1.add_argument("-M", metavar="dir", nargs=1, default="./mcs_result", help="Modify output directory for MCS (default: \"./mcs_result\")")
    g1.add_argument("-O", metavar="dir", nargs=1, help="Modify output directory for rendering (default: same directory than query)")

    g2 = argparser.add_argument_group()
    g2.add_argument("-v", "--verbose", action="store_true")
    argparser.usage = "main.py [-h] (-a | [-gmrs]) [-e E] [-M dir] [-O dir] [-v] FILES"
    args = argparser.parse_args()

    if args.all:
        args.graph = args.mcs = args.relation = args.simple = True
    if isinstance(args.M, list):
        args.M = args.M[0]
    if isinstance(args.O, list):
        args.O = args.O[0]
    if isinstance(args.e, list):
        args.e = args.e[0]

    ####################################################################

    main(args.graph, args.mcs, args.relation, args.simple, args.verbose, args.e, args.O, args.M)

