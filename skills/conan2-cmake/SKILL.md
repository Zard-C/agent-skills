---
name: conan2-cmake
description: Set up and troubleshoot Conan 2 dependencies consumed by CMake in C/C++ projects, including conanfile.py, profiles, fmt and Google Benchmark examples, generated presets, and Ubuntu development containers on macOS. Use for Conan 2 installation, CMake dependency integration, or missing Conan presets; preserve existing package-manager choices.
---

# Conan 2 + CMake

建立并验证 `conan install -> CMake configure -> CMake build` 流程。默认参考环境是 macOS 上的 Docker Desktop 与 Ubuntu 24.04 容器；其他环境按实际工具链调整。

## 先确认工作位置

1. 读取项目现有的 `conanfile.*`、`CMakeLists.txt`、presets 和本地说明；尊重用户要操作指令还是要直接修改文件的选择。
2. 区分 Mac 终端和容器终端。需要定位挂载目录时，在宿主机执行 `docker inspect --format '{{json .Mounts}}' <container>`。容器名、镜像名、挂载路径均以实际值为准。
3. 在真正编译的环境内检查 `conan --version`、`cmake --version`、`c++ --version` 和 `conan profile show`。使用 Conan 2 API；本文 preset 流程要求 CMake 3.23 或更高。
4. 先让源码目录具有有效的 `CMakeLists.txt`，再执行 `conan install`。Conan 的 `source_folder` 必须对应这份文件的位置。

## 按需读取

- 安装工具、创建容器、首次接入或 VS Code/代理配置：读取 [references/setup.md](references/setup.md)。
- 配置、依赖、preset 或链接错误：读取 [references/troubleshooting.md](references/troubleshooting.md)。
- 用户询问现成 skills 或后续扩展：读取 [references/community-skills.md](references/community-skills.md)，重新核实源码可访问性。
- 新建最小可运行项目：使用 [assets/fmt-demo](assets/fmt-demo/) 的三个文件；复制前检查目标目录已有文件，按项目结构调整。
- 接入 Google Benchmark 或创建微基准：读取 [references/benchmark.md](references/benchmark.md)，使用独立的 [assets/benchmark-demo](assets/benchmark-demo/) 模板。

## 接入方式

- 新工程需要继续扩展时，优先使用 `conanfile.py`；现有简单 `conanfile.txt` 可以继续使用。
- 基础 recipe 声明 `settings`、依赖、`CMakeDeps`、`CMakeToolchain`，通过 `layout()` 调用 `cmake_layout(self)`。显式执行 CMake 的消费流程不要求 recipe 定义 `build()`。
- fmt 示例固定使用 `fmt/12.2.0`；这是示例选择，不代表最新版本。新增或升级依赖前核实 ConanCenter/项目 remote 上的配方，并确认目标 CMake 名称。
- CMake 使用 `find_package(fmt CONFIG REQUIRED)` 和 `target_link_libraries(hello PRIVATE fmt::fmt)`；头文件路径、传递依赖和库文件由 imported target 提供。
- fmt 用于 C++ 源码；`project(... LANGUAGES CXX)` 中的关键字带 `S`。系统线程仍使用 `Threads::Threads`，无需把 libc 或 pthread 改造成 Conan 依赖。
- Google Benchmark 示例使用 `benchmark/1.10.0`、C++17 和 Release 配置，链接 `benchmark::benchmark_main` 提供入口；此时不要再定义自己的 `main()` 或 `BENCHMARK_MAIN()`。
- 在容器内检测并使用 Linux profile。Mac 和 Linux 的构建目录分开；不要将宿主机生成的 CMake 缓存或 Conan 绝对路径直接用于容器。

## 安装和编译

先创建模板的全部源码文件。以下命令在项目根目录、目标构建环境内执行：

```bash
conan profile detect --exist-ok
conan profile show
conan install . -s:h build_type=Debug -s:h compiler.cppstd=17 --build=missing
cmake --list-presets
cmake --preset conan-debug
cmake --build --preset conan-debug --parallel
./build/Debug/hello
```

这里假设 Ubuntu 默认的单配置生成器和模板目标 `hello`。其他生成器或定制 layout 以实际 preset 名称、`binaryDir` 和 Conan 输出为准。`--build=missing` 只在缺少匹配的依赖二进制时构建依赖。

`cmake_layout()` 已管理目录布局，通常不再额外指定 `--output-folder=build`。调整源码路径或 recipe 布局后，在正确位置重新执行 `conan install`。

## 验收和报告

- 确认 Conan 安装成功，profile 的 OS、架构、编译器和 C++ 标准符合目标环境。
- 确认项目根目录有可用的 preset 入口，`cmake --list-presets` 能列出所选配置。
- 配置、编译并运行最小模板；期望输出 `Hello, Conan! Answer = 42`。已有项目使用其实际测试与运行方式。
- Benchmark 模板注册四组 vector append 用例，运行其 CTest smoke test 并检查结果。smoke test 验证功能，不根据短测量时间设定性能阈值；性能结果同时报告构建模式、输入规模、硬件和测量环境。
- 报告实际测试的系统、版本和生成器；若只核对了文件或文档，明确说明尚未完成安装/运行验证。
- 保留用户已有 profiles 和手写 presets。按错误定位处理，避免默认覆盖 profile、清空整个 Conan cache 或切换依赖来源。
- 复现环境时记录实际 Conan 版本；团队/CI 进一步固定依赖 revisions、profiles 和锁文件，版本号声明本身不等于完整可复现性。

## 官方依据

- [Conan 2 安装](https://docs.conan.io/2/installation.html)
- [conanfile.py 与 conanfile.txt](https://docs.conan.io/2/tutorial/consuming_packages/the_flexibility_of_conanfile_py.html)
- [CMakeToolchain 与 preset 生成条件](https://docs.conan.io/2/reference/tools/cmake/cmaketoolchain.html)
- [fmt 的 CMake 目标](https://fmt.dev/latest/get-started/)
- [Google Benchmark 使用说明](https://github.com/google/benchmark/blob/v1.10.0/docs/user_guide.md)
