# make sure we have a python3 interpreter
find_package(Python3)
if( NOT Python3_FOUND )
message(WARNING "No Pyhton3 executable found. Setting to 'python3', but the compile failure testing script may not run.")
set(Python3_EXECUTABLE "python3")
endif()

# make sure that the JSON compile database will be generated
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# write the script that will perform the tests
file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/TestCompileErrors.py
"
{{TEST_SCRIPT_TEXT}}
"
)

# add the testing script as a ctest test
add_test(NAME compile_failures COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_BINARY_DIR}/TestCompileErrors.py)

# write a file that will be force included to remove all snippets
# that are supposed to fail so that they don't fail during a normal build.
file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/TestCompileErrors-RemoveFailSnippets.h
"
#define CHECK_COMPILE_FAILS(...)
"
)
# add preprocessor define so that code can detect if we are running
add_compile_definitions( TEST_COMPILE_ERRORS )
# force include the file above
if(MSVC)
add_compile_options(/FI${CMAKE_CURRENT_BINARY_DIR}/TestCompileErrors-RemoveFailSnippets.h)
else()
add_compile_options(-include ${CMAKE_CURRENT_BINARY_DIR}/TestCompileErrors-RemoveFailSnippets.h)
endif()
