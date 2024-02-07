cmake_minimum_required(VERSION 3.15)
project(
    movie
    VERSION
        1.0
    DESCRIPTION
        "challange"
    LANGUAGES
        CXX    
)
set (CMAKE_CXX_STANDARD 17)
add_executable(moveDemo main.cpp Movie.cpp Movies.cpp)





