#include<iostream>
#include<fstream>
#include<string>
#include<sstream>
#include<vector>

#include "token.h"
#include "scanner.h"

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
        printf("%s\n", token.toString().c_str());
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

