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

# include_directories(
#     "/opt/homebrew/Cellar/pybind11/2.10.4/include"
#     "/opt/homebrew/opt/python@3.9/Frameworks/Python.framework/Versions/3.9/include/python3.9"
# )

# add_executable(
#     ${PROJECT_NAME}
#     main.cpp
# )

find_package(pybind11 REQUIRED)
pybind11_add_module(${PROJECT_NAME} main.cpp)