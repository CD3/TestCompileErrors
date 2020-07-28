#include <iostream>

int main(int argc, char *argv[])
{
  double x;
  x = 10;
  std::cout << x << std::endl;
  CHECK_COMPILE_FAILS(
      cout << x << std::endl;
  )
  return 0;
}
