#include<string>
#include "token.h"

Token::Token(TokenType tokenType, std::string lexeme, Literal literal, int line):
    tokenType{tokenType}, lexeme{lexeme}, literal{literal}, line{line} 
{}

std::string Token::toString() {
    return std::to_string(1) + " " + lexeme;
}






