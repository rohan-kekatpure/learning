grammar waffle;

program: stat* EOF;

stat: TBL (ID | ID EQ table) ';' ;

// A table is a base expression followed by zero or more chained operations
table: table_base table_tail;
table_tail: whereclause_op table_tail | aggclause_op table_tail | ;
whereclause_op: WHERE condition;
aggclause_op: GROUPBY column;

// The base of a table can be an ID, a column, or a column list
table_base: ID | column | columnlist;

// A condition is a base condition followed by zero or more AND/OR clauses
condition: columncondition condition_tail;
condition_tail: (AND | OR) columncondition condition_tail | ;

// A column can be an ID, a renamed column, or a table attribute
// The mutual recursion with table is broken here by defining base_column as a non-recursive starting point
column: base_column column_tail;
column_tail: renamecolumn_op column_tail | tableattr_op column_tail | ;
base_column: ID;
renamecolumn_op: TILDE column;
tableattr_op: DOT ID;

// A column list is a comma-separated list of columns
columnlist: column (COMMA column)*;

columncondition: column ('>' | '<' | EQ | NE) (column | literal);

literal: INT | FLOAT| STRING | 'true' | 'false' | 'NULL';

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
FLOAT: [0-9]+'.'[0-9]*;
STRING: '"'[a-zA-Z0-9]*'"';
ID: [a-zA-Z_][a-zA-Z_0-9]* ;
WS: [ \t\n\r\f]+ -> skip ;