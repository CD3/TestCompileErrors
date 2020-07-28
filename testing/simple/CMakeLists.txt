cmake_minimum_required(VERSION 3.13)

project(None)

enable_testing()
include("../TestCompileErrors.cmake")
add_executable(main main.cpp)

add_executable(fails fails.cpp)
add_executable(fails2 fails.cpp)

add_executable(main2 main.cpp lib.cpp)
