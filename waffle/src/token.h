#ifndef WAFFLE_TOKEN
#define WAFFLE_TOKEN

#include<variant>
#include<string>
#include<iostream>

typedef std::variant<std::string, int, double> Literal ;

enum class TokenType {
    // Single character tokens
    LEFT_PAREN, RIGHT_PAREN, LEFT_BRACE, RIGHT_BRACE, TILDE, 
    COMMA, DOT, MINUS, PLUS, STAR, 
    SEMICOLON, SLASH,

    // One or two character tokens
    BANG, BANG_EQUAL, EQUAL, EQUAL_EQUAL, GREATER, 
    GREATER_EQUAL, LESS, LESS_EQUAL, 
    
    // New operators for waffle
    BAR, // inner join |
    BAR_LEFT, // left join <|
    BAR_RIGHT, // right join |>
    LEFT_RIGHT, // outer join <>

    // Literals
    IDENTIFIER, STRING, NUMBER,

    //Key words
    LET, TBL, AND, OR, NOT, RSET, NIL,

    _EOF
};

class Token {
    private:
    const TokenType tokenType;
    const std::string lexeme;
    const Literal literal;
    const int line;

    public:
    Token(TokenType tokenType, std::string lexeme, Literal literal, int line);        
    std::string toString();

};

#endif