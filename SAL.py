#! /usr/bin/env python3

from antlr4 import *
from collections import deque
from graphviz import Digraph
import networkx as nx
import re
from SparqlLexer import SparqlLexer
from SparqlParser import SparqlParser
from SparqlListener import SparqlListener

#Constants enums
class Color:
    ALIAS_IN = "magenta"
    ALIAS_OUT = "grey"
    BLANK = "black"
    DEFAULT = "blue"
    DUPLICATE = "grey"
    PROJECTION = "red"
    TYPE = "grey"
    VALUE = "green3"
    VALUES = "grey"

class Shape:
    ALIAS = "hexagon"
    BLANK = "ellipse"
    DEFAULT = "ellipse"
    DUPLICATE = "ellipse"
    PROJECTION = "ellipse"
    TYPE = "hexagon"
    VALUE = "box"
    VALUES = "box"

class Style:
    ALIAS_IN = "dotted"
    ALIAS_OUT = "dashed"
    DEFAULT = "solid"
    DUPLICATE = "dashed"
    FILTER = "dashed"
    GROUP = "dashed"
    OPTIONAL = "dashed"
    SELECT = "dashed"
    TYPE = "solid"
    UNION = "solid"

class ArrowStyle:
    ALIAS_IN = "none"
    ALIAS_OUT = "none"
    DEFAULT = "normal"
    DUPLICATE = "none"
    TYPE = "normal"

#Classes
class Alias:
    """
    Class that store an alias
    """
    @staticmethod
    def dSpace(s) -> str: 
        return f" {s.group(0)} "
    
    @staticmethod
    def nSpace(s) -> str: 
        return f"{s.group(0)} "
    
    @staticmethod
    def __sub(s : str) -> str:
        return re.sub("distinct|,", Alias.nSpace, re.sub("[+*/<>=&|;]|(?<=\w)-", Alias.dSpace, s), flags=re.IGNORECASE)
    
    def __init__(self, vars, target, text):
        #Regex that insert spaces in string near operators that are followed by '?' or a digit
        self.text = ""
        currentIndex = 0
        for e in re.finditer("\"|'.*?\"|'", text):
            self.text += Alias.__sub(text[currentIndex:e.start()]) + e.string
            currentIndex = e.end() + 1
        self.text += Alias.__sub(text[currentIndex:])
            

        self.vars = set(vars)
        self.target = target
    
    def getVars(self):
        return self.vars
    
    def getTarget(self):
        return self.target
    
    def getText(self):
        return self.text
    
    def __str__(self):
        return f"Vars: {self.vars}\nTarget: {self.target}\nText: {self.text}"

class Cluster:
    """
    Class that will be used as dot special cluster
    """

    cluster = -1

    def __init__(self, label = "SELECT", style = Style.DEFAULT):
        self.aliases = dict()
        self.name = Cluster.getNextCluster()
        self.projections = set()
        self.subclusters = []
        self.supercluster = None
        self.label = label
        self.style = style
        self.tss = []
        self.values = dict()
        self.vars = set()

    @staticmethod
    def getNextCluster():
        Cluster.cluster += 1
        return f"cluster{Cluster.cluster}"
    
    @staticmethod
    def reset():
        Cluster.cluster = -1
        
    def addSubCluster(self, s):
        self.subclusters.append(s)
        s.supercluster = self

    def setLabel(self, label):
        self.label = label
    
    def getStyle(self):
        return self.style
    
    def getLabel(self):
        return self.label
    
    def getClusterName(self, v): 
        r = None
        if self.supercluster:
            r = self.supercluster.getClusterName(v)

        if r is None:
            if v in self.vars:
                return self.name
            return None
        return r

    def getAliases(self):
        return self.aliases
    
    def addAlias(self, vars, var, text):
        self.aliases[var] = Alias(vars, var, text)

    def addVar(self, v):
        if v != "":
            self.vars.add(v)
        else:
            print("WARNING: Attempted to add empty string in variables !")

    def addVarValues(self, v, values):
        self.values[v] = set(values)

    def addVars(self, vs):
        self.vars |= set(vs) - {""}

    def addTSS(self, tss):
        self.tss.append(tss)

    def getProjections(self):
        if len(self.projections) == 0:
            return self.vars
        return self.projections

    def setProjections(self, ps):
        self.projections = set(ps)
        self.addVars(ps)

    def generateGraph(self):
        return SubDigraph(self)
    
    def getFullGraph(self):
        d = nx.DiGraph()

        SubDigraph(self)
        for name in SubDigraph.subgraphes:
            d = nx.compose(d, SubDigraph.subgraphes[name])
        return d
    
class TSS:
    """
    Class that stores triples or 'chained' triples
    """
    def __init__(self):
        self.subject = None
        self.__neednewpath = True
        self.paths = [] #List of paths. A path is a list of verbPaths with a value as its end. Between each relation, there is a virtual blank node
        self.blankpath = None
        self.blen = 0

    def openBlankPath(self):
        self.blankpath = (len(self.paths)-1, self.paths[-1][:])

    def closeBlankPath(self):
        for i in range(self.blankpath[0]+1, len(self.paths)):
            self.paths[i] = self.blankpath[1][:] + self.paths[i]
        self.blankpath = None

    def close(self):
        j = 0
        alone = True
        for i in range(len(self.paths)):
            if len(self.paths[i]) == 1:
                self.paths[i] = self.paths[j][:-1] + self.paths[i]
            else:
                alone = False
                j = i
        
        if alone and len(self.paths):
            for i in range(1, len(self.paths)):
                self.paths[0] += self.paths[i]
            self.paths = [self.paths[0]]

        #Clean TSSP end if some artefacts are remaining
        #TODO: Find artefacts origin
        for i in range(len(self.paths) -1, -1, -1):
            if self.paths[i] != ['']:
                self.paths = self.paths[:i+1]
                break

    def addToPath(self, value, isVerbPath):
        if self.subject is None:
            self.subject = value
        else:
            #Handle 'a' alias for 'rdf:type'
            if value.lower() == "a":
                value = "rdf:type"

            if self.__neednewpath:
                self.paths.append([])
                self.__neednewpath = False

            self.paths[-1].append(value)
            if not isVerbPath:            
                self.__neednewpath = True

    def addToBlank(self, value):
        self.blen += 1

        #Handle 'a' alias for 'rdf:type'
        if value.lower() == "a":
            value = "rdf:type"

        if self.blen == 3:
            self.blen = 0
            self.paths.append([value])
        else:
            self.paths[-1].append(value)

    def __str__(self):
        return f"{self.subject}\n{self.paths}"

class SubDigraph(nx.DiGraph):
    """
    Class that inherits from NetworkX DiGraph, many instances will be used for the composition of the final graph
    """

    #Tuples for shaping and coloring from constants
    ALIAS = (Shape.ALIAS, Color.ALIAS_OUT, Color.ALIAS_OUT)
    BLANK = (Shape.BLANK, Color.BLANK, Color.BLANK)
    DEFAULT = (Shape.DEFAULT, Color.DEFAULT, Color.DEFAULT)
    DUPLICATE = (Shape.DUPLICATE, Color.DUPLICATE, Color.DUPLICATE)
    PROJECTION = (Shape.PROJECTION, Color.PROJECTION, Color.PROJECTION)
    VALUE = (Shape.VALUE, Color.VALUE, Color.VALUE)
    VALUES = (Shape.VALUES, Color.VALUES, Color.VALUES)
    TYPE = (Shape.TYPE, Color.TYPE, Color.TYPE)

    blankCount = 0
    subgraphes = dict()
    nodeAlreadyAdded = set()

    def __init__(self, cluster : Cluster, **attr): #May add MINUS (need to know operand order)
        super().__init__(None, **attr)

        if cluster.name in SubDigraph.subgraphes:
            return
        
        SubDigraph.subgraphes[cluster.name] = self
        
        self.cluster = cluster

        self.addTSSes()
        self.addAliases()
        
        if cluster.name == "cluster0":
            for p in cluster.projections:
                self.addNode(p, p, *SubDigraph.PROJECTION)

        for s in cluster.subclusters:
            SubDigraph(s)
        
        self.addValues()

    @staticmethod
    def getNextBlankIdentifier():
        """
        If name is None, return a unique blank node identifier
        else name
        """

        SubDigraph.blankCount += 1
        return f"blank_{SubDigraph.blankCount}"
    
    @staticmethod
    def reset():
        SubDigraph.blankCount = 0
        SubDigraph.subgraphes = dict()
        SubDigraph.nodeAlreadyAdded = set()

    @staticmethod
    def allSubgraphsToDot(name, format = "png", view = False, cleanup=False):
        graph = Digraph(name)
        graph.graph_attr["rankdir"] = "LR"
        projections = { "cluster0_" + p for p in SubDigraph.subgraphes["cluster0"].cluster.getProjections() }

        sg = dict()

        for name in SubDigraph.subgraphes:
            g = Digraph(name)
            if name != "cluster0":
                g.graph_attr["style"] = SubDigraph.subgraphes[name].cluster.getStyle()
                g.graph_attr["label"] = SubDigraph.subgraphes[name].cluster.getLabel()
            else:
                g.graph_attr["style"] = "invis"

            for node in SubDigraph.subgraphes[name].nodes:            
                x = SubDigraph.subgraphes[name].cluster.getClusterName(node[node.find('_')+1:])
                if x is None or x == name:
                    if node in projections:
                        g.node(hex(hash(node)), label=SubDigraph.subgraphes[name].nodes[node]["label"], shape=Shape.PROJECTION, color=Color.PROJECTION, fontcolor=Color.PROJECTION)
                        projections.remove(node)
                    else:
                        g.node(hex(hash(node)), **SubDigraph.subgraphes[name].nodes[node])
        
            for edge in SubDigraph.subgraphes[name].edges:
                graph.edge(hex(hash(edge[0])), hex(hash(edge[1])), **SubDigraph.subgraphes[name].edges[edge])
                    
            sg[g.name] = g

        def __linksubgraph(sdg : SubDigraph):
            for s in sdg.cluster.subclusters:
                __linksubgraph(SubDigraph.subgraphes[s.name])
                sg[sdg.cluster.name].subgraph(sg[s.name])
            
        __linksubgraph(SubDigraph.subgraphes["cluster0"])
        graph.subgraph(sg["cluster0"])

        #Render 
        graph.format = format
        if view:
            graph.view(cleanup=cleanup)
        else:
            graph.render(cleanup=cleanup)

    def prefixVar(self, name):
        """
        Prefix a node name by its owner select name
        If no select owner were found, use current select as owner
        """

        n = self.cluster.getClusterName(name)
        if n is None:
            n = self.cluster.name
        return f"{n}_{name}"
    
    def getBlankNodeFrom(self, origin, by):
        for e in self.edges:
            if e[0] == origin and self.edges[e]["label"] == by:
                return e[1]
            
    def addNode(self, name = None, label = "[]", shape = Shape.DEFAULT, color = Color.DEFAULT, fontcolor = Color.DEFAULT):
        """
        Add a node to Networkx graph by resolving its identifier and setting its attributes
        Return resolved name 
        """

        #Blank node
        if name is None:
            if label == "[]":
                shape, color, fontcolor = SubDigraph.BLANK

            name = f"{self.cluster.name}_{self.getNextBlankIdentifier()}"
        #Node
        else:
            name = self.prefixVar(name)
        if name not in SubDigraph.nodeAlreadyAdded:
            self.add_node(name, label=label, shape=shape, color=color, fontcolor=fontcolor)
            SubDigraph.nodeAlreadyAdded.add(name)
        return name

    def addValues(self):
        for value in self.cluster.values:
            g = self.cluster.getClusterName(value)
            n = f"{g}_{value}"
            
            #Path values

            if g == self.cluster.name and n not in self.nodes :
                n = self.addNode(None, '\n' + value, shape="primersite", color="black", fontcolor="black")
            for v in self.cluster.values[value]:
                self.add_edge(n, self.addNode(None, v.replace("^^xsd:string", ""), *SubDigraph.VALUES), label="VALUE", color=Color.VALUES, fontcolor=Color.VALUES, style=Style.DEFAULT, arrowhead=ArrowStyle.DEFAULT)
    
    def addTSSes(self):
        """
        Create all nodes and edges from a list of TSS

        tsses : List[TSS]
            List of TSS instances that defines all TriplesSameSubjectPaths of the query
        """

        asNode = dict()
        if self.cluster.name != "cluster0":
            for tss in self.cluster.tss:
                if tss.subject not in asNode:
                    xsubject = self.cluster.getClusterName(tss.subject)
                
                    if xsubject is None:
                        print(f"WARNING: {tss.subject} PLACED IN {self.cluster.name}")
                        xsubject = self.cluster.name

                    if xsubject != self.cluster.name:
                        asNode[tss.subject] = self.addNode(f"duplicate_{tss.subject}", tss.subject, *SubDigraph.DUPLICATE)
                        self.add_edge(SubDigraph.subgraphes[xsubject].addNode(tss.subject, tss.subject), asNode[tss.subject], label="", color=Color.DUPLICATE, style=Style.DUPLICATE, arrowhead=ArrowStyle.DUPLICATE)
        
                for path in tss.paths:
                    if path[-1] not in asNode and (path[-1].startswith('?') or path[-1].startswith('$')):
                        xend = self.cluster.getClusterName(path[-1])
                        if xend is None:
                            print(f"WARNING: {path[-1]} PLACED IN {self.cluster.name}")
                            xend = self.cluster.name

                        if xend != self.cluster.name:
                            asNode[path[-1]] = self.addNode(f"duplicate_{path[-1]}", path[-1], *SubDigraph.DUPLICATE)
                            self.add_edge(asNode[path[-1]], SubDigraph.subgraphes[xend].addNode(path[-1], path[-1]), label="", color=Color.DUPLICATE, style=Style.DUPLICATE, arrowhead=ArrowStyle.DUPLICATE)        

        for tss in self.cluster.tss:
            if tss.subject in asNode:
                sNode = asNode[tss.subject]
            else:
                sNode = self.addNode(tss.subject, tss.subject)

            for path in tss.paths:
                bNode = sNode
                for i in range(len(path)-1):
                    #Check end of TSS
                    if i == len(path) - 2:
                        #Variable at end
                        if path[i+1].startswith('?') or path[i+1].startswith('$'):
                            if path[i+1] in asNode:
                                self.add_edge(bNode, asNode[path[i+1]], label=path[i], style=Style.DEFAULT, arrowhead=ArrowStyle.DEFAULT)
                            else:
                                self.add_edge(bNode, self.addNode(path[i+1], path[i+1]), label=path[i], style=Style.DEFAULT, arrowhead=ArrowStyle.DEFAULT)
                        #Value at end (value is terminal)
                        elif path[i+1].startswith('"') and path[i+1].endswith('"'):
                            xsdstring = self.prefixVar(path[i+1]) not in self.nodes
                            n = self.addNode(path[i+1], path[i+1], *SubDigraph.VALUE)
                            if xsdstring:
                                self.add_edge(n, self.addNode(None, "xsd:string", *SubDigraph.TYPE), label="TYPE", color=Color.TYPE, fontcolor=Color.TYPE, style=Style.TYPE, arrowhead=ArrowStyle.TYPE)
                            self.add_edge(bNode, n, label=path[i])
                        #Link blank node to end
                        else:
                            self.add_edge(bNode, self.addNode(path[i+1], path[i+1], *SubDigraph.VALUE), label=path[i], style=Style.DEFAULT, arrowhead=ArrowStyle.DEFAULT)
                    #Link blank nodes together
                    else:
                        n = self.getBlankNodeFrom(bNode, path[i])
                        if n is None:
                            tmp, bNode = bNode, self.addNode()
                            self.add_edge(tmp, bNode, label=path[i], style=Style.DEFAULT, arrowhead=ArrowStyle.DEFAULT)
                        else:
                            tmp, bNode = bNode, n

    def addAliases(self):
        d = self.cluster.getAliases()
        for a in d:
            aNode = self.addNode(None, d[a].getText(), *SubDigraph.ALIAS)
            self.add_edge(aNode, self.addNode(d[a].getTarget(), d[a].getTarget()), label="AS", style=Style.ALIAS_OUT, arrowhead=ArrowStyle.ALIAS_OUT)
            for i in d[a].getVars():
                self.add_edge(self.addNode(i, i), aNode, color=Color.ALIAS_IN, style=Style.ALIAS_IN, arrowhead=ArrowStyle.ALIAS_IN)

def parse_file(file, verbose=False):
    """
    file : str, path of file
    verbose : bool, true will make a lot of prints
    """
    input_stream = FileStream(file, encoding="utf-8")
    lexer = SparqlLexer(input_stream)
    stream = CommonTokenStream(lexer)
    listener = SAL(verbose)  
    ParseTreeWalker.DEFAULT.walk(listener, SparqlParser(stream).statement()) #statement() is the tree entry
    return listener.getMainClusters()[0]

# This class defines a complete listener for a parse tree produced by SparqlParser.
class SAL(SparqlListener):
    """
    Class that tracks AST rules
    """
    def __init__(self, verbose = False):
        #Flags
        self.alias = False
        self.datablock = False
        self.isVerbPath = False
        self.modifier = False
        self.filter = False
        self.verbose = verbose
        self.blank = False

        #Dicts
        self.prefixNamespace = dict()
        self.prefixCurie = dict()

        #Logic
        self.mainclusters = []
        self.clusters = deque()
        self.currentTSS = None
        self.datavars = None
        self.datavalues = None
        self.__ctx = None
        self.expressionLevel = 0
        self.expressionText = None
        self.expressionVars = []
        self.indent = 0
    
    def enter(self, ctx):
        if self.verbose:
            print(" "*self.indent, ">", ctx.__class__.__name__[:-7], sep="")
            self.indent += 1

        self.__ctx = ctx
        pass

    def exit(self, ctx):
        if self.verbose:
            if self.__ctx == ctx:
                print(ctx.getText())
            print(" "*(self.indent-1), "<", ctx.__class__.__name__[:-7], sep="")
            self.indent -= 1

        #TODO: remove explicit xsd:string 
        if self.currentTSS and self.__ctx == ctx and ctx.getText() != "xsd:string" and not self.modifier and not isinstance(ctx, SparqlParser.PathModContext):
            if self.blank:
                self.currentTSS.addToBlank(ctx.getText())
            else:
                self.currentTSS.addToPath(ctx.getText(), self.isVerbPath)
        pass

    def addCluster(self, label, style = Style.DEFAULT):
        s = Cluster(label, style)
        if self.clusters:
            self.clusters[-1].addSubCluster(s)
        else:
            self.mainclusters.append(s)
        
        self.clusters.append(s)
        return s

    def getMainClusters(self):
        return self.mainclusters[:]
    
    # Enter a parse tree produced by SparqlParser#statement.
    def enterStatement(self, ctx:SparqlParser.StatementContext):
        self.enter(ctx)
        pass    

    # Exit a parse tree produced by SparqlParser#statement.
    def exitStatement(self, ctx:SparqlParser.StatementContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#query.
    def enterQuery(self, ctx:SparqlParser.QueryContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#query.
    def exitQuery(self, ctx:SparqlParser.QueryContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#prologue.
    def enterPrologue(self, ctx:SparqlParser.PrologueContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#prologue.
    def exitPrologue(self, ctx:SparqlParser.PrologueContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#baseDecl.
    def enterBaseDecl(self, ctx:SparqlParser.BaseDeclContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#baseDecl.
    def exitBaseDecl(self, ctx:SparqlParser.BaseDeclContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#prefixDecl.
    def enterPrefixDecl(self, ctx:SparqlParser.PrefixDeclContext):
        """
        Store in dictionary prefix couples (value-key, key-value)
        """
        self.enter(ctx)
        self.prefixNamespace[ctx.PNAME_NS()] = ctx.IRIREF()
        self.prefixCurie[ctx.IRIREF()] = ctx.PNAME_NS()
        pass

    # Exit a parse tree produced by SparqlParser#prefixDecl.
    def exitPrefixDecl(self, ctx:SparqlParser.PrefixDeclContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#selectQuery.
    def enterSelectQuery(self, ctx:SparqlParser.SelectQueryContext):
        self.enter(ctx)
        self.addCluster("SELECT", Style.SELECT)
        pass

    # Exit a parse tree produced by SparqlParser#selectQuery.
    def exitSelectQuery(self, ctx:SparqlParser.SelectQueryContext):
        self.clusters.pop()
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#subSelect.
    def enterSubSelect(self, ctx:SparqlParser.SubSelectContext):
        self.enter(ctx)
        self.addCluster("SELECT", Style.SELECT)
        pass

    # Exit a parse tree produced by SparqlParser#subSelect.
    def exitSubSelect(self, ctx:SparqlParser.SubSelectContext):
        self.clusters.pop()
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#selectClause.
    def enterSelectClause(self, ctx:SparqlParser.SelectClauseContext):
        self.enter(ctx)
        self.alias = True
        pass

    # Exit a parse tree produced by SparqlParser#selectClause.
    def exitSelectClause(self, ctx:SparqlParser.SelectClauseContext):
        self.clusters[-1].setProjections([v.getText() for v in ctx.var()])
        self.alias = False 
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#constructQuery.
    def enterConstructQuery(self, ctx:SparqlParser.ConstructQueryContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#constructQuery.
    def exitConstructQuery(self, ctx:SparqlParser.ConstructQueryContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#describeQuery.
    def enterDescribeQuery(self, ctx:SparqlParser.DescribeQueryContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#describeQuery.
    def exitDescribeQuery(self, ctx:SparqlParser.DescribeQueryContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#askQuery.
    def enterAskQuery(self, ctx:SparqlParser.AskQueryContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#askQuery.
    def exitAskQuery(self, ctx:SparqlParser.AskQueryContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#datasetClause.
    def enterDatasetClause(self, ctx:SparqlParser.DatasetClauseContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#datasetClause.
    def exitDatasetClause(self, ctx:SparqlParser.DatasetClauseContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#defaultGraphClause.
    def enterDefaultGraphClause(self, ctx:SparqlParser.DefaultGraphClauseContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#defaultGraphClause.
    def exitDefaultGraphClause(self, ctx:SparqlParser.DefaultGraphClauseContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#namedGraphClause.
    def enterNamedGraphClause(self, ctx:SparqlParser.NamedGraphClauseContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#namedGraphClause.
    def exitNamedGraphClause(self, ctx:SparqlParser.NamedGraphClauseContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#sourceSelector.
    def enterSourceSelector(self, ctx:SparqlParser.SourceSelectorContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#sourceSelector.
    def exitSourceSelector(self, ctx:SparqlParser.SourceSelectorContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#whereClause.
    def enterWhereClause(self, ctx:SparqlParser.WhereClauseContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#whereClause.
    def exitWhereClause(self, ctx:SparqlParser.WhereClauseContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#solutionModifier.
    def enterSolutionModifier(self, ctx:SparqlParser.SolutionModifierContext):
        self.enter(ctx)
        self.modifier = True
        pass

    # Exit a parse tree produced by SparqlParser#solutionModifier.
    def exitSolutionModifier(self, ctx:SparqlParser.SolutionModifierContext):
        self.exit(ctx)
        self.modifier = False
        pass

    # Enter a parse tree produced by SparqlParser#groupClause.
    def enterGroupClause(self, ctx:SparqlParser.GroupClauseContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#groupClause.
    def exitGroupClause(self, ctx:SparqlParser.GroupClauseContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#groupCondition.
    def enterGroupCondition(self, ctx:SparqlParser.GroupConditionContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#groupCondition.
    def exitGroupCondition(self, ctx:SparqlParser.GroupConditionContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#havingClause.
    def enterHavingClause(self, ctx:SparqlParser.HavingClauseContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#havingClause.
    def exitHavingClause(self, ctx:SparqlParser.HavingClauseContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#havingCondition.
    def enterHavingCondition(self, ctx:SparqlParser.HavingConditionContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#havingCondition.
    def exitHavingCondition(self, ctx:SparqlParser.HavingConditionContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#orderClause.
    def enterOrderClause(self, ctx:SparqlParser.OrderClauseContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#orderClause.
    def exitOrderClause(self, ctx:SparqlParser.OrderClauseContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#orderCondition.
    def enterOrderCondition(self, ctx:SparqlParser.OrderConditionContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#orderCondition.
    def exitOrderCondition(self, ctx:SparqlParser.OrderConditionContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#limitOffsetClauses.
    def enterLimitOffsetClauses(self, ctx:SparqlParser.LimitOffsetClausesContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#limitOffsetClauses.
    def exitLimitOffsetClauses(self, ctx:SparqlParser.LimitOffsetClausesContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#limitClause.
    def enterLimitClause(self, ctx:SparqlParser.LimitClauseContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#limitClause.
    def exitLimitClause(self, ctx:SparqlParser.LimitClauseContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#offsetClause.
    def enterOffsetClause(self, ctx:SparqlParser.OffsetClauseContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#offsetClause.
    def exitOffsetClause(self, ctx:SparqlParser.OffsetClauseContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#valuesClause.
    def enterValuesClause(self, ctx:SparqlParser.ValuesClauseContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#valuesClause.
    def exitValuesClause(self, ctx:SparqlParser.ValuesClauseContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#update.
    def enterUpdate(self, ctx:SparqlParser.UpdateContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#update.
    def exitUpdate(self, ctx:SparqlParser.UpdateContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#update1.
    def enterUpdate1(self, ctx:SparqlParser.Update1Context):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#update1.
    def exitUpdate1(self, ctx:SparqlParser.Update1Context):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#load.
    def enterLoad(self, ctx:SparqlParser.LoadContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#load.
    def exitLoad(self, ctx:SparqlParser.LoadContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#clear.
    def enterClear(self, ctx:SparqlParser.ClearContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#clear.
    def exitClear(self, ctx:SparqlParser.ClearContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#drop.
    def enterDrop(self, ctx:SparqlParser.DropContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#drop.
    def exitDrop(self, ctx:SparqlParser.DropContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#create.
    def enterCreate(self, ctx:SparqlParser.CreateContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#create.
    def exitCreate(self, ctx:SparqlParser.CreateContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#add.
    def enterAdd(self, ctx:SparqlParser.AddContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#add.
    def exitAdd(self, ctx:SparqlParser.AddContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#move.
    def enterMove(self, ctx:SparqlParser.MoveContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#move.
    def exitMove(self, ctx:SparqlParser.MoveContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#copy.
    def enterCopy(self, ctx:SparqlParser.CopyContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#copy.
    def exitCopy(self, ctx:SparqlParser.CopyContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#insertData.
    def enterInsertData(self, ctx:SparqlParser.InsertDataContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#insertData.
    def exitInsertData(self, ctx:SparqlParser.InsertDataContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#deleteData.
    def enterDeleteData(self, ctx:SparqlParser.DeleteDataContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#deleteData.
    def exitDeleteData(self, ctx:SparqlParser.DeleteDataContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#deleteWhere.
    def enterDeleteWhere(self, ctx:SparqlParser.DeleteWhereContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#deleteWhere.
    def exitDeleteWhere(self, ctx:SparqlParser.DeleteWhereContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#modify.
    def enterModify(self, ctx:SparqlParser.ModifyContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#modify.
    def exitModify(self, ctx:SparqlParser.ModifyContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#deleteClause.
    def enterDeleteClause(self, ctx:SparqlParser.DeleteClauseContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#deleteClause.
    def exitDeleteClause(self, ctx:SparqlParser.DeleteClauseContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#insertClause.
    def enterInsertClause(self, ctx:SparqlParser.InsertClauseContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#insertClause.
    def exitInsertClause(self, ctx:SparqlParser.InsertClauseContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#usingClause.
    def enterUsingClause(self, ctx:SparqlParser.UsingClauseContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#usingClause.
    def exitUsingClause(self, ctx:SparqlParser.UsingClauseContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#graphOrDefault.
    def enterGraphOrDefault(self, ctx:SparqlParser.GraphOrDefaultContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#graphOrDefault.
    def exitGraphOrDefault(self, ctx:SparqlParser.GraphOrDefaultContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#graphRef.
    def enterGraphRef(self, ctx:SparqlParser.GraphRefContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#graphRef.
    def exitGraphRef(self, ctx:SparqlParser.GraphRefContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#graphRefAll.
    def enterGraphRefAll(self, ctx:SparqlParser.GraphRefAllContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#graphRefAll.
    def exitGraphRefAll(self, ctx:SparqlParser.GraphRefAllContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#quadPattern.
    def enterQuadPattern(self, ctx:SparqlParser.QuadPatternContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#quadPattern.
    def exitQuadPattern(self, ctx:SparqlParser.QuadPatternContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#quadData.
    def enterQuadData(self, ctx:SparqlParser.QuadDataContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#quadData.
    def exitQuadData(self, ctx:SparqlParser.QuadDataContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#quads.
    def enterQuads(self, ctx:SparqlParser.QuadsContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#quads.
    def exitQuads(self, ctx:SparqlParser.QuadsContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#quadsNotTriples.
    def enterQuadsNotTriples(self, ctx:SparqlParser.QuadsNotTriplesContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#quadsNotTriples.
    def exitQuadsNotTriples(self, ctx:SparqlParser.QuadsNotTriplesContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#triplesTemplate.
    def enterTriplesTemplate(self, ctx:SparqlParser.TriplesTemplateContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#triplesTemplate.
    def exitTriplesTemplate(self, ctx:SparqlParser.TriplesTemplateContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#groupGraphPattern.
    def enterGroupGraphPattern(self, ctx:SparqlParser.GroupGraphPatternContext):
        self.enter(ctx)
        if self.clusters[-1].getLabel() in ("UNION", ""):
            self.addCluster("", Style.GROUP)
        pass

    # Exit a parse tree produced by SparqlParser#groupGraphPattern.
    def exitGroupGraphPattern(self, ctx:SparqlParser.GroupGraphPatternContext):
        self.exit(ctx)
        if self.clusters[-1].getLabel() == "":
            #Remove sub blank cluster if it has only one subcluster and no TSS !
            u = self.clusters.pop()

            if len(u.tss) == 0:
                if self.clusters:
                    for s in u.subclusters:
                        self.clusters[-1].addSubCluster(s)
                    self.clusters[-1].subclusters.remove(u)
                    self.clusters[-1].tss.extend(u.tss)
                else:
                    for s in u.subclusters:
                        self.mainclusters[-1].addSubCluster(s)
                    self.mainclusters[-1].subclusters.remove(u)
                    self.mainclusters[-1].tss.extend(u.tss)


        pass

    # Enter a parse tree produced by SparqlParser#groupGraphPatternSub.
    def enterGroupGraphPatternSub(self, ctx:SparqlParser.GroupGraphPatternSubContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#groupGraphPatternSub.
    def exitGroupGraphPatternSub(self, ctx:SparqlParser.GroupGraphPatternSubContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#triplesBlock.
    def enterTriplesBlock(self, ctx:SparqlParser.TriplesBlockContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#triplesBlock.
    def exitTriplesBlock(self, ctx:SparqlParser.TriplesBlockContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#graphPatternNotTriples.
    def enterGraphPatternNotTriples(self, ctx:SparqlParser.GraphPatternNotTriplesContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#graphPatternNotTriples.
    def exitGraphPatternNotTriples(self, ctx:SparqlParser.GraphPatternNotTriplesContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#optionalGraphPattern.
    def enterOptionalGraphPattern(self, ctx:SparqlParser.OptionalGraphPatternContext):
        self.enter(ctx)
        self.addCluster("OPTIONAL", Style.OPTIONAL)
        pass

    # Exit a parse tree produced by SparqlParser#optionalGraphPattern.
    def exitOptionalGraphPattern(self, ctx:SparqlParser.OptionalGraphPatternContext):
        self.exit(ctx)
        self.clusters.pop()
        pass

    # Enter a parse tree produced by SparqlParser#graphGraphPattern.
    def enterGraphGraphPattern(self, ctx:SparqlParser.GraphGraphPatternContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#graphGraphPattern.
    def exitGraphGraphPattern(self, ctx:SparqlParser.GraphGraphPatternContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#serviceGraphPattern.
    def enterServiceGraphPattern(self, ctx:SparqlParser.ServiceGraphPatternContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#serviceGraphPattern.
    def exitServiceGraphPattern(self, ctx:SparqlParser.ServiceGraphPatternContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#bind.
    def enterBind(self, ctx:SparqlParser.BindContext):
        self.enter(ctx)
        self.alias = True        
        pass

    # Exit a parse tree produced by SparqlParser#bind.
    def exitBind(self, ctx:SparqlParser.BindContext):
        self.alias = False
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#inlineData.
    def enterInlineData(self, ctx:SparqlParser.InlineDataContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#inlineData.
    def exitInlineData(self, ctx:SparqlParser.InlineDataContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#dataBlock.
    def enterDataBlock(self, ctx:SparqlParser.DataBlockContext):
        self.enter(ctx)
        self.datablock = True
        self.datavalues = []
        self.datavars = []
        pass

    # Exit a parse tree produced by SparqlParser#dataBlock.
    def exitDataBlock(self, ctx:SparqlParser.DataBlockContext):
        self.exit(ctx)
        for v in self.datavars:
            self.clusters[-1].addVarValues(v, self.datavalues)
        self.datablock = False
        self.datavalues = None
        self.datavars = None
        pass

    # Enter a parse tree produced by SparqlParser#inlineDataOneVar.
    def enterInlineDataOneVar(self, ctx:SparqlParser.InlineDataOneVarContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#inlineDataOneVar.
    def exitInlineDataOneVar(self, ctx:SparqlParser.InlineDataOneVarContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#inlineDataFull.
    def enterInlineDataFull(self, ctx:SparqlParser.InlineDataFullContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#inlineDataFull.
    def exitInlineDataFull(self, ctx:SparqlParser.InlineDataFullContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#dataBlockValue.
    def enterDataBlockValue(self, ctx:SparqlParser.DataBlockValueContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#dataBlockValue.
    def exitDataBlockValue(self, ctx:SparqlParser.DataBlockValueContext):
        self.exit(ctx)
        self.datavalues.append(ctx.getText())
        pass

    # Enter a parse tree produced by SparqlParser#minusGraphPattern.
    def enterMinusGraphPattern(self, ctx:SparqlParser.MinusGraphPatternContext):
        self.enter(ctx)
        #self.addCluster("MINUS")
        pass

    # Exit a parse tree produced by SparqlParser#minusGraphPattern.
    def exitMinusGraphPattern(self, ctx:SparqlParser.MinusGraphPatternContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#groupOrUnionGraphPattern.
    def enterGroupOrUnionGraphPattern(self, ctx:SparqlParser.GroupOrUnionGraphPatternContext):
        self.enter(ctx)
        self.addCluster("UNION", Style.UNION)
        pass

    # Exit a parse tree produced by SparqlParser#groupOrUnionGraphPattern.
    def exitGroupOrUnionGraphPattern(self, ctx:SparqlParser.GroupOrUnionGraphPatternContext):
        self.exit(ctx)
        
        if self.clusters:
            u = self.clusters.pop()
            if "}union{" not in ctx.getText().lower():
                if self.clusters:
                    for s in u.subclusters:
                        self.clusters[-1].addSubCluster(s)
                    self.clusters[-1].subclusters.remove(u)
                    self.clusters[-1].tss.extend(u.tss)
                else:
                    for s in u.subclusters:
                        self.mainclusters[-1].addSubCluster(s)
                    self.mainclusters[-1].subclusters.remove(u)
                    self.mainclusters[-1].tss.extend(u.tss)
        pass

    # Enter a parse tree produced by SparqlParser#filterClause.
    def enterFilterClause(self, ctx:SparqlParser.FilterClauseContext):
        self.enter(ctx)
        self.addCluster("FILTER", Style.FILTER)
        pass

    # Exit a parse tree produced by SparqlParser#filterClause.
    def exitFilterClause(self, ctx:SparqlParser.FilterClauseContext):
        self.exit(ctx)
        self.clusters.pop()
        pass

    # Enter a parse tree produced by SparqlParser#constraint.
    def enterConstraint(self, ctx:SparqlParser.ConstraintContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#constraint.
    def exitConstraint(self, ctx:SparqlParser.ConstraintContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#functionCall.
    def enterFunctionCall(self, ctx:SparqlParser.FunctionCallContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#functionCall.
    def exitFunctionCall(self, ctx:SparqlParser.FunctionCallContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#argList.
    def enterArgList(self, ctx:SparqlParser.ArgListContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#argList.
    def exitArgList(self, ctx:SparqlParser.ArgListContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#expressionList.
    def enterExpressionList(self, ctx:SparqlParser.ExpressionListContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#expressionList.
    def exitExpressionList(self, ctx:SparqlParser.ExpressionListContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#constructTemplate.
    def enterConstructTemplate(self, ctx:SparqlParser.ConstructTemplateContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#constructTemplate.
    def exitConstructTemplate(self, ctx:SparqlParser.ConstructTemplateContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#constructTriples.
    def enterConstructTriples(self, ctx:SparqlParser.ConstructTriplesContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#constructTriples.
    def exitConstructTriples(self, ctx:SparqlParser.ConstructTriplesContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#triplesSameSubject.
    def enterTriplesSameSubject(self, ctx:SparqlParser.TriplesSameSubjectContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#triplesSameSubject.
    def exitTriplesSameSubject(self, ctx:SparqlParser.TriplesSameSubjectContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#propertyList.
    def enterPropertyList(self, ctx:SparqlParser.PropertyListContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#propertyList.
    def exitPropertyList(self, ctx:SparqlParser.PropertyListContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#propertyListNotEmpty.
    def enterPropertyListNotEmpty(self, ctx:SparqlParser.PropertyListNotEmptyContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#propertyListNotEmpty.
    def exitPropertyListNotEmpty(self, ctx:SparqlParser.PropertyListNotEmptyContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#verb.
    def enterVerb(self, ctx:SparqlParser.VerbContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#verb.
    def exitVerb(self, ctx:SparqlParser.VerbContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#objectList.
    def enterObjectList(self, ctx:SparqlParser.ObjectListContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#objectList.
    def exitObjectList(self, ctx:SparqlParser.ObjectListContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#objectClause.
    def enterObjectClause(self, ctx:SparqlParser.ObjectClauseContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#objectClause.
    def exitObjectClause(self, ctx:SparqlParser.ObjectClauseContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#triplesSameSubjectPath.
    def enterTriplesSameSubjectPath(self, ctx:SparqlParser.TriplesSameSubjectPathContext):
        self.enter(ctx)
        self.currentTSS = TSS()
        self.clusters[-1].addTSS(self.currentTSS)
        pass

    # Exit a parse tree produced by SparqlParser#triplesSameSubjectPath.
    def exitTriplesSameSubjectPath(self, ctx:SparqlParser.TriplesSameSubjectPathContext):
        self.currentTSS.close()
        self.currentTSS = None
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#propertyListPath.
    def enterPropertyListPath(self, ctx:SparqlParser.PropertyListPathContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#propertyListPath.
    def exitPropertyListPath(self, ctx:SparqlParser.PropertyListPathContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#propertyListPathNotEmpty.
    def enterPropertyListPathNotEmpty(self, ctx:SparqlParser.PropertyListPathNotEmptyContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#propertyListPathNotEmpty.
    def exitPropertyListPathNotEmpty(self, ctx:SparqlParser.PropertyListPathNotEmptyContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#verbPath.
    def enterVerbPath(self, ctx:SparqlParser.VerbPathContext):
        self.enter(ctx)
        self.isVerbPath = True
        pass

    # Exit a parse tree produced by SparqlParser#verbPath.
    def exitVerbPath(self, ctx:SparqlParser.VerbPathContext):
        self.exit(ctx)
        self.isVerbPath = False
        pass

    # Enter a parse tree produced by SparqlParser#verbSimple.
    def enterVerbSimple(self, ctx:SparqlParser.VerbSimpleContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#verbSimple.
    def exitVerbSimple(self, ctx:SparqlParser.VerbSimpleContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#objectListPath.
    def enterObjectListPath(self, ctx:SparqlParser.ObjectListPathContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#objectListPath.
    def exitObjectListPath(self, ctx:SparqlParser.ObjectListPathContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#objectPath.
    def enterObjectPath(self, ctx:SparqlParser.ObjectPathContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#objectPath.
    def exitObjectPath(self, ctx:SparqlParser.ObjectPathContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#path.
    def enterPath(self, ctx:SparqlParser.PathContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#path.
    def exitPath(self, ctx:SparqlParser.PathContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#pathAlternative.
    def enterPathAlternative(self, ctx:SparqlParser.PathAlternativeContext):
        self.enter(ctx)
        pass    

    # Exit a parse tree produced by SparqlParser#pathAlternative.
    def exitPathAlternative(self, ctx:SparqlParser.PathAlternativeContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#pathSequence.
    def enterPathSequence(self, ctx:SparqlParser.PathSequenceContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#pathSequence.
    def exitPathSequence(self, ctx:SparqlParser.PathSequenceContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#pathElt.
    def enterPathElt(self, ctx:SparqlParser.PathEltContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#pathElt.
    def exitPathElt(self, ctx:SparqlParser.PathEltContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#pathEltOrInverse.
    def enterPathEltOrInverse(self, ctx:SparqlParser.PathEltOrInverseContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#pathEltOrInverse.
    def exitPathEltOrInverse(self, ctx:SparqlParser.PathEltOrInverseContext):
        if ctx.getText().startswith('^'):
            self.currentTSS.paths[-1][-1] = '^' + self.currentTSS.paths[-1][-1]
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#pathMod.
    def enterPathMod(self, ctx:SparqlParser.PathModContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#pathMod.
    def exitPathMod(self, ctx:SparqlParser.PathModContext):
        self.currentTSS.paths[-1][-1] = self.currentTSS.paths[-1][-1] + ctx.getText()
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#pathPrimary.
    def enterPathPrimary(self, ctx:SparqlParser.PathPrimaryContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#pathPrimary.
    def exitPathPrimary(self, ctx:SparqlParser.PathPrimaryContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#pathNegatedPropertySet.
    def enterPathNegatedPropertySet(self, ctx:SparqlParser.PathNegatedPropertySetContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#pathNegatedPropertySet.
    def exitPathNegatedPropertySet(self, ctx:SparqlParser.PathNegatedPropertySetContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#pathOneInPropertySet.
    def enterPathOneInPropertySet(self, ctx:SparqlParser.PathOneInPropertySetContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#pathOneInPropertySet.
    def exitPathOneInPropertySet(self, ctx:SparqlParser.PathOneInPropertySetContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#triplesNode.
    def enterTriplesNode(self, ctx:SparqlParser.TriplesNodeContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#triplesNode.
    def exitTriplesNode(self, ctx:SparqlParser.TriplesNodeContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#blankNodePropertyList.
    def enterBlankNodePropertyList(self, ctx:SparqlParser.BlankNodePropertyListContext):
        self.enter(ctx)
        self.currentTSS.openBlankPath()
        self.blank = True
        pass

    # Exit a parse tree produced by SparqlParser#blankNodePropertyList.
    def exitBlankNodePropertyList(self, ctx:SparqlParser.BlankNodePropertyListContext):
        self.exit(ctx)
        self.currentTSS.closeBlankPath()
        self.blank = False
        pass

    # Enter a parse tree produced by SparqlParser#triplesNodePath.
    def enterTriplesNodePath(self, ctx:SparqlParser.TriplesNodePathContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#triplesNodePath.
    def exitTriplesNodePath(self, ctx:SparqlParser.TriplesNodePathContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#blankNodePropertyListPath.
    def enterBlankNodePropertyListPath(self, ctx:SparqlParser.BlankNodePropertyListPathContext):
        self.enter(ctx)
        self.currentTSS.openBlankPath()
        pass

    # Exit a parse tree produced by SparqlParser#blankNodePropertyListPath.
    def exitBlankNodePropertyListPath(self, ctx:SparqlParser.BlankNodePropertyListPathContext):
        self.exit(ctx)
        self.currentTSS.closeBlankPath()
        pass

    # Enter a parse tree produced by SparqlParser#collection.
    def enterCollection(self, ctx:SparqlParser.CollectionContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#collection.
    def exitCollection(self, ctx:SparqlParser.CollectionContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#collectionPath.
    def enterCollectionPath(self, ctx:SparqlParser.CollectionPathContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#collectionPath.
    def exitCollectionPath(self, ctx:SparqlParser.CollectionPathContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#graphNode.
    def enterGraphNode(self, ctx:SparqlParser.GraphNodeContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#graphNode.
    def exitGraphNode(self, ctx:SparqlParser.GraphNodeContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#graphNodePath.
    def enterGraphNodePath(self, ctx:SparqlParser.GraphNodePathContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#graphNodePath.
    def exitGraphNodePath(self, ctx:SparqlParser.GraphNodePathContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#varOrTerm.
    def enterVarOrTerm(self, ctx:SparqlParser.VarOrTermContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#varOrTerm.
    def exitVarOrTerm(self, ctx:SparqlParser.VarOrTermContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#varOrIri.
    def enterVarOrIri(self, ctx:SparqlParser.VarOrIriContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#varOrIri.
    def exitVarOrIri(self, ctx:SparqlParser.VarOrIriContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#var.
    def enterVar(self, ctx:SparqlParser.VarContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#var.
    def exitVar(self, ctx:SparqlParser.VarContext):
        self.exit(ctx)
        if self.modifier:
            return
        
        self.clusters[-1].addVar(ctx.getText())

        if self.alias:
            if self.expressionLevel > 0:
                if self.expressionVars:
                    self.expressionVars.append(ctx.getText())
                else:
                    self.expressionVars = [ctx.getText()]
            elif self.expressionLevel == 0 and self.expressionVars:
                self.clusters[-1].addAlias(self.expressionVars, ctx.getText(), self.expressionText)
                self.expressionVars = None
                self.expressionText = None
        elif self.datablock:
            self.datavars.append(ctx.getText())
        pass

    # Enter a parse tree produced by SparqlParser#graphTerm.
    def enterGraphTerm(self, ctx:SparqlParser.GraphTermContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#graphTerm.
    def exitGraphTerm(self, ctx:SparqlParser.GraphTermContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#expression.
    def enterExpression(self, ctx:SparqlParser.ExpressionContext):
        self.enter(ctx)
        self.expressionLevel += 1
        pass

    # Exit a parse tree produced by SparqlParser#expression.
    def exitExpression(self, ctx:SparqlParser.ExpressionContext):
        self.exit(ctx)
        self.expressionLevel -= 1
        self.expressionText = ctx.getText()
        pass

    # Enter a parse tree produced by SparqlParser#conditionalOrExpression.
    def enterConditionalOrExpression(self, ctx:SparqlParser.ConditionalOrExpressionContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#conditionalOrExpression.
    def exitConditionalOrExpression(self, ctx:SparqlParser.ConditionalOrExpressionContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#conditionalAndExpression.
    def enterConditionalAndExpression(self, ctx:SparqlParser.ConditionalAndExpressionContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#conditionalAndExpression.
    def exitConditionalAndExpression(self, ctx:SparqlParser.ConditionalAndExpressionContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#valueLogical.
    def enterValueLogical(self, ctx:SparqlParser.ValueLogicalContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#valueLogical.
    def exitValueLogical(self, ctx:SparqlParser.ValueLogicalContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#relationalExpression.
    def enterRelationalExpression(self, ctx:SparqlParser.RelationalExpressionContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#relationalExpression.
    def exitRelationalExpression(self, ctx:SparqlParser.RelationalExpressionContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#numericExpression.
    def enterNumericExpression(self, ctx:SparqlParser.NumericExpressionContext):
        self.enter(ctx)
    
        pass

    # Exit a parse tree produced by SparqlParser#numericExpression.
    def exitNumericExpression(self, ctx:SparqlParser.NumericExpressionContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#additiveExpression.
    def enterAdditiveExpression(self, ctx:SparqlParser.AdditiveExpressionContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#additiveExpression.
    def exitAdditiveExpression(self, ctx:SparqlParser.AdditiveExpressionContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#multiplicativeExpression.
    def enterMultiplicativeExpression(self, ctx:SparqlParser.MultiplicativeExpressionContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#multiplicativeExpression.
    def exitMultiplicativeExpression(self, ctx:SparqlParser.MultiplicativeExpressionContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#unaryExpression.
    def enterUnaryExpression(self, ctx:SparqlParser.UnaryExpressionContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#unaryExpression.
    def exitUnaryExpression(self, ctx:SparqlParser.UnaryExpressionContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#primaryExpression.
    def enterPrimaryExpression(self, ctx:SparqlParser.PrimaryExpressionContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#primaryExpression.
    def exitPrimaryExpression(self, ctx:SparqlParser.PrimaryExpressionContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#brackettedExpression.
    def enterBrackettedExpression(self, ctx:SparqlParser.BrackettedExpressionContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#brackettedExpression.
    def exitBrackettedExpression(self, ctx:SparqlParser.BrackettedExpressionContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#builtInCall.
    def enterBuiltInCall(self, ctx:SparqlParser.BuiltInCallContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#builtInCall.
    def exitBuiltInCall(self, ctx:SparqlParser.BuiltInCallContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#regexExpression.
    def enterRegexExpression(self, ctx:SparqlParser.RegexExpressionContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#regexExpression.
    def exitRegexExpression(self, ctx:SparqlParser.RegexExpressionContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#substringExpression.
    def enterSubstringExpression(self, ctx:SparqlParser.SubstringExpressionContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#substringExpression.
    def exitSubstringExpression(self, ctx:SparqlParser.SubstringExpressionContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#strReplaceExpression.
    def enterStrReplaceExpression(self, ctx:SparqlParser.StrReplaceExpressionContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#strReplaceExpression.
    def exitStrReplaceExpression(self, ctx:SparqlParser.StrReplaceExpressionContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#existsFunc.
    def enterExistsFunc(self, ctx:SparqlParser.ExistsFuncContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#existsFunc.
    def exitExistsFunc(self, ctx:SparqlParser.ExistsFuncContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#notExistsFunc.
    def enterNotExistsFunc(self, ctx:SparqlParser.NotExistsFuncContext):
        self.enter(ctx)
        self.clusters[-1].setLabel("FILTER NOT EXISTS")
        pass

    # Exit a parse tree produced by SparqlParser#notExistsFunc.
    def exitNotExistsFunc(self, ctx:SparqlParser.NotExistsFuncContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#aggregate.
    def enterAggregate(self, ctx:SparqlParser.AggregateContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#aggregate.
    def exitAggregate(self, ctx:SparqlParser.AggregateContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#iriOrFunction.
    def enterIriOrFunction(self, ctx:SparqlParser.IriOrFunctionContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#iriOrFunction.
    def exitIriOrFunction(self, ctx:SparqlParser.IriOrFunctionContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#rdfLiteral.
    def enterRdfLiteral(self, ctx:SparqlParser.RdfLiteralContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#rdfLiteral.
    def exitRdfLiteral(self, ctx:SparqlParser.RdfLiteralContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#numericLiteral.
    def enterNumericLiteral(self, ctx:SparqlParser.NumericLiteralContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#numericLiteral.
    def exitNumericLiteral(self, ctx:SparqlParser.NumericLiteralContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#numericLiteralUnsigned.
    def enterNumericLiteralUnsigned(self, ctx:SparqlParser.NumericLiteralUnsignedContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#numericLiteralUnsigned.
    def exitNumericLiteralUnsigned(self, ctx:SparqlParser.NumericLiteralUnsignedContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#numericLiteralPositive.
    def enterNumericLiteralPositive(self, ctx:SparqlParser.NumericLiteralPositiveContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#numericLiteralPositive.
    def exitNumericLiteralPositive(self, ctx:SparqlParser.NumericLiteralPositiveContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#numericLiteralNegative.
    def enterNumericLiteralNegative(self, ctx:SparqlParser.NumericLiteralNegativeContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#numericLiteralNegative.
    def exitNumericLiteralNegative(self, ctx:SparqlParser.NumericLiteralNegativeContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#booleanLiteral.
    def enterBooleanLiteral(self, ctx:SparqlParser.BooleanLiteralContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#booleanLiteral.
    def exitBooleanLiteral(self, ctx:SparqlParser.BooleanLiteralContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#string.
    def enterString(self, ctx:SparqlParser.StringContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#string.
    def exitString(self, ctx:SparqlParser.StringContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#iri.
    def enterIri(self, ctx:SparqlParser.IriContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#iri.
    def exitIri(self, ctx:SparqlParser.IriContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#prefixedName.
    def enterPrefixedName(self, ctx:SparqlParser.PrefixedNameContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#prefixedName.
    def exitPrefixedName(self, ctx:SparqlParser.PrefixedNameContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#blankNode.
    def enterBlankNode(self, ctx:SparqlParser.BlankNodeContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#blankNode.
    def exitBlankNode(self, ctx:SparqlParser.BlankNodeContext):
        self.exit(ctx)
        pass