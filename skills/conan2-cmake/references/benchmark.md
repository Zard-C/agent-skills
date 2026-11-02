# Google Benchmark 示例

使用 Conan 2 安装依赖，以 CMake 编译一个 C++17 微基准。最小工程位于 [assets/benchmark-demo](../assets/benchmark-demo/)，与 fmt 模板独立，具有各自的 recipe 和构建目录。

## 文件与依赖

- [conanfile.py](../assets/benchmark-demo/conanfile.py)：声明 `benchmark/1.10.0`、两个 CMake generators 和 `cmake_layout()`。
- [CMakeLists.txt](../assets/benchmark-demo/CMakeLists.txt)：查找 `benchmark`，链接 `benchmark::benchmark_main`，注册 CTest smoke test。
- [src/main.cpp](../assets/benchmark-demo/src/main.cpp)：注册两个实现、两种输入规模，共四组用例。

`benchmark::benchmark_main` 已包含默认入口并传递 Benchmark 的链接要求，源码只注册用例。它与自己定义 `main()` 或使用 `BENCHMARK_MAIN()` 是不同的入口选择，不要同时使用。

配方和 CMake 目标于 2026-11-03 在 [ConanCenter Index](https://github.com/conan-io/conan-center-index/blob/master/recipes/benchmark/all/conanfile.py) 核实；版本号是示例固定值，不代表未来最新版本或任意平台都有预编译包。

首次源码构建可能额外获取配方声明的 CMake 构建工具。这些工具由 Conan 缓存管理，不会替换容器通过 apt 安装的系统 CMake。

## 安装和构建

先创建或复制模板的完整文件，在实际构建环境的模板根目录运行：

```bash
conan profile detect --exist-ok
conan profile show
conan install . -s:h build_type=Release -s:h compiler.cppstd=17 --build=missing
cmake --list-presets
cmake --preset conan-release
cmake --build --preset conan-release --parallel
```

示例路径对应 Ubuntu 默认的单配置生成器。已有定制 layout 或多配置生成器时，使用实际生成的 preset 和 binaryDir。Conan 与 CMake 的配置需一致。

## 用例测量什么

| 用例前缀 | 操作 | 元素个数 |
| --- | --- | --- |
| `vector_append/no_reserve` | 空 vector 直接逐个 push_back，由其自行扩容 | 64、4096 |
| `vector_append/reserve` | 先 reserve，再逐个 push_back | 64、4096 |

每次迭代都包含 vector 构造、内存分配或扩容、写入和析构。两组代码写入相同的整数序列；这是整体构造流程的对比，不是仅测 push_back 指令的耗时。

`DoNotOptimize` 用于暴露数据指针，`ClobberMemory` 用于建立编译器内存屏障，减少工作被优化掉的可能。它们不代表清空 CPU cache，也不能保证任意写法都不会被常量折叠。`SetItemsProcessed` 额外报告元素处理吞吐。

## 运行与导出

查看注册的用例，不进行计时：

```bash
./build/Release/vector_append_benchmark --benchmark_list_tests=true
```

运行一个较短的交互式示例：

```bash
./build/Release/vector_append_benchmark --benchmark_min_time=0.1s
```

重复测量并保留 JSON 输出：

```bash
./build/Release/vector_append_benchmark \
  --benchmark_min_time=0.5s \
  --benchmark_repetitions=5 \
  --benchmark_out=build/Release/benchmark-results.json \
  --benchmark_out_format=json
```

保留原始样本和环境信息，再根据目标选择统计量。CPU 频率、宿主机负载、容器调度和虚拟化都会影响读数；示例不预设哪个实现必须更快，也不据此承诺性能回归结论。

## CTest 与 CI

```bash
ctest --test-dir build/Release --output-on-failure
```

smoke test 将每组最小测量时间设为 `0.01s`，确认可执行文件正常退出且输出包含预期用例，并生成 `build/Release/benchmark-smoke.json`。超时仅用于避免测试挂起，不是性能基线。

若配置时明确关闭了 `BUILD_TESTING`，不会注册这项测试。CI 的 `benchmark-smoke` job 使用默认测试配置，执行依赖安装、Release 编译和 CTest；不比较计时数值。

## 本次验证范围

2026-11-03 在既有 Ubuntu 24.04.4 容器的独立临时目录验证：Conan 2.34.0、GCC 13.3.0、Linux/armv8 profile、C++17、Release、Unix Makefiles。

本次从 ConanCenter 下载 Benchmark 配方和源代码并构建 `benchmark/1.10.0`；该依赖的构建工具要求解析到了 Conan 管理的 CMake 4.4.4。示例工程的配置和编译使用系统 CMake 3.28.3。

四组用例的列表、Release 配置与编译、CTest smoke test 均通过；另检查了导出的 JSON，确认四组记录均有实际迭代且无错误。验证复用了现有容器和 profile，没有重建全新系统，也没有执行正式的硬件性能对比。

## 官方参考

- [Google Benchmark 使用指南](https://github.com/google/benchmark/blob/v1.10.0/docs/user_guide.md)
- [ConanCenter Benchmark 版本](https://github.com/conan-io/conan-center-index/blob/master/recipes/benchmark/config.yml)
- [ConanCenter Benchmark 配方与目标](https://github.com/conan-io/conan-center-index/blob/master/recipes/benchmark/all/conanfile.py)
