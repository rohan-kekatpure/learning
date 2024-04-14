cmake_minimum_required(VERSION 3.15)
project(
    waffle
    VERSION
        1.0
    DESCRIPTION
        "Waffle"
    LANGUAGES
        CXX    
)

set (CMAKE_CXX_STANDARD 17)
add_executable(
    waffle 
    src/main.cpp
    src/scanner.cpp
    src/token.cpp
)