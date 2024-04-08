# include<iostream>
# include<fstream>
# include<string>
# include<sstream>
# include<vector>

enum Token {

};

class Scanner {
    public:
    std::vector<Token> scanTokens(std::string bytes){
        std::vector<Token> t;
        return t;
    }
};

class Waffle {
    public:
    int runFile(std::string filePath) {
        // Read file contents
        std::ifstream is{filePath};
        std::stringstream buffer;
        buffer << is.rdbuf();
        auto source{buffer.str()};        

        // Scan the file and emit tokens
        Scanner s;
        auto tokens = s.scanTokens(source);        
        for (auto token: tokens) {
            printf("%s", token);
        }

        return 0;
    }
};

int main(int argc, char* argv[]) {
    if (argc > 1) {
        std::string filePath = argv[1];
        printf("Running %s\n", filePath.c_str());

        // Run the file
        Waffle w;
        w.runFile(filePath);
    }
    
    return 0;
}

