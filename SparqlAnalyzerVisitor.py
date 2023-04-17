import sys
from antlr4 import *
from SparqlLexer import SparqlLexer
from SparqlParser import SparqlParser
from SparqlVisitor import SparqlVisitor

from graphviz import Digraph

class Color:
    DEFAULT = "blue"
    FILTERNOTEXIST = "grey"
    LITERAL= "black"
    PROJECTION = "red"

class Shape:
    DEFAULT = "ellipse"
    LITERAL = "plain"
    PROJECTION = "ellipse"

class SparqlAnalyzerVisitor(SparqlVisitor):

    def __init__(self, mainGraphName="queryGraph"):
        super().__init__()
        self._main_graph_name = mainGraphName.replace(" ", "_")
        #Counters to attribute new 
        self._identCounter = 0
        self._prefixCounter = 0
        self._clusterCounter = 0

        #Reference dictionaries
        self._prefixNsToValue = {}
        self._prefixValueToNs = {}
        self._nodeNameToGraphNode = {} # nodeName -> {name:"", label="", shape="", color="", fontcolor=""}

        self._g = Digraph(self._main_graph_name)
        self._g.attr(rankdir="LR")

        self._currentGraph = self._g
        self._previousGraph = self._g

        self.projectionVariables = []


    def _getNewNodeIdent(self) -> str:
        self._identCounter += 1
        return f"node{self._identCounter - 1}"

    def _getNewPrefixIdent(self) -> str:
        self._prefixCounter += 1
        return f"ns{self._prefixCounter - 1}"
    
    def _getNewClusterIdent(self) -> str:
        self._clusterCounter += 1
        return f"cluster_{self._clusterCounter - 1}"


    def _getGraphNodeIdent(self, nodeName):
        #Prefixing CURIE
        if nodeName.startswith("<http"):
            #Get prefix
            for (nsValue, nsPrefix) in self._prefixValueToNs.items():
                if nodeName.startswith("<" + str(nsValue)):
                    nodeName = nodeName[:-1].replace("<" + nsValue, nsPrefix + ":")
                    break
            #Store prefix if unknown
            else:
                currentNsPrefix = self._getNewPrefixIdent()
                currentNsValue = nodeName[1:max(nodeName.rfind("#"), nodeName.rfind("/"))+1]
                self._prefixNsToValue[currentNsPrefix] = currentNsValue
                self._prefixValueToNs[currentNsValue] = currentNsPrefix
                nodeName = nodeName[:-1].replace("<" + currentNsValue, currentNsPrefix + ":")

        #Check whether the node has been encountered before
        if nodeName not in self._nodeNameToGraphNode.keys():
            nodeIdent = self._getNewNodeIdent()
            self._nodeNameToGraphNode[nodeName] =  {"name" : nodeIdent, "label" : nodeName, "shape" : "box", "color" : "black", "fontcolor" : "black"}

            if nodeName.startswith("?"):
                self._nodeNameToGraphNode[nodeName]["shape"] = Shape.PROJECTION
                #Check whether the node is in projection
                if nodeName in self.projectionVariables:
                    self._nodeNameToGraphNode[nodeName]["color"] = Color.PROJECTION
                    self._nodeNameToGraphNode[nodeName]["fontcolor"] = Color.PROJECTION
                    self._nodeNameToGraphNode[nodeName]["shape"] = Shape.PROJECTION
                else:
                    self._nodeNameToGraphNode[nodeName]["color"] = Color.DEFAULT
                    self._nodeNameToGraphNode[nodeName]["fontcolor"] = Color.DEFAULT
                    self._nodeNameToGraphNode[nodeName]["shape"] = Shape.DEFAULT
            elif self._currentGraph != self._g: #WARNING: REALLY FILTERNOTEXIST BELOW ?
                    self._nodeNameToGraphNode[nodeName]["color"] = Color.FILTERNOTEXIST
                    self._nodeNameToGraphNode[nodeName]["fontcolor"] = Color.FILTERNOTEXIST

            #self._g.node(nodeIdent, label=self._nodeNameToGraphNode[nodeName]["label"], shape=self._nodeNameToGraphNode[nodeName]["shape"], color=self._nodeNameToGraphNode[nodeName]["color"], fontcolor=self._nodeNameToGraphNode[nodeName]["color"])
            self._currentGraph.node(**self._nodeNameToGraphNode[nodeName])
        elif self._currentGraph != self._g:
            cloneNodeIdent = self._createCloneNode(nodeName, graph=self._currentGraph, color=Color.FILTERNOTEXIST)
            self._g.edge(self._nodeNameToGraphNode[nodeName]["name"], cloneNodeIdent, arrowhead="none", color=Color.FILTERNOTEXIST, style="dotted")
            return cloneNodeIdent
        return self._nodeNameToGraphNode[nodeName]["name"]

    def _createLiteralNode(self, literalValue, graph=None):
        nodeIdent = self._getNewNodeIdent()
        if graph is None:
            graph = self._g

        graph.node(nodeIdent, label=literalValue, shape=Shape.LITERAL, color=Color.LITERAL)
        return nodeIdent

    def _createBuiltInFunctionNode(self, functionLabel, graph=None , fontcolor="black"):
        nodeIdent = self._getNewNodeIdent()
        if graph is None:
            graph = self._g
            
        graph.node(nodeIdent, label=functionLabel, shape="plaintext", fontcolor=fontcolor)
        return nodeIdent

    def _createCloneNode(self, origNodeIdent, graph=None, color=None):
        #print("///// DEBUG ///// {}".format(origNodeIdent))
        nodeIdent = self._getNewNodeIdent()
        if graph is None:
            graph = self._g
        
        if color is None:
            graph.node(nodeIdent, label=self._nodeNameToGraphNode[origNodeIdent]["label"], shape=self._nodeNameToGraphNode[origNodeIdent]["shape"], color=self._nodeNameToGraphNode[origNodeIdent]["color"], fontcolor=self._nodeNameToGraphNode[origNodeIdent]["fontcolor"])
        else:
            graph.node(nodeIdent, label=self._nodeNameToGraphNode[origNodeIdent]["label"], shape=self._nodeNameToGraphNode[origNodeIdent]["shape"], color=color, fontcolor=color)

        return nodeIdent

    def _createRelationalOperatorNode(self, relationalOperatorLabel, graph = None , color = "black"):
        nodeIdent = self._getNewNodeIdent()
        if graph is None:
            graph = self._g

        graph.node(nodeIdent, label = relationalOperatorLabel, shape = "hexagon", color=color, fontcolor=color)

        return nodeIdent

    def _createBlankNode(self):
        nodeIdent = self._getNewNodeIdent()
        nodeName = "_:" + nodeIdent
        self._nodeNameToGraphNode[nodeName] = { "name": nodeIdent, "label": "[]", "shape": "box", "color": "black" }
        self._currentGraph.node(**self._nodeNameToGraphNode[nodeName])
        return nodeIdent

    def _setNodeLabel(self, nodeName, nodeLabel):
        if nodeName in self._nodeNameToGraphNode.keys():
            self._nodeNameToGraphNode[nodeName]["label"] = nodeLabel

    def saveToDot(self, fileName):
        self._g.save(fileName)

    def printNamespaces(self):
        print()
        print("NAMESPACES")
        print("prefix -> value")
        for (prefix, value) in self._prefixNsToValue.items():
            print(f"  {prefix}\t->\t{value}")
        print("value -> prefix")
        for (value, prefix) in self._prefixValueToNs.items():
            print(f"  {value}\t<-\t{prefix}")
        print()

    def visitPrefixDecl(self, ctx:SparqlParser.PrefixDeclContext):
        #print("Oh, a PREFIX declaration! {}".format(ctx) )
        self._prefixNsToValue[ctx.PNAME_NS()] = ctx.IRIREF()
        self._prefixValueToNs[ctx.IRIREF()] = ctx.PNAME_NS()
        #return super().visitTriplesBlock(ctx)
        return super().visitPrefixDecl(ctx)

    def visitSelectClause(self, ctx:SparqlParser.SelectClauseContext):
        print("Oh, a SELECT clause! {}".format(ctx) )
        for currentVar in ctx.var():
            print("Projection variable: {}".format(currentVar.getText()))
            self.projectionVariables.append(currentVar.getText())
        return super().visitSelectClause(ctx)

    def _processTriplesSameSubject(self, subjectIdent, propertyContext, objectContext, edgeStyle="solid"):
        # propertyContext is an instance of PathContext 
        for currentSequence in propertyContext.pathAlternative().pathSequence():
            currentSubjectIdent = subjectIdent
            print("      sequence: {}".format(currentSequence.getText()))
            for currentProperty in currentSequence.pathEltOrInverse()[:-1]:
                if currentProperty.pathElt().pathPrimary().iri() != None:
                    propertyIdent = currentProperty.getText()
                    currentIntermediateIdent = self._createBlankNode()
                    #self._currentGraph.edge(currentSubjectIdent, currentIntermediateIdent, label=propertyIdent, style=edgeStyle)
                    if self._currentGraph != self._g:
                        self._currentGraph.edge(currentSubjectIdent, currentIntermediateIdent, label=propertyIdent, style=edgeStyle, color="grey", fontcolor="grey")
                    else:
                        self._currentGraph.edge(currentSubjectIdent, currentIntermediateIdent, label=propertyIdent, style=edgeStyle)
                    currentSubjectIdent = currentIntermediateIdent
                elif currentProperty.pathElt().pathPrimary().path() != None:
                    if (edgeStyle == "dashed") or (len(currentProperty.pathElt().pathPrimary().path().pathAlternative().pathSequence()) > 1):
                        self._processTriplesSameSubject(currentSubjectIdent, currentProperty.pathElt().pathPrimary().path(), objectContext, edgeStyle="dashed")
                    else:
                        self._processTriplesSameSubject(currentSubjectIdent, currentProperty.pathElt().pathPrimary().path(), objectContext, edgeStyle)
            currentProperty = currentSequence.pathEltOrInverse()[-1]
            if currentProperty.pathElt().pathPrimary().iri() != None:
                propertyIdent = currentProperty.getText()
                currentObjectIndex = 0
                while currentObjectIndex < objectContext.getChildCount():
                    currentObject = objectContext.getChild(currentObjectIndex)
                    if isinstance(currentObject, SparqlParser.ObjectClauseContext):
                        if isinstance(currentObject.graphNode().varOrTerm().getChild(0), SparqlParser.VarContext):
                            objectIdent = self._getGraphNodeIdent(currentObject.getText())
                            #self._currentGraph.edge(currentSubjectIdent, objectIdent, label=propertyIdent, style=edgeStyle)
                            if self._currentGraph != self._g:
                                self._currentGraph.edge(currentSubjectIdent, objectIdent, label=propertyIdent, style=edgeStyle, color="grey", fontcolor="grey")
                            else:
                                self._currentGraph.edge(currentSubjectIdent, objectIdent, label=propertyIdent, style=edgeStyle)
                    elif isinstance(currentObject, SparqlParser.ObjectPathContext):
                        if isinstance(currentObject.graphNodePath().varOrTerm().getChild(0), SparqlParser.VarContext):
                            objectIdent = self._getGraphNodeIdent(currentObject.getText())
                            #self._currentGraph.edge(currentSubjectIdent, objectIdent, label=propertyIdent, style=edgeStyle)
                            if self._currentGraph != self._g:
                                self._currentGraph.edge(currentSubjectIdent, objectIdent, label=propertyIdent, style=edgeStyle, color="grey", fontcolor="grey")
                            else:
                                self._currentGraph.edge(currentSubjectIdent, objectIdent, label=propertyIdent, style=edgeStyle)
                        elif isinstance(currentObject.graphNodePath().varOrTerm().graphTerm().getChild(0), SparqlParser.IriContext):
                            objectIdent = self._getGraphNodeIdent(currentObject.getText())
                            #self._currentGraph.edge(currentSubjectIdent, objectIdent, label=propertyIdent, style=edgeStyle)
                            if self._currentGraph != self._g:
                                #objectIdent = self._getGraphNodeIdent(currentObject.getText())
                                self._currentGraph.edge(currentSubjectIdent, objectIdent, label=propertyIdent, style=edgeStyle, color="grey", fontcolor="grey")
                            else:
                                #objectIdent = self._getGraphNodeIdent(currentObject.getText())
                                self._currentGraph.edge(currentSubjectIdent, objectIdent, label=propertyIdent, style=edgeStyle)
                        elif isinstance(currentObject.graphNodePath().varOrTerm().graphTerm().getChild(0), SparqlParser.RdfLiteralContext):
                            objectIdent = self._createLiteralNode(currentObject.getText())
                            #self._currentGraph.edge(currentSubjectIdent, objectIdent, label=propertyIdent, style=edgeStyle)
                            if self._currentGraph != self._g:
                                self._currentGraph.edge(currentSubjectIdent, objectIdent, label=propertyIdent, style=edgeStyle, color="grey", fontcolor="grey")
                            else:
                                self._currentGraph.edge(currentSubjectIdent, objectIdent, label=propertyIdent, style=edgeStyle)
                    currentObjectIndex += 1
            elif currentProperty.pathElt().pathPrimary().path() != None:
                if (edgeStyle == "dashed") or (len(currentProperty.pathElt().pathPrimary().path().pathAlternative().pathSequence()) > 1):
                    self._processTriplesSameSubject(currentSubjectIdent, currentProperty.pathElt().pathPrimary().path(), objectContext, edgeStyle="dashed")
                else:
                    self._processTriplesSameSubject(currentSubjectIdent, currentProperty.pathElt().pathPrimary().path(), objectContext, edgeStyle)

    def visitTriplesSameSubjectPath(self, ctx:SparqlParser.TriplesSameSubjectPathContext):
        print("Oh, a triplesSameSubjectPath! {}".format(ctx) )
        #print("    {}".format(dir(ctx)))
        print("    Text: {}".format(ctx.getText()))
        #print("    getChildCount(): {}".format(ctx.getChildCount()))
        print("    subject (VarOrTerm): {}".format(ctx.varOrTerm().getText()))
        subjectIdent = self._getGraphNodeIdent(ctx.varOrTerm().getText())
        currentChildIndex = 0
        while currentChildIndex < ctx.propertyListPathNotEmpty().getChildCount():
            currentChild = ctx.propertyListPathNotEmpty().getChild(currentChildIndex)
            print("    child {}: {}".format(currentChildIndex, type(currentChild)))
            if isinstance(currentChild, SparqlParser.VerbPathContext):
                nbAlternatives = len(currentChild.path().pathAlternative().pathSequence())
                print("      property: {} ({} alternatives)".format(currentChild.getText(), nbAlternatives))
                if nbAlternatives > 1:
                    self._processTriplesSameSubject(subjectIdent, currentChild.path(), ctx.propertyListPathNotEmpty().getChild(currentChildIndex+1), edgeStyle="dashed")
                else:
                    self._processTriplesSameSubject(subjectIdent, currentChild.path(), ctx.propertyListPathNotEmpty().getChild(currentChildIndex+1), edgeStyle="solid")
            if isinstance(currentChild, SparqlParser.VerbSimpleContext):
                print("      property: {}".format(currentChild.getText()))
                propertyIdent = currentChild.getText()
                # FIXME: create edge to next child
                currentObjectIndex = 0
                while currentObjectIndex < ctx.propertyListPathNotEmpty().getChild(currentChildIndex+1).getChildCount():
                    currentObject = ctx.propertyListPathNotEmpty().getChild(currentChildIndex+1).getChild(currentObjectIndex)
                    if isinstance(currentObject, (SparqlParser.ObjectPathContext, SparqlParser.ObjectClauseContext)):
                        objectIdent = self._getGraphNodeIdent(currentObject.getText())
                        #self._currentGraph.edge(subjectIdent, objectIdent, label=propertyIdent)
                        if self._currentGraph != self._g:
                            self._currentGraph.edge(subjectIdent, objectIdent, label=propertyIdent, color="grey", fontcolor="grey")
                        else:
                            self._currentGraph.edge(subjectIdent, objectIdent, label=propertyIdent)
                    currentObjectIndex += 1
            currentChildIndex += 1
        print()
        return super().visitTriplesSameSubjectPath(ctx)

    def _processNumericExpression(self, numericExpressionContext, graph=None, fontcolor="black"):
        for currentMultiplicativeExpression in numericExpressionContext.additiveExpression().multiplicativeExpression():
            for currentUnaryExpression in currentMultiplicativeExpression.unaryExpression():
                currentPrimaryExpressionChild = currentUnaryExpression.primaryExpression().getChild(0)
                print("          {}".format(type(currentPrimaryExpressionChild)))
                # grammar primaryExpression:  brackettedExpression | builtInCall | iriOrFunction | rdfLiteral | numericLiteral | booleanLiteral | var
                if isinstance(currentPrimaryExpressionChild, SparqlParser.BrackettedExpressionContext):
                    print("          TODO BrackettedExpressionContext")
                    # TODO: re-engineer as recursive function?
                elif isinstance(currentPrimaryExpressionChild, SparqlParser.VarContext):
                    origNodeName = currentPrimaryExpressionChild.getChild(0).getText()
                    origNodeIdent = self._getGraphNodeIdent(origNodeName)
                    nodeCloneIdent = self._createCloneNode(origNodeName, graph=graph, fontcolor="grey")
                    if graph is None:
                        self._g.edge(nodeCloneIdent, origNodeIdent, arrowhead="none", color="grey", style="dotted")
                    else:
                        graph.edge(nodeCloneIdent, origNodeIdent, arrowhead="none", color="grey", style="dotted")
                    return nodeCloneIdent
                elif isinstance(currentPrimaryExpressionChild, SparqlParser.BuiltInCallContext):
                    functionNodeIdent = self._createBuiltInFunctionNode(currentPrimaryExpressionChild.getChild(0).getText()+"(...)", graph=graph, fontcolor="grey")
                    functionArgumentNodeIdent = self._getGraphNodeIdent(currentPrimaryExpressionChild.getChild(2).getText())
                    if functionArgumentNodeIdent != None:
                        if graph is None:
                            self._g.edge(functionNodeIdent, functionArgumentNodeIdent, arrowhead="none", color="grey", style="dotted") 
                        else:
                            graph.edge(functionNodeIdent, functionArgumentNodeIdent, arrowhead="none", color="grey", style="dotted") 
                    return functionNodeIdent
                elif isinstance(currentPrimaryExpressionChild, SparqlParser.IriOrFunctionContext):
                    print("          TODO IriOrFunctionContext")
                elif isinstance(currentPrimaryExpressionChild, SparqlParser.RdfLiteralContext):
                    print("          TODO RdfLiteralContext")
                elif isinstance(currentPrimaryExpressionChild, SparqlParser.NumericLiteralContext):
                    print("          TODO NumericLiteralContext")
                elif isinstance(currentPrimaryExpressionChild, SparqlParser.BooleanLiteralContext):
                    print("          TODO BooleanLiteralContext")
                elif isinstance(currentPrimaryExpressionChild, SparqlParser.VarContext):
                    print("          TODO VarContext")

    def visitFilterClause(self, ctx:SparqlParser.FilterClauseContext):
        print("Oh, a filterClause! {}".format(ctx) )
        with self._currentGraph.subgraph(name=self._getNewClusterIdent()) as subcluster:
            #subcluster.attr(label='FILTER')
            subcluster.attr(style='dashed')
            subcluster.attr(color='grey')
            #subcluster.attr(fontcolor='grey')
            currentConstraint = ctx.constraint().getChild(0)
            #print("!!!!! {}".format(type(currentConstraint)))
            # grammar constraint: brackettedExpression | builtInCall | functionCall
            if isinstance(currentConstraint, SparqlParser.BrackettedExpressionContext):
                subcluster.attr(label='FILTER')
                #print("  BrackettedExpressionContext")
                for currentConditionalAndExpression in currentConstraint.expression().conditionalOrExpression().conditionalAndExpression():
                    for currentValueLogical in currentConditionalAndExpression.valueLogical():
                        currentRelationalExpression = currentValueLogical.relationalExpression()
                        #print("    {}".format(dir(currentRelationalExpression)))
                        if len(currentRelationalExpression.numericExpression()) == 2:
                            operatorNodeIdent = self._createRelationalOperatorNode(currentRelationalExpression.getChild(1).getText(), graph=subcluster, fontcolor="grey")
                            operand1NodeIdent = self._processNumericExpression(currentRelationalExpression.numericExpression()[0], graph=subcluster, fontcolor="grey")
                            operand2NodeIdent = self._processNumericExpression(currentRelationalExpression.numericExpression()[1], graph=subcluster, fontcolor="grey")
                            subcluster.edge(operand1NodeIdent, operatorNodeIdent, style="solid", color="grey")
                            subcluster.edge(operatorNodeIdent, operand2NodeIdent, style="solid", color="grey")
                        else:
                            print("      TODO: handle numericExpression IN expressionList and numericExpression NOT IN expressionList")
            elif isinstance(currentConstraint, SparqlParser.BuiltInCallContext):
                print("  TODO BuiltInCallContext")
                constraintChild = currentConstraint.getChild(0)
                if isinstance(constraintChild, SparqlParser.NotExistsFuncContext):
                    #print("///// DEBUG ///// {}".format(dir(constraintChild)))
                    subcluster.attr(label='FILTER NOT EXISTS')
                    backupCurrentGraph = self._currentGraph # FIXME: necessary???
                    backupPreviousGraph = self._previousGraph
                    self._previousGraph = self._currentGraph
                    self._currentGraph = subcluster
                    for currentGroupGraphPatternSubChild in constraintChild.groupGraphPattern().groupGraphPatternSub().getChildren():
                        print("    {}".format(type(currentGroupGraphPatternSubChild)))
                        self.visitTriplesBlock(currentGroupGraphPatternSubChild)
                    self._currentGraph = backupCurrentGraph
                    self._previousGraph = backupPreviousGraph
            elif isinstance(currentConstraint, SparqlParser.FunctionCallContext):
                print("  TODO FunctionCallContext")
        #print("///// DEBUG ///// {}".format(type(super().visitFilterClause(ctx))))
        print()
        #return super().visitFilterClause(ctx)
        return

    #def visitPropertyListPathNotEmpty(self, ctx:SparqlParser.PropertyListPathNotEmptyContext):
    #    print("Oh, a propertyListPathNotEmpty! {}".format(ctx) )
    #    print("  {}".format(dir(ctx)))
    #    print("  subjectIdent: {}".format(self._getGraphNodeIdent(ctx.parentCtx.varOrTerm().getText())))
    #    print("  Nb children: {}".format(ctx.getChildCount()))
    #    print()
    #    return super().visitPropertyListPathNotEmpty(ctx)

    #def visitIri(self, ctx:SparqlParser.IriContext):
    #    print("Oh, an IRI! {}".format(ctx) )
    #    print("  {}".format(dir(ctx)))
    #    print("    Text: {}".format(ctx.getText()))
    #    print("    getChildCount(): {}".format(ctx.getChildCount()))
    #    for currentChild in ctx.getChildren():
    #        print("      {}".format(type(currentChild)))
    #    print("    IRIREF: {}".format(ctx.IRIREF()))
    #    print()
    #    return super().visitChildren(ctx)

    #def visitPrefixedName(self, ctx:SparqlParser.PrefixedNameContext):
    #    print("Oh, a prefixedName! {}".format(ctx) )
    #    #print("  {}".format(dir(ctx)))
    #    print("    Text: {}".format(ctx.getText()))
    #    print()
    #    return super().visitChildren(ctx)

    #def visitVar(self, ctx:SparqlParser.VarContext):
    #    print("Oh, a variable! {}".format(ctx) )
    #    print("  {}".format(dir(ctx)))
    #    print("    Text: {}".format(ctx.getText()))
    #    print("    getChildCount(): {}".format(ctx.getChildCount()))
    #    print()
    #    return super().visitChildren(ctx)
        
 
def main(argv):
    input_stream = FileStream(argv[1])
    #TODO: Add intermediate FileStream to change keyword case
    lexer = SparqlLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = SparqlParser(stream)
    tree = parser.statement()

    visitor = SparqlAnalyzerVisitor()
    output = visitor.visit(tree)
    print(output)
    visitor.saveToDot(argv[1][:-3] + ".dot")

    visitor.printNamespaces()


 
if __name__ == '__main__':
    main(sys.argv)
