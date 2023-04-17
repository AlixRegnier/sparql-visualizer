#! /usr/bin/env python3

import sys
from antlr4 import *
from SparqlLexer import SparqlLexer
from SparqlParser import SparqlParser
from SparqlListener import SparqlListener

class TriplePrinter(SparqlListener):     
    def exitTriplesNode(self, ctx):         
        print("Oh, a triple!") 
 
def main(argv):
    input_stream = FileStream(argv[1])
    lexer = SparqlLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = SparqlParser(stream)
    tree = parser.statement()

    printer = TriplePrinter()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
 
if __name__ == '__main__':
    main(sys.argv)
