parser grammar ExprParser;
options { tokenVocab=ExprLexer; }

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