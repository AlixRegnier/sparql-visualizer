#Parser and graph renderers
from SAL import parse_file, SubDigraph, getRelationGraph, getSimpleGraph, Cluster

#Most Common Subgraph
from MCS import MCS, Module

from utils import dotGraph, get_tags

from pathlib import Path
from os.path import basename
import sys

def usage():
    print("Usage: python main.py [-v] (file1 file2 ..)\n\n\t-v\tVerbose (print parsing tree and nested values)\n")
    return 1

def process(files, render_query = True, render_simple = False, render_relation = False):
    pfiles = dict()
    tfiles = dict()
    for i in range(len(files)):
        try:
            #Parse file
            maincluster = parse_file(str(files[i]))

            #Retrieve parser results
            maincluster.generateGraph()
            if render_query:
                SubDigraph.allSubgraphsToDot(str(files[i])) #TODO: Replace all static stuff by dynamic ones

            fullgraph = maincluster.getFullGraph()
            simplegraph = getSimpleGraph(fullgraph)
            if render_simple:
                dotGraph(simplegraph, str(files[i]) + ".simple", nodelabel=False)
            if render_relation:
                dotGraph(getRelationGraph(fullgraph), str(files[i]) + ".relation", edgelabel=False)

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


def main():
    try:
        if len(sys.argv) == 1:
            exit(usage())
        #TODO: Add argument parser for getting if graph/relation/MCS need to be rendered, single/multiple log file if verbose
        files = []
        for i in range(1, len(sys.argv)):
            p = Path(sys.argv[i])
            if p.is_dir():
                for file in Path.iterdir(p):
                    if file.suffix == ".rq":
                        files.append(file)
            elif p.is_file() and p.suffix == ".rq":
                files.append(p)
        
        graphs, tags = process(files, False, False, False)
        modules = []

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
                            m.addTags(tags[key_graph[i]] & tags[key_graph[j]])
                            m.addQueries(key_graph[i], key_graph[j])
                            break
                    else:
                        modules.append(Module(isomorph, 1, tags[key_graph[i]] & tags[key_graph[j]], [key_graph[i], key_graph[j]]))
                x += 1
                print(f"\r{x} / {total} {key_graph[i]} {key_graph[j]}", end="")
        padding=len(str(len(modules)))                
        print()
        for i, m in enumerate(sorted(modules, key=lambda e: e.getOccurrence(), reverse=True)):
            with open(f"./mcs_result/module{i+1:0{padding}}.txt", "w") as f:
                f.write(f"Nombre d'occurrences:\n{m.getOccurrence()}\n")
                f.write("\nTags:\n")
                if m.getTags():
                    f.write('\n'.join(sorted(m.getTags())))
                else:
                    f.write("NONE")
                f.write("\n\nQueries:\n")
                f.write('\n'.join(sorted(m.getQueries())))    
            print(f"module{i+1:0{padding}} : {m.getOccurrence()} occurences")
            dotGraph(m.getGraph(), f"./mcs_result/module{i+1:0{padding}}", False, True)

    except KeyboardInterrupt:
        print("\nAborted by user")

if __name__ == "__main__":
    main()
