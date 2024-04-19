#ifndef WAFFLE_TOKEN
#define WAFFLE_TOKEN

#include<variant>
#include<string>
#include<iostream>

 typedef std::variant<std::string, int, double> Literal;

enum class TokenType {
    // Single character tokens
    LEFT_PAREN, //0
    RIGHT_PAREN, //1
    LEFT_BRACE, //2
    RIGHT_BRACE, //3
    TILDE, //4
    COMMA, //5
    DOT, //6
    MINUS, //7
    PLUS, //8
    STAR, //9
    SEMICOLON, //10 
    SLASH, //11

    // One or two character tokens
    BANG, //12 
    BANG_EQUAL, //13
    EQUAL, //14
    EQUAL_EQUAL, //15
    GREATER, //16
    GREATER_EQUAL, //17 
    LESS, //18
    LESS_EQUAL, //19

    // Two character tokens
    DBL_PERCENT, //20
    DBL_AT, //21
    DBL_COLON, //22
    
    // New operators for waffle
    BAR, // inner join | //23
    BAR_LEFT, // left join <| //24
    BAR_RIGHT, // right join |> //25
    LEFT_RIGHT, // outer join <> //26

    // Literals
    IDENTIFIER, //27
    STRING, //28
    NUMBER, //29

    //Key words
    LET, //30
    TBL, //31
    AND, //32
    OR, //33
    NOT, //34
    RSET, //35
    NIL, //36

    _EOF //37
};

class Token {
    private:
    const TokenType tokenType;
    const std::string lexeme;
    const Literal literal;
    const int line;
    std::string tokenTypeStr() const;

    public:
    Token(TokenType tokenType, std::string lexeme, Literal literal, int line);        
    std::string toString();
};

#endif