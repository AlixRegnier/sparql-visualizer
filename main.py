#Parser and graph renderers
from SAL import parse_file, SubDigraph, getRelationGraph, getSimpleGraph, Cluster

#Most Common Subgraph
from MCS import dotGraph, MCS

from pathlib import Path
from os.path import basename
import sys

def usage():
    print("Usage: python main.py [-v] (file1 file2 ..)\n\n\t-v\tVerbose (print parsing tree and nested values)\n")
    return 1

def process(files, render_query = True, render_simple = False, render_relation = False):
    pfiles = dict()
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
            pfiles[basename(files[i].stem)] = simplegraph
            print(f"\r{i+1} / {len(files)}", end=' ')
        except Exception as e:
            print("\rFAILED:", files[i], end="\n\n")
            print(e, file=sys.stderr)
        finally:
            #Reset static values for next iteration
            SubDigraph.reset()
            Cluster.reset()
    return pfiles


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
        
        graphs = process(files, True, True, True)
        print("\nCalculating all MCS:\n")
        m = (len(graphs) * len(graphs) - len(graphs)) // 2
        x = 0
        key_graph = list(graphs.keys())
        for i in range(len(key_graph)):
            for j in range(i+1, len(key_graph)):
                print(key_graph[i], key_graph[j])
                c = 1
                for mcs in MCS(graphs[key_graph[i]], graphs[key_graph[j]]):
                    dotGraph(graphs[key_graph[i]].subgraph(mcs.keys()), f"./mcs_result/{key_graph[i]}_{key_graph[j]}.{c}")
                    c += 1
                x += 1
                print(f"{x} / {m}", end='\n')
    except KeyboardInterrupt:
        print("Aborted by user")

if __name__ == "__main__":
    main()
            