# Spec Evaluation

这一个目录放的是**可复用的 Spec 评测能力**，目标是让别的 Spec 也能复用同一套比较方法。

适合复用的内容：

- [protocol.md](./protocol.md)
  - comparison doc set 的评测协议
- [agent-evaluator.md](./agent-evaluator.md)
  - 评测 agent 的固定说明
- [templates/semantic-eval.template.json](./templates/semantic-eval.template.json)
  - 语义评测输出模板
- [bin/](./bin)
  - 评测入口脚本
- [scripts/](./scripts)
  - 评测实现脚本

这些内容的特点是：

- 不绑定 `tdd` 这个具体 Spec
- 不绑定本仓库 README 的最终文案
- 可以被别的 Spec 或别的 comparison row 复用

当前目录下最重要的入口：

```sh
authoring/spec-evaluation/bin/build-external-eval-pack.sh --row-id <row-id>
authoring/spec-evaluation/bin/measure-eval-pack.sh --pack-dir authoring/eval-packs/<row-id>
authoring/spec-evaluation/bin/measure-orbit-spec.sh --orbit <orbit-id>
authoring/spec-evaluation/bin/validate-semantic.sh --eval-file <semantic.json> --root <files-root>
```

补充说明：

- `measure-eval-pack.sh` + `validate-semantic.sh` 是主表对比的核心复用能力
- `measure-orbit-spec.sh` 更适合作为 OrbitSpec authored truth 的内部诊断
- README 主表真正对外展示的指标，仍应优先走 comparison doc set 口径
