# Agent Skills

从实际开发和排错过程中整理的可复用 AI agent skills。每个 skill 独立保存适用场景、操作流程、参考资料和必要的模板。

## Skills 索引

| Skill | 分类 | 用途 | 已验证范围 |
| --- | --- | --- | --- |
| [conan2-cmake](skills/conan2-cmake/SKILL.md) | C/C++ | Conan 2 依赖管理、CMake presets、容器环境与排错 | Ubuntu 24.04.4 / Linux armv8 profile，fmt 12.2.0 模板在现有缓存下配置、编译、运行通过 |

详细版本和验证边界见各 skill 的参考文件；索引不代表所有平台或全新安装均经过验证。

## 使用方式

选择需要的 skill，将其整个目录安装到所用 agent 支持的 skills 目录。支持 GitHub 目录安装的工具应指定 `skills/<skill-name>`，例如 `skills/conan2-cmake`。

目录内的 `references/`、`assets/`、`scripts/` 与 `agents/` 是 skill 的组成部分，安装时保留相对结构。`agents/openai.yaml` 提供 Codex 展示信息；其他 agent 是否支持其扩展字段，以对应工具的文档为准。

仓库内容作为维护源，本机 skills 目录作为安装副本。升级已有同名 skill 前，先比较并保留本地定制内容。

## 目录结构

```text
skills/<skill-name>/
  SKILL.md             # 必需：元数据、触发条件和核心流程
  agents/openai.yaml   # 可选：Codex 展示和调用信息
  references/          # 可选：详细说明、排错和依据
  assets/              # 可选：项目模板等可复制资源
  scripts/             # 可选：实际需要的可执行辅助工具
```

技能保持单层目录，在本页通过分类建立索引。详细资料从 `SKILL.md` 按需引用，避免重复堆叠在入口文件中。

## 本地检查

需要 Python 3.10 或更高：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/validate_skills.py
python -m unittest discover -s tests -v
```

校验器检查必需的 frontmatter、名称与目录是否一致、内部 Markdown 链接和可选 Codex YAML 文件。它不验证公网链接、实际执行效果或所有 agent 的兼容性。

## fmt 模板验证

在具备 Conan 2、CMake 3.23+ 和 C++ 编译器的目标环境执行：

```bash
cd skills/conan2-cmake/assets/fmt-demo
conan profile detect --exist-ok
conan install . -s:h build_type=Debug -s:h compiler.cppstd=17 --build=missing
cmake --list-presets
cmake --preset conan-debug
cmake --build --preset conan-debug --parallel
./build/Debug/hello
```

以上运行命令对应 Ubuntu 的默认单配置生成器。预期输出：`Hello, Conan! Answer = 42`。依赖缓存位于当前用户的 Conan home；生成的 presets 与构建产物不提交。

GitHub Actions 定义了格式检查与 Ubuntu fmt 构建任务。远程仓库建立后，以实际 Actions 运行结果为准。

## 扩展与贡献

- [第三方候选索引](docs/skill-candidates.md)：已查看源码的候选及待核实线索。
- [贡献约定](CONTRIBUTING.md)：命名、验证、分支与 DCO。

本仓库原创内容采用 [MIT License](LICENSE)。引入第三方内容时保留其原始许可和归属说明。
