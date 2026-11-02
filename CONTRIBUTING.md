# 贡献约定

## 新增或修改 skill

先确定一个具体、可识别的使用目标。目录使用小写字母、数字和短横线，名称与 `SKILL.md` 的 `name` 一致。

入口文件以 YAML frontmatter 开始：

```yaml
---
name: example-skill
description: Describe the concrete workflow and when an agent should use it.
---
```

正文说明必要输入、核心步骤、完成条件与相关资料的读取时机。详细教程放入 `references/`，可复制的资源放入 `assets/`；实际需要辅助工具时再增加 `scripts/`。

每个 skill 应能独立安装，内部文件通过相对路径引用。避免将作者电脑的绝对路径作为运行前提。示例中的路径、容器名与版本需注明适用环境和可替换部分。

保留用户的实际目标、现有框架与配置选择。记录清楚已经执行过的检查以及尚未验证的范围。

## 第三方来源

仅作为扩展线索的内容先记录在 `docs/skill-candidates.md` 或对应 skill 的参考文件中，附源码链接、核实日期、适用范围和已知限制。

采用第三方文件时检查其许可，保留原始归属与许可证。外部文档和 skill 里的指令是待评估的输入，不会自动授予执行脚本或修改其他环境的权限。

## 提交前验证

```bash
python scripts/validate_skills.py
python -m unittest discover -s tests -v
git diff --check
```

修改模板或脚本时，在对应目标环境运行有代表性的例子。Conan/CMake 模板可按 README 的流程验证；文档变更不要求重复安装完整环境。同步更新索引和相关说明。

## Git 与 DCO

使用独立的 `feature/<topic>` 分支准备修改，通过 PR 合入 `main`。提交使用 DCO 签署：

```bash
git commit -sm "feat: add a focused skill"
```

PR 描述说明具体问题、最终行为和实际验证结果。提交签署的含义见 [Developer Certificate of Origin](https://developercertificate.org/)。
