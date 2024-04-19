#include<string>
#include "token.h"

Token::Token(TokenType tokenType, std::string lexeme, Literal literal, int line):
    tokenType{tokenType}, lexeme{lexeme}, literal{literal}, line{line} 
{}

std::string Token::tokenTypeStr() const {
    // This is essentially a giant dictionary
    switch (this->tokenType) {
        case TokenType::LEFT_PAREN: return "LEFT_PAREN"; break;
        case TokenType::RIGHT_PAREN: return "RIGHT_PAREN"; break;
        case TokenType::LEFT_BRACE: return "LEFT_BRACE"; break;
        case TokenType::RIGHT_BRACE: return "RIGHT_BRACE";
        case TokenType::TILDE: return "TILDE";
        case TokenType::COMMA: return "COMMA"; 
        case TokenType::DOT: return "DOT"; 
        case TokenType::MINUS: return "MINUS";
        case TokenType::PLUS: return "PLUS";
        case TokenType::STAR: return "STAR";
        case TokenType::SEMICOLON: return "SEMICOLON"; 
        case TokenType::SLASH: return "SLASH";

        // One or two character tokens
        case TokenType::BANG: return "BANG";
        case TokenType::BANG_EQUAL: return "BANG_EQUAL";
        case TokenType::EQUAL: return "EQUAL";
        case TokenType::EQUAL_EQUAL: return "EQUAL_EQUAL";
        case TokenType::GREATER: return "GREATER";
        case TokenType::GREATER_EQUAL: return "GREATER_EQUAL";
        case TokenType::LESS: return "LESS";
        case TokenType::LESS_EQUAL: return "LESS_EQUAL";

        // Two character tokens
        case TokenType::DBL_PERCENT: return "DBL_PERCENT";
        case TokenType::DBL_AT: return "DBL_AT";
        case TokenType::DBL_COLON: return "DBL_COLON";
        
        // New operators for waffle
        case TokenType::BAR: return "BAR"; // inner join | 
        case TokenType::BAR_LEFT: return "BAR_LEFT"; // left join <| 
        case TokenType::BAR_RIGHT: return "BAR_RIGHT"; // right join |> 
        case TokenType::LEFT_RIGHT: return "LEFT_RIGHT"; // outer join <> 

        // Literals
        case TokenType::IDENTIFIER: return "IDENTIFIER"; 
        case TokenType::STRING: return "STRING";
        case TokenType::NUMBER: return "NUMBER";

        //Key words
        case TokenType::LET: return "KWD_LET";
        case TokenType::TBL: return "KWD_TBL";
        case TokenType::AND: return "KWD_AND";
        case TokenType::OR: return "KWD_OR";
        case TokenType::NOT: return "KWD_NOT";
        case TokenType::RSET: return "KWD_RSET";
        case TokenType::NIL: return "KWD_NIL";

        case TokenType::_EOF: return "EOF";

    }
}

std::string Token::toString() {
    std::string tts(tokenTypeStr());
    return tts + " " + this->lexeme;
}






