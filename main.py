#Parser and graph renderers
from SAL import parse_file, SubDigraph, getRelationGraph, getSimpleGraph, Cluster

#Most Common Subgraph
from MCS import MCS, Module

from utils import dotGraph, get_tags
import argparse
from networkx.algorithms.isomorphism import DiGraphMatcher
from pathlib import Path
from os.path import basename
import sys
import pickle

def process(files, render_query = True, render_simple = False, render_relation = False, render_output=None, verbose=False):
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

def em(e1, e2) -> bool:
    try:
        return e1["label"] == e2["label"]
    except KeyError:
        return "label" not in e1 and "label" not in e2

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
                        isomorph = graphs[key_graph[i]].subgraph(mcs.keys())
                        for m in modules:
                            if m == isomorph:
                                m.increaseOccurrence()
                                m.addTags(tags[key_graph[i]])
                                m.addTags(tags[key_graph[j]])
                                m.addQuery(key_graph[i])
                                m.addQuery(key_graph[j])
                                break
                        else:
                            module = Module(isomorph, 1)
                            module.addTags(tags[key_graph[i]])
                            module.addTags(tags[key_graph[j]])
                            module.addQuery(key_graph[i])
                            module.addQuery(key_graph[j])
                            modules.append(module)
                    x += 1
                    print(f"\r{x} / {total} {key_graph[i]} {key_graph[j]}", end="")
            padding=len(str(len(modules)))                
            for m in modules:
                for k in key_graph:
                    if k not in m.getQueries() and DiGraphMatcher(graphs[k], m.getGraph(), edge_match=em).subgraph_is_isomorphic():
                        m.addQuery(k)
                        m.addTags(tags[k])

            for i, m in enumerate(sorted(modules, key=lambda e: e.getOccurrence(), reverse=True)):
                with open(f"{mcs_output}/module{i+1:0{padding}}.txt", "w") as f:
                    f.write(str(m))   
                print(f"module{i+1:0{padding}} : {m.getOccurrence()} occurences")
                dotGraph(m.getGraph(), f"{mcs_output}/module{i+1:0{padding}}", False, True)
                with open(f"{mcs_output}/module{i+1:0{padding}}.dat", "wb") as f:
                    m.setName(f"module{i+1:0{padding}}")
                    pickle.dump(m, f)
    except KeyboardInterrupt:
        print("\nAborted by user")

if __name__ == "__main__":
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

    main(args.graph, args.mcs, args.relation, args.simple, args.verbose, args.e, args.O, args.M)

