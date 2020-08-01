cmake_minimum_required(VERSION 3.13)

project(None)

enable_testing()
include("../../TestCompileErrors.cmake")

add_executable(main main.cpp lib.cpp)
add_executable(fails fails.cpp)
