#!/bin/bash

#Utilisation:
# ./tool.sh [all|clear]

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
        python SAL.py $f >> tool.log 2>&1
    done
    echo -e "\e[K"
    rm -f ./nextprot-queries/*.g
#Effacer les fichiers créés
elif [ "$1" = "clear" ]; then
    rm -f ./nextprot-queries/*.gv
    rm -f ./nextprot-queries/*.png
    rm -f ./nextprot-queries/*.gexf
fi