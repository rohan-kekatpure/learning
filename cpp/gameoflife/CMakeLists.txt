cmake_minimum_required(VERSION 3.15)
project(
    gameoflife
    VERSION
        1.0
    DESCRIPTION
        "First project"
    LANGUAGES
        CXX    
)

set (CMAKE_CXX_STANDARD 17)

find_package(Qt6 REQUIRED COMPONENTS Widgets)
qt_standard_project_setup()
add_executable(gameoflife main.cpp )
target_link_libraries(gameoflife PRIVATE Qt6::Widgets)
