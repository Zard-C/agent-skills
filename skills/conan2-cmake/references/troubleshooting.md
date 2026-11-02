# 常见错误与定位

## `cmake --preset conan-debug` 报 preset 文件不存在

先检查当前源码根目录和三个条件：

```bash
pwd
ls -l CMakeLists.txt conanfile.py
ls -l CMakeUserPresets.json
```

正常的模板流程要求：

1. `CMakeLists.txt` 已存在于 recipe 的 `source_folder`，默认是 `conanfile.py` 所在目录。
2. recipe 声明 `CMakeToolchain` 并提供 `layout()`。
3. 在正确目录成功执行过相应构建类型的 `conan install`。

典型情况是先执行 Conan，再创建或移动 `CMakeLists.txt`。此时 generators 目录已有 `CMakePresets.json`，根目录却没有 `CMakeUserPresets.json`。

修正目录或补齐源文件后，在项目根目录执行：

```bash
conan install . -s:h build_type=Debug -s:h compiler.cppstd=17 --build=missing
cmake --list-presets
cmake --preset conan-debug
```

若 root entry 已存在且是用户手写文件，Conan 通常不会覆盖。先读取并按现有结构包含生成的 preset，避免覆盖用户配置。若源码在子目录，调整 recipe 的 `cmake_layout(self, src_folder="...")`，而非盲目复制 preset JSON。

若命令列出了其他名称，使用实际名称。多配置生成器可能提供 `conan-default` configure preset 和单独的 `conan-debug` build preset。

## `CMakeDetermineLANGUAGECompiler.cmake` / `CMAKE_LANGUAGE_COMPILER`

查看 `project()` 或 `enable_language()`。`LANGUAGE` 会被当成语言名，正确关键字是复数 `LANGUAGES`：

```cmake
project(fmt_demo LANGUAGES CXX)
```

若 C/CXX 已识别而错误只指向 LANGUAGE，优先检查拼写。修正后可在原配置上使用 `cmake --fresh --preset conan-debug`，但该命令要求 CMake 3.24 或更高；旧版本使用新的构建目录。不要为这类拼写错误重装 GCC。

## 错误对照

| 现象 | 优先检查 | 处理方向 |
| --- | --- | --- |
| `externally-managed-environment` | 是否对系统 Python 使用 pip | Ubuntu 使用 pipx 或独立 venv 安装 Conan 2 |
| `conan: command not found` | pipx 安装位置、当前用户和 PATH | 核实 `$HOME/.local/bin`，执行 ensurepath 并更新当前 shell |
| 默认 profile 不存在 | 当前用户的 Conan home | 在实际构建环境执行 `conan profile detect --exist-ok` |
| `fmt/12.2.0` 未找到 | `conan remote list`、包版本、网络错误 | 核实配方和目标 remote，区分缺少配方与缺少二进制 |
| 缺少可用的依赖二进制 | host profile、编译器、标准、build_type | 配置正确后使用 `--build=missing`，并读首个真实编译错误 |
| CMake 找不到 fmt | preset/toolchain 是否被使用、配置是否匹配 | 使用 Conan preset，或显式传入实际生成的 toolchain |
| fmt 头文件可见但链接失败 | 目标是否链接 `fmt::fmt`、依赖是否同 ABI | 检查 imported target 和实际 profile/配置，避免手工混入系统 fmt |
| C 源码包含 fmt 后报大量错误 | 源码扩展名、启用的语言 | fmt 示例使用 `.cpp` 和 `LANGUAGES CXX` |
| 生成路径多了一层 `build` | `cmake_layout` 和 `--output-folder` 的组合 | 以 Conan 输出为准；基础模板使用 layout 即可 |
| 换目录后 preset 引用旧路径 | 生成的绝对路径、源码目录 | 在新位置重跑 Conan，避免沿用旧机器或旧容器生成文件 |
| Mac 构建产物在容器中无法运行 | OS、架构和宿主机缓存是否混用 | 使用独立 Linux 构建目录并重新安装匹配依赖 |

## 网络问题

先区分 DNS、TCP/代理连接、TLS、HTTP 鉴权/限流和 remote 配方可用性；同一个错误不要通过反复切 profile 或全量清缓存处理。

若用户只需要逐步排障，每次给一个能区分原因的验证命令并解释结果。代理变量设置方式见 [setup.md](setup.md)。不要记录凭据或将 token 放入可提交的 recipe。

## 需要更改工具链时

`profile detect --exist-ok` 只保证不覆盖旧 profile，不保证旧值正确。编译器、C++ 标准、OS 或架构变更后查看 profile，使用适当的独立 profile 与构建目录。跨编译应分别确认 build profile 和 host profile，以及实际交叉编译器路径；仅修改 `arch` 不能提供编译器或 sysroot。

定位问题后只处理相关构建目录或确有问题的包，不默认执行全 cache 删除或所有依赖强制重编译。
