# 社区 skills 扩展储备

检索与源码核实日期：2026-11-03。下列第三方 skill 作为阅读与扩展候选；未安装，也未运行其脚本。搜索索引或聚合站的评分不能替代源码核对。再次使用时重新确认路径和内容。

## 已读到源码

| Skill | 原始源码 | 适合扩展的能力 | 使用前需要复核 |
| --- | --- | --- | --- |
| `conan-vcpkg` | [mohitmishra786/low-level-dev-skills](https://github.com/mohitmishra786/low-level-dev-skills/blob/main/skills/build-systems/conan-vcpkg/SKILL.md) | Conan 2/CMake 接入、profiles、交叉编译和不同包管理器的目标名对照 | 安装示例使用直接 pip；依赖版本为示例，不应视为当前推荐；交叉编译 profile 不会自动安装交叉工具链 |
| `cmake` | [mohitmishra786/low-level-dev-skills](https://github.com/mohitmishra786/low-level-dev-skills/blob/main/skills/build-systems/cmake/SKILL.md) | target 用法、PUBLIC/PRIVATE/INTERFACE、presets、库导出、sanitizers | 这是配套 CMake skill，不是专门的 Conan 2 skill；preset JSON schema 与最低 CMake 版本需要单独核对 |
| `taosgen-build` | [taosdata/taosgen](https://github.com/taosdata/taosgen/blob/main/.agent/skills/taosgen-build/SKILL.md) | 一个真实 C++17 项目的 Conan 2 构建、CTest、IDE 与多平台排错结构 | 强项目绑定；其 pip 命令、profile 强制覆盖、全 cache 清理建议不适合作为本流程默认动作；快速构建段的 toolchain 接入需结合该项目 CMake 实现核实 |

它们来自社区或具体项目，并非本次确认的 Conan 官方通用 skill。本次读取确认的是文件内容，不是全部命令的运行正确性。

## 仅有索引，源码路径待核实

`mise-cpp-package-managers`，作者索引为 `ray-manaloto/claude-code-marketplace`：

- [检索入口](https://skills.rest/skill/mise-cpp-package-managers)
- 索引描述包含通过 mise 固定 Conan 版本、使用 pipx backend，以及将 Conan/CMake 接入任务流。
- 索引给出的 `main/mise-toolkit/skills/mise-cpp-package-managers/SKILL.md` 路径在核实时返回 GitHub API 404，另一个常见 plugins 路径也未读到。原因可能是移动、删除或访问限制，未进一步确认。
- 仅保留为待核实线索，不提供为已验证可安装的推荐。

搜索中出现的 `setup-conan-skills` 属于另一套以 Conan 命名的 Claude hooks/skills 集合，不是 Conan 2 C/C++ 包管理器安装 skill，未纳入候选。

## 后续扩展顺序

1. 固定项目 profile 和 Conan 版本，接入 lockfile 与 CI cache，验证复现范围。
2. 学习 build/host profiles，按目标机器补充真实的交叉编译器和 sysroot。
3. 为更多第三方库增加 `find_package` / imported target 接入，逐个验证 ABI、静态/动态配置和运行时库路径。
4. 需要分发自有 C++ 库时，再扩展 recipe 的 `build()`、`package()`、`package_info()` 和 `test_package`。

借鉴社区实现时，用官方 Conan 2 文档核对 API 与命令；仅在用户要求采用时安装候选 skill，选择具体 skill 目录而非默认拉入整个第三方集合。

## 持续查阅的官方来源

- [Conan 与 CMake 集成](https://docs.conan.io/2/integrations/cmake.html)
- [Profiles](https://docs.conan.io/2/reference/config_files/profiles.html)
- [Lockfiles](https://docs.conan.io/2/tutorial/versioning/lockfiles.html)
- [交叉编译](https://docs.conan.io/2/tutorial/consuming_packages/cross_building_with_conan.html)
- [创建包教程](https://docs.conan.io/2/tutorial/creating_packages.html)
