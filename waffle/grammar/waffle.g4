grammar waffle;

program: stat* EOF;

stat: TBL  (ID | ID '=' table) ';' ;

table: 
    name 
  | column 
  | table WHERE table
  | table GROUPBY column
  ;

name: ID;

column:
    ID
  | ID '~' ID    
  | ID'.'ID 
  | ID'.'ID '~' ID 
  | INT '~' ID
  | column ',' column
  ;
  
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