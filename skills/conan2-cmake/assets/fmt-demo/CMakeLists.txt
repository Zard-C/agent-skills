cmake_minimum_required(VERSION 3.23)
project(fmt_demo LANGUAGES CXX)

find_package(fmt CONFIG REQUIRED)

add_executable(hello src/main.cpp)
target_compile_features(hello PRIVATE cxx_std_17)
target_link_libraries(hello PRIVATE fmt::fmt)
