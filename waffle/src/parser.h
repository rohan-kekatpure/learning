#ifndef WAFFLE_PARSER_H
#define WAFFLE_PARSER_H

#include <vector>
#include <memory>
#include <string>
#include <stdexcept>

#include "token.h"
#include "ast_node.h"

class ParseError : public std::runtime_error {
public:
    ParseError(const std::string& message) : std::runtime_error(message) {}
};

class Parser {
private:
    std::vector<Token> tokens;
    int current = 0;

    // Utility methods
    bool isAtEnd();
    Token peek();
    Token previous();
    Token advance();
    bool check(TokenType type);
    bool match(std::vector<TokenType> types);
    bool match(TokenType type);
    void consume(TokenType type, const std::string& message);
    
    // Parsing methods following the grammar
    std::shared_ptr<Program> program();
    AstNodePtr statement();
    AstNodePtr tableStatement();
    AstNodePtr resultStatement();
    TablePtr table();
    AstNodePtr tableSource();
    ColumnPtr column();
    ColumnListPtr columnList();
    ConditionListPtr conditions();
    ConditionPtr condition();
    AstNodePtr primary();
    std::shared_ptr<LiteralNode> literal();
    std::shared_ptr<Identifier> identifier();
    
    // Helper methods
    LogicalOp parseLogicalOperator();
    Token parseComparisonOperator();
    Literal parseLiteralValue();
    
    // Error handling
    void synchronize();
    ParseError error(const Token& token, const std::string& message);

public:
    Parser(const std::vector<Token>& tokens);
    std::shared_ptr<Program> parse();
};

#endif // WAFFLE_PARSER_H