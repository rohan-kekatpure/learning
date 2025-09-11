grammar waffle;

program: stmt* EOF;

/*
 A Statement can be either a table manipulation statement
 or a resultset statement. To be expanded later.
*/ 
stmt: table_stmt | result_stmt ;

/*
 A resultset statement is just declaring the final resultset
 rset X
*/
result_stmt: RSET ID ';' ;

/*
 A table statement is of a simple form:
 tbl A = <table expression>
*/
table_stmt: TBL ID EQ table ';' ;
table: (ID | column | columnlist) (WHERE conditions | GROUPBY columnlist |);

/*
 Column can be an id or a dot attribute or a list 
*/
column:  ID DOT ID | column TILDE ID; 
columnlist: column (COMMA column)*;

/*
 A single condition is column or literal compared to other 
 column or literal. Conditions is one or more condition.
*/
conditions: condition ((AND | OR) condition)*;
condition: (column | literal) (GT | GEQ | LT | LEQ | EQ | NE) (column | literal);

/*
 Literals
*/
literal: INT | FLOAT| STRING | 'true' | 'false' | 'NULL';

/*
 Operators and terminal rules
*/
EQ : '=' ;
SEMI : ';' ;
DOT: '.' ;
TBL: 'tbl' ;
COMMA: ',' ;
TILDE: '~' ;
WHERE: '%%';
GROUPBY: '::';
NE : '!=';
AND: 'and';
OR: 'or';
RSET: 'rset';
GT: '>';
GEQ: '>=';
LT: '<';
LEQ: '<=';

INT : [0-9]+ ;
FLOAT: [0-9]+'.'[0-9]*;
STRING: '"'[a-zA-Z0-9]*'"';
ID: [a-zA-Z_][a-zA-Z_0-9]* ;
WS: [ \t\n\r\f]+ -> skip ;