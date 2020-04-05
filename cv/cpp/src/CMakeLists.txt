project(OBJECT_TRACKING)
cmake_minimum_required(VERSION 2.6 FATAL_ERROR)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(OpenCV REQUIRED)


# Project Executable
add_executable (main main.cpp )
target_link_libraries(main ${OpenCV_LIBS})