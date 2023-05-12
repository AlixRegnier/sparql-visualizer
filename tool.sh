#!/bin/bash

#Utilisation:
# ./tool.sh [all|antlr4|clear]

> tool.log
files=`ls ./nextprot-queries/*.rq`
count=`echo "$files" | wc -l`

#Appliquer le script sur tout les scripts dans ./nextprot-queries
x=0
if [ "$1" = "all" ]; then
    echo ""
    for f in $files; do
        echo $f >> tool.log
        echo -e "\e[0A $((++x)) / $count"
        python SAL.py $f 2>> tool.log
        #python SAL.py $f -v > $f.log 2>> tool.log
    done
    echo -e "\e[K"
    rm -f ./nextprot-queries/*.g
#Effacer les fichiers créés
elif [ "$1" = "clear" ]; then
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