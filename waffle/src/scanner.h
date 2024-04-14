#ifndef WAFFLE_SCANNER_H
#define WAFFLE_SCANNER_H

#include<string>
#include<vector>
#include "token.h"

class Scanner {
    private:
        std::string source;
        std::vector<Token> tokens;
        int start = 0;
        int current = 0;
        int line = 1;
        bool isAtEnd();
        char advance(); 
        char peek();
        void addToken(TokenType type);
        void addTokenWithLiteralValue(TokenType type, Literal literal);
        bool match(char expected);
        void less();
        void string();
        void number();
        void scanToken();

    public:
        Scanner(std::string source);
        std::vector<Token> scanTokens();
};

#endif