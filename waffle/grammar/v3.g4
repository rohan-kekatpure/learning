grammar waffle;

program: stat* EOF;

stat: TBL  (ID | ID EQ table) ';' ;
table: ID | whereclause | aggclause | column | columnlist;
whereclause: table WHERE condition ;
aggclause: table GROUPBY column;
condition: columncondition | compoundcondition;
columncondition: column ('>' | '<' | EQ | NE) column;
compoundcondition: condition (AND | OR) condition;
column: ID | renamecolumn | tableattr;
tableattr: table DOT ID;
renamecolumn: column TILDE column;
columnlist: ID | column COMMA columnlist;

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

INT : [0-9]+ ;
ID: [a-zA-Z_][a-zA-Z_0-9]* ;
WS: [ \t\n\r\f]+ -> skip ;