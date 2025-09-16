#include "parser.h"
#include <iostream>

Parser::Parser(const std::vector<Token>& tokens) : tokens(tokens) {}

// Utility methods
bool Parser::isAtEnd() {
    return peek().tokenType == TokenType::_EOF;
}

Token Parser::peek() {
    return tokens[current];
}

Token Parser::previous() {
    return tokens[current - 1];
}

Token Parser::advance() {
    if (!isAtEnd()) current++;
    return previous();
}

bool Parser::check(TokenType type) {
    if (isAtEnd()) return false;
    return peek().tokenType == type;
}

bool Parser::match(std::vector<TokenType> types) {
    for (TokenType type : types) {
        if (check(type)) {
            advance();
            return true;
        }
    }
    return false;
}

bool Parser::match(TokenType type) {
    if (check(type)) {
        advance();
        return true;
    }
    return false;
}

void Parser::consume(TokenType type, const std::string& message) {
    if (check(type)) {
        advance();
        return;
    }
    throw error(peek(), message);
}

ParseError Parser::error(const Token& token, const std::string& message) {
    std::string errorMsg = "Parse error at line " + std::to_string(token.line) + 
                          ": " + message + " (found '" + token.lexeme + "')";
    return ParseError(errorMsg);
}

void Parser::synchronize() {
    advance();
    while (!isAtEnd()) {
        if (previous().tokenType == TokenType::SEMICOLON) return;
        
        switch (peek().tokenType) {
            case TokenType::TBL:
            case TokenType::RSET:
                return;
            default:
                break;
        }
        advance();
    }
}

// Main parsing entry point
std::shared_ptr<Program> Parser::parse() {
    try {
        return program();
    } catch (const ParseError& error) {
        std::cerr << error.what() << std::endl;
        synchronize();
        return nullptr;
    }
}

// Grammar rule implementations
std::shared_ptr<Program> Parser::program() {
    auto prog = std::make_shared<Program>();
    
    while (!isAtEnd()) {
        try {
            auto stmt = statement();
            if (stmt) {
                prog->addStatement(stmt);
            }
        } catch (const ParseError& error) {
            std::cerr << error.what() << std::endl;
            synchronize();
        }
    }
    
    return prog;
}

AstNodePtr Parser::statement() {
    if (match(TokenType::TBL)) {
        return tableStatement();
    }
    
    if (match(TokenType::RSET)) {
        return resultStatement();
    }
    
    throw error(peek(), "Expected 'tbl' or 'rset'");
}

AstNodePtr Parser::tableStatement() {
    // We already consumed TBL
    Token nameToken = peek();
    consume(TokenType::IDENTIFIER, "Expected table name");
    std::string tableName = nameToken.lexeme;
    
    consume(TokenType::EQUAL, "Expected '=' after table name");
    
    TablePtr tableExpr = table();
    
    consume(TokenType::SEMICOLON, "Expected ';' after table statement");
    
    return std::make_shared<TableStmt>(tableName, tableExpr);
}

AstNodePtr Parser::resultStatement() {
    // We already consumed RSET
    Token nameToken = peek();
    consume(TokenType::IDENTIFIER, "Expected result set name");
    std::string resultName = nameToken.lexeme;
    
    consume(TokenType::SEMICOLON, "Expected ';' after result statement");
    
    return std::make_shared<ResultStmt>(resultName);
}

TablePtr Parser::table() {
    // Parse table source (ID | column | columnlist)
    AstNodePtr source = tableSource();
    auto tableNode = std::make_shared<Table>(source);
    
    // Optional WHERE clause
    if (match(TokenType::DBL_PERCENT)) { // %%
        ConditionListPtr whereConditions = conditions();
        tableNode->setWhereClause(whereConditions);
    }
    
    // Optional GROUP BY clause  
    if (match(TokenType::DBL_COLON)) { // ::
        ColumnListPtr groupByColumns = columnList();
        tableNode->setGroupByClause(groupByColumns);
    }
    
    return tableNode;
}

AstNodePtr Parser::tableSource() {
    // Check if it's a column list (starts with column)
    if (check(TokenType::IDENTIFIER)) {
        // Look ahead to see if this is a single identifier or part of a column/columnlist
        int savePoint = current;
        
        // Try to parse as column first
        try {
            auto col = column();
            
            // If next token is comma, it's a column list
            if (check(TokenType::COMMA)) {
                current = savePoint; // Reset and parse as column list
                return columnList();
            }
            
            // If it has dot or tilde, it's definitely a column
            if (col->parentTable != "" || col->alias != "") {
                current = savePoint; // Reset
                return column();
            }
            
            // Otherwise it's just an identifier
            current = savePoint; // Reset
            return identifier();
            
        } catch (const ParseError&) {
            current = savePoint; // Reset on error
            return identifier();
        }
    }
    
    throw error(peek(), "Expected table source (identifier, column, or column list)");
}

ColumnPtr Parser::column() {
    Token nameToken = peek();
    consume(TokenType::IDENTIFIER, "Expected column name");
    std::string columnName = nameToken.lexeme;
    std::string parentTable = "";
    std::string alias = "";
    
    // Handle DOT notation (table.column)
    if (match(TokenType::DOT)) {
        parentTable = columnName;
        Token columnToken = peek();
        consume(TokenType::IDENTIFIER, "Expected column name after '.'");
        columnName = columnToken.lexeme;
    }
    
    // Handle TILDE notation (column~alias)
    if (match(TokenType::TILDE)) {
        Token aliasToken = peek();
        consume(TokenType::IDENTIFIER, "Expected alias after '~'");
        alias = aliasToken.lexeme;
    }
    
    if (alias.empty()) {
        return std::make_shared<Column>(columnName, parentTable);
    } else {
        return std::make_shared<Column>(columnName, parentTable, alias);
    }
}

ColumnListPtr Parser::columnList() {
    std::vector<ColumnPtr> columns;
    
    columns.push_back(column());
    
    while (match(TokenType::COMMA)) {
        columns.push_back(column());
    }
    
    return std::make_shared<ColumnList>(columns);
}

ConditionListPtr Parser::conditions() {
    std::vector<ConditionPtr> condList;
    std::vector<LogicalOp> opList;
    
    condList.push_back(condition());
    
    while (match({TokenType::AND, TokenType::OR})) {
        LogicalOp op = (previous().tokenType == TokenType::AND) ? LogicalOp::AND : LogicalOp::OR;
        opList.push_back(op);
        condList.push_back(condition());
    }
    
    return std::make_shared<ConditionList>(condList, opList);
}

ConditionPtr Parser::condition() {
    AstNodePtr left = primary();
    
    // Parse comparison operator
    if (!match({TokenType::GREATER, TokenType::GREATER_EQUAL, TokenType::LESS, 
                TokenType::LESS_EQUAL, TokenType::EQUAL_EQUAL, TokenType::BANG_EQUAL})) {
        throw error(peek(), "Expected comparison operator");
    }
    
    Token op = previous();
    AstNodePtr right = primary();
    
    return std::make_shared<Condition>(left, op, right);
}

AstNodePtr Parser::primary() {
    if (check(TokenType::NUMBER) || check(TokenType::STRING) || 
        check(TokenType::NIL) || peek().lexeme == "true" || peek().lexeme == "false") {
        return literal();
    }
    
    if (check(TokenType::IDENTIFIER)) {
        // Could be column or identifier - try column first
        int savePoint = current;
        try {
            return column();
        } catch (const ParseError&) {
            current = savePoint;
            return identifier();
        }
    }
    
    throw error(peek(), "Expected literal, column, or identifier");
}

std::shared_ptr<LiteralNode> Parser::literal() {
    if (match(TokenType::NUMBER)) {
        return std::make_shared<LiteralNode>(previous().literal);
    }
    
    if (match(TokenType::STRING)) {
        return std::make_shared<LiteralNode>(previous().literal);
    }
    
    if (match(TokenType::NIL)) {
        return std::make_shared<LiteralNode>(nullptr);
    }
    
    // Handle boolean literals
    if (check(TokenType::IDENTIFIER)) {
        Token token = peek();
        if (token.lexeme == "true") {
            advance();
            return std::make_shared<LiteralNode>(true);
        }
        if (token.lexeme == "false") {
            advance();
            return std::make_shared<LiteralNode>(false);
        }
    }
    
    throw error(peek(), "Expected literal value");
}

std::shared_ptr<Identifier> Parser::identifier() {
    Token nameToken = peek();
    consume(TokenType::IDENTIFIER, "Expected identifier");
    return std::make_shared<Identifier>(nameToken.lexeme);
}