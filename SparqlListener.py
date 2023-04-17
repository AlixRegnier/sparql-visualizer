# Generated from Sparql.g4 by ANTLR 4.10.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SparqlParser import SparqlParser
else:
    from SparqlParser import SparqlParser

# This class defines a complete listener for a parse tree produced by SparqlParser.
class SparqlListener(ParseTreeListener):

    # Enter a parse tree produced by SparqlParser#statement.
    def enterStatement(self, ctx:SparqlParser.StatementContext):
        pass

    # Exit a parse tree produced by SparqlParser#statement.
    def exitStatement(self, ctx:SparqlParser.StatementContext):
        pass


    # Enter a parse tree produced by SparqlParser#query.
    def enterQuery(self, ctx:SparqlParser.QueryContext):
        pass

    # Exit a parse tree produced by SparqlParser#query.
    def exitQuery(self, ctx:SparqlParser.QueryContext):
        pass


    # Enter a parse tree produced by SparqlParser#prologue.
    def enterPrologue(self, ctx:SparqlParser.PrologueContext):
        pass

    # Exit a parse tree produced by SparqlParser#prologue.
    def exitPrologue(self, ctx:SparqlParser.PrologueContext):
        pass


    # Enter a parse tree produced by SparqlParser#baseDecl.
    def enterBaseDecl(self, ctx:SparqlParser.BaseDeclContext):
        pass

    # Exit a parse tree produced by SparqlParser#baseDecl.
    def exitBaseDecl(self, ctx:SparqlParser.BaseDeclContext):
        pass


    # Enter a parse tree produced by SparqlParser#prefixDecl.
    def enterPrefixDecl(self, ctx:SparqlParser.PrefixDeclContext):
        pass

    # Exit a parse tree produced by SparqlParser#prefixDecl.
    def exitPrefixDecl(self, ctx:SparqlParser.PrefixDeclContext):
        pass


    # Enter a parse tree produced by SparqlParser#selectQuery.
    def enterSelectQuery(self, ctx:SparqlParser.SelectQueryContext):
        pass

    # Exit a parse tree produced by SparqlParser#selectQuery.
    def exitSelectQuery(self, ctx:SparqlParser.SelectQueryContext):
        pass


    # Enter a parse tree produced by SparqlParser#subSelect.
    def enterSubSelect(self, ctx:SparqlParser.SubSelectContext):
        pass

    # Exit a parse tree produced by SparqlParser#subSelect.
    def exitSubSelect(self, ctx:SparqlParser.SubSelectContext):
        pass


    # Enter a parse tree produced by SparqlParser#selectClause.
    def enterSelectClause(self, ctx:SparqlParser.SelectClauseContext):
        pass

    # Exit a parse tree produced by SparqlParser#selectClause.
    def exitSelectClause(self, ctx:SparqlParser.SelectClauseContext):
        pass


    # Enter a parse tree produced by SparqlParser#constructQuery.
    def enterConstructQuery(self, ctx:SparqlParser.ConstructQueryContext):
        pass

    # Exit a parse tree produced by SparqlParser#constructQuery.
    def exitConstructQuery(self, ctx:SparqlParser.ConstructQueryContext):
        pass


    # Enter a parse tree produced by SparqlParser#describeQuery.
    def enterDescribeQuery(self, ctx:SparqlParser.DescribeQueryContext):
        pass

    # Exit a parse tree produced by SparqlParser#describeQuery.
    def exitDescribeQuery(self, ctx:SparqlParser.DescribeQueryContext):
        pass


    # Enter a parse tree produced by SparqlParser#askQuery.
    def enterAskQuery(self, ctx:SparqlParser.AskQueryContext):
        pass

    # Exit a parse tree produced by SparqlParser#askQuery.
    def exitAskQuery(self, ctx:SparqlParser.AskQueryContext):
        pass


    # Enter a parse tree produced by SparqlParser#datasetClause.
    def enterDatasetClause(self, ctx:SparqlParser.DatasetClauseContext):
        pass

    # Exit a parse tree produced by SparqlParser#datasetClause.
    def exitDatasetClause(self, ctx:SparqlParser.DatasetClauseContext):
        pass


    # Enter a parse tree produced by SparqlParser#defaultGraphClause.
    def enterDefaultGraphClause(self, ctx:SparqlParser.DefaultGraphClauseContext):
        pass

    # Exit a parse tree produced by SparqlParser#defaultGraphClause.
    def exitDefaultGraphClause(self, ctx:SparqlParser.DefaultGraphClauseContext):
        pass


    # Enter a parse tree produced by SparqlParser#namedGraphClause.
    def enterNamedGraphClause(self, ctx:SparqlParser.NamedGraphClauseContext):
        pass

    # Exit a parse tree produced by SparqlParser#namedGraphClause.
    def exitNamedGraphClause(self, ctx:SparqlParser.NamedGraphClauseContext):
        pass


    # Enter a parse tree produced by SparqlParser#sourceSelector.
    def enterSourceSelector(self, ctx:SparqlParser.SourceSelectorContext):
        pass

    # Exit a parse tree produced by SparqlParser#sourceSelector.
    def exitSourceSelector(self, ctx:SparqlParser.SourceSelectorContext):
        pass


    # Enter a parse tree produced by SparqlParser#whereClause.
    def enterWhereClause(self, ctx:SparqlParser.WhereClauseContext):
        pass

    # Exit a parse tree produced by SparqlParser#whereClause.
    def exitWhereClause(self, ctx:SparqlParser.WhereClauseContext):
        pass


    # Enter a parse tree produced by SparqlParser#solutionModifier.
    def enterSolutionModifier(self, ctx:SparqlParser.SolutionModifierContext):
        pass

    # Exit a parse tree produced by SparqlParser#solutionModifier.
    def exitSolutionModifier(self, ctx:SparqlParser.SolutionModifierContext):
        pass


    # Enter a parse tree produced by SparqlParser#groupClause.
    def enterGroupClause(self, ctx:SparqlParser.GroupClauseContext):
        pass

    # Exit a parse tree produced by SparqlParser#groupClause.
    def exitGroupClause(self, ctx:SparqlParser.GroupClauseContext):
        pass


    # Enter a parse tree produced by SparqlParser#groupCondition.
    def enterGroupCondition(self, ctx:SparqlParser.GroupConditionContext):
        pass

    # Exit a parse tree produced by SparqlParser#groupCondition.
    def exitGroupCondition(self, ctx:SparqlParser.GroupConditionContext):
        pass


    # Enter a parse tree produced by SparqlParser#havingClause.
    def enterHavingClause(self, ctx:SparqlParser.HavingClauseContext):
        pass

    # Exit a parse tree produced by SparqlParser#havingClause.
    def exitHavingClause(self, ctx:SparqlParser.HavingClauseContext):
        pass


    # Enter a parse tree produced by SparqlParser#havingCondition.
    def enterHavingCondition(self, ctx:SparqlParser.HavingConditionContext):
        pass

    # Exit a parse tree produced by SparqlParser#havingCondition.
    def exitHavingCondition(self, ctx:SparqlParser.HavingConditionContext):
        pass


    # Enter a parse tree produced by SparqlParser#orderClause.
    def enterOrderClause(self, ctx:SparqlParser.OrderClauseContext):
        pass

    # Exit a parse tree produced by SparqlParser#orderClause.
    def exitOrderClause(self, ctx:SparqlParser.OrderClauseContext):
        pass


    # Enter a parse tree produced by SparqlParser#orderCondition.
    def enterOrderCondition(self, ctx:SparqlParser.OrderConditionContext):
        pass

    # Exit a parse tree produced by SparqlParser#orderCondition.
    def exitOrderCondition(self, ctx:SparqlParser.OrderConditionContext):
        pass


    # Enter a parse tree produced by SparqlParser#limitOffsetClauses.
    def enterLimitOffsetClauses(self, ctx:SparqlParser.LimitOffsetClausesContext):
        pass

    # Exit a parse tree produced by SparqlParser#limitOffsetClauses.
    def exitLimitOffsetClauses(self, ctx:SparqlParser.LimitOffsetClausesContext):
        pass


    # Enter a parse tree produced by SparqlParser#limitClause.
    def enterLimitClause(self, ctx:SparqlParser.LimitClauseContext):
        pass

    # Exit a parse tree produced by SparqlParser#limitClause.
    def exitLimitClause(self, ctx:SparqlParser.LimitClauseContext):
        pass


    # Enter a parse tree produced by SparqlParser#offsetClause.
    def enterOffsetClause(self, ctx:SparqlParser.OffsetClauseContext):
        pass

    # Exit a parse tree produced by SparqlParser#offsetClause.
    def exitOffsetClause(self, ctx:SparqlParser.OffsetClauseContext):
        pass


    # Enter a parse tree produced by SparqlParser#valuesClause.
    def enterValuesClause(self, ctx:SparqlParser.ValuesClauseContext):
        pass

    # Exit a parse tree produced by SparqlParser#valuesClause.
    def exitValuesClause(self, ctx:SparqlParser.ValuesClauseContext):
        pass


    # Enter a parse tree produced by SparqlParser#update.
    def enterUpdate(self, ctx:SparqlParser.UpdateContext):
        pass

    # Exit a parse tree produced by SparqlParser#update.
    def exitUpdate(self, ctx:SparqlParser.UpdateContext):
        pass


    # Enter a parse tree produced by SparqlParser#update1.
    def enterUpdate1(self, ctx:SparqlParser.Update1Context):
        pass

    # Exit a parse tree produced by SparqlParser#update1.
    def exitUpdate1(self, ctx:SparqlParser.Update1Context):
        pass


    # Enter a parse tree produced by SparqlParser#load.
    def enterLoad(self, ctx:SparqlParser.LoadContext):
        pass

    # Exit a parse tree produced by SparqlParser#load.
    def exitLoad(self, ctx:SparqlParser.LoadContext):
        pass


    # Enter a parse tree produced by SparqlParser#clear.
    def enterClear(self, ctx:SparqlParser.ClearContext):
        pass

    # Exit a parse tree produced by SparqlParser#clear.
    def exitClear(self, ctx:SparqlParser.ClearContext):
        pass


    # Enter a parse tree produced by SparqlParser#drop.
    def enterDrop(self, ctx:SparqlParser.DropContext):
        pass

    # Exit a parse tree produced by SparqlParser#drop.
    def exitDrop(self, ctx:SparqlParser.DropContext):
        pass


    # Enter a parse tree produced by SparqlParser#create.
    def enterCreate(self, ctx:SparqlParser.CreateContext):
        pass

    # Exit a parse tree produced by SparqlParser#create.
    def exitCreate(self, ctx:SparqlParser.CreateContext):
        pass


    # Enter a parse tree produced by SparqlParser#add.
    def enterAdd(self, ctx:SparqlParser.AddContext):
        pass

    # Exit a parse tree produced by SparqlParser#add.
    def exitAdd(self, ctx:SparqlParser.AddContext):
        pass


    # Enter a parse tree produced by SparqlParser#move.
    def enterMove(self, ctx:SparqlParser.MoveContext):
        pass

    # Exit a parse tree produced by SparqlParser#move.
    def exitMove(self, ctx:SparqlParser.MoveContext):
        pass


    # Enter a parse tree produced by SparqlParser#copy.
    def enterCopy(self, ctx:SparqlParser.CopyContext):
        pass

    # Exit a parse tree produced by SparqlParser#copy.
    def exitCopy(self, ctx:SparqlParser.CopyContext):
        pass


    # Enter a parse tree produced by SparqlParser#insertData.
    def enterInsertData(self, ctx:SparqlParser.InsertDataContext):
        pass

    # Exit a parse tree produced by SparqlParser#insertData.
    def exitInsertData(self, ctx:SparqlParser.InsertDataContext):
        pass


    # Enter a parse tree produced by SparqlParser#deleteData.
    def enterDeleteData(self, ctx:SparqlParser.DeleteDataContext):
        pass

    # Exit a parse tree produced by SparqlParser#deleteData.
    def exitDeleteData(self, ctx:SparqlParser.DeleteDataContext):
        pass


    # Enter a parse tree produced by SparqlParser#deleteWhere.
    def enterDeleteWhere(self, ctx:SparqlParser.DeleteWhereContext):
        pass

    # Exit a parse tree produced by SparqlParser#deleteWhere.
    def exitDeleteWhere(self, ctx:SparqlParser.DeleteWhereContext):
        pass


    # Enter a parse tree produced by SparqlParser#modify.
    def enterModify(self, ctx:SparqlParser.ModifyContext):
        pass

    # Exit a parse tree produced by SparqlParser#modify.
    def exitModify(self, ctx:SparqlParser.ModifyContext):
        pass


    # Enter a parse tree produced by SparqlParser#deleteClause.
    def enterDeleteClause(self, ctx:SparqlParser.DeleteClauseContext):
        pass

    # Exit a parse tree produced by SparqlParser#deleteClause.
    def exitDeleteClause(self, ctx:SparqlParser.DeleteClauseContext):
        pass


    # Enter a parse tree produced by SparqlParser#insertClause.
    def enterInsertClause(self, ctx:SparqlParser.InsertClauseContext):
        pass

    # Exit a parse tree produced by SparqlParser#insertClause.
    def exitInsertClause(self, ctx:SparqlParser.InsertClauseContext):
        pass


    # Enter a parse tree produced by SparqlParser#usingClause.
    def enterUsingClause(self, ctx:SparqlParser.UsingClauseContext):
        pass

    # Exit a parse tree produced by SparqlParser#usingClause.
    def exitUsingClause(self, ctx:SparqlParser.UsingClauseContext):
        pass


    # Enter a parse tree produced by SparqlParser#graphOrDefault.
    def enterGraphOrDefault(self, ctx:SparqlParser.GraphOrDefaultContext):
        pass

    # Exit a parse tree produced by SparqlParser#graphOrDefault.
    def exitGraphOrDefault(self, ctx:SparqlParser.GraphOrDefaultContext):
        pass


    # Enter a parse tree produced by SparqlParser#graphRef.
    def enterGraphRef(self, ctx:SparqlParser.GraphRefContext):
        pass

    # Exit a parse tree produced by SparqlParser#graphRef.
    def exitGraphRef(self, ctx:SparqlParser.GraphRefContext):
        pass


    # Enter a parse tree produced by SparqlParser#graphRefAll.
    def enterGraphRefAll(self, ctx:SparqlParser.GraphRefAllContext):
        pass

    # Exit a parse tree produced by SparqlParser#graphRefAll.
    def exitGraphRefAll(self, ctx:SparqlParser.GraphRefAllContext):
        pass


    # Enter a parse tree produced by SparqlParser#quadPattern.
    def enterQuadPattern(self, ctx:SparqlParser.QuadPatternContext):
        pass

    # Exit a parse tree produced by SparqlParser#quadPattern.
    def exitQuadPattern(self, ctx:SparqlParser.QuadPatternContext):
        pass


    # Enter a parse tree produced by SparqlParser#quadData.
    def enterQuadData(self, ctx:SparqlParser.QuadDataContext):
        pass

    # Exit a parse tree produced by SparqlParser#quadData.
    def exitQuadData(self, ctx:SparqlParser.QuadDataContext):
        pass


    # Enter a parse tree produced by SparqlParser#quads.
    def enterQuads(self, ctx:SparqlParser.QuadsContext):
        pass

    # Exit a parse tree produced by SparqlParser#quads.
    def exitQuads(self, ctx:SparqlParser.QuadsContext):
        pass


    # Enter a parse tree produced by SparqlParser#quadsNotTriples.
    def enterQuadsNotTriples(self, ctx:SparqlParser.QuadsNotTriplesContext):
        pass

    # Exit a parse tree produced by SparqlParser#quadsNotTriples.
    def exitQuadsNotTriples(self, ctx:SparqlParser.QuadsNotTriplesContext):
        pass


    # Enter a parse tree produced by SparqlParser#triplesTemplate.
    def enterTriplesTemplate(self, ctx:SparqlParser.TriplesTemplateContext):
        pass

    # Exit a parse tree produced by SparqlParser#triplesTemplate.
    def exitTriplesTemplate(self, ctx:SparqlParser.TriplesTemplateContext):
        pass


    # Enter a parse tree produced by SparqlParser#groupGraphPattern.
    def enterGroupGraphPattern(self, ctx:SparqlParser.GroupGraphPatternContext):
        pass

    # Exit a parse tree produced by SparqlParser#groupGraphPattern.
    def exitGroupGraphPattern(self, ctx:SparqlParser.GroupGraphPatternContext):
        pass


    # Enter a parse tree produced by SparqlParser#groupGraphPatternSub.
    def enterGroupGraphPatternSub(self, ctx:SparqlParser.GroupGraphPatternSubContext):
        pass

    # Exit a parse tree produced by SparqlParser#groupGraphPatternSub.
    def exitGroupGraphPatternSub(self, ctx:SparqlParser.GroupGraphPatternSubContext):
        pass


    # Enter a parse tree produced by SparqlParser#triplesBlock.
    def enterTriplesBlock(self, ctx:SparqlParser.TriplesBlockContext):
        pass

    # Exit a parse tree produced by SparqlParser#triplesBlock.
    def exitTriplesBlock(self, ctx:SparqlParser.TriplesBlockContext):
        pass


    # Enter a parse tree produced by SparqlParser#graphPatternNotTriples.
    def enterGraphPatternNotTriples(self, ctx:SparqlParser.GraphPatternNotTriplesContext):
        pass

    # Exit a parse tree produced by SparqlParser#graphPatternNotTriples.
    def exitGraphPatternNotTriples(self, ctx:SparqlParser.GraphPatternNotTriplesContext):
        pass


    # Enter a parse tree produced by SparqlParser#optionalGraphPattern.
    def enterOptionalGraphPattern(self, ctx:SparqlParser.OptionalGraphPatternContext):
        pass

    # Exit a parse tree produced by SparqlParser#optionalGraphPattern.
    def exitOptionalGraphPattern(self, ctx:SparqlParser.OptionalGraphPatternContext):
        pass


    # Enter a parse tree produced by SparqlParser#graphGraphPattern.
    def enterGraphGraphPattern(self, ctx:SparqlParser.GraphGraphPatternContext):
        pass

    # Exit a parse tree produced by SparqlParser#graphGraphPattern.
    def exitGraphGraphPattern(self, ctx:SparqlParser.GraphGraphPatternContext):
        pass


    # Enter a parse tree produced by SparqlParser#serviceGraphPattern.
    def enterServiceGraphPattern(self, ctx:SparqlParser.ServiceGraphPatternContext):
        pass

    # Exit a parse tree produced by SparqlParser#serviceGraphPattern.
    def exitServiceGraphPattern(self, ctx:SparqlParser.ServiceGraphPatternContext):
        pass


    # Enter a parse tree produced by SparqlParser#bind.
    def enterBind(self, ctx:SparqlParser.BindContext):
        pass

    # Exit a parse tree produced by SparqlParser#bind.
    def exitBind(self, ctx:SparqlParser.BindContext):
        pass


    # Enter a parse tree produced by SparqlParser#inlineData.
    def enterInlineData(self, ctx:SparqlParser.InlineDataContext):
        pass

    # Exit a parse tree produced by SparqlParser#inlineData.
    def exitInlineData(self, ctx:SparqlParser.InlineDataContext):
        pass


    # Enter a parse tree produced by SparqlParser#dataBlock.
    def enterDataBlock(self, ctx:SparqlParser.DataBlockContext):
        pass

    # Exit a parse tree produced by SparqlParser#dataBlock.
    def exitDataBlock(self, ctx:SparqlParser.DataBlockContext):
        pass


    # Enter a parse tree produced by SparqlParser#inlineDataOneVar.
    def enterInlineDataOneVar(self, ctx:SparqlParser.InlineDataOneVarContext):
        pass

    # Exit a parse tree produced by SparqlParser#inlineDataOneVar.
    def exitInlineDataOneVar(self, ctx:SparqlParser.InlineDataOneVarContext):
        pass


    # Enter a parse tree produced by SparqlParser#inlineDataFull.
    def enterInlineDataFull(self, ctx:SparqlParser.InlineDataFullContext):
        pass

    # Exit a parse tree produced by SparqlParser#inlineDataFull.
    def exitInlineDataFull(self, ctx:SparqlParser.InlineDataFullContext):
        pass


    # Enter a parse tree produced by SparqlParser#dataBlockValue.
    def enterDataBlockValue(self, ctx:SparqlParser.DataBlockValueContext):
        pass

    # Exit a parse tree produced by SparqlParser#dataBlockValue.
    def exitDataBlockValue(self, ctx:SparqlParser.DataBlockValueContext):
        pass


    # Enter a parse tree produced by SparqlParser#minusGraphPattern.
    def enterMinusGraphPattern(self, ctx:SparqlParser.MinusGraphPatternContext):
        pass

    # Exit a parse tree produced by SparqlParser#minusGraphPattern.
    def exitMinusGraphPattern(self, ctx:SparqlParser.MinusGraphPatternContext):
        pass


    # Enter a parse tree produced by SparqlParser#groupOrUnionGraphPattern.
    def enterGroupOrUnionGraphPattern(self, ctx:SparqlParser.GroupOrUnionGraphPatternContext):
        pass

    # Exit a parse tree produced by SparqlParser#groupOrUnionGraphPattern.
    def exitGroupOrUnionGraphPattern(self, ctx:SparqlParser.GroupOrUnionGraphPatternContext):
        pass


    # Enter a parse tree produced by SparqlParser#filterClause.
    def enterFilterClause(self, ctx:SparqlParser.FilterClauseContext):
        pass

    # Exit a parse tree produced by SparqlParser#filterClause.
    def exitFilterClause(self, ctx:SparqlParser.FilterClauseContext):
        pass


    # Enter a parse tree produced by SparqlParser#constraint.
    def enterConstraint(self, ctx:SparqlParser.ConstraintContext):
        pass

    # Exit a parse tree produced by SparqlParser#constraint.
    def exitConstraint(self, ctx:SparqlParser.ConstraintContext):
        pass


    # Enter a parse tree produced by SparqlParser#functionCall.
    def enterFunctionCall(self, ctx:SparqlParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by SparqlParser#functionCall.
    def exitFunctionCall(self, ctx:SparqlParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by SparqlParser#argList.
    def enterArgList(self, ctx:SparqlParser.ArgListContext):
        pass

    # Exit a parse tree produced by SparqlParser#argList.
    def exitArgList(self, ctx:SparqlParser.ArgListContext):
        pass


    # Enter a parse tree produced by SparqlParser#expressionList.
    def enterExpressionList(self, ctx:SparqlParser.ExpressionListContext):
        pass

    # Exit a parse tree produced by SparqlParser#expressionList.
    def exitExpressionList(self, ctx:SparqlParser.ExpressionListContext):
        pass


    # Enter a parse tree produced by SparqlParser#constructTemplate.
    def enterConstructTemplate(self, ctx:SparqlParser.ConstructTemplateContext):
        pass

    # Exit a parse tree produced by SparqlParser#constructTemplate.
    def exitConstructTemplate(self, ctx:SparqlParser.ConstructTemplateContext):
        pass


    # Enter a parse tree produced by SparqlParser#constructTriples.
    def enterConstructTriples(self, ctx:SparqlParser.ConstructTriplesContext):
        pass

    # Exit a parse tree produced by SparqlParser#constructTriples.
    def exitConstructTriples(self, ctx:SparqlParser.ConstructTriplesContext):
        pass


    # Enter a parse tree produced by SparqlParser#triplesSameSubject.
    def enterTriplesSameSubject(self, ctx:SparqlParser.TriplesSameSubjectContext):
        pass

    # Exit a parse tree produced by SparqlParser#triplesSameSubject.
    def exitTriplesSameSubject(self, ctx:SparqlParser.TriplesSameSubjectContext):
        pass


    # Enter a parse tree produced by SparqlParser#propertyList.
    def enterPropertyList(self, ctx:SparqlParser.PropertyListContext):
        pass

    # Exit a parse tree produced by SparqlParser#propertyList.
    def exitPropertyList(self, ctx:SparqlParser.PropertyListContext):
        pass


    # Enter a parse tree produced by SparqlParser#propertyListNotEmpty.
    def enterPropertyListNotEmpty(self, ctx:SparqlParser.PropertyListNotEmptyContext):
        pass

    # Exit a parse tree produced by SparqlParser#propertyListNotEmpty.
    def exitPropertyListNotEmpty(self, ctx:SparqlParser.PropertyListNotEmptyContext):
        pass


    # Enter a parse tree produced by SparqlParser#verb.
    def enterVerb(self, ctx:SparqlParser.VerbContext):
        pass

    # Exit a parse tree produced by SparqlParser#verb.
    def exitVerb(self, ctx:SparqlParser.VerbContext):
        pass


    # Enter a parse tree produced by SparqlParser#objectList.
    def enterObjectList(self, ctx:SparqlParser.ObjectListContext):
        pass

    # Exit a parse tree produced by SparqlParser#objectList.
    def exitObjectList(self, ctx:SparqlParser.ObjectListContext):
        pass


    # Enter a parse tree produced by SparqlParser#objectClause.
    def enterObjectClause(self, ctx:SparqlParser.ObjectClauseContext):
        pass

    # Exit a parse tree produced by SparqlParser#objectClause.
    def exitObjectClause(self, ctx:SparqlParser.ObjectClauseContext):
        pass


    # Enter a parse tree produced by SparqlParser#triplesSameSubjectPath.
    def enterTriplesSameSubjectPath(self, ctx:SparqlParser.TriplesSameSubjectPathContext):
        pass

    # Exit a parse tree produced by SparqlParser#triplesSameSubjectPath.
    def exitTriplesSameSubjectPath(self, ctx:SparqlParser.TriplesSameSubjectPathContext):
        pass


    # Enter a parse tree produced by SparqlParser#propertyListPath.
    def enterPropertyListPath(self, ctx:SparqlParser.PropertyListPathContext):
        pass

    # Exit a parse tree produced by SparqlParser#propertyListPath.
    def exitPropertyListPath(self, ctx:SparqlParser.PropertyListPathContext):
        pass


    # Enter a parse tree produced by SparqlParser#propertyListPathNotEmpty.
    def enterPropertyListPathNotEmpty(self, ctx:SparqlParser.PropertyListPathNotEmptyContext):
        pass

    # Exit a parse tree produced by SparqlParser#propertyListPathNotEmpty.
    def exitPropertyListPathNotEmpty(self, ctx:SparqlParser.PropertyListPathNotEmptyContext):
        pass


    # Enter a parse tree produced by SparqlParser#verbPath.
    def enterVerbPath(self, ctx:SparqlParser.VerbPathContext):
        pass

    # Exit a parse tree produced by SparqlParser#verbPath.
    def exitVerbPath(self, ctx:SparqlParser.VerbPathContext):
        pass


    # Enter a parse tree produced by SparqlParser#verbSimple.
    def enterVerbSimple(self, ctx:SparqlParser.VerbSimpleContext):
        pass

    # Exit a parse tree produced by SparqlParser#verbSimple.
    def exitVerbSimple(self, ctx:SparqlParser.VerbSimpleContext):
        pass


    # Enter a parse tree produced by SparqlParser#objectListPath.
    def enterObjectListPath(self, ctx:SparqlParser.ObjectListPathContext):
        pass

    # Exit a parse tree produced by SparqlParser#objectListPath.
    def exitObjectListPath(self, ctx:SparqlParser.ObjectListPathContext):
        pass


    # Enter a parse tree produced by SparqlParser#objectPath.
    def enterObjectPath(self, ctx:SparqlParser.ObjectPathContext):
        pass

    # Exit a parse tree produced by SparqlParser#objectPath.
    def exitObjectPath(self, ctx:SparqlParser.ObjectPathContext):
        pass


    # Enter a parse tree produced by SparqlParser#path.
    def enterPath(self, ctx:SparqlParser.PathContext):
        pass

    # Exit a parse tree produced by SparqlParser#path.
    def exitPath(self, ctx:SparqlParser.PathContext):
        pass


    # Enter a parse tree produced by SparqlParser#pathAlternative.
    def enterPathAlternative(self, ctx:SparqlParser.PathAlternativeContext):
        pass

    # Exit a parse tree produced by SparqlParser#pathAlternative.
    def exitPathAlternative(self, ctx:SparqlParser.PathAlternativeContext):
        pass


    # Enter a parse tree produced by SparqlParser#pathSequence.
    def enterPathSequence(self, ctx:SparqlParser.PathSequenceContext):
        pass

    # Exit a parse tree produced by SparqlParser#pathSequence.
    def exitPathSequence(self, ctx:SparqlParser.PathSequenceContext):
        pass


    # Enter a parse tree produced by SparqlParser#pathElt.
    def enterPathElt(self, ctx:SparqlParser.PathEltContext):
        pass

    # Exit a parse tree produced by SparqlParser#pathElt.
    def exitPathElt(self, ctx:SparqlParser.PathEltContext):
        pass


    # Enter a parse tree produced by SparqlParser#pathEltOrInverse.
    def enterPathEltOrInverse(self, ctx:SparqlParser.PathEltOrInverseContext):
        pass

    # Exit a parse tree produced by SparqlParser#pathEltOrInverse.
    def exitPathEltOrInverse(self, ctx:SparqlParser.PathEltOrInverseContext):
        pass


    # Enter a parse tree produced by SparqlParser#pathMod.
    def enterPathMod(self, ctx:SparqlParser.PathModContext):
        pass

    # Exit a parse tree produced by SparqlParser#pathMod.
    def exitPathMod(self, ctx:SparqlParser.PathModContext):
        pass


    # Enter a parse tree produced by SparqlParser#pathPrimary.
    def enterPathPrimary(self, ctx:SparqlParser.PathPrimaryContext):
        pass

    # Exit a parse tree produced by SparqlParser#pathPrimary.
    def exitPathPrimary(self, ctx:SparqlParser.PathPrimaryContext):
        pass


    # Enter a parse tree produced by SparqlParser#pathNegatedPropertySet.
    def enterPathNegatedPropertySet(self, ctx:SparqlParser.PathNegatedPropertySetContext):
        pass

    # Exit a parse tree produced by SparqlParser#pathNegatedPropertySet.
    def exitPathNegatedPropertySet(self, ctx:SparqlParser.PathNegatedPropertySetContext):
        pass


    # Enter a parse tree produced by SparqlParser#pathOneInPropertySet.
    def enterPathOneInPropertySet(self, ctx:SparqlParser.PathOneInPropertySetContext):
        pass

    # Exit a parse tree produced by SparqlParser#pathOneInPropertySet.
    def exitPathOneInPropertySet(self, ctx:SparqlParser.PathOneInPropertySetContext):
        pass


    # Enter a parse tree produced by SparqlParser#triplesNode.
    def enterTriplesNode(self, ctx:SparqlParser.TriplesNodeContext):
        pass

    # Exit a parse tree produced by SparqlParser#triplesNode.
    def exitTriplesNode(self, ctx:SparqlParser.TriplesNodeContext):
        pass


    # Enter a parse tree produced by SparqlParser#blankNodePropertyList.
    def enterBlankNodePropertyList(self, ctx:SparqlParser.BlankNodePropertyListContext):
        pass

    # Exit a parse tree produced by SparqlParser#blankNodePropertyList.
    def exitBlankNodePropertyList(self, ctx:SparqlParser.BlankNodePropertyListContext):
        pass


    # Enter a parse tree produced by SparqlParser#triplesNodePath.
    def enterTriplesNodePath(self, ctx:SparqlParser.TriplesNodePathContext):
        pass

    # Exit a parse tree produced by SparqlParser#triplesNodePath.
    def exitTriplesNodePath(self, ctx:SparqlParser.TriplesNodePathContext):
        pass


    # Enter a parse tree produced by SparqlParser#blankNodePropertyListPath.
    def enterBlankNodePropertyListPath(self, ctx:SparqlParser.BlankNodePropertyListPathContext):
        pass

    # Exit a parse tree produced by SparqlParser#blankNodePropertyListPath.
    def exitBlankNodePropertyListPath(self, ctx:SparqlParser.BlankNodePropertyListPathContext):
        pass


    # Enter a parse tree produced by SparqlParser#collection.
    def enterCollection(self, ctx:SparqlParser.CollectionContext):
        pass

    # Exit a parse tree produced by SparqlParser#collection.
    def exitCollection(self, ctx:SparqlParser.CollectionContext):
        pass


    # Enter a parse tree produced by SparqlParser#collectionPath.
    def enterCollectionPath(self, ctx:SparqlParser.CollectionPathContext):
        pass

    # Exit a parse tree produced by SparqlParser#collectionPath.
    def exitCollectionPath(self, ctx:SparqlParser.CollectionPathContext):
        pass


    # Enter a parse tree produced by SparqlParser#graphNode.
    def enterGraphNode(self, ctx:SparqlParser.GraphNodeContext):
        pass

    # Exit a parse tree produced by SparqlParser#graphNode.
    def exitGraphNode(self, ctx:SparqlParser.GraphNodeContext):
        pass


    # Enter a parse tree produced by SparqlParser#graphNodePath.
    def enterGraphNodePath(self, ctx:SparqlParser.GraphNodePathContext):
        pass

    # Exit a parse tree produced by SparqlParser#graphNodePath.
    def exitGraphNodePath(self, ctx:SparqlParser.GraphNodePathContext):
        pass


    # Enter a parse tree produced by SparqlParser#varOrTerm.
    def enterVarOrTerm(self, ctx:SparqlParser.VarOrTermContext):
        pass

    # Exit a parse tree produced by SparqlParser#varOrTerm.
    def exitVarOrTerm(self, ctx:SparqlParser.VarOrTermContext):
        pass


    # Enter a parse tree produced by SparqlParser#varOrIri.
    def enterVarOrIri(self, ctx:SparqlParser.VarOrIriContext):
        pass

    # Exit a parse tree produced by SparqlParser#varOrIri.
    def exitVarOrIri(self, ctx:SparqlParser.VarOrIriContext):
        pass


    # Enter a parse tree produced by SparqlParser#var.
    def enterVar(self, ctx:SparqlParser.VarContext):
        pass

    # Exit a parse tree produced by SparqlParser#var.
    def exitVar(self, ctx:SparqlParser.VarContext):
        pass


    # Enter a parse tree produced by SparqlParser#graphTerm.
    def enterGraphTerm(self, ctx:SparqlParser.GraphTermContext):
        pass

    # Exit a parse tree produced by SparqlParser#graphTerm.
    def exitGraphTerm(self, ctx:SparqlParser.GraphTermContext):
        pass


    # Enter a parse tree produced by SparqlParser#expression.
    def enterExpression(self, ctx:SparqlParser.ExpressionContext):
        pass

    # Exit a parse tree produced by SparqlParser#expression.
    def exitExpression(self, ctx:SparqlParser.ExpressionContext):
        pass


    # Enter a parse tree produced by SparqlParser#conditionalOrExpression.
    def enterConditionalOrExpression(self, ctx:SparqlParser.ConditionalOrExpressionContext):
        pass

    # Exit a parse tree produced by SparqlParser#conditionalOrExpression.
    def exitConditionalOrExpression(self, ctx:SparqlParser.ConditionalOrExpressionContext):
        pass


    # Enter a parse tree produced by SparqlParser#conditionalAndExpression.
    def enterConditionalAndExpression(self, ctx:SparqlParser.ConditionalAndExpressionContext):
        pass

    # Exit a parse tree produced by SparqlParser#conditionalAndExpression.
    def exitConditionalAndExpression(self, ctx:SparqlParser.ConditionalAndExpressionContext):
        pass


    # Enter a parse tree produced by SparqlParser#valueLogical.
    def enterValueLogical(self, ctx:SparqlParser.ValueLogicalContext):
        pass

    # Exit a parse tree produced by SparqlParser#valueLogical.
    def exitValueLogical(self, ctx:SparqlParser.ValueLogicalContext):
        pass


    # Enter a parse tree produced by SparqlParser#relationalExpression.
    def enterRelationalExpression(self, ctx:SparqlParser.RelationalExpressionContext):
        pass

    # Exit a parse tree produced by SparqlParser#relationalExpression.
    def exitRelationalExpression(self, ctx:SparqlParser.RelationalExpressionContext):
        pass


    # Enter a parse tree produced by SparqlParser#numericExpression.
    def enterNumericExpression(self, ctx:SparqlParser.NumericExpressionContext):
        pass

    # Exit a parse tree produced by SparqlParser#numericExpression.
    def exitNumericExpression(self, ctx:SparqlParser.NumericExpressionContext):
        pass


    # Enter a parse tree produced by SparqlParser#additiveExpression.
    def enterAdditiveExpression(self, ctx:SparqlParser.AdditiveExpressionContext):
        pass

    # Exit a parse tree produced by SparqlParser#additiveExpression.
    def exitAdditiveExpression(self, ctx:SparqlParser.AdditiveExpressionContext):
        pass


    # Enter a parse tree produced by SparqlParser#multiplicativeExpression.
    def enterMultiplicativeExpression(self, ctx:SparqlParser.MultiplicativeExpressionContext):
        pass

    # Exit a parse tree produced by SparqlParser#multiplicativeExpression.
    def exitMultiplicativeExpression(self, ctx:SparqlParser.MultiplicativeExpressionContext):
        pass


    # Enter a parse tree produced by SparqlParser#unaryExpression.
    def enterUnaryExpression(self, ctx:SparqlParser.UnaryExpressionContext):
        pass

    # Exit a parse tree produced by SparqlParser#unaryExpression.
    def exitUnaryExpression(self, ctx:SparqlParser.UnaryExpressionContext):
        pass


    # Enter a parse tree produced by SparqlParser#primaryExpression.
    def enterPrimaryExpression(self, ctx:SparqlParser.PrimaryExpressionContext):
        pass

    # Exit a parse tree produced by SparqlParser#primaryExpression.
    def exitPrimaryExpression(self, ctx:SparqlParser.PrimaryExpressionContext):
        pass


    # Enter a parse tree produced by SparqlParser#brackettedExpression.
    def enterBrackettedExpression(self, ctx:SparqlParser.BrackettedExpressionContext):
        pass

    # Exit a parse tree produced by SparqlParser#brackettedExpression.
    def exitBrackettedExpression(self, ctx:SparqlParser.BrackettedExpressionContext):
        pass


    # Enter a parse tree produced by SparqlParser#builtInCall.
    def enterBuiltInCall(self, ctx:SparqlParser.BuiltInCallContext):
        pass

    # Exit a parse tree produced by SparqlParser#builtInCall.
    def exitBuiltInCall(self, ctx:SparqlParser.BuiltInCallContext):
        pass


    # Enter a parse tree produced by SparqlParser#regexExpression.
    def enterRegexExpression(self, ctx:SparqlParser.RegexExpressionContext):
        pass

    # Exit a parse tree produced by SparqlParser#regexExpression.
    def exitRegexExpression(self, ctx:SparqlParser.RegexExpressionContext):
        pass


    # Enter a parse tree produced by SparqlParser#substringExpression.
    def enterSubstringExpression(self, ctx:SparqlParser.SubstringExpressionContext):
        pass

    # Exit a parse tree produced by SparqlParser#substringExpression.
    def exitSubstringExpression(self, ctx:SparqlParser.SubstringExpressionContext):
        pass


    # Enter a parse tree produced by SparqlParser#strReplaceExpression.
    def enterStrReplaceExpression(self, ctx:SparqlParser.StrReplaceExpressionContext):
        pass

    # Exit a parse tree produced by SparqlParser#strReplaceExpression.
    def exitStrReplaceExpression(self, ctx:SparqlParser.StrReplaceExpressionContext):
        pass


    # Enter a parse tree produced by SparqlParser#existsFunc.
    def enterExistsFunc(self, ctx:SparqlParser.ExistsFuncContext):
        pass

    # Exit a parse tree produced by SparqlParser#existsFunc.
    def exitExistsFunc(self, ctx:SparqlParser.ExistsFuncContext):
        pass


    # Enter a parse tree produced by SparqlParser#notExistsFunc.
    def enterNotExistsFunc(self, ctx:SparqlParser.NotExistsFuncContext):
        pass

    # Exit a parse tree produced by SparqlParser#notExistsFunc.
    def exitNotExistsFunc(self, ctx:SparqlParser.NotExistsFuncContext):
        pass


    # Enter a parse tree produced by SparqlParser#aggregate.
    def enterAggregate(self, ctx:SparqlParser.AggregateContext):
        pass

    # Exit a parse tree produced by SparqlParser#aggregate.
    def exitAggregate(self, ctx:SparqlParser.AggregateContext):
        pass


    # Enter a parse tree produced by SparqlParser#iriOrFunction.
    def enterIriOrFunction(self, ctx:SparqlParser.IriOrFunctionContext):
        pass

    # Exit a parse tree produced by SparqlParser#iriOrFunction.
    def exitIriOrFunction(self, ctx:SparqlParser.IriOrFunctionContext):
        pass


    # Enter a parse tree produced by SparqlParser#rdfLiteral.
    def enterRdfLiteral(self, ctx:SparqlParser.RdfLiteralContext):
        pass

    # Exit a parse tree produced by SparqlParser#rdfLiteral.
    def exitRdfLiteral(self, ctx:SparqlParser.RdfLiteralContext):
        pass


    # Enter a parse tree produced by SparqlParser#numericLiteral.
    def enterNumericLiteral(self, ctx:SparqlParser.NumericLiteralContext):
        pass

    # Exit a parse tree produced by SparqlParser#numericLiteral.
    def exitNumericLiteral(self, ctx:SparqlParser.NumericLiteralContext):
        pass


    # Enter a parse tree produced by SparqlParser#numericLiteralUnsigned.
    def enterNumericLiteralUnsigned(self, ctx:SparqlParser.NumericLiteralUnsignedContext):
        pass

    # Exit a parse tree produced by SparqlParser#numericLiteralUnsigned.
    def exitNumericLiteralUnsigned(self, ctx:SparqlParser.NumericLiteralUnsignedContext):
        pass


    # Enter a parse tree produced by SparqlParser#numericLiteralPositive.
    def enterNumericLiteralPositive(self, ctx:SparqlParser.NumericLiteralPositiveContext):
        pass

    # Exit a parse tree produced by SparqlParser#numericLiteralPositive.
    def exitNumericLiteralPositive(self, ctx:SparqlParser.NumericLiteralPositiveContext):
        pass


    # Enter a parse tree produced by SparqlParser#numericLiteralNegative.
    def enterNumericLiteralNegative(self, ctx:SparqlParser.NumericLiteralNegativeContext):
        pass

    # Exit a parse tree produced by SparqlParser#numericLiteralNegative.
    def exitNumericLiteralNegative(self, ctx:SparqlParser.NumericLiteralNegativeContext):
        pass


    # Enter a parse tree produced by SparqlParser#booleanLiteral.
    def enterBooleanLiteral(self, ctx:SparqlParser.BooleanLiteralContext):
        pass

    # Exit a parse tree produced by SparqlParser#booleanLiteral.
    def exitBooleanLiteral(self, ctx:SparqlParser.BooleanLiteralContext):
        pass


    # Enter a parse tree produced by SparqlParser#string.
    def enterString(self, ctx:SparqlParser.StringContext):
        pass

    # Exit a parse tree produced by SparqlParser#string.
    def exitString(self, ctx:SparqlParser.StringContext):
        pass


    # Enter a parse tree produced by SparqlParser#iri.
    def enterIri(self, ctx:SparqlParser.IriContext):
        pass

    # Exit a parse tree produced by SparqlParser#iri.
    def exitIri(self, ctx:SparqlParser.IriContext):
        pass


    # Enter a parse tree produced by SparqlParser#prefixedName.
    def enterPrefixedName(self, ctx:SparqlParser.PrefixedNameContext):
        pass

    # Exit a parse tree produced by SparqlParser#prefixedName.
    def exitPrefixedName(self, ctx:SparqlParser.PrefixedNameContext):
        pass


    # Enter a parse tree produced by SparqlParser#blankNode.
    def enterBlankNode(self, ctx:SparqlParser.BlankNodeContext):
        pass

    # Exit a parse tree produced by SparqlParser#blankNode.
    def exitBlankNode(self, ctx:SparqlParser.BlankNodeContext):
        pass



del SparqlParser