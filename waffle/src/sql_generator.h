#ifndef WAFFLE_SQL_GENERATOR_H
#define WAFFLE_SQL_GENERATOR_H

#include <string>
#include <sstream>
#include <memory>
#include <stdexcept>
#include "operators.h"

class SQLGenerator {
public:
    std::string generate(const std::shared_ptr<Program>& program);

private:
    std::string generateStatement(const std::shared_ptr<Stat>& statement);
    std::string generateTableExpr(const std::shared_ptr<TableExpr>& tableExpr);
    std::string generateTableBase(const std::shared_ptr<TableBase>& base);
    std::string generateWhereClause(const std::shared_ptr<WhereClause>& where);
    std::string generateGroupByClause(const std::shared_ptr<GroupByClause>& groupBy);
    std::string generateCondition(const std::shared_ptr<Condition>& condition);
    std::string generateColumnCondition(const std::shared_ptr<ColumnCondition>& cond);
    std::string generateColumn(const std::shared_ptr<Column>& column);
    std::string generateColumnList(const std::shared_ptr<ColumnList>& list);
    std::string generateLiteral(const std::shared_ptr<LiteralExpr>& literal);
    std::string mapOpToSQL(TokenType op);
};

#endif
