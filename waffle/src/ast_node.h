# ifndef AST_NODES_H
# define AST_NODES_H
#include <vector>
#include <memory>
#include <string>

#include "token.h"

class Identifier;
class Column;
class ColumnList;
class Condition;
class ConditionList;
class AstNode;
class Table;

using ColumnPtr = std::shared_ptr<Column>;
using ColumnListPtr = std::shared_ptr<ColumnList>;
using AstNodePtr = std::shared_ptr<AstNode>;
using ConditionPtr = std::shared_ptr<Condition>;
using ConditionListPtr = std::shared_ptr<ConditionList>;
using TablePtr = std::shared_ptr<Table>;

class AstNode {};

class Column : public AstNode {
    std::string name;
    std::string parentTable;
    std::string alias;
    public:
    Column(std::string name, std::string parentTable)
        : name{name}, parentTable{parentTable} {}
    Column(std::string name, std::string parentTable, std::string alias)
        : name{name}, parentTable{parentTable}, alias{alias} {}    
};

class ColumnList : public AstNode {
    std::vector<ColumnPtr> colList;

    public:
    ColumnList(std::vector<ColumnPtr> colList) 
        : colList{colList} {}
};

class Condition : public AstNode {
    AstNodePtr left;        
    AstNodePtr right;
    Token operation;

    public:
    Condition(AstNodePtr l, Token op, AstNodePtr r) 
        : left{l}, operation{op}, right{r} {}
};

enum class LogicalOp {
    AND,
    OR
};

class ConditionList : public AstNode {
    std::vector<ConditionPtr> condList;
    std::vector<LogicalOp> opList;

    public:
    ConditionList(
        std::vector<ConditionPtr> condList, 
        std::vector<LogicalOp> opList
    ) : condList{condList}, opList{opList} {}
};

class LiteralNode : public AstNode {
    Literal value;

    public:
    LiteralNode(Literal v) : value{v} {}
};

class Identifier : public AstNode {
    std::string name;

    public:
    Identifier(std::string name) : name{name} {}
};

class Program : public AstNode {
    std::vector<AstNodePtr> statements;    
};

enum class TableClause {
    WHERE, 
    GROUPBY
};

class Table : public AstNode {
    // Table node can be Id, Column or ColumnList
    AstNodePtr source; 
    ConditionListPtr whereClause;
    ColumnListPtr groupbyClause;

    public:
    Table(std::shared_ptr<AstNode> src) : source{src} {}

    void setWhereClause(ConditionListPtr where) {
        whereClause = std::move(where);
    }
    
    void setGroupByClause(ColumnListPtr groupBy) {
        groupbyClause = std::move(groupBy);
    }    
};

class TableStmt : public AstNode {
    std::string tableName;
    TablePtr table;

    public:
    TableStmt(std::string name, TablePtr tbl) 
        : tableName{name}, table{tbl} {}        
};

class ResultStmt : public AstNode {
    std::string resultSetName;

    public:
    ResultStmt(std::string rs) : resultSetName{rs} {}
};

class Program : public AstNode {
    std::vector<AstNodePtr> statements;

    public:
    void addStatement(AstNodePtr stmt) {
        statements.push_back(std::move(stmt));
    }
};

# endif