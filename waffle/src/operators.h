#ifndef WAFFLE_AST_H
#define WAFFLE_AST_H

#include <vector>
#include <memory>
#include <string>

#include "token.h"

// Forward declarations to handle mutual dependencies
class Expr;
class TableExpr;
class Condition;
class Column;
class TableBase;
class TableTailOp;
class ColumnCondition;

// Base class for all expressions in the language
class Expr {
public:
    virtual ~Expr() = default;
};

// Represents a literal value (INT, FLOAT, STRING, 'true', 'false', 'NULL')
class LiteralExpr : public Expr {
public:
    Literal literal;
    LiteralExpr(Literal lit) : literal(lit) {}
};

class IdentifierExpr : public Expr {
public:
    Token name;
    IdentifierExpr(Token token) : name(token) {}
};

class Column : public Expr {
public:
    std::string name;
    std::string alias; // Stores the alias from a '~' operator
    std::shared_ptr<Column> parentTable; // For 'tableattr_op' (.)
};

class ColumnList : public Expr {
public:
    std::vector<std::shared_ptr<Column>> columns;
};

class TableBase {
public:
    virtual ~TableBase() = default;
};

class IDTableBase : public TableBase {
public:
    std::shared_ptr<IdentifierExpr> id;
    IDTableBase(std::shared_ptr<IdentifierExpr> identifier) : id(identifier) {}
};

class ColumnTableBase : public TableBase {
public:
    std::shared_ptr<Column> column;
    ColumnTableBase(std::shared_ptr<Column> col) : column(col) {}
};

class ColumnListTableBase : public TableBase {
public:
    std::shared_ptr<ColumnList> columnList;
    ColumnListTableBase(std::shared_ptr<ColumnList> list) : columnList(list) {}
};

class ColumnCondition {
public:
    std::shared_ptr<Column> left;
    Token op;
    std::shared_ptr<Expr> right; // Can be a Column or a LiteralExpr
    ColumnCondition(std::shared_ptr<Column> l, Token o, std::shared_ptr<Expr> r)
        : left(l), op(o), right(r) {}
};

class Condition {
public:
    std::shared_ptr<ColumnCondition> baseCondition;
    std::vector<std::pair<Token, std::shared_ptr<ColumnCondition>>> tail; // Pair of op (AND/OR) and condition
    Condition(std::shared_ptr<ColumnCondition> base) : baseCondition(base) {}
};

class TableTailOp {
public:
    virtual ~TableTailOp() = default;
};

class WhereClause : public TableTailOp {
public:
    std::shared_ptr<Condition> condition;
    WhereClause(std::shared_ptr<Condition> cond) : condition(cond) {}
};

class GroupByClause : public TableTailOp {
public:
    std::shared_ptr<Column> column;
    GroupByClause(std::shared_ptr<Column> col) : column(col) {}
};

class TableExpr {
public:
    std::shared_ptr<TableBase> base;
    std::vector<std::shared_ptr<TableTailOp>> chainedOps;
    TableExpr(std::shared_ptr<TableBase> b) : base(b) {}
};

class Stat {
public:
    Token id;
    std::shared_ptr<TableExpr> tableExpr;
    Stat(Token identifier, std::shared_ptr<TableExpr> expr)
        : id(identifier), tableExpr(expr) {}
};

class Program {
public:
    std::vector<std::shared_ptr<Stat>> statements;
};

#endif
