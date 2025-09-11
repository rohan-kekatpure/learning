#include "token.h"
#include "parser.h"

std::shared_ptr<Program> Parser::parse() {
    auto program = std::make_shared<Program>();
    while (!isAtEnd()) {
        program->statements.push_back(stat());
    }
    return program;
}

std::shared_ptr<Stat> Parser::stat() {
    consume(TokenType::TBL, "Expected 'tbl'.");
    Token id = consume(TokenType::IDENTIFIER, "Expected table name after 'tbl'.");
    consume(TokenType::EQUAL, "Expected '=' after table name.");
    auto tableExpr = table();
    consume(TokenType::SEMICOLON, "Expected ';' after table expression.");
    return std::make_shared<Stat>(id, tableExpr);
}

std::shared_ptr<TableExpr> Parser::table() {
    auto base = tableBase();
    auto tableExpr = std::make_shared<TableExpr>(base);
    tableExpr->chainedOps = tableTail();
    return tableExpr;
}

std::shared_ptr<TableBase> Parser::tableBase() {
    if (check(TokenType::IDENTIFIER)) {
        return std::make_shared<IDTableBase>(std::make_shared<IdentifierExpr>(advance()));
    } else if (check(TokenType::TILDE) || check(TokenType::DOT) || check(TokenType::IDENTIFIER)) {
        auto col = column();
        if (match(TokenType::COMMA)) {
            // It's a column list
            auto list = std::make_shared<ColumnList>();
            list->columns.push_back(col);
            do {
                list->columns.push_back(column());
            } while (match(TokenType::COMMA));
            return std::make_shared<ColumnListTableBase>(list);
        }
        // It's a single column
        return std::make_shared<ColumnTableBase>(col);
    }
    error(peek(), "Expected a table base (ID, column, or column list).");
    return nullptr;
}

std::vector<std::shared_ptr<TableTailOp>> Parser::tableTail() {
    std::vector<std::shared_ptr<TableTailOp>> ops;
    while (check(TokenType::DBL_PERCENT) || check(TokenType::DBL_COLON)) {
        if (match(TokenType::DBL_PERCENT)) {
            ops.push_back(whereClause());
        } else if (match(TokenType::DBL_COLON)) {
            ops.push_back(groupByClause());
        }
    }
    return ops;
}

std::shared_ptr<WhereClause> Parser::whereClause() {
    auto cond = condition();
    return std::make_shared<WhereClause>(cond);
}

std::shared_ptr<GroupByClause> Parser::groupByClause() {
    auto col = column();
    return std::make_shared<GroupByClause>(col);
}

std::shared_ptr<Condition> Parser::condition() {
    auto baseCond = columnCondition();
    auto cond = std::make_shared<Condition>(baseCond);
    while (match(TokenType::AND) || match(TokenType::OR)) {
        Token op = previous();
        auto nextCond = columnCondition();
        cond->tail.push_back({op, nextCond});
    }
    return cond;
}

std::shared_ptr<ColumnCondition> Parser::columnCondition() {
    auto left = column();
    Token op = advance();
    if (! (op.toString().find("GREATER") != std::string::npos ||
           op.toString().find("LESS") != std::string::npos ||
           op.toString().find("EQUAL") != std::string::npos ||
           op.toString().find("BANG_EQUAL") != std::string::npos)) {
        error(op, "Expected a comparison operator.");
    }
    auto right = literalOrColumn();
    return std::make_shared<ColumnCondition>(left, op, right);
}

std::shared_ptr<Column> Parser::column() {
    auto base_column = std::make_shared<Column>();
    base_column->name = consume(TokenType::IDENTIFIER, "Expected column identifier.").toString();
    
    if (match(TokenType::DOT)) {
        base_column->parentTable = column();
    }
    if (match(TokenType::TILDE)) {
        Token aliasToken = consume(TokenType::IDENTIFIER, "Expected alias after '~'.");
        base_column->alias = aliasToken.toString();
    }
    return base_column;
}

std::shared_ptr<ColumnList> Parser::columnList() {
    auto list = std::make_shared<ColumnList>();
    list->columns.push_back(column());
    while (match(TokenType::COMMA)) {
        list->columns.push_back(column());
    }
    return list;
}

std::shared_ptr<Expr> Parser::literalOrColumn() {
    if (check(TokenType::NUMBER) || check(TokenType::STRING)) {
        return std::make_shared<LiteralExpr>(advance().literal);
    } else if (check(TokenType::IDENTIFIER)) {
        return column();
    }
    error(peek(), "Expected a literal or column.");
    return nullptr;
}

// Helper methods
bool Parser::match(TokenType type) {
    if (check(type)) {
        advance();
        return true;
    }
    return false;
}

bool Parser::check(TokenType type) {
    if (isAtEnd()) return false;
    return peek().tokenType == type;
}

Token Parser::advance() {
    if (!isAtEnd()) {
        current_++;
    }
    return previous();
}

bool Parser::isAtEnd() {
    return peek().tokenType == TokenType::_EOF;
}

Token Parser::peek() {
    return tokens_[current_];
}

Token Parser::previous() {
    return tokens_[current_ - 1];
}

Token Parser::consume(TokenType type, const std::string& message) {
    if (check(type)) {
        return advance();
    }
    error(peek(), message);
    return Token(type, "", 0, 0);
}

void Parser::error(const Token& token, const std::string& message) {
    std::stringstream ss;
    ss << "Parse Error at line " << token.line << ": " << message;
    throw std::runtime_error(ss.str());
}
