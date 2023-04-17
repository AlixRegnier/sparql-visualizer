# Generated from Sparql.g4 by ANTLR 4.10.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SparqlParser import SparqlParser
else:
    from SparqlParser import SparqlParser

# This class defines a complete generic visitor for a parse tree produced by SparqlParser.

class SparqlVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SparqlParser#statement.
    def visitStatement(self, ctx:SparqlParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#query.
    def visitQuery(self, ctx:SparqlParser.QueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#prologue.
    def visitPrologue(self, ctx:SparqlParser.PrologueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#baseDecl.
    def visitBaseDecl(self, ctx:SparqlParser.BaseDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#prefixDecl.
    def visitPrefixDecl(self, ctx:SparqlParser.PrefixDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#selectQuery.
    def visitSelectQuery(self, ctx:SparqlParser.SelectQueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#subSelect.
    def visitSubSelect(self, ctx:SparqlParser.SubSelectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#selectClause.
    def visitSelectClause(self, ctx:SparqlParser.SelectClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#constructQuery.
    def visitConstructQuery(self, ctx:SparqlParser.ConstructQueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#describeQuery.
    def visitDescribeQuery(self, ctx:SparqlParser.DescribeQueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#askQuery.
    def visitAskQuery(self, ctx:SparqlParser.AskQueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#datasetClause.
    def visitDatasetClause(self, ctx:SparqlParser.DatasetClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#defaultGraphClause.
    def visitDefaultGraphClause(self, ctx:SparqlParser.DefaultGraphClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#namedGraphClause.
    def visitNamedGraphClause(self, ctx:SparqlParser.NamedGraphClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#sourceSelector.
    def visitSourceSelector(self, ctx:SparqlParser.SourceSelectorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#whereClause.
    def visitWhereClause(self, ctx:SparqlParser.WhereClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#solutionModifier.
    def visitSolutionModifier(self, ctx:SparqlParser.SolutionModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#groupClause.
    def visitGroupClause(self, ctx:SparqlParser.GroupClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#groupCondition.
    def visitGroupCondition(self, ctx:SparqlParser.GroupConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#havingClause.
    def visitHavingClause(self, ctx:SparqlParser.HavingClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#havingCondition.
    def visitHavingCondition(self, ctx:SparqlParser.HavingConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#orderClause.
    def visitOrderClause(self, ctx:SparqlParser.OrderClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#orderCondition.
    def visitOrderCondition(self, ctx:SparqlParser.OrderConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#limitOffsetClauses.
    def visitLimitOffsetClauses(self, ctx:SparqlParser.LimitOffsetClausesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#limitClause.
    def visitLimitClause(self, ctx:SparqlParser.LimitClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#offsetClause.
    def visitOffsetClause(self, ctx:SparqlParser.OffsetClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#valuesClause.
    def visitValuesClause(self, ctx:SparqlParser.ValuesClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#update.
    def visitUpdate(self, ctx:SparqlParser.UpdateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#update1.
    def visitUpdate1(self, ctx:SparqlParser.Update1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#load.
    def visitLoad(self, ctx:SparqlParser.LoadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#clear.
    def visitClear(self, ctx:SparqlParser.ClearContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#drop.
    def visitDrop(self, ctx:SparqlParser.DropContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#create.
    def visitCreate(self, ctx:SparqlParser.CreateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#add.
    def visitAdd(self, ctx:SparqlParser.AddContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#move.
    def visitMove(self, ctx:SparqlParser.MoveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#copy.
    def visitCopy(self, ctx:SparqlParser.CopyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#insertData.
    def visitInsertData(self, ctx:SparqlParser.InsertDataContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#deleteData.
    def visitDeleteData(self, ctx:SparqlParser.DeleteDataContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#deleteWhere.
    def visitDeleteWhere(self, ctx:SparqlParser.DeleteWhereContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#modify.
    def visitModify(self, ctx:SparqlParser.ModifyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#deleteClause.
    def visitDeleteClause(self, ctx:SparqlParser.DeleteClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#insertClause.
    def visitInsertClause(self, ctx:SparqlParser.InsertClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#usingClause.
    def visitUsingClause(self, ctx:SparqlParser.UsingClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#graphOrDefault.
    def visitGraphOrDefault(self, ctx:SparqlParser.GraphOrDefaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#graphRef.
    def visitGraphRef(self, ctx:SparqlParser.GraphRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#graphRefAll.
    def visitGraphRefAll(self, ctx:SparqlParser.GraphRefAllContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#quadPattern.
    def visitQuadPattern(self, ctx:SparqlParser.QuadPatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#quadData.
    def visitQuadData(self, ctx:SparqlParser.QuadDataContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#quads.
    def visitQuads(self, ctx:SparqlParser.QuadsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#quadsNotTriples.
    def visitQuadsNotTriples(self, ctx:SparqlParser.QuadsNotTriplesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#triplesTemplate.
    def visitTriplesTemplate(self, ctx:SparqlParser.TriplesTemplateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#groupGraphPattern.
    def visitGroupGraphPattern(self, ctx:SparqlParser.GroupGraphPatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#groupGraphPatternSub.
    def visitGroupGraphPatternSub(self, ctx:SparqlParser.GroupGraphPatternSubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#triplesBlock.
    def visitTriplesBlock(self, ctx:SparqlParser.TriplesBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#graphPatternNotTriples.
    def visitGraphPatternNotTriples(self, ctx:SparqlParser.GraphPatternNotTriplesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#optionalGraphPattern.
    def visitOptionalGraphPattern(self, ctx:SparqlParser.OptionalGraphPatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#graphGraphPattern.
    def visitGraphGraphPattern(self, ctx:SparqlParser.GraphGraphPatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#serviceGraphPattern.
    def visitServiceGraphPattern(self, ctx:SparqlParser.ServiceGraphPatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#bind.
    def visitBind(self, ctx:SparqlParser.BindContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#inlineData.
    def visitInlineData(self, ctx:SparqlParser.InlineDataContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#dataBlock.
    def visitDataBlock(self, ctx:SparqlParser.DataBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#inlineDataOneVar.
    def visitInlineDataOneVar(self, ctx:SparqlParser.InlineDataOneVarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#inlineDataFull.
    def visitInlineDataFull(self, ctx:SparqlParser.InlineDataFullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#dataBlockValue.
    def visitDataBlockValue(self, ctx:SparqlParser.DataBlockValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#minusGraphPattern.
    def visitMinusGraphPattern(self, ctx:SparqlParser.MinusGraphPatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#groupOrUnionGraphPattern.
    def visitGroupOrUnionGraphPattern(self, ctx:SparqlParser.GroupOrUnionGraphPatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#filterClause.
    def visitFilterClause(self, ctx:SparqlParser.FilterClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#constraint.
    def visitConstraint(self, ctx:SparqlParser.ConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#functionCall.
    def visitFunctionCall(self, ctx:SparqlParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#argList.
    def visitArgList(self, ctx:SparqlParser.ArgListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#expressionList.
    def visitExpressionList(self, ctx:SparqlParser.ExpressionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#constructTemplate.
    def visitConstructTemplate(self, ctx:SparqlParser.ConstructTemplateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#constructTriples.
    def visitConstructTriples(self, ctx:SparqlParser.ConstructTriplesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#triplesSameSubject.
    def visitTriplesSameSubject(self, ctx:SparqlParser.TriplesSameSubjectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#propertyList.
    def visitPropertyList(self, ctx:SparqlParser.PropertyListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#propertyListNotEmpty.
    def visitPropertyListNotEmpty(self, ctx:SparqlParser.PropertyListNotEmptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#verb.
    def visitVerb(self, ctx:SparqlParser.VerbContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#objectList.
    def visitObjectList(self, ctx:SparqlParser.ObjectListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#objectClause.
    def visitObjectClause(self, ctx:SparqlParser.ObjectClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#triplesSameSubjectPath.
    def visitTriplesSameSubjectPath(self, ctx:SparqlParser.TriplesSameSubjectPathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#propertyListPath.
    def visitPropertyListPath(self, ctx:SparqlParser.PropertyListPathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#propertyListPathNotEmpty.
    def visitPropertyListPathNotEmpty(self, ctx:SparqlParser.PropertyListPathNotEmptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#verbPath.
    def visitVerbPath(self, ctx:SparqlParser.VerbPathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#verbSimple.
    def visitVerbSimple(self, ctx:SparqlParser.VerbSimpleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#objectListPath.
    def visitObjectListPath(self, ctx:SparqlParser.ObjectListPathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#objectPath.
    def visitObjectPath(self, ctx:SparqlParser.ObjectPathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#path.
    def visitPath(self, ctx:SparqlParser.PathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#pathAlternative.
    def visitPathAlternative(self, ctx:SparqlParser.PathAlternativeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#pathSequence.
    def visitPathSequence(self, ctx:SparqlParser.PathSequenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#pathElt.
    def visitPathElt(self, ctx:SparqlParser.PathEltContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#pathEltOrInverse.
    def visitPathEltOrInverse(self, ctx:SparqlParser.PathEltOrInverseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#pathMod.
    def visitPathMod(self, ctx:SparqlParser.PathModContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#pathPrimary.
    def visitPathPrimary(self, ctx:SparqlParser.PathPrimaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#pathNegatedPropertySet.
    def visitPathNegatedPropertySet(self, ctx:SparqlParser.PathNegatedPropertySetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#pathOneInPropertySet.
    def visitPathOneInPropertySet(self, ctx:SparqlParser.PathOneInPropertySetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#triplesNode.
    def visitTriplesNode(self, ctx:SparqlParser.TriplesNodeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#blankNodePropertyList.
    def visitBlankNodePropertyList(self, ctx:SparqlParser.BlankNodePropertyListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#triplesNodePath.
    def visitTriplesNodePath(self, ctx:SparqlParser.TriplesNodePathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#blankNodePropertyListPath.
    def visitBlankNodePropertyListPath(self, ctx:SparqlParser.BlankNodePropertyListPathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#collection.
    def visitCollection(self, ctx:SparqlParser.CollectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#collectionPath.
    def visitCollectionPath(self, ctx:SparqlParser.CollectionPathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#graphNode.
    def visitGraphNode(self, ctx:SparqlParser.GraphNodeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#graphNodePath.
    def visitGraphNodePath(self, ctx:SparqlParser.GraphNodePathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#varOrTerm.
    def visitVarOrTerm(self, ctx:SparqlParser.VarOrTermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#varOrIri.
    def visitVarOrIri(self, ctx:SparqlParser.VarOrIriContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#var.
    def visitVar(self, ctx:SparqlParser.VarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#graphTerm.
    def visitGraphTerm(self, ctx:SparqlParser.GraphTermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#expression.
    def visitExpression(self, ctx:SparqlParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#conditionalOrExpression.
    def visitConditionalOrExpression(self, ctx:SparqlParser.ConditionalOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#conditionalAndExpression.
    def visitConditionalAndExpression(self, ctx:SparqlParser.ConditionalAndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#valueLogical.
    def visitValueLogical(self, ctx:SparqlParser.ValueLogicalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#relationalExpression.
    def visitRelationalExpression(self, ctx:SparqlParser.RelationalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#numericExpression.
    def visitNumericExpression(self, ctx:SparqlParser.NumericExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#additiveExpression.
    def visitAdditiveExpression(self, ctx:SparqlParser.AdditiveExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#multiplicativeExpression.
    def visitMultiplicativeExpression(self, ctx:SparqlParser.MultiplicativeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#unaryExpression.
    def visitUnaryExpression(self, ctx:SparqlParser.UnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#primaryExpression.
    def visitPrimaryExpression(self, ctx:SparqlParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#brackettedExpression.
    def visitBrackettedExpression(self, ctx:SparqlParser.BrackettedExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#builtInCall.
    def visitBuiltInCall(self, ctx:SparqlParser.BuiltInCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#regexExpression.
    def visitRegexExpression(self, ctx:SparqlParser.RegexExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#substringExpression.
    def visitSubstringExpression(self, ctx:SparqlParser.SubstringExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#strReplaceExpression.
    def visitStrReplaceExpression(self, ctx:SparqlParser.StrReplaceExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#existsFunc.
    def visitExistsFunc(self, ctx:SparqlParser.ExistsFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#notExistsFunc.
    def visitNotExistsFunc(self, ctx:SparqlParser.NotExistsFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#aggregate.
    def visitAggregate(self, ctx:SparqlParser.AggregateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#iriOrFunction.
    def visitIriOrFunction(self, ctx:SparqlParser.IriOrFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#rdfLiteral.
    def visitRdfLiteral(self, ctx:SparqlParser.RdfLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#numericLiteral.
    def visitNumericLiteral(self, ctx:SparqlParser.NumericLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#numericLiteralUnsigned.
    def visitNumericLiteralUnsigned(self, ctx:SparqlParser.NumericLiteralUnsignedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#numericLiteralPositive.
    def visitNumericLiteralPositive(self, ctx:SparqlParser.NumericLiteralPositiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#numericLiteralNegative.
    def visitNumericLiteralNegative(self, ctx:SparqlParser.NumericLiteralNegativeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#booleanLiteral.
    def visitBooleanLiteral(self, ctx:SparqlParser.BooleanLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#string.
    def visitString(self, ctx:SparqlParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#iri.
    def visitIri(self, ctx:SparqlParser.IriContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#prefixedName.
    def visitPrefixedName(self, ctx:SparqlParser.PrefixedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SparqlParser#blankNode.
    def visitBlankNode(self, ctx:SparqlParser.BlankNodeContext):
        return self.visitChildren(ctx)



del SparqlParser