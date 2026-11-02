#include <benchmark/benchmark.h>

#include <cstddef>
#include <vector>

template <bool Reserve>
static void BM_VectorAppend(benchmark::State& state)
{
    const auto count = static_cast<std::size_t>(state.range(0));

    for (auto _ : state) {
        std::vector<int> values;
        if constexpr (Reserve) {
            values.reserve(count);
        }
        for (std::size_t i = 0; i < count; ++i) {
            values.push_back(static_cast<int>(i));
        }
        auto* data = values.data();
        benchmark::DoNotOptimize(data);
        benchmark::ClobberMemory();
    }

    state.SetItemsProcessed(state.iterations() * state.range(0));
}

BENCHMARK_TEMPLATE(BM_VectorAppend, false)
    ->Name("vector_append/no_reserve")
    ->Arg(64)
    ->Arg(4096);

BENCHMARK_TEMPLATE(BM_VectorAppend, true)
    ->Name("vector_append/reserve")
    ->Arg(64)
    ->Arg(4096);
