# README Authoring

这一个目录放的是**本仓库 README 优化与对比配置**，它们是 repo-specific 的，不应被默认当成通用 Spec 评测能力。

当前内容：

- [comparison-plan.md](./comparison-plan.md)
  - 本仓库 README 对比模块的改造方案
- [reference-comparison-config.json](./reference-comparison-config.json)
  - 本仓库主表外部参考对象的 comparison doc set 配置
- [semantic-eval.tdd.example.json](./semantic-eval.tdd.example.json)
  - `tdd` 这一行的语义评测样例
- [fetch-reference-docs.sh](./fetch-reference-docs.sh)
  - 本仓库外部参考文档快照的刷新脚本

如果要迁移这套方法到别的 Spec，优先复用的是：

- [../spec-evaluation](../spec-evaluation)

而不是直接复用本目录里的 repo-specific 配置。
