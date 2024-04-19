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
        case TokenType::RIGHT_BRACE: return "RIGHT_BRACE"; break;
        case TokenType::TILDE: return "TILDE"; break;
        case TokenType::COMMA: return "COMMA"; break; 
        case TokenType::DOT: return "DOT"; break; 
        case TokenType::MINUS: return "MINUS"; break;
        case TokenType::PLUS: return "PLUS"; break;
        case TokenType::STAR: return "STAR"; break;
        case TokenType::SEMICOLON: return "SEMICOLON"; break; 
        case TokenType::SLASH: return "SLASH"; break;

        // One or two character tokens
        case TokenType::BANG: return "BANG"; break;
        case TokenType::BANG_EQUAL: return "BANG_EQUAL"; break;
        case TokenType::EQUAL: return "EQUAL"; break;
        case TokenType::EQUAL_EQUAL: return "EQUAL_EQUAL"; break;
        case TokenType::GREATER: return "GREATER"; break;
        case TokenType::GREATER_EQUAL: return "GREATER_EQUAL"; break;
        case TokenType::LESS: return "LESS"; break;
        case TokenType::LESS_EQUAL: return "LESS_EQUAL"; break;

        // Two character tokens
        case TokenType::DBL_PERCENT: return "DBL_PERCENT"; break;
        case TokenType::DBL_AT: return "DBL_AT"; break;
        case TokenType::DBL_COLON: return "DBL_COLON"; break;
        
        // New operators for waffle
        case TokenType::BAR: return "BAR"; break; // inner join | 
        case TokenType::BAR_LEFT: return "BAR_LEFT"; break; // left join <| 
        case TokenType::BAR_RIGHT: return "BAR_RIGHT"; break; // right join |> 
        case TokenType::LEFT_RIGHT: return "LEFT_RIGHT"; break; // outer join <> 

        // Literals
        case TokenType::IDENTIFIER: return "IDENTIFIER"; break; 
        case TokenType::STRING: return "STRING"; break;
        case TokenType::NUMBER: return "NUMBER"; break;

        //Key words
        case TokenType::LET: return "KWD_LET"; break;
        case TokenType::TBL: return "KWD_TBL"; break;
        case TokenType::AND: return "KWD_AND"; break;
        case TokenType::OR: return "KWD_OR"; break;
        case TokenType::NOT: return "KWD_NOT"; break;
        case TokenType::RSET: return "KWD_RSET"; break;
        case TokenType::NIL: return "KWD_NIL"; break;

        case TokenType::_EOF: return "EOF"; break;

    }
}

std::string Token::toString() {
    std::string tts(tokenTypeStr());
    return tts + " " + this->lexeme;
}






