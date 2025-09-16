#ifndef WAFFLE_PARSER_H
#define WAFFLE_PARSER_H

#include <vector>
#include <memory>
#include <stdexcept>
#include <sstream>

#include "token.h"
#include "ast_node.h"

class Parser {
public:
    explicit Parser(const std::vector<Token>& tokens) : tokens_(tokens), current_(0) {}
    std::shared_ptr<Program> parse();

private:
    std::shared_ptr<Stmt> stmt();
    std::shared_ptr<Table> table();            
    std::shared_ptr<Condition> condition();
    std::shared_ptr<ConditionList> conditionList();
    std::shared_ptr<Column> column();
    std::shared_ptr<ColumnList> columnList();    

    // Helper functions
    bool match(TokenType type);
    bool check(TokenType type);
    Token advance();
    bool isAtEnd();
    Token peek();
    Token previous();
    Token consume(TokenType type, const std::string& message);
    void error(const Token& token, const std::string& message);

    const std::vector<Token>& tokens_;
    int current_;
};

#endif
