cmake_minimum_required(VERSION 3.23)
project(benchmark_demo LANGUAGES CXX)

find_package(benchmark CONFIG REQUIRED)

add_executable(vector_append_benchmark src/main.cpp)
target_compile_features(vector_append_benchmark PRIVATE cxx_std_17)
target_link_libraries(vector_append_benchmark PRIVATE benchmark::benchmark_main)

include(CTest)
if(BUILD_TESTING)
    add_test(
        NAME vector_append_smoke
        COMMAND vector_append_benchmark
            --benchmark_min_time=0.01s
            --benchmark_color=false
            "--benchmark_out=${CMAKE_CURRENT_BINARY_DIR}/benchmark-smoke.json"
            --benchmark_out_format=json
    )
    set_tests_properties(vector_append_smoke PROPERTIES
        TIMEOUT 60
        PASS_REGULAR_EXPRESSION "vector_append/no_reserve/64"
    )
endif()
