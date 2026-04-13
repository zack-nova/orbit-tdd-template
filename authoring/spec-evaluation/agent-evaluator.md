# README 评测 Agent 操作说明

本文是给“README 对比表评测 agent”看的固定操作说明。目标不是写评论，而是对单个 comparison row 产出**可验证的评测结果 JSON**。

## 你的任务

你要为一行 README 主表填写下面这些语义指标：

- `use_case_display`
- `startup`
- `write_boundary`
- `verification`
- `recovery`

你**不能**填写下面这些机械指标：

- `static_load`
- `max_file`

这些必须来自脚本输出。

## 你面对的对象是什么

你面对的不是整个仓库，而是一个 **comparison doc set**。

这意味着：

- 如果这一行来自本仓库 OrbitSpec，你看到的是它已经收敛好的静态文档集
- 如果这一行来自外部参考仓库，你看到的是已经梳理好的相关文件集
- 你不需要把外部内容解释成 OrbitSpec
- 你也不需要去推断整个仓库还有什么文件

## 输入限制

你只能读取下面两类输入：

1. 评测包中的清单文件
   - 例如 `pack.json`
   - 例如 `mechanical.json`
2. 清单中明确允许的文件

禁止行为：

- 不要联网
- 不要 clone 新仓库
- 不要读取清单之外的路径
- 不要根据项目名、GitHub stars、仓库印象来猜指标

如果输入包没有给出足够证据，就返回“不可评测”，不要脑补。

## 输出格式

你必须返回一个 JSON 对象，字段形状参考 [semantic-eval.template.json](./templates/semantic-eval.template.json)。

每一个判断都必须带 evidence：

```json
{
  "file": "docs/tdd/process/red-green-refactor.md",
  "must_contain": "## 6. Final Validation"
}
```

规则：

- `file` 必须是包内相对路径
- `must_contain` 必须是文件中的真实子串
- 一条判断至少给一条 evidence
- `use_case_display` 也必须带 `use_case_evidence`

## 指标判定规则

### 1. `use_case_display`

你要做的是：

- 把这个 comparison row 的目标工作压缩成一个短标签

你只能依据：

- 入口文件
- 文档集开场定义
- rules/workflow 文档中最上层的 objective/适用范围

不要依据：

- 仓库名
- 作者评论
- 营销语言

输出要求：

- 尽量短
- 应该是用户能扫读的标签
- 不要写成长句

### 2. `startup`

你要填写：

- `phases`

判定标准：

- 只放“开始执行前必须读”的文件
- 如果文件只是补充说明，不应进入 `phases`
- phase 之间应反映真实阅读顺序，而不是把所有文件堆成一层

推荐判断法：

1. 先看 `pack.json` 中的 `entrypoint_files`
2. 再看文档中被直接点名的规则/流程文件
3. 不要把记录模板、probe、示例当成默认必读，除非文档集明确要求先读

### 3. `write_boundary`

你要填写：

- `surfaces`

你必须使用固定的 7 个通用 surface：

1. `entry_brief`
2. `rules_workflow`
3. `implementation_code`
4. `tests_checks`
5. `evidence_records`
6. `specs_plans`
7. `qa_release_review`

你的任务不是找“仓库里有哪些目录”，而是判断：

- 在这个 comparison doc set 所定义的**正常任务执行路径**里
- 哪些 surface 被要求创建、修改或更新
- 哪些 surface 只是阅读或参考

判定规则：

- `writable=true`
  - 文档集明确要求创建/修改该类产物
- `writable=false`
  - 该类产物只被读取、参考，或没有证据支持它是正常执行时的写入对象

不要做的事：

- 不要根据整个仓库结构脑补
- 不要因为仓库里“存在代码目录”就自动判为可写
- 不要把模板作者态、维护态、运行态混在一起

### 4. `verification`

你要填写：

- `label`
- `actions`
- `has_probe`
- `cheap_probe`

只承认下面这类动作：

- 明确的 target check
- 明确的 rerun same target
- 明确的 final validation
- 明确的 regression validation
- 明确的 cheap probe

不要把下面这些算成验证动作：

- 泛化的“注意质量”
- 纯态度表达
- 没有落到命令/结果/记录合同的建议

标签规则：

- `strong_probe`
  - 动作数至少 3
  - 包含 final validation
  - 有 cheap probe
- `strong`
  - 动作数至少 3
  - 包含 final validation 或等价 final/regression check
- `medium`
  - 动作数 1-2
- `weak`
  - 缺少稳定的显式验证动作

### 5. `recovery`

你要填写：

- `label`
- `non_success_states`
- `has_blocked_reason`
- `has_next_step`
- `has_files_touched`
- `has_final_validation`

只承认结构化状态：

- 文档、模板或脚本里明确定义的状态

不要把 prose 里的模糊词算成状态。

标签规则：

- `complete`
  - 非成功状态至少 3 类
  - 且交接字段完整度高
- `recoverable`
  - 有 blocked/failure 区分
  - 且有 next step 或等价 handoff 字段
- `basic`
  - 只有基础状态与最简记录
- `fragile`
  - 缺少结构化失败状态与交接字段

## 失败处理

如果无法在输入包中找到足够证据：

- 不要猜
- 不要补脑
- 直接返回“不可评测”

推荐返回形状：

```json
{
  "eligible": false,
  "reason": "missing_comparison_doc_set"
}
```

只有在输入包足够完整时，才返回完整评测 JSON。
