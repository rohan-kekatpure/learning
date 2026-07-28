cmake_minimum_required(VERSION 3.15)
project(emm LANGUAGES CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(APPLE)
    set(CMAKE_OSX_ARCHITECTURES "arm64" CACHE STRING "Build for Apple Silicon" FORCE)
endif()

set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)

file(GLOB EMM_SOURCES 
    "src/*.cc"
    "src/*.h"
)

# Optional: exclude src/main.cc with a C++ main() function
# list(REMOVE_ITEM EMM_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/main.cc")

# Build the module with all gathered sources
pybind11_add_module(emm ${EMM_SOURCES})

target_include_directories(emm PRIVATE src)