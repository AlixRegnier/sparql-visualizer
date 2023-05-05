grammar Sparql;


statement: query | update
;

query: prologue (selectQuery | constructQuery | describeQuery | askQuery) valuesClause
;

prologue: (baseDecl | prefixDecl)*
;

baseDecl: ( 'base' | 'BASE' ) IRIREF
;

prefixDecl: ( 'prefix' | 'PREFIX' ) PNAME_NS IRIREF
;

selectQuery: selectClause datasetClause* whereClause solutionModifier;

subSelect: selectClause whereClause solutionModifier valuesClause;

selectClause: ( 'select' | 'SELECT' ) ('distinct' | 'DISTINCT' | 'reduced' | 'REDUCED')? ((var | ('(' expression ( 'as' | 'AS' ) var ')'))+ | '*');

constructQuery: ( 'construct' | 'CONSTRUCT' ) (constructTemplate datasetClause* whereClause solutionModifier | datasetClause* ( 'where' | 'WHERE' ) '{' triplesTemplate? '}' solutionModifier);

describeQuery: ( 'describe' | 'DESCRIBE' ) (varOrIri+ | '*') datasetClause* whereClause? solutionModifier;

askQuery: ( 'ask' | 'ASK' ) datasetClause* whereClause solutionModifier;

datasetClause: ( 'from' | 'FROM' ) (defaultGraphClause| namedGraphClause);

defaultGraphClause: sourceSelector;

namedGraphClause: ( 'named' | 'NAMED' ) sourceSelector;

sourceSelector: iri;

whereClause: ('where' | 'WHERE' )? groupGraphPattern;

solutionModifier: groupClause? havingClause? orderClause? limitOffsetClauses?;

groupClause: ( 'group' | 'GROUP' ) ( 'by' | 'BY' ) groupCondition+;

groupCondition: builtInCall | functionCall | '(' expression (('as' | 'AS') var)? ')' | var;

havingClause: ( 'having' | 'HAVING' ) havingCondition+;

havingCondition: constraint;

orderClause: ( 'order' | 'ORDER' ) ( 'by' | 'BY' ) orderCondition+;

orderCondition: (('ASC' | 'asc' | 'DESC' | 'desc') brackettedExpression)
| (constraint | var)
;

limitOffsetClauses: limitClause offsetClause? | offsetClause limitClause?;

limitClause: ( 'limit' | 'LIMIT' ) INTEGER;

offsetClause: ( 'offset' | 'OFFSET' ) INTEGER;

valuesClause: (('values' | 'VALUES') dataBlock)?;

update: prologue (update1 (';' update)? )?;

update1: load | clear | drop | add | move | copy | create | insertData | deleteData | deleteWhere | modify ;

load: ( 'load' | 'LOAD' ) ('silent' | 'SILENT')? iri (('into' | 'INTO') graphRef)?
;

clear: ( 'clear' | 'CLEAR' ) ('silent' | 'SILENT')? graphRefAll;

drop: ( 'drop' | 'DROP' ) ('silent' | 'SILENT')? graphRefAll;

create: ( 'create' | 'CREATE' ) ('silent' | 'SILENT')? graphRef;

add: ( 'add' | 'ADD' ) ('silent' | 'SILENT')? graphOrDefault ( 'to' | 'TO' ) graphOrDefault;

move: ( 'move' | 'MOVE' ) ('silent' | 'SILENT')? graphOrDefault ( 'to' | 'TO' ) graphOrDefault;

copy: ( 'copy' | 'COPY' ) ('silent' | 'SILENT')? graphOrDefault ( 'to' | 'TO' ) graphOrDefault;

insertData
: ('INSERT DATA' | 'insert data') quadData;

deleteData
@init {
allowsBlankNodes = False
}
@after {
allowsBlankNodes = True
}
: ('DELETE DATA' | 'delete data') quadData;

deleteWhere
@init {
allowsBlankNodes = False
}
@after {
allowsBlankNodes = True
}
: ('DELETE WHERE' | 'delete where') quadPattern;

modify: (('with' | 'WITH') iri)? (deleteClause insertClause?| insertClause) usingClause* ( 'where' | 'WHERE' ) groupGraphPattern;

deleteClause
@init {
allowsBlankNodes = False
}
@after {
allowsBlankNodes = True
}
: ( 'delete' | 'DELETE' ) quadPattern;

insertClause: ( 'insert' | 'INSERT' ) quadPattern;

usingClause: ( 'using' | 'USING' ) (iri | ( 'named' | 'NAMED' ) iri);

graphOrDefault: ( 'default' | 'DEFAULT' ) | ('graph' | 'GRAPH')? iri;

graphRef: ( 'graph' | 'GRAPH' ) iri;

graphRefAll: graphRef | ( 'default' | 'DEFAULT' ) | ( 'named' | 'NAMED' ) | ('all' | 'ALL');

quadPattern: '{' quads '}';

quadData: '{' quads '}';

quads: triplesTemplate? (quadsNotTriples '.'? triplesTemplate?) *
;

quadsNotTriples: ( 'graph' | 'GRAPH' ) varOrIri groupGraphPattern
;

triplesTemplate: triplesSameSubject ('.' triplesTemplate?)?
;

groupGraphPattern: '{' (subSelect | groupGraphPatternSub) '}'
;

groupGraphPatternSub: triplesBlock? (graphPatternNotTriples '.'? triplesBlock? )*
;

triplesBlock: triplesSameSubjectPath ( '.' triplesBlock?)?
;

graphPatternNotTriples: groupOrUnionGraphPattern | optionalGraphPattern | minusGraphPattern | graphGraphPattern
| serviceGraphPattern | filterClause | bind | inlineData
;

optionalGraphPattern: ( 'optional' | 'OPTIONAL' ) groupGraphPattern
;

graphGraphPattern: ( 'graph' | 'GRAPH' ) varOrIri groupGraphPattern
;

serviceGraphPattern: ( 'service' | 'SERVICE' ) ('silent' | 'SILENT')? varOrIri groupGraphPattern
;

bind: ( 'bind' | 'BIND' ) '(' expression ( 'as' | 'AS' ) var ')'
;

inlineData: ( 'values' | 'VALUES' ) dataBlock
;

dataBlock: inlineDataOneVar | inlineDataFull
;

inlineDataOneVar: var '{' dataBlockValue* '}'
;

inlineDataFull: (NIL | '(' var* ')') '{' ( '(' dataBlockValue* ')' | NIL)* '}'
;

dataBlockValue: iri | rdfLiteral | numericLiteral | booleanLiteral | ( 'undef' | 'UNDEF' )
;

minusGraphPattern: ( 'minus' | 'MINUS' ) groupGraphPattern
;

groupOrUnionGraphPattern: groupGraphPattern (('union' | 'UNION') groupGraphPattern)*
;

filterClause: ( 'filter' | 'FILTER' ) constraint
;

constraint: brackettedExpression | builtInCall | functionCall
;

functionCall: iri argList
;

argList: NIL | '(' ('distinct' | 'DISTINCT')? expression ( ',' expression)* ')'
;

expressionList: NIL | '(' expression ( ',' expression)* ')'
;

constructTemplate: '{' constructTriples? '}'
;

constructTriples: triplesSameSubject ( '.' constructTriples? )?
;

triplesSameSubject: varOrTerm propertyListNotEmpty | triplesNode propertyList
;

propertyList: propertyListNotEmpty?
;

propertyListNotEmpty: verb objectList (';' (verb objectList)?)*
;

verb:
varOrIri
| 'a'
| 'A' // See note at the beginning of the grammar
;

objectList: objectClause (',' objectClause)*
;

objectClause: graphNode
;

triplesSameSubjectPath: varOrTerm propertyListPathNotEmpty | triplesNodePath propertyListPath
;

propertyListPath: propertyListPathNotEmpty?
;

propertyListPathNotEmpty: (verbPath | verbSimple) objectListPath ( ';' ((verbPath | verbSimple) objectList)?)*
;

verbPath: path
;

verbSimple: var
;

objectListPath: objectPath (',' objectPath)*
;

objectPath: graphNodePath
;

path: pathAlternative
;

pathAlternative: pathSequence ('|' pathSequence)*
;

pathSequence: pathEltOrInverse ('/' pathEltOrInverse)*
;

pathElt: pathPrimary pathMod?
;

pathEltOrInverse: pathElt | '^' pathElt
;

pathMod: '?' | '*' | '+'
;

pathPrimary:
iri
| 'a'
| 'A' // See note at the beginning of the grammar
| '!' pathNegatedPropertySet
| '(' path ')'
;

pathNegatedPropertySet: pathOneInPropertySet | '(' ( pathOneInPropertySet ( '|' pathOneInPropertySet )* )? ')'
;

pathOneInPropertySet: iri
| 'a'
| 'A' // See note at the beginning of the grammar
| '^' (
iri
| 'a'
| 'A' // See note at the beginning of the grammar
)
;

triplesNode: collection | blankNodePropertyList
;

blankNodePropertyList: '[' propertyListNotEmpty ']'
;

triplesNodePath: collectionPath | blankNodePropertyListPath
;

blankNodePropertyListPath: '[' propertyListPathNotEmpty ']'
;

collection: '(' graphNode+ ')'
;

collectionPath: '(' graphNodePath+ ')'
;

graphNode: varOrTerm | triplesNode
;

graphNodePath: varOrTerm | triplesNodePath
;

varOrTerm: var | graphTerm
;

varOrIri: var | iri
;

var: VAR1 | VAR2
;

graphTerm: iri | rdfLiteral | numericLiteral | booleanLiteral | {allowsBlankNodes}? blankNode | NIL
;

expression: conditionalOrExpression
;

conditionalOrExpression: conditionalAndExpression ( '||' conditionalAndExpression )*
;

conditionalAndExpression: valueLogical ( '&&' valueLogical )*
;

valueLogical: relationalExpression
;

relationalExpression: numericExpression ( '=' numericExpression | '!=' numericExpression | '<' numericExpression | '>' numericExpression | '<=' numericExpression | '>=' numericExpression | ( 'in' | 'IN' ) expressionList | ( 'not' | 'NOT' ) ( 'in' | 'IN' ) expressionList )?
;

numericExpression: additiveExpression
;

additiveExpression: multiplicativeExpression ( '+' multiplicativeExpression | '-' multiplicativeExpression | ( numericLiteralPositive | numericLiteralNegative ) ( ( '*' unaryExpression ) | ( '/' unaryExpression ) )* )*
;

multiplicativeExpression: unaryExpression ( '*' unaryExpression | '/' unaryExpression )*
;

unaryExpression: '!' primaryExpression
| '+' primaryExpression
| '-' primaryExpression
| primaryExpression
;

primaryExpression: brackettedExpression | builtInCall | iriOrFunction | rdfLiteral | numericLiteral | booleanLiteral | var
;

brackettedExpression: '(' expression ')'
;

builtInCall: aggregate
| ( 'str' | 'STR' ) '(' expression ')'
| ( 'lang' | 'LANG' ) '(' expression ')'
| ( 'langmatches' | 'LANGMATCHES' ) '(' expression ',' expression ')'
| ( 'datatype' | 'DATATYPE' ) '(' expression ')'
| ( 'bound' | 'BOUND' ) '(' var ')'
| ( 'iri' | 'IRI' ) '(' expression ')'
| ( 'uri' | 'URI' ) '(' expression ')'
| ( 'bnode' | 'BNODE' ) ( '(' expression ')' | NIL )
| ( 'rand' | 'RAND' ) NIL
| ( 'abs' | 'ABS' ) '(' expression ')'
| ( 'ceil' | 'CEIL' ) '(' expression ')'
| ( 'floor' | 'FLOOR' ) '(' expression ')'
| ( 'round' | 'ROUND' ) '(' expression ')'
| ( 'concat' | 'CONCAT' ) expressionList
| substringExpression
| ( 'strlen' | 'STRLEN' ) '(' expression ')'
| strReplaceExpression
| ( 'ucase' | 'UCASE' ) '(' expression ')'
| ( 'lcase' | 'LCASE' ) '(' expression ')'
| ( 'ENCODE_FOR_URI' | 'encode_for_uri' ) '(' expression ')'
| ( 'contains' | 'CONTAINS' ) '(' expression ',' expression ')'
| ( 'strstarts' | 'STRSTARTS' ) '(' expression ',' expression ')'
| ( 'strends' | 'STRENDS' ) '(' expression ',' expression ')'
| ( 'strbefore' | 'STRBEFORE' ) '(' expression ',' expression ')'
| ( 'strafter' | 'STRAFTER' ) '(' expression ',' expression ')'
| ( 'year' | 'YEAR' ) '(' expression ')'
| ( 'month' | 'MONTH' ) '(' expression ')'
| ( 'day' | 'DAY' ) '(' expression ')'
| ( 'hours' | 'HOURS' ) '(' expression ')'
| ( 'minutes' | 'MINUTES' ) '(' expression ')'
| ( 'seconds' | 'SECONDS' ) '(' expression ')'
| ( 'timezone' | 'TIMEZONE' ) '(' expression ')'
| ( 'tz' | 'TZ' ) '(' expression ')'
| ( 'now' | 'NOW' ) NIL
| ( 'uuid' | 'UUID' ) NIL
| ( 'struuid' | 'STRUUID' ) NIL
| ( 'md5' | 'MD5' ) '(' expression ')'
| ( 'sha1' | 'SHA1' ) '(' expression ')'
| ( 'sha256' | 'SHA256' ) '(' expression ')'
| ( 'sha384' | 'SHA384' ) '(' expression ')'
| ( 'sha512' | 'SHA512' ) '(' expression ')'
| ( 'coalesce' | 'COALESCE' ) expressionList
| ( 'if' | 'IF' ) '(' expression ',' expression ',' expression ')'
| ( 'strlang' | 'STRLANG' ) '(' expression ',' expression ')'
| ( 'strdt' | 'STRDT' ) '(' expression ',' expression ')'
| ( 'sameterm' | 'SAMETERM' ) '(' expression ',' expression ')'
| ( 'isiri' | 'ISIRI' ) '(' expression ')'
| ( 'isuri' | 'ISURI' ) '(' expression ')'
| ( 'isblank' | 'ISBLANK' ) '(' expression ')'
| ( 'isliteral' | 'ISLITERAL' ) '(' expression ')'
| ( 'isnumeric' | 'ISNUMERIC' ) '(' expression ')'
| regexExpression
| existsFunc
| notExistsFunc
;

regexExpression: ( 'regex' | 'REGEX' ) '(' expression ',' expression ( ',' expression )? ')'
;

substringExpression: ( 'substr' | 'SUBSTR' ) '(' expression ',' expression ( ',' expression )? ')'
;

strReplaceExpression: ( 'replace' | 'REPLACE' ) '(' expression ',' expression ',' expression ( ',' expression )? ')'
;

existsFunc: ( 'exists' | 'EXISTS' ) groupGraphPattern
;

notExistsFunc: ( 'not' | 'NOT' ) ( 'exists' | 'EXISTS' ) groupGraphPattern
;

aggregate: ( 'count' | 'COUNT' ) '(' ('distinct' | 'DISTINCT')? ( '*' | expression ) ')'
| ( 'sum' | 'SUM' ) '(' ('distinct' | 'DISTINCT')? expression ')'
| ( 'min' | 'MIN' ) '(' ('distinct' | 'DISTINCT')? expression ')'
| ( 'max' | 'MAX' ) '(' ('distinct' | 'DISTINCT')? expression ')'
| ( 'avg' | 'AVG' ) '(' ('distinct' | 'DISTINCT')? expression ')'
| ( 'sample' | 'SAMPLE' ) '(' ('distinct' | 'DISTINCT')? expression ')'
| ('group_concat' | 'GROUP_CONCAT') '(' ('distinct' | 'DISTINCT')? expression ( ';' ( 'separator' | 'SEPARATOR' ) '=' string )? ')'
;

iriOrFunction: iri argList?
;

rdfLiteral: string ( LANGTAG | ( '^^' iri ) )?
;

numericLiteral: numericLiteralUnsigned | numericLiteralPositive | numericLiteralNegative
;

numericLiteralUnsigned: INTEGER | DECIMAL | DOUBLE
;

numericLiteralPositive: INTEGER_POSITIVE | DECIMAL_POSITIVE | DOUBLE_POSITIVE
;

numericLiteralNegative: INTEGER_NEGATIVE | DECIMAL_NEGATIVE | DOUBLE_NEGATIVE
;

booleanLiteral:
'true'
| 'false'
| 'TRUE' // See Note at the beginning of the grammar
| 'FALSE' // See Note at the beginning of the grammar
;

string: STRING_LITERAL1 | STRING_LITERAL2 | STRING_LITERAL_LONG1 | STRING_LITERAL_LONG2
;

iri: IRIREF | prefixedName
;

prefixedName: PNAME_LN | PNAME_NS
;

blankNode: BLANK_NODE_LABEL | ANON
;


IRIREF: '<' ( ~('<' | '>' | '"' | '{' | '}' | '|' | '^' | '\\' | '`' | [\u0000-\u0020] ))* '>'
;

PNAME_NS: PN_PREFIX? ':'
;

PNAME_LN: PNAME_NS PN_LOCAL
;

BLANK_NODE_LABEL: '_:' ( PN_CHARS_U | [0-9] ) ((PN_CHARS|'.')* PN_CHARS)?
;

VAR1: '?' VARNAME
;

VAR2: '$' VARNAME
;

LANGTAG: '@' [a-zA-Z]+ ('-' [a-zA-Z0-9]+)*
;

INTEGER: [0-9]+
;

DECIMAL: [0-9]* '.' [0-9]+
;

DOUBLE: [0-9]+ '.' [0-9]* EXPONENT | '.' ([0-9])+ EXPONENT | ([0-9])+ EXPONENT
;

INTEGER_POSITIVE: '+' INTEGER
;

DECIMAL_POSITIVE: '+' DECIMAL
;

DOUBLE_POSITIVE: '+' DOUBLE
;

INTEGER_NEGATIVE: '-' INTEGER
;

DECIMAL_NEGATIVE: '-' DECIMAL
;

DOUBLE_NEGATIVE: '-' DOUBLE
;

EXPONENT: [eE] [+-]? [0-9]+
;

STRING_LITERAL1: '\'' ( ~('\u0027' | '\u005C' | '\u000A' | '\u000D') | ECHAR )* '\''
;

STRING_LITERAL2: '"' ( ~('\u0022' | '\u005C' | '\u000A' | '\u000D') | ECHAR )* '"'
;

STRING_LITERAL_LONG1: '\'\'\'' ( ( '\'' | '\'\'' )? ( [^'\\] | ECHAR ) )* '\'\'\''
;

STRING_LITERAL_LONG2: '"""' ( ( '"' | '""' )? ( [^"\\] | ECHAR ) )* '"""'
;

ECHAR: '\\' ('t' | 'b' | 'n' | 'r' | 'f' | '"' | '\'')
;

NIL: '(' WS* ')'
;

WS: (COMMENT | (' ' | '\t' | '\r' | '\n')+) -> skip
;

COMMENT: '#' ~('\u000A' | '\u000D')* ('\u000A' | '\u000D')
;

ANON: '[' WS* ']'
;

PN_CHARS_BASE
: [A-Z]
| [a-z]
| [\u00C0-\u00D6]
| [\u00D8-\u00F6]
| [\u00F8-\u02FF]
| [\u0370-\u037D]
| [\u037F-\u1FFF]
| [\u200C-\u200D]
| [\u2070-\u218F]
| [\u2C00-\u2FEF]
| [\u3001-\uD7FF]
| [\uF900-\uFDCF]
| [\uFDF0-\uFFFD]
;

PN_CHARS_U: PN_CHARS_BASE | '_'
;

VARNAME: ( PN_CHARS_U | [0-9] ) ( PN_CHARS_U | [0-9] | '\u00B7' | [\u0300-\u036F] | [\u203F-\u2040] )*
;

PN_CHARS: PN_CHARS_U | '-' | [0-9] | '\u00B7' | [\u0300-\u036F] | [\u203F-\u2040]
;

PN_PREFIX: PN_CHARS_BASE ((PN_CHARS|'.')* PN_CHARS)?
;

PN_LOCAL: (PN_CHARS_U | ':' | [0-9] | PLX ) ((PN_CHARS | '.' | ':' | PLX)* (PN_CHARS | ':' | PLX) )?
;

PLX: PERCENT | PN_LOCAL_ESC
;

PERCENT: '%' HEX HEX
;

HEX: [0-9] | [A-F] | [a-f]
;

PN_LOCAL_ESC: '\\' ( ':' | '_' | '~' | '.' | '-' | '!' | '$' | '&' | '\'' | '(' | ')' | '*' | '+' | ',' | ';' | '=' | '/' | '?' | '#' | '@' | '%' )
;


