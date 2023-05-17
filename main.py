#Parser and graph renderers
from SAL import *

#Most Common Subgraph
from MCS import *

from pathlib import Path
from os.path import basename
import sys

def usage():
    print("Usage: python main.py [-v] (file1 file2 ..)\n\n\t-v\tVerbose (print parsing tree and nested values)\n")
    return 1

def process(files, render_query = True, render_relation = True):
    pfiles = dict()
    for i in range(len(files)):
        try:
            #Parse file
            maincluster = parse_file(str(files[i]))

            #Retrieve parser results
            maincluster.generateGraph()
            if render_query:
                SubDigraph.allSubgraphsToDot(str(files[i])) #TODO: Replace all static stuff by dynamic ones
            if render_relation:
                dotGraph(getRelationGraph(maincluster.getFullGraph()), str(files[i]) + ".relation")
            #Reset static values for next iteration
            SubDigraph.reset()
            Cluster.reset()
            
            #Merge all subdigraphes to create a customized line graph (relations as nodes)
            pfiles[basename(files[i].stem)] = getRelationGraph(maincluster.getFullGraph())
            print(f"\r{i+1} / {len(files)}", end=' ')
        except Exception as e:
            print("\rFAILED:", files[i], end="\n\n")
        #    print(e, file=sys.stderr)
    return pfiles


def main():
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
    
    relationsGraphs = process(files, False, False)

    print("\nCalculating all MCS:")
    m = len(relationsGraphs) * len(relationsGraphs) - len(relationsGraphs)
    x = 0
    for k1 in relationsGraphs:
        for k2 in relationsGraphs:
            if k1 != k2:
                print(k1, k2)
                for i, e in enumerate(MCS(relationsGraphs[k1], relationsGraphs[k2])):
                    dotGraph(e, f"./mcs_result/{k1}_{k2}.{i+1}")
                    x += 1
                    print(f"{x} / {m}", end='')
    print("End !")

if __name__ == "__main__":
    main()
            