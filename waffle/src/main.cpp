#include<iostream>
#include<fstream>
#include<string>
#include<sstream>
#include<vector>

#include "token.h"
#include "scanner.h"
#include "parser.h"
#include "sql_generator.h"
#include "ast_node.h"

int runFile(std::string filePath) {
    // Read file contents
    std::ifstream is{filePath};
    if (!is.is_open()) {
        std::cerr << "Error: Could not open file " << filePath << std::endl;
        return 1;
    }
    std::stringstream buffer;
    buffer << is.rdbuf();
    auto source{buffer.str()};

    try {
        // 1. Scan the file and emit tokens
        Scanner scanner(source);
        auto tokens = scanner.scanTokens();
        std::cout << "Tokens:" << std::endl;
        for (const auto& token : tokens) {
            std::cout << token.toString() << std::endl;
        }

        // 2. Parse tokens and build the AST
        Parser parser(tokens);
        auto ast = parser.parse();
        std::cout << "\nAST built successfully." << std::endl;

        // 3. Generate SQL from the AST
        // SQLGenerator sqlGen;
        // std::string sqlOutput = sqlGen.generate(ast);
        // std::cout << "\nGenerated SQL:" << std::endl;
        // std::cout << sqlOutput << std::endl;

    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}


int main(int argc, char* argv[]) {
    if (argc > 1) {
        std::string filePath = argv[1];
        printf("Running %s\n", filePath.c_str());

        // Run the file
        return runFile(filePath);
    } else {
        std::cerr << "Usage: waffle <filePath>" << std::endl;
        return 1;
    }
}
