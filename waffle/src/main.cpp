#include<iostream>
#include<fstream>
#include<string>
#include<sstream>
#include<vector>

#include "token.h"
#include "scanner.h"
#include <memory>
#include <stdexcept>
#include "operators.h"

int runFile(std::string filePath) {
    // Read file contents
    std::ifstream is{filePath}; 
    std::stringstream buffer;
    buffer << is.rdbuf();
    auto source{buffer.str()};        

    // Scan the file and emit tokens
    Scanner s{source};
    auto tokens = s.scanTokens(); 
    for (auto token: tokens) {
        printf("%s\n", token.toString().c_str());
    }

    return 0;
}


int main(int argc, char* argv[]) {
    if (argc > 1) {
        std::string filePath = argv[1];        
        printf("Running %s\n", filePath.c_str());

        // Run the file
        runFile(filePath);
    }

    return 0;
}


void createAndPrintAST() {    

    Token tbl_token(TokenType::TBL, "tbl", 0, 1);
    Token id_token(TokenType::IDENTIFIER, "active_users", 0, 1);
    Token eq_token(TokenType::EQUAL, "=", 0, 1);
    Token users_id_token(TokenType::IDENTIFIER, "users", 0, 1);
    Token dot_token(TokenType::DOT, ".", 0, 1);
    Token where_token(TokenType::DBL_PERCENT, "%%", 0, 1);
    Token age_id_token(TokenType::IDENTIFIER, "age", 0, 1);
    Token gt_token(TokenType::GREATER, ">", 0, 1);
    Token number_literal(TokenType::NUMBER, "30", 30, 1);
    Token semicolon_token(TokenType::SEMICOLON, ";", 0, 1);

    auto age_column = std::make_shared<Column>();
    age_column->name = "age";
    auto thirty_literal = std::make_shared<LiteralExpr>(30.0);
    auto age_condition = std::make_shared<ColumnCondition>(age_column, gt_token, thirty_literal);    
    auto full_condition = std::make_shared<Condition>(age_condition);
    auto where_clause = std::make_shared<WhereClause>(full_condition);
    auto users_base = std::make_shared<IDTableBase>(std::make_shared<IdentifierExpr>(users_id_token));
    auto table_expr = std::make_shared<TableExpr>(users_base);
    table_expr->chainedOps.push_back(where_clause);

    auto statement = std::make_shared<Stat>(id_token, table_expr);
    auto program = std::make_shared<Program>();
    program->statements.push_back(statement);

    std::cout << "Successfully built AST for 'tbl active_users = users.WHERE(age > 30);'." << std::endl;
    std::cout << "The created AST nodes are ready to be used by your parser." << std::endl;
}

