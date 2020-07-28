#define CATCH_CONFIG_MAIN
#include <catch.hpp>

#include<vector>

TEST_CASE("std::vector has a .size() method")
{
  std::vector<int> v;
  v.push_back(1);
  v.push_back(2);
  CHECK(v.size() == 2);
  CHECK_COMPILE_FAILS(
  v.length();
  )
}


