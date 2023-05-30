# **sparql-visualizer**

**sparql-visualizer** is a program for visualizing queries in graph form.

## **Requirements**

Before using the program, make sure that your environment is compatible by submitting ``requirements.txt`` to **pip** with:

```bash
pip3 install -r requirements.txt
```

## **Usage**

<!-- main.py may be changed for another filename, and imported python files may be moved into a new directory -->
Command line|
--|
``python3 main.py [-e \<extension>] [-a|-gmrs] \<files> [-O \<renderdir>] [-M \<mcsdir>]``

*files* either can be a set of file or directories containing *.rq

### **Arguments**

Argument|Value|Description
:--:|:--:|--
-a|-|Alias using -g -m -r -s
-e|extension|Change query extension from ".rq" to \<extension>
-g|-|Render graph
-m|-|Calculate all MCS (<a href="https://en.wikipedia.org/wiki/Maximum_common_induced_subgraph">*maximum common induced subgraphs*</a> )
-M|directory|Modify output directory for MCS (*default:* `./mcs_result` )
-O|directory|Modify output directory for rendering (*default:* `same directory than query` )
-r|-|Render relation graph
-s|-|Render simplified graph

*Examples:*
```bash
#Rendering graphs, simplified graphs, relation graphs and MCS
python3 main.py -g -m -r -s ./queries
python3 main.py -gmrs ./queries/*.rq
python3 main.py -a ./queries/*.rq
```

```bash
#Change default input extension
python3 main.py -a -e .txt ./queries ./otherqueries
python3 main.pt -a ./queries/*.txt ./otherqueries/*.txt
```

```bash
#Change output directories
python3 main.py -a ./queries -M ./mcs -O ./render

#Combining -M and -O to same directory
python3 main.py -a ./queries -O ./output -M ./output
python3 main.py -a ./queries -OM ./output
python3 main.py -a ./queries -MO ./output
```