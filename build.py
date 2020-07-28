import pathlib

template_cmake_file = pathlib.Path('TestCompileErrors.cmake.t')
output_cmake_file = pathlib.Path('TestCompileErrors.cmake')
test_script = pathlib.Path('TestCompileErrors.py')

script_text = test_script.read_text()
cmake_text = template_cmake_file.read_text().replace("{{TEST_SCRIPT_TEXT}}",script_text)

output_cmake_file.write_text(cmake_text)

