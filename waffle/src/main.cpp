#include<iostream>
#include<fstream>
#include<string>
#include<sstream>
#include<vector>
#include<variant>

typedef std::variant<std::string, int, double> Literal ;

enum TokenType {
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
    Token(TokenType tokenType, std::string lexeme, Literal literal, int line): 
        tokenType{tokenType}, lexeme{lexeme}, literal{literal}, line{line} 
    {}

    std::string toString() {
        return std::to_string(tokenType) + " " + lexeme;
    }
};

class Scanner {
    private:
    std::string source;
    std::vector<Token> tokens;
    int start = 0;
    int current = 0;
    int line = 1;

    bool isAtEnd() {
        return current >= source.length();
    }

    char advance() {
        return source.at(current++);
    }

    char peek() {
        if (isAtEnd()) return '\0';
        return source.at(current);
    }

    void addToken(TokenType type) {
        addTokenWithLiteralValue(type, 0);
    }

    void addTokenWithLiteralValue(TokenType type, Literal literal) {
        std::string text = source.substr(start, current);
        tokens.push_back(Token(type, text, literal, line));
    }

    bool match(char expected) {
        if (isAtEnd()) return false;        
        if (source.at(current) != expected) return false;        
        current++;
        return true;
    }

    void scanToken() {
        char c = advance();
        switch (c) {
            // Single char tokens
            case '(': addToken(LEFT_PAREN); break;
            case ')': addToken(RIGHT_PAREN); break;
            case '{': addToken(LEFT_BRACE); break;
            case '}': addToken(RIGHT_BRACE); break;
            case ',': addToken(COMMA); break;
            case '.': addToken(DOT); break;
            case '-': addToken(MINUS); break;
            case '+': addToken(PLUS); break;
            case ';': addToken(SEMICOLON); break;
            case '*': addToken(STAR); break;

            // One or two char tokens
            case '!': 
                addToken(match('=') ? BANG_EQUAL : BANG); 
                break;
            
            case '=':
                addToken(match('=') ? EQUAL_EQUAL : EQUAL);
                break;
            
            case '>':
                addToken(match('=') ? GREATER_EQUAL : GREATER);
                break;

            case '|':
                addToken(match('>') ? BAR_RIGHT : BAR);
                break;

            case '<':
                if (match('=')) {
                    addToken(LESS_EQUAL);                    
                } else if (match('>')) {
                    addToken(LEFT_RIGHT);
                } else if (match('|')) {
                    addToken(BAR_LEFT);
                } else {
                    addToken(LESS);
                }
                break;
            
            default: 
                throw std::runtime_error("Invalid character: " + std::to_string(char(c))); 
                break;           
        }
    }

    public:
    Scanner(std::string source): source{source} {}

    std::vector<Token> scanTokens() {            
        while (!isAtEnd()) {
            start = current;
            scanToken();
        }

        // Add the EOF token
        tokens.push_back(Token(_EOF, " ", 0, line));
        return tokens;
    }
};

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
        printf("%s", token.toString().c_str());
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

