#!/bin/bash

#Utilisation:
# ./tool.sh [all|antlr4|clear]

#Appliquer le script sur tout les scripts dans ./nextprot-queries
if [ "$1" = "all" ]; then
    python main.py ./nextprot-queries
#Effacer les fichiers créés
if [ "$1" = "clear" ]; then
    rm -f ./nextprot-queries/*.gv
    rm -f ./nextprot-queries/*.png
    rm -f ./nextprot-queries/*.gexf
    rm -f ./nextprot-queries/*.log
#Génère le parser et retirer les fichiers superflus
#Ajoute "allowsBlankNodes" en variable globale
elif [ "$1" = "antlr4" ]; then
    java -jar ~/software/antlr-4.10.1/antlr-4.10.1-complete.jar -Dlanguage=Python3 Sparql.g4
    head -9 SparqlParser.py > tmp.txt
    echo "allowsBlankNodes = True" >> tmp.txt
    tail -n+10 SparqlParser.py >> tmp.txt
    mv tmp.txt SparqlParser.py
    rm -f ./*.interp ./*.tokens ./SparqlVisitor.py
fi