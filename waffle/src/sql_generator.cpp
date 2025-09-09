#include <variant>
#include <string>
#include "sql_generator.h"
#include "token.h"

std::string SQLGenerator::generate(const std::shared_ptr<Program>& program) {
    std::stringstream ss;
    for (const auto& statement : program->statements) {
        ss << generateStatement(statement) << "\n\n";
    }
    return ss.str();
}

std::string SQLGenerator::generateStatement(const std::shared_ptr<Stat>& statement) {
    std::stringstream ss;
    ss << "SELECT * FROM (" << generateTableExpr(statement->tableExpr) << ") AS " << statement->id.lexeme << ";";
    return ss.str();
}

std::string SQLGenerator::generateTableExpr(const std::shared_ptr<TableExpr>& tableExpr) {
    std::stringstream ss;
    // Start with the base table
    ss << "SELECT * FROM " << generateTableBase(tableExpr->base);

    // Apply chained operations
    for (const auto& op : tableExpr->chainedOps) {
        if (auto whereClause = std::dynamic_pointer_cast<WhereClause>(op)) {
            ss << generateWhereClause(whereClause);
        } else if (auto groupByClause = std::dynamic_pointer_cast<GroupByClause>(op)) {
            ss << generateGroupByClause(groupByClause);
        }
    }

    return ss.str();
}

std::string SQLGenerator::generateTableBase(const std::shared_ptr<TableBase>& base) {
    if (auto idBase = std::dynamic_pointer_cast<IDTableBase>(base)) {
        return idBase->id->name.lexeme;
    } else if (auto columnListBase = std::dynamic_pointer_cast<ColumnListTableBase>(base)) {
        return "(SELECT " + generateColumnList(columnListBase->columnList) + " FROM a_base_table_placeholder)"; // A hack to handle 'columnlist' as a table. Needs more grammar info.
    } else if (auto columnBase = std::dynamic_pointer_cast<ColumnTableBase>(base)) {
        // This case is ambiguous in the grammar. We'll treat it as a single column from a placeholder.
        return "(SELECT " + generateColumn(columnBase->column) + " FROM a_base_table_placeholder)";
    }
    throw std::runtime_error("Unknown TableBase type.");
}

std::string SQLGenerator::generateWhereClause(const std::shared_ptr<WhereClause>& where) {
    return " WHERE " + generateCondition(where->condition);
}

std::string SQLGenerator::generateGroupByClause(const std::shared_ptr<GroupByClause>& groupBy) {
    return " GROUP BY " + generateColumn(groupBy->column);
}

std::string SQLGenerator::generateCondition(const std::shared_ptr<Condition>& condition) {
    std::stringstream ss;
    ss << generateColumnCondition(condition->baseCondition);
    for (const auto& pair : condition->tail) {
        ss << " " << mapOpToSQL(pair.first.tokenType) << " " << generateColumnCondition(pair.second);
    }
    return ss.str();
}

std::string SQLGenerator::generateColumnCondition(const std::shared_ptr<ColumnCondition>& cond) {
    std::stringstream ss;
    ss << generateColumn(cond->left) << " " << mapOpToSQL(cond->op.tokenType) << " ";
    if (auto literal = std::dynamic_pointer_cast<LiteralExpr>(cond->right)) {
        ss << generateLiteral(literal);
    } else if (auto column = std::dynamic_pointer_cast<Column>(cond->right)) {
        ss << generateColumn(column);
    } else {
        throw std::runtime_error("Invalid right-hand side of column condition.");
    }
    return ss.str();
}

std::string SQLGenerator::generateColumn(const std::shared_ptr<Column>& column) {
    std::stringstream ss;
    if (column->parentTable) {
        // This is a table attribute (e.g., 'users.name')
        ss << generateColumn(column->parentTable) << "." << column->name;
    } else {
        ss << column->name;
    }
    if (!column->alias.empty()) {
        ss << " AS " << column->alias;
    }
    return ss.str();
}

std::string SQLGenerator::generateColumnList(const std::shared_ptr<ColumnList>& list) {
    std::stringstream ss;
    for (size_t i = 0; i < list->columns.size(); ++i) {
        ss << generateColumn(list->columns[i]);
        if (i < list->columns.size() - 1) {
            ss << ", ";
        }
    }
    return ss.str();
}

std::string SQLGenerator::generateLiteral(const std::shared_ptr<LiteralExpr>& literal) {
    std::stringstream ss;
    if (std::holds_alternative<std::string>(literal->literal)) {
        ss << "'" << std::get<std::string>(literal->literal) << "'";
    } else if (std::holds_alternative<int>(literal->literal)) {
        ss << std::get<int>(literal->literal);
    } else if (std::holds_alternative<double>(literal->literal)) {
        ss << std::get<double>(literal->literal);
    }
    return ss.str();
}

std::string SQLGenerator::mapOpToSQL(TokenType op) {
    switch (op) {
        case TokenType::GREATER: return ">";
        case TokenType::GREATER_EQUAL: return ">=";
        case TokenType::LESS: return "<";
        case TokenType::LESS_EQUAL: return "<=";
        case TokenType::EQUAL: return "=";
        case TokenType::EQUAL_EQUAL: return "=";
        case TokenType::BANG_EQUAL: return "!=";
        case TokenType::AND: return "AND";
        case TokenType::OR: return "OR";
        default:
            throw std::runtime_error("Unsupported operator for SQL generation.");
    }
}
