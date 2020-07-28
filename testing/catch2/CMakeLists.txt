cmake_minimum_required(VERSION 3.13)

project(Test)

enable_testing()
include("../../TestCompileErrors.cmake")
add_executable(unittest unittest.cpp)
target_include_directories(unittest PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
