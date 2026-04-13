# README 评价与对比模块改进方案

状态：讨论稿

本文用于沉淀 `README.md` / `README.zh-CN.md` 的对比模块改造方案，以及后续如何**可验证地**填充对比表。它是 source-only authoring material，不应进入最终 `orbit_template` payload。

如果本文与 [protocol.md](../spec-evaluation/protocol.md) 冲突，以后者为准。

本文更偏向：

- README 模块结构
- 用户视角下的产品表达
- 本仓库主表文案与展示建议

README 主表的实际评测口径，一律以 `authoring/spec-evaluation/` 下的协议和脚本为准。

## 目标

README 的对比模块应服务首次访问者的选择判断，而不是继续充当作者调研清单。

本轮收口目标：

- README 只保留一张主表。
- 表头第一列从 `Harness` 改成 `Spec`。
- 去掉 `重复规则率` 与 `潜在矛盾` 两列。
- 不展示 GitHub stars、更新时间等容易过时的噪音指标。
- 对外展示值必须能追溯到明确的数据源和校验步骤，不能靠 README 文案启发式猜测。

推荐主表列：

| Spec | Use Case | Static Load | Startup | 写入边界 | 验证强度 | 恢复/交接 | 最大文件 |
| --- | --- | ---: | ---: | --- | --- | --- | ---: |

## README 推荐结构

推荐把当前 README 的叙事调整为：

1. Hero
   - 一句话定位：严格 TDD 核心，但保持轻量、可恢复、可交接。
2. Quick Start
3. What You Get
4. Why This Spec
   - 3 个短点，不展开成长段比较文。
5. Comparison At A Glance
   - 放单张主表
   - 表后放极短图例
6. Design Lineage
   - 保留 2-4 句简述，不再放 stars 表

当前 [README.md](../README.md) 的 `Research Behind This Template` 和 [README.zh-CN.md](../README.zh-CN.md) 的“这份模板参考了哪些经验”建议降级为 `Design Lineage`。如果仍需保留完整外部参考清单，应留在 source-only 作者材料，而不是 README 主体。

## 显示值格式

主表建议统一显示格式如下：

- `Spec`：短名，例如 `tdd`
- `Use Case`：短标签，例如 `TDD / code change`
- `Static Load`：`2.8k`
- `Startup`：`D2/R4`
- `写入边界`：`窄 (2/7)` / `中 (3/7)` / `宽 (5/7)` / `模糊`
- `验证强度`：`强 + probe` / `强` / `中` / `弱`
- `恢复/交接`：`完整 (4态)` / `可恢复 (3态)` / `基础 (2态)` / `脆弱`
- `最大文件`：`0.9k`

表下图例建议压缩为：

- `Static Load`：默认安装态静态文件总 token 数
- `Startup`：`D=必经阅读层数`，`R=开始执行前必读文件数`
- `写入边界`：固定 7 个通用 surface 中的可写数 / 7
- `验证强度`：基于显式验证动作、final validation、cheap probe
- `恢复/交接`：基于非成功状态枚举与交接字段
- `最大文件`：静态文件集中的最大 token 数

## 关键原则：只展示“可追溯值”

README 中这张表不应直接从 prose 推断。推荐把表格填充分成两类输入：

1. 机械可提取输入
   - 由 OrbitSpec、发布态文件集、脚本、模板文件直接计算得出
2. 作者显式声明输入
   - 无法稳定自动推断、但又必须展示的语义值，由 source-only 清单声明，并由脚本交叉校验

不允许的做法：

- 从 README/文档里抓几个动词就推断 `Use Case`
- 从“Read ...”自然语言自动猜 `Startup`
- 从泛化语气词自动判定 `验证强度`
- 从叙事 prose 自动脑补 `恢复/交接`
- 在没有固定 tokenizer 的情况下展示 token 数

## 推荐数据流

推荐后续把 README 表格的生成收口到下面这条链路：

1. `orbit validate --json`
   - 确认当前 spec 合法，拿到 orbit id 与 `scope_count`
2. `orbit template publish --orbit <id> --json`
   - 生成或刷新本地 `orbit-template/<id>` 发布分支
3. 在发布分支上解析安装态静态文件集
   - 推荐通过临时 worktree + `orbit files <id> --json`
4. 用固定 tokenizer 统计静态文件 token
5. 读取 source-only 的 comparison metadata
   - 只承载难以自动推断但必须展示的语义信息
6. 交叉校验 metadata 与发布态文件/模板/脚本
7. 渲染 README 表格行

推荐新增一个 source-only 元数据文件，示例路径：

- `authoring/readme-spec-metrics.yaml`

它不进入模板 payload，只服务 README 生成与校验。

## 推荐元数据形状

下面这类字段适合由作者显式声明，再让脚本校验：

```yaml
spec_display: tdd
use_case_display: TDD / code change

startup:
  phases:
    - files:
        - .harness/orbits/tdd.yaml
    - files:
        - docs/tdd/README.md
        - docs/tdd/process/red-green-refactor.md
        - docs/tdd/process/blocked-and-handoff.md

verification:
  actions:
    - id: red_target
      kind: target_check
      evidence_files:
        - docs/tdd/README.md
        - docs/tdd/templates/tdd-record.md
      required_markers:
        - RED command:
        - RED result:
    - id: green_rerun
      kind: rerun_same_target
      evidence_files:
        - docs/tdd/README.md
        - docs/tdd/templates/tdd-record.md
      required_markers:
        - GREEN command:
        - GREEN result:
    - id: final_validation
      kind: final_validation
      evidence_files:
        - docs/tdd/process/red-green-refactor.md
        - docs/tdd/templates/tdd-record.md
      required_markers:
        - Final validation
        - Final validation command:
        - Final validation result:
  cheap_probe:
    path: tools/check-tdd-records.sh

recovery:
  non_success_statuses:
    - failure
    - blocked
    - abnormal_exit
    - external_stop
  required_fields:
    - files_touched
    - blocked_reason
    - next_step
    - final_validation
```

这里的原则是：

- `Use Case` 不自动生成，必须人工给出短标签
- `Startup` 不靠 NLP 猜，直接声明“必经阅读分层”
- `验证强度` 与 `恢复/交接` 的语义判断可以由 metadata 声明，再由脚本去验证支撑证据是否存在

## 各列的统计与填充方案

### 1. `Spec`

显示值来源：

- 优先用 metadata 中的 `spec_display`
- 否则回退到 `.harness/orbits/<id>.yaml -> id`

展示规则：

- 应是短标签，不放 repo 名，不放 branch 名
- 建议与用户安装/调用时看到的 orbit id 一致

### 2. `Use Case`

显示值来源：

- 只允许来自 metadata 的 `use_case_display`

原因：

- 这是用户决策文案，不是稳定 schema 字段
- 自动从 description 或 README 摘要会不可避免地引入“看起来合理、实际上不稳”的文案漂移

校验要求：

- 长度建议不超过 24 个英文字符或 12 个中文字符的等价阅读负担
- 必须能被 OrbitSpec 的 `description`、README Hero 或 rule objective 支撑

### 3. `Static Load`

定义：

- 默认安装态中，该 spec 自带静态文件的总 token 数
- 不统计目标项目自己的业务代码/测试文件
- 不统计运行时产生的 task records

推荐文件集：

- 以发布态 `orbit-template/<id>` 为准
- 用临时 worktree 进入发布分支
- 运行 `orbit files <id> --json`
- 用返回的文件集作为静态统计集合

为什么不用 `git ls-tree` 直接全算：

- 发布分支里还会有 `.harness/manifest.yaml` 这类控制面文件
- `orbit files` 输出更接近“安装后该 spec 默认投影可见的静态文件集”

tokenizer 建议：

- 必须固定一种 tokenizer 后才能对外展示
- 当前推荐 `o200k_base`

推荐理由：

- 与当前 OpenAI 新模型家族更接近
- 对中英混排更稳
- 本仓库试跑中 `cl100k_base` 与 `o200k_base` 的总量差异仅 `2780 -> 2787`，量级稳定

展示规则：

- 四舍五入到百位后显示为 `k`
- 例如 `2787 -> 2.8k`

禁止展示条件：

- tokenizer 未固定
- 发布态 worktree 无法生成
- `orbit files <id> --json` 失败

### 4. `Startup`

定义：

- `D` = 必经阅读层数
- `R` = 开始执行前必读文件数

推荐口径：

- 不从 prose 自动猜“哪些文件必读”
- 由 metadata 显式声明 `startup.phases`
- `D = phases` 数量
- `R = phases` 中去重后的文件总数

为什么不用 NLP：

- brief 中可能写 `Read X`、`see Y`、`use Z`，但它们的重要性不同
- 没有作者显式声明时，脚本无法可靠区分“真正必读”和“补充说明”

校验要求：

- `startup.phases[*].files` 中的文件必须都存在于发布态
- 这些文件必须属于安装态静态文件集，或能被 orchestration lane 稳定消费

### 5. `写入边界`

定义：

- 固定 7 个通用 surface 中，可写 surface 的数量 / 7

固定 surface taxonomy：

1. `entry_brief`
2. `rules_workflow`
3. `implementation_code`
4. `tests_checks`
5. `evidence_records`
6. `specs_plans`
7. `qa_release_review`

计算方法：

1. agent 逐项判断 7 个 surface 在“正常任务执行路径”中是否可写
2. 每一项都必须给出 evidence
3. 校验脚本验证 evidence 真实存在
4. 统计 `writable=true` 的 surface 数
5. 以 7 为固定分母
5. 套用标签：
   - `窄`：≤ 30%
   - `中`：31%–60%
   - `宽`：> 60%

重要说明：

- 这列是**通用比较指标**
- 它不等于 Orbit 内部 member 数
- 它也不等于整个仓库目录数
- 它只反映 comparison doc set 所描述的“正常执行时写入边界”

### 6. `验证强度`

定义：

- 基于显式验证动作、final validation、cheap probe 的组合强度

推荐做法：

- 由 metadata 列出 `verification.actions`
- 由脚本校验这些动作确实有文件和 marker 支撑

标签规则：

- `强 + probe`
  - 显式验证动作 ≥ 3
  - 包含 `final_validation`
  - 有 cheap probe
- `强`
  - 显式验证动作 ≥ 3
  - 包含 `final_validation` 或等价 regression/final check
- `中`
  - 显式验证动作 1-2
- `弱`
  - 缺少稳定、可执行的验证动作定义

这里的“验证动作”不建议靠全文搜索动词来推断，推荐只承认 metadata 中声明且通过校验的动作。

### 7. `恢复/交接`

定义：

- 基于非成功状态数量和最小交接字段的完整度

推荐做法：

- 由 metadata 显式列出 `recovery.non_success_statuses`
- 由脚本校验记录模板/验证脚本/状态文档是否真的支撑这些状态与字段

标签规则：

- `完整 (N态)`
  - 非成功状态数 ≥ 3
  - 同时存在 `blocked_reason`、`next_step`、`files_touched`、`final_validation` 中的大部分
- `可恢复 (N态)`
  - 有 blocked/failure 区分
  - 且有 `next_step` 或等价 handoff 字段
- `基础 (N态)`
  - 只有 success/fail 或简单记录
- `脆弱`
  - 失败状态不结构化，也缺少交接字段

这里的 `N` 推荐显示非成功状态数，而不是总状态数。

### 8. `最大文件`

定义：

- 与 `Static Load` 使用同一静态文件集和同一 tokenizer
- 取其中 token 最大的单文件

展示规则：

- 四舍五入到百位后显示为 `k`
- 例如 `932 -> 0.9k`

禁止展示条件：

- 与 `Static Load` 相同

## 行准入规则

不是所有“参考仓库”都应该直接进 README 主表。

推荐只允许已经变成 comparison doc set 的对象进入。

对于外部参考仓库，这意味着：

- 可以进主表
- 但前提是已经固定相关文件清单
- 评测时只读这些文件
- 不能让 agent 自己去扩读整仓库

如果一个外部参考仓库虽然被参考了，但还没有：

- `pack.json`
- `files/`
- `mechanical.json`
- `semantic.json`

那它仍然只适合出现在 `Design Lineage`。

## 当前 `tdd` spec 的试跑结果

下面这些值已经可以作为当前 spec 的方法试跑结果，但其中部分仍应在 metadata 落地后再正式公开展示。

### 已机械验证

- 发布态静态文件集：
  - `.harness/orbits/tdd.yaml`
  - `docs/tdd/README.md`
  - `docs/tdd/process/blocked-and-handoff.md`
  - `docs/tdd/process/red-green-refactor.md`
  - `docs/tdd/records/README.md`
  - `docs/tdd/templates/tdd-record.md`
  - `tools/check-tdd-records.sh`
- 发布态总静态 token：
  - `2787` (`o200k_base`)
  - 显示值：`2.8k`
- 最大文件：
  - `.harness/orbits/tdd.yaml`
  - `932` tokens
  - 显示值：`0.9k`
- 写入边界：
  - `7/7`
  - 当前标签：`宽 (7/7)`

### 在 metadata 落地后即可正式公开

- `Use Case`
  - 推荐：`TDD / code change`
- `Startup`
  - 推荐 phases：
    - phase 1: `.harness/orbits/tdd.yaml`
    - phase 2:
      - `docs/tdd/README.md`
      - `docs/tdd/process/red-green-refactor.md`
      - `docs/tdd/process/blocked-and-handoff.md`
  - 预期显示：`D2/R4`
- `验证强度`
  - 当前 authored contract 明确支撑：
    - RED 验证
    - GREEN rerun
    - final validation
    - cheap probe
  - 预期显示：`强 + probe`
- `恢复/交接`
  - 当前 non-success statuses：
    - `failure`
    - `blocked`
    - `abnormal_exit`
    - `external_stop`
  - 且模板中已有 `files touched`、`blocked reason`、`next step`、`final validation`
  - 预期显示：`完整 (4态)`

## 推荐的下一步

1. 确认 token 口径固定为 `o200k_base`
2. 为每个外部参考对象建立 comparison doc set
3. 产出对应的 `mechanical.json` 与 `semantic.json`
4. 再写一个合并脚本，把结果渲染成 Markdown 表格行
5. 最后再改 `README.md` 与 `README.zh-CN.md`

## 当前建议

如果目标是“吸引用户，但不能误导用户”，推荐采用下面这条红线：

- README 主表只展示**已经完成 comparison doc set 评测闭环**的行

这样既能保留外部对比，也能避免在主表里混入临场脑补的结果。
