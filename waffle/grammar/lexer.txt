// DELETE THIS CONTENT IF YOU PUT COMBINED GRAMMAR IN Parser TAB
lexer grammar ExprLexer;

EQ : '=' ;
SEMI : ';' ;
DOT: '.' ;
TBL: 'tbl' ;
COMMA: ',' ;
TILDE: '~' ;
WHERE: '%%';
GROUPBY: '::';

INT : [0-9]+ ;
ID: [a-zA-Z_][a-zA-Z_0-9]* ;
WS: [ \t\n\r\f]+ -> skip ;

