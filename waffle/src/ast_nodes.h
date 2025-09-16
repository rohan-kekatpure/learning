# ifndef AST_NODES_H
# define AST_NODES_H
#include <vector>
#include <memory>
#include <string>

#include "token.h"

class Identifier;
class Column;
class AstNode;

using ColPtr = std::shared_ptr<Column>;
using AstNodePtr = std::shared_ptr<AstNode>;
using ConditionPtr = std::shared_ptr<Condition>;

class AstNode {};

class Stmt : public AstNode {};

class ResultStmt : public Stmt {
    std::string id;
    public: 
    ResultStmt(std::string id) : id{id} {}
};

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
    std::vector<ColPtr> colList;
    ColumnList(std::vector<ColPtr> colList) 
        : colList{colList} {}
};

class Condition : public AstNode {
    AstNodePtr left;        
    AstNodePtr right;
    Token operation;

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

    ConditionList(
        std::vector<ConditionPtr> condList, 
        std::vector<LogicalOp> opList
    ) : condList{condList}, opList{opList} {}
};

class LiteralNode : public AstNode {
    Literal value;
    LiteralNode(Literal v) : value{v} {}
};


# endif