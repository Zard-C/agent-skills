# 环境与首次接入

## macOS 上的持久容器

宿主机安装并启动 Docker Desktop，确认 `docker info` 能连接服务。以下假设已有 `cs107-dev` 镜像；使用前通过 `docker image ls` 核实。缺少镜像时按项目 Dockerfile 构建。

在需要挂载的项目目录中执行：

```bash
docker run -it --name cs107 -v "$PWD":/workspace -w /workspace cs107-dev
```

此示例适用于默认用户为 root 的 CS107 镜像，不添加 `--rm`。已有同名容器时先查看状态；停止后使用 `docker start -ai cs107`，运行中需要额外 shell 时使用 `docker exec -it cs107 bash`。

容器内安装的软件和 `/root/.conan2` 随容器保留；删除/重新创建容器时不会自动保留。仅挂载 `/workspace` 不会持久化 root 家目录。需要跨容器复用 Conan cache 时单独设计卷及其所有权。

## 在 Ubuntu 容器中安装 Conan 2

以下命令以容器内 root 执行；其他用户根据权限调整。已有 Conan 2 时先核实版本和来源，无需重复安装。

```bash
apt-get update
apt-get install -y build-essential cmake ca-certificates pipx python3-venv
pipx install 'conan>=2,<3'
pipx ensurepath
export PATH="$HOME/.local/bin:$PATH"
conan --version
cmake --version
c++ --version
```

`pipx` 隔离 Conan 的 Python 依赖，适合 Ubuntu 24.04 的 externally-managed Python。`export` 让当前终端立即生效，`pipx ensurepath` 配置后续 shell；无需默认使用 `--break-system-packages`。

这条安装命令选择可用的 Conan 2 版本。若团队要求重复构建，核实并固定实际版本，例如将范围改成经过验证的 `conan==2.x.y`，其中版本需替换为真实值。

首次建立 profile：

```bash
conan profile detect --exist-ok
conan profile show
```

`--exist-ok` 保留已存在的 default profile；已有 profile 不一定匹配当前编译器，仍需查看内容。配置应描述容器里的 Linux/GCC/架构，而不是宿主机 macOS。CI 使用审核过的 profiles，自动检测主要用于交互式初始化。

## 最小项目文件

从本 skill 的 `assets/fmt-demo/` 获取模板。它应具有以下结构，三个文件必须先于 `conan install` 创建：

```text
demo/
  conanfile.py
  CMakeLists.txt
  src/
    main.cpp
```

Conan recipe 描述依赖与生成方式；CMake 描述项目 targets。CMake 使用 `fmt::fmt` 自动获得编译和链接要求。标准消费流程无需 recipe 的 `build()` 方法。

`conanfile.py` 的示例版本为 `fmt/12.2.0`，其配方已于 2026-11-03 在 [ConanCenter Index](https://github.com/conan-io/conan-center-index/blob/master/recipes/fmt/config.yml) 核实。再次使用时仍需核实所选 remote；配方存在不保证所有平台都有预编译包。

进入新项目根目录，再执行主 skill 的安装与构建命令。`CMakeUserPresets.json` 由 Conan 在源码目录生成，用于包含 generators 目录里的 `CMakePresets.json`。Conan 找不到 `source_folder/CMakeLists.txt` 时，可能已有内部 preset，却没有根目录入口。

模板不带自定义 profile、layout 配置或生成器时，Ubuntu 单配置构建输出通常位于 `build/Debug`，可执行文件为 `build/Debug/hello`。生成文件目录随 Conan 版本与 layout 配置变化；使用实际 presets，不凭经验硬编码 generators 路径。

## 不使用 preset 的等价方式

先查看 `conan install` 输出，取得实际生成的 `conan_toolchain.cmake` 路径。保持 Conan 与 CMake 的构建类型、编译器及标准一致，并使用新的构建目录。

```bash
cmake -S . -B build/manual-debug \
  -DCMAKE_TOOLCHAIN_FILE=/absolute/path/to/generated/conan_toolchain.cmake \
  -DCMAKE_BUILD_TYPE=Debug
cmake --build build/manual-debug --parallel
```

替换上述工具链占位路径。切换 layout、生成器或工具链时，优先选择独立的构建目录；只刷新 CMake 缓存不会重新安装 Conan 依赖。

## VS Code 附加

在 Mac 本地 VS Code 安装微软 `Dev Containers`，扩展 ID 为 `ms-vscode-remote.remote-containers`。Docker/Container Tools 的 Attach Shell 只提供终端。

运行 `Dev Containers: Attach to Running Container...`，选中容器并打开项目的真实路径，例如 `/workspace/demo`。仅附加已有容器无需先创建 `devcontainer.json`。

在容器环境安装需要的 C/C++、CMake Tools 扩展。CMake Tools 选择实际生成的 Conan configure preset；使用 `cmake --list-presets` 核对。若 `conan` 不在 VS Code 终端 PATH 中，检查 pipx 的 PATH 配置及该 shell 是否加载了它。

## 宿主机 VPN 与代理

Docker Desktop 的容器流量通过宿主机网络进程发出，VPN/TUN 是否接管取决于实际分流规则。仅开启 Mac 系统代理时，容器应用不一定自动继承代理。

如需让 pipx、Conan、Git 等支持代理变量的程序访问 Mac 上的 HTTP/Mixed 代理，可在容器 shell 中设置。下例 `7890` 仅为示例，先核实客户端端口及监听范围：

```bash
export http_proxy="http://host.docker.internal:7890"
export https_proxy="$http_proxy"
export HTTP_PROXY="$http_proxy"
export HTTPS_PROXY="$https_proxy"
export no_proxy="localhost,127.0.0.1,host.docker.internal"
export NO_PROXY="$no_proxy"
```

容器的 `127.0.0.1` 指向容器自身；`host.docker.internal` 用于连接 Mac。代理需要允许 Docker 连接其监听端口；不要未核实就更改监听地址或对局域网开放。HTTP 代理变量不是所有协议的透明 VPN，单次 `export` 也不会自动持久化。

## 进一步复现环境

- Dockerfile 固化系统工具和 Conan 版本；依赖安装仍按项目 recipe/profile 执行。
- 源码仓库保存 recipe、CMake 配置和需要的 profiles/lockfile；生成的 `CMakeUserPresets.json`、构建产物和整个 Conan cache 通常不提交。保留项目原有 Git 策略。
- 包名与版本号、recipe revision、package ID、二进制 revision 不是同一概念。严格复现时结合锁文件、profiles、remote 与工具链版本，而不是只固定 `fmt/12.2.0`。

## 本次验证范围

2026-11-03 在既有 `cs107` 容器的独立 `/tmp` 目录验证了自带 fmt 模板：Ubuntu 24.04.4、Conan 2.34.0、CMake 3.28.3、GCC 13.3.0、Linux/armv8 profile，生成器为 Unix Makefiles。

安装验证使用主流程的参数并额外加了 `--no-remote`，成功复用已有 fmt 12.2.0 缓存；`cmake --list-presets`、配置、编译、运行全部通过，输出为 `Hello, Conan! Answer = 42`。这证明了当前容器中的依赖消费链路，未重新验证空缓存下载、全新系统安装、其他平台或交叉编译。

## 官方参考

- [Conan 安装与 pipx](https://docs.conan.io/2/installation.html)
- [Conan profile 命令](https://docs.conan.io/2/reference/commands/profile.html)
- [CMake presets 构建流程](https://docs.conan.io/2/examples/tools/cmake/cmake_toolchain/build_project_cmake_presets.html)
- [Docker Desktop VPN 与宿主机连接](https://docs.docker.com/desktop/features/networking/networking-how-tos/)
- [VS Code 附加已有容器](https://code.visualstudio.com/docs/devcontainers/attach-container)
- [Conan lockfiles](https://docs.conan.io/2/tutorial/versioning/lockfiles.html)
