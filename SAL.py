#! /usr/bin/env python3

import sys
from antlr4 import *
from SparqlLexer import SparqlLexer
from SparqlParser import SparqlParser
from SparqlListener import SparqlListener

from collections import deque
from graphviz import *
import networkx as nx
import matplotlib.pyplot as plt

class Color:
    BLANK = "black"
    DEFAULT = "blue"
    PROJECTION = "red"
    VALUE = "green3"

class Shape:
    BLANK = "ellipse"
    DEFAULT = "ellipse"
    PROJECTION = "ellipse"
    VALUE = "box"

BLANK = (Shape.BLANK, Color.BLANK, Color.BLANK)
DEFAULT = (Shape.DEFAULT, Color.DEFAULT, Color.DEFAULT)
PROJECTION = (Shape.PROJECTION, Color.PROJECTION, Color.PROJECTION)
VALUE = (Shape.VALUE, Color.VALUE, Color.VALUE)

class DigraphGenerator:
    def __init__(self, name):
        self.graph = nx.DiGraph(name=name)

        self.namesCount = dict()
    
    def set_name(self, name):
        self.graph.name = name
    
    def renderDOT(self, format = "png", view = False):
        g = Digraph(self.graph.name)
        for node in self.graph.nodes:
            g.node(hex(hash(node)), **self.graph.nodes[node])
        
        edge_labels = nx.get_edge_attributes(self.graph, "label")
        for edge in self.graph.edges:
            g.edge(hex(hash(edge[0])), hex(hash(edge[1])), edge_labels[edge])

        g.format = format

        if view:
            g.view(cleanup=True)
        else:
            g.render(cleanup=True)

    def getName(self, name : str):
        if name is None:
            if None in self.namesCount:
                self.namesCount[None] += 1
            else:
                self.namesCount[None] = 1
            return f"blank{self.namesCount[None]}"
        return name

    def quote(s):
        return f"\"{s}\""
    
    def isDirected(self):
        return self.graph.is_directed()
    
    def addNode(self, name = None, label = "[]", shape = Shape.DEFAULT, color = Color.DEFAULT, fontcolor = Color.DEFAULT):
        if name is None:
            shape, color, fontcolor = BLANK

        name = self.getName(name)   
        self.graph.add_node(name, label=label, shape=shape, color=color, fontcolor=fontcolor)
        return name

    def addTSSes(self, tsses):
        for tss in tsses:
            sNode = self.addNode(tss.subject, tss.subject)
            for path in tss.paths:
                bNode = sNode
                for i in range(len(path)-1):
                    if i == len(path) - 2:
                        if path[i+1].startswith('?'):
                            self.graph.add_edge(bNode, self.addNode(path[i+1], path[i+1]), label=path[i])
                        else:
                            self.graph.add_edge(bNode, self.addNode(path[i+1], path[i+1], *VALUE), label=path[i])
                    else:
                        tmp, bNode = bNode, self.addNode()
                        self.graph.add_edge(tmp, bNode, label=path[i])

    def setNodesColor(self, labels, color):
        for name in labels:
            if self.graph.has_node(name):
                self.graph.nodes[name]["color"] = color
                self.graph.nodes[name]["fontcolor"] = color
            else:
                print(f"WARNING: '{name}' was given as key but is invalid")

    def draw(self):
        #nx.draw_networkx_nodes(self.graph, pos=nx.spring_layout(self.graph))#, node_color="red")
        #nx.draw_networkx_edges(self.graph)
        nx.write(self.graph, "test.dot")

    def addSubgraph(self):
        pass
    
class Select:
    def __init__(self):
        self.projections = set()
        self.vars = set()
        self.subselects = []
        self.tss = []
        self.filters = []
        self.aliases = dict()
        #self.modifiers = [] #maybe class if taken into account later

    def addSubSelect(self, s):
        self.subselects.append(s)

    def addFilter(self, f):
        self.filters.append(f)

    def addVar(self, v):
        if v != "":
            self.vars.add(v)
        else:
            print("WARNING: Attempted to add empty string in var !")

    def addVars(self, vs):
        self.vars |= set(vs) - {""}

    def addTSS(self, tss):
        self.tss.append(tss)

    def getProjections(self):
        if len(self.projections) == 0:
            return self.vars
        else:
            a = set()
            for p in self.projections:
                if p in self.aliases:
                    a.add(self.aliases[p])
        return self.projections | a
    
    def setAlias(self, a1, a2):
        self.aliases[a1] = a2
        self.aliases[a2] = a1

    def setProjections(self, ps):
        self.projections = set(ps)
        self.addVars(ps)

    def __setEdges(self, d):
        d.addTSSes(self.tss) 
        for s in self.subselects:
            s.__setEdges(d)

    def getGraph(self, name):
        d = DigraphGenerator(name)
        self.__setEdges(d)
        d.setNodesColor(self.getProjections(), Color.PROJECTION)
        return d

class Filter:
    def __init__(self):
        self.negate = False
        self.tss = []

    def setNegate(self, n):
        self.negate = n

    def addTSS(self, tss):
        self.tss.append(tss)

class TSS:
    def __init__(self):
        self.subject = None
        self.__neednewpath = True
        self.paths = [] #List of paths. A path is a list of verbPaths with a value as its end. Between each relation, there is a virtual blank node

    def addToPath(self, value, isVerbPath):
        if self.subject is None:
            self.subject = value
        else:
            #Handle 'a' alias for 'rdf:type'
            if value == "a":
                value = "rdf:type"

            if self.__neednewpath:
                self.paths.append([])
                self.__neednewpath = False

            self.paths[-1].append(value)
            if not isVerbPath:            
                self.__neednewpath = True

    def __str__(self):
        return f"{self.subject}\n{self.paths}"


# This class defines a complete listener for a parse tree produced by SparqlParser.
class SAL(SparqlListener):
    
    def __init__(self, verbose = False):
        #Flags
        self.isVerbPath = False
        self.alias = False
        self.verbose = verbose

        #Dicts
        self.prefixNamespace = dict()
        self.prefixCurie = dict()

        #Logic
        self.mainselects = []
        self.selects = deque()
        self.tsser = deque()
        self.currentTSS = None
        self.currentFilter = None
        self.currentAlias = None
        self.__ctx = None
        self.indent = 0
    
    def enter(self, ctx):
        if self.verbose:
            print(" "*self.indent, ">", ctx.__class__.__name__[:-7], sep="")
            self.indent += 1

        self.__ctx = ctx
        pass

    def exit(self, ctx):
        if self.verbose: #Convert 'a' to 'rdf:type'
            if self.__ctx == ctx:
                print(ctx.getText())
            print(" "*(self.indent-1), "<", ctx.__class__.__name__[:-7], sep="")
            self.indent -= 1

        if self.currentTSS and self.__ctx == ctx:
            self.currentTSS.addToPath(ctx.getText(), self.isVerbPath)
        pass

    def getMainSelects(self):
        return self.mainselects[:]
    
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
       
        s = Select()
        if self.selects:
            self.selects[-1].addSubSelect(s)
        else:
            self.mainselects.append(s)

        self.selects.append(s)
        self.tsser.append(s)
        pass

    # Exit a parse tree produced by SparqlParser#selectQuery.
    def exitSelectQuery(self, ctx:SparqlParser.SelectQueryContext):
        self.exit(ctx)
        self.selects.pop()
        self.tsser.pop()
        pass

    # Enter a parse tree produced by SparqlParser#subSelect.
    def enterSubSelect(self, ctx:SparqlParser.SubSelectContext):
        self.enter(ctx)
        s = Select()
        if self.selects:
            self.selects[-1].addSubSelect(s)
        else:
            self.mainselects.append(s)

        self.selects.append(s)
        self.tsser.append(s)
        pass

    # Exit a parse tree produced by SparqlParser#subSelect.
    def exitSubSelect(self, ctx:SparqlParser.SubSelectContext):
        self.exit(ctx)
        self.selects.pop()
        self.tsser.pop()
        pass

    # Enter a parse tree produced by SparqlParser#selectClause.
    def enterSelectClause(self, ctx:SparqlParser.SelectClauseContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#selectClause.
    def exitSelectClause(self, ctx:SparqlParser.SelectClauseContext):
        self.selects[-1].setProjections([v.getText() for v in ctx.var()])
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
        pass

    # Exit a parse tree produced by SparqlParser#solutionModifier.
    def exitSolutionModifier(self, ctx:SparqlParser.SolutionModifierContext):
        self.exit(ctx)
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
        pass

    # Exit a parse tree produced by SparqlParser#groupGraphPattern.
    def exitGroupGraphPattern(self, ctx:SparqlParser.GroupGraphPatternContext):
        self.exit(ctx)
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
        pass

    # Exit a parse tree produced by SparqlParser#optionalGraphPattern.
    def exitOptionalGraphPattern(self, ctx:SparqlParser.OptionalGraphPatternContext):
        self.exit(ctx)
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
        pass

    # Exit a parse tree produced by SparqlParser#bind.
    def exitBind(self, ctx:SparqlParser.BindContext):
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
        pass

    # Exit a parse tree produced by SparqlParser#dataBlock.
    def exitDataBlock(self, ctx:SparqlParser.DataBlockContext):
        self.exit(ctx)
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
        pass

    # Enter a parse tree produced by SparqlParser#minusGraphPattern.
    def enterMinusGraphPattern(self, ctx:SparqlParser.MinusGraphPatternContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#minusGraphPattern.
    def exitMinusGraphPattern(self, ctx:SparqlParser.MinusGraphPatternContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#groupOrUnionGraphPattern.
    def enterGroupOrUnionGraphPattern(self, ctx:SparqlParser.GroupOrUnionGraphPatternContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#groupOrUnionGraphPattern.
    def exitGroupOrUnionGraphPattern(self, ctx:SparqlParser.GroupOrUnionGraphPatternContext):
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#filterClause.
    def enterFilterClause(self, ctx:SparqlParser.FilterClauseContext):
        self.enter(ctx)
        self.currentFilter = Filter()
        self.selects[-1].addFilter(self.currentFilter)
        self.tsser.append(self.currentFilter)
        pass

    # Exit a parse tree produced by SparqlParser#filterClause.
    def exitFilterClause(self, ctx:SparqlParser.FilterClauseContext):
        self.exit(ctx)
        self.tsser.pop()
        self.currentFilter = None #Maybe to remove
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
        self.tsser[-1].addTSS(self.currentTSS)
        pass

    # Exit a parse tree produced by SparqlParser#triplesSameSubjectPath.
    def exitTriplesSameSubjectPath(self, ctx:SparqlParser.TriplesSameSubjectPathContext):
        self.exit(ctx)
        self.currentTSS = None #May remove
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
        self.exit(ctx)
        pass

    # Enter a parse tree produced by SparqlParser#pathMod.
    def enterPathMod(self, ctx:SparqlParser.PathModContext):
        self.enter(ctx)
        pass

    # Exit a parse tree produced by SparqlParser#pathMod.
    def exitPathMod(self, ctx:SparqlParser.PathModContext):
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
        pass

    # Exit a parse tree produced by SparqlParser#blankNodePropertyList.
    def exitBlankNodePropertyList(self, ctx:SparqlParser.BlankNodePropertyListContext):
        self.exit(ctx)
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
        pass

    # Exit a parse tree produced by SparqlParser#blankNodePropertyListPath.
    def exitBlankNodePropertyListPath(self, ctx:SparqlParser.BlankNodePropertyListPathContext):
        self.exit(ctx)
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
        self.selects[-1].addVar(ctx.getText())
        if self.alias:
            if self.currentAlias is None:
                self.currentAlias = ctx.getText()
            else:
                self.selects[-1].setAlias(ctx.getText(), self.currentAlias)
                self.currentAlias = None
                self.alias = False
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
        pass

    # Exit a parse tree produced by SparqlParser#expression.
    def exitExpression(self, ctx:SparqlParser.ExpressionContext):
        self.exit(ctx)
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
        self.alias = True
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
        self.currentFilter.setNegate(True)
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


 
def main(argv):
    verbose = False
    if len(argv) > 2 and argv[2] == "-v":
        verbose = True
    input_stream = FileStream(argv[1])
    lexer = SparqlLexer(input_stream)
    stream = CommonTokenStream(lexer)
    listener = SAL(verbose)
    parser = SparqlParser(stream)
    parser.addParseListener(listener)

    parser.statement() #=tree
    #ParseTreeWalker.DEFAULT.walk(listener, tree)

    graph = listener.getMainSelects()[0].getGraph(argv[1]).renderDOT()
    #nx.write_gexf(graph, sys.argv[1].replace(".rq", ".gexf"))
if __name__ == '__main__':
    main(sys.argv)
