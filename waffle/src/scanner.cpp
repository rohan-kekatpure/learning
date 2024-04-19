#include<vector>
#include<string>
#include "scanner.h"

const char SINGLE_QUOTE = '\'';

bool Scanner::isAtEnd() {
        return current >= source.length();
}

char Scanner::advance() {
        return source.at(current++);
}

char Scanner::peek(unsigned int lookAhead) {
    if (isAtEnd()) return '\0';
    return source.at(current + lookAhead - 1);
}

void Scanner::addToken(TokenType type) {
    addTokenWithLiteralValue(type, 0);
}

void Scanner::addTokenWithLiteralValue(TokenType type, Literal literal) {
    std::string text = source.substr(start, current - start);
    tokens.push_back(Token(type, text, literal, line));
}

bool Scanner::match(char expected) {
    if (isAtEnd()) return false;        
    if (source.at(current) != expected) return false;        
    current++;
    return true;
}

void Scanner::less() {
    if (match('=')) {
        addToken(TokenType::LESS_EQUAL);                    
    } else if (match('>')) {
        addToken(TokenType::LEFT_RIGHT);
    } else if (match('|')) {
        addToken(TokenType::BAR_LEFT);
    } else {
        addToken(TokenType::LESS);
    }
}

void Scanner::string() {
    while ((peek() != SINGLE_QUOTE) && !isAtEnd()) {
        advance();
    }

    if (isAtEnd()) {
        throw std::runtime_error("Unterminated string");
    }

    // Consume the closing SINGLE_QUOTE char
    advance();

    // Trim quotes and generate token
    Literal strval = source.substr(start + 1, current - 1);
    addTokenWithLiteralValue(TokenType::STRING, strval);
}

bool Scanner::isAlphaNumeric(char c) {
    return isalnum(c) || (c == '_');
}

void Scanner::number() {
    while (isdigit(peek(1))) advance();
    if ((peek(1) == '.') && isdigit(peek(2))){
        advance();
        while (isdigit(peek(2))) advance();
    }
    std::string numStr = source.substr(start, current);
    double val = std::stod(numStr);
    addTokenWithLiteralValue(TokenType::NUMBER, val);
}

void Scanner::identifier() {
    while (!isAtEnd() && isAlphaNumeric(peek())) advance();
    addToken(TokenType::IDENTIFIER);
}

void Scanner::badCharError(const char c) {
    std::string badchar(1, c);
    std::string msg = std::string("Invalid character") 
                        + "'" + badchar + "'" 
                        + " on line " + std::to_string(line);
    throw std::runtime_error(msg);                     

}

void Scanner::scanToken() {
    char c = advance();
    switch (c) {
        // Single char tokens
        case '(': addToken(TokenType::LEFT_PAREN); break;
        case ')': addToken(TokenType::RIGHT_PAREN); break;
        case '{': addToken(TokenType::LEFT_BRACE); break;
        case '}': addToken(TokenType::RIGHT_BRACE); break;
        case ',': addToken(TokenType::COMMA); break;
        case '.': addToken(TokenType::DOT); break;
        case '-': addToken(TokenType::MINUS); break;
        case '+': addToken(TokenType::PLUS); break;
        case ';': addToken(TokenType::SEMICOLON); break;
        case '*': addToken(TokenType::STAR); break;
        case '/': addToken(TokenType::SLASH); break;
        case '~': addToken(TokenType::TILDE); break;
        case '\r':
        case '\t':
        case ' ': break;

        case '\n': 
            line++; 
            break;

        // One or two char tokens
        case '!': 
            addToken(match('=') ? TokenType::BANG_EQUAL : TokenType::BANG); 
            break;
        
        case '=':
            addToken(match('=') ? TokenType::EQUAL_EQUAL : TokenType::EQUAL);
            break;
        
        case '>':
            addToken(match('=') ? TokenType::GREATER_EQUAL : TokenType::GREATER);
            break;

        case '|':
            addToken(match('>') ? TokenType::BAR_RIGHT : TokenType::BAR);
            break;

        // Two character tokens        
        case '%':
            if (match('%')) {
                addToken(TokenType::DBL_PERCENT);  
                break;              
            } else {
                badCharError(c);
            }            
        
        case '@':
            if (match('@')) {
                addToken(TokenType::DBL_AT);
                break;
            } else {
                badCharError(c);
            }

        case ':':
            if (match(':')) {
                addToken(TokenType::DBL_COLON);
                break;
            } else {
                badCharError(c);
            }

        case '<':
            less();
            break;
        
        case SINGLE_QUOTE:
            string();
            break;
        
        default: 
            if (isdigit(c)) {
                number();                    
            } else if (isAlphaNumeric(c)) {
                identifier();
            } else {
                badCharError(c);
            }   
            break;      
    }
}

Scanner::Scanner(std::string source): source{source} {}

std::vector<Token> Scanner::scanTokens() {            
    while (!isAtEnd()) {
        start = current;
        scanToken();
    }

    // Add the EOF token
    tokens.push_back(Token(TokenType::_EOF, " ", 0, line));
    return tokens;
}

