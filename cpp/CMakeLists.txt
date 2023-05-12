cmake_minimum_required(VERSION 3.15)
project(
    hellolib
    VERSION
        1.0
    DESCRIPTION
        "First project"
    LANGUAGES
        CXX    
)

set (CMAKE_CXX_STANDARD 17)

find_package(pybind11 REQUIRED)

pybind11_add_module(${PROJECT_NAME} main.cpp)
