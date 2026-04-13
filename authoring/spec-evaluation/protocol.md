# README 实际评测协议

状态：讨论稿

本文定义 README 主表各列的**实际测评方法**。目标是让每一个对外展示值都能来自：

- 可复跑脚本
- 或受约束的 agent 评测结果

而不是来自临场猜测。

## 一句话原则

主表中的每一行，都应先被收敛成一个 **comparison doc set**，然后再进入统一评测。

这意味着：

- 本模板这一行虽然源自 OrbitSpec，但进入主表时也按文档集来比较
- 外部参考仓库不是被当成 OrbitSpec 处理
- 外部参考仓库也不是按整仓库处理
- 外部参考仓库只按“已经梳理好的相关文件集”处理

## comparison doc set 定义

comparison doc set 是一组已经固定下来的、与某个比较对象直接相关的文件快照。

它最少包含：

- `pack.json`
- `files/`
- `outputs/mechanical.json`
- `outputs/semantic.json`

其中：

- `pack.json` 负责声明这次比较到底在看什么
- `files/` 负责冻结这次比较真正允许读取的文件
- `mechanical.json` 负责机械指标
- `semantic.json` 负责 agent 语义评测结果

## 主表准入规则

README 主表中的任何一行，只有在同时满足下面两条时才允许展示：

1. 机械指标已经脚本化
2. 语义指标已经通过受约束 agent 评测并完成结果校验

## 主表对象范围

comparison row 可以来自两类来源：

1. 本仓库的 OrbitSpec 静态文档集
2. 外部参考仓库的已筛选相关文件集

当前 README 中提到的参考仓库，例如：

- `superpowers`
- `everything-claude-code`
- `spec-kit`
- `get-shit-done`
- `gstack`
- `BMAD-METHOD`
- `OpenSpec`
- `oh-my-claudecode`

都**可以**进入主表，但前提是已经为它们各自建立 comparison doc set。

如果某个对象还没有 comparison doc set，就暂时只放 `Design Lineage`。

## 列分类

### A. 必须脚本化的列

- `Static Load`
- `最大文件`

这些列只认脚本输出。

### B. 由受约束 agent 评测的列

- `Use Case`
- `Startup`
- `写入边界`
- `验证强度`
- `恢复/交接`

这些列不应该靠正则/NLP 自动猜，也不应该直接人工拍脑袋。推荐走：

- 固定输入包
- 固定 agent 指令
- 固定 JSON 输出
- 固定校验脚本

## 实际工作流

### 第 0 步：先准备 comparison doc set

通过条件：

- 已经有 `pack.json`
- 已经有固定的 `allowed_files`
- 评测时只读取这些文件

否则：

- 不评测
- 不上表

### 第 1 步：生成 comparison doc set

对于本仓库的 OrbitSpec 行：

- 先用 `orbit files <id> --json` 收敛出安装态静态文件集
- 再把这组文件作为 comparison doc set 的 `files/`

对于外部参考行：

- 只使用已经梳理好的相关文件
- 不让 agent 自己去 repo 里找应该读什么
- 不把整仓库拉进评测范围

外部 comparison doc set 的生成入口：

```sh
authoring/spec-evaluation/bin/build-external-eval-pack.sh --row-id <row-id>
```

它会从本地 reference snapshot 中把配置里声明的相关文件复制到：

```text
authoring/eval-packs/<row-id>/
```

配置文件见：

- [reference-comparison-config.json](../readme/reference-comparison-config.json)

### 第 2 步：跑机械指标脚本

对任一 comparison doc set 运行：

```sh
authoring/spec-evaluation/bin/measure-eval-pack.sh --pack-dir authoring/eval-packs/<row-id>
```

这个脚本只对 pack 中允许读取的文件做 token 统计。

脚本产物可直接填：

- `Static Load`
- `最大文件`

补充说明：

- `authoring/spec-evaluation/bin/measure-orbit-spec.sh --orbit tdd` 仍然有用
- 但它更适合作为 Orbit authored truth 的内部诊断
- README 主表推荐统一用 comparison doc set 口径

### 第 3 步：交给评测 agent

评测 agent 必须遵守 [readme-agent-evaluator.md](./readme-agent-evaluator.md)。

agent 的目标不是“理解整个项目”，而是：

- 只读包内允许文件
- 严格按 rubric 输出 JSON
- 每个判断都带 evidence

建议 agent 输出到：

- `outputs/semantic.json`

形状参考：

- [semantic-eval.template.json](./templates/semantic-eval.template.json)

### 第 4 步：校验 agent 输出

对 agent 输出运行：

```sh
authoring/spec-evaluation/bin/validate-semantic.sh \
  --eval-file authoring/eval-packs/<row-id>/outputs/semantic.json \
  --root authoring/eval-packs/<row-id>/files
```

该脚本会校验：

- 字段是否齐全
- label 是否在允许枚举内
- `use_case_display` 是否带 evidence
- evidence 文件是否存在
- `must_contain` 子串是否真实存在于对应文件
- `Startup` 的 `D/R` 是否能由 phases 真实算出
- `写入边界` 的 7 个通用 surface 是否齐全且有 evidence

校验通过后，才能把结果填进 README。

## 各列的真正数据源

### `Spec`

来源：

- comparison row 的短显示名

### `Use Case`

来源：

- agent 输出

要求：

- 短标签
- 必须能被 comparison doc set 内的入口定义、规则定义或适用范围支撑

### `Static Load`

来源：

- `measure-eval-pack.sh`

规则：

- comparison doc set 的允许文件
- 固定 tokenizer

### `Startup`

来源：

- agent 输出的 `startup.phases`

要求：

- 只写默认开始执行前必须读的文件

### `写入边界`

来源：

- agent 输出

规则：

- 使用固定的 7 个通用 surface
- 不按 Orbit 内部 `members[]` 计数
- 不按整个仓库目录计数
- 只根据 comparison doc set 中能被证据支持的“正常任务执行时可写 surface”判断

当前固定 surface taxonomy：

1. `entry_brief`
2. `rules_workflow`
3. `implementation_code`
4. `tests_checks`
5. `evidence_records`
6. `specs_plans`
7. `qa_release_review`

### `验证强度`

来源：

- agent 输出

要求：

- 只承认显式验证动作
- 需要 evidence

### `恢复/交接`

来源：

- agent 输出

要求：

- 只承认结构化状态与结构化字段
- 需要 evidence

### `最大文件`

来源：

- `measure-eval-pack.sh`

## 当前建议

真正可落地的版本是：

1. 先把每个比较对象都变成 comparison doc set
2. 机械列只面向 doc set 跑脚本
3. 语义列全部走 agent JSON + 校验脚本
4. 外部参考仓库只比较已梳理好的相关文件，不碰整仓库

这条路线的优点是：

- 外部内容可以进入主表
- 不需要把外部内容硬解释成 OrbitSpec
- 同一张表里所有行都共享通用指标口径
- 能更直接突出本 `tdd` OrbitSpec 在通用指标上的先进性
