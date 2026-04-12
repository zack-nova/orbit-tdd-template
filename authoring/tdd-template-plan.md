# TDD Orbit Template Plan

状态：讨论稿

本文用于设计 `tdd` orbit template 的 source-branch 作者方案。它是 source-only authoring material，不应进入最终 `orbit_template` payload。

## 输入材料

- 本地参考清单：`tdd_related_repos_notes.md`
- 下载原文：`references/repo-docs-latest/`
- Orbit 作者指南：`/Users/zack/Code/Vocation/orbit/docs/orbit_template_authoring_guide.md`
- Orbit 内容指南：`/Users/zack/Code/Vocation/orbit/docs/orbit_template_content_guide.md`
- Orbit 当前代码：`/Users/zack/Code/Vocation/orbit/cmd/orbit/cli/template/*`
- Orbit source 示例：`/Users/zack/Code/Vocation/orbit/docs/examples/issues_orbit_source_branch/`

## Orbit 约束摘要

当前模板应按 v0.4 hosted control plane 设计：

- revision identity 放在 `.harness/manifest.yaml`
- Orbit authored truth 放在 `.harness/orbits/tdd.yaml`
- source branch 用 `kind: source`
- 发布用 `orbit template publish` 产出 `orbit-template/tdd`
- source-only 文件可以保留在 source branch，但不能进入 published payload
- 根 `AGENTS.md` 只能当 brief materialized artifact，不能当 authored truth
- brief 的结构化 truth 是 `.harness/orbits/tdd.yaml -> meta.agents_template`
- publish / save 只消费 `export` surface，不能把 projection 误当 template payload

当前代码里 source manifest parser 实际期待的形状是：

```yaml
schema_version: 1
kind: source
source:
  orbit_id: tdd
  source_branch: main
```

注意：部分旧文档仍出现 `.orbit/source.yaml` 或 `publish_target` 口径；本模板不采用这些旧入口。

## 参考内容对比

| 来源 | 优点 | 不适合直接搬进 Orbit 模板的点 | 建议提炼 |
| --- | --- | --- | --- |
| `obra/superpowers` | TDD 合同最清楚，red/green/refactor、失败原因验证、反例都很强 | 语气过硬，要求删除既有代码的规则不一定适合所有项目；整份 skill 太像 prompt | 采用“先看到有效 RED，再改生产代码”的核心规则；异常情况改成“需人确认” |
| `affaan-m/everything-claude-code` | TDD 步骤完整，覆盖率、测试层级、Git checkpoint 证据很具体 | 80%+ 覆盖、unit/integration/E2E 全量要求偏重；checkpoint commit 规则可能侵入用户 Git 流程 | 采用 RED/GREEN evidence 和可选 checkpoint 概念；覆盖率改成项目约定优先 |
| `github/spec-kit` | 很适合把 TDD 作为 spec / constitution 驱动的可选或强制原则；任务按 user story 独立测试 | 它的主对象是 spec-driven project flow，不是单个 TDD worker orbit | 采用“如果任务/spec要求 TDD，则测试任务必须排在实现任务前”的任务排序思想 |
| `gsd-build/get-shit-done` | 证据、验收、分类和 blocked/gap 记录做得好；特别适合防止“测试存在但不证明目标” | `add-tests` 是 post-implementation 测试补充，不是严格 TDD；流程较重 | 采用文件分类、测试计划确认、blocked/gap 记录，不采用 post-hoc 作为主路径 |
| `garrytan/gstack` | 强测试文化、回归测试、coverage audit、真实 QA 很有价值 | 更像 QA / regression / ship gate，不是默认 test-first | 采用“bug fix 必须有 regression evidence”和“测试框架发现”启发 |
| `bmad-code-org/BMAD-METHOD` | 测试治理、ATDD、traceability、release gate 维度完整 | 企业测试策略太大，不适合塞进一个轻量 orbit | 只保留“复杂/合规场景升级到测试策略或 harness 级问题”的提示 |
| `Fission-AI/OpenSpec` | spec-first、轻量 artifact flow、verify-before-archive 思路好 | 不是 TDD，中心是 spec/change 管理 | 采用“不清楚需求先澄清/写可测试意图，不急着写代码”的前置判断 |
| `Yeachan-Heo/oh-my-claudecode` | keyword/shortcut 模式说明了 TDD 入口如何被触发 | 更像宿主调度和多 agent 路由，不是模板合同 | 可借鉴 brief 入口要短，`tdd` 应快速进入 test-first 模式 |

## 推荐模板定位

模板名：`tdd`

目标：让 worker 在一个代码变更中遵守 test-first 外部合同，并留下可消费的 RED/GREEN/REFACTOR evidence。

不负责：

- 全项目 QA 或 release gate
- 企业级测试策略 / traceability
- 替代 spec authoring 工具
- 规定 agent 内部思维
- 强制所有项目达到同一个覆盖率数字
- 自动选择或安装测试框架，除非用户明确要求

## Authored Contract 草案

### Objective

对一个 feature、bug fix、refactor 或 behavior change，先写或调整一个能证明目标的测试，确认它因正确原因进入 RED，再写最小生产代码使它进入 GREEN，最后只在 GREEN 后做 refactor。

### Scope Boundary

建议默认让模板覆盖常见代码和测试路径，但把它作为可调整起点：

- code subject: `src/**`, `app/**`, `lib/**`, `cmd/**`, `internal/**`, `pkg/**`
- test subject: `test/**`, `tests/**`, `spec/**`, `__tests__/**`, `e2e/**`
- TDD records: `docs/tdd/records/**`
- template rules/process/templates: `docs/tdd/**`, `tools/check-tdd-records.sh`

需要注意：Orbit 当前模板变量只对 Markdown `$var` 生效，不适合直接把路径 patterns 做成 install-time variables。因此 generic path scope 只能选择“常见默认 + 安装后可改”，而不是完全变量化。

### Rules

- RED 必须被执行或至少被编译触发，不能只写测试不运行。
- RED 必须由目标行为缺失、业务 bug 或未实现逻辑导致；语法错、导入错、依赖缺失不能算有效 RED。
- GREEN 必须 rerun 同一个相关测试目标，并证明先前 RED 已经通过。
- refactor 只能在 GREEN 后进行；refactor 后必须保持 GREEN。
- bug fix 必须留下 regression evidence。
- 如果无法建立测试、测试环境不可用、需求不可测试、或需要先探索，应记录 abnormal exit / handoff，而不是伪造 GREEN。

### Done Probe

Cheap probe 不应跑全量质量系统。建议只检查 TDD record 是否存在且至少包含：

- task/objective
- touched files
- RED command and result
- GREEN command and result
- final validation command
- status: `success`, `failure`, `blocked`, or `abnormal_exit`

### Failure / Abnormal Exit

Failure:

- RED 能证明需求当前不满足，但无法实现 GREEN
- GREEN 后相关验证仍失败
- 测试证明需求本身与现有系统冲突

Abnormal exit:

- 无法运行测试环境
- 没有可定位的测试入口
- 需求不可测试或验收标准不清
- 需要改动超出当前 orbit scope
- 用户中断或要求暂停

### Record Target

推荐使用：

- record template: `docs/tdd/templates/tdd-record.md`
- runtime records: `docs/tdd/records/<YYYYMMDD>-<slug>.md`
- rule/process: `docs/tdd/README.md` and `docs/tdd/process/*.md`

Record minimum:

- Objective
- Scope / files touched
- RED evidence: command, expected failure reason, actual result
- GREEN evidence: command, actual pass result
- Refactor evidence if any
- Final validation
- Gaps / blocked reason / next step

## Proposed Source-Branch Layout

```text
.harness/
  manifest.yaml
  orbits/
    tdd.yaml

docs/
  tdd/
    README.md
    process/
      red-green-refactor.md
      blocked-and-handoff.md
    templates/
      tdd-record.md
    records/
      README.md

tools/
  check-tdd-records.sh

authoring/
  publish-checklist.md
  tdd-template-plan.md

references/
  repo-docs-latest/

tdd_related_repos_notes.md
```

Published `orbit_template` payload should include:

- `.harness/orbits/tdd.yaml`
- `docs/tdd/README.md`
- `docs/tdd/process/**` if we decide process is stable enough to export
- `docs/tdd/templates/tdd-record.md`
- `docs/tdd/records/README.md` if we want an empty record directory contract
- `tools/check-tdd-records.sh`

Published payload should exclude:

- `authoring/**`
- `references/**`
- `tdd_related_repos_notes.md`
- root `AGENTS.md`
- runtime records under `docs/tdd/records/*.md`

## Proposed OrbitSpec Shape

Key modeling choice: because this orbit must commit code/test/record changes, `subject` needs write access. The default role mapping would make subject visible but not writable, so this template should set `write_roles: [meta, subject, rule]` or use explicit member `scopes.write: true`.

Initial member plan:

- `tdd-code-surface`: role `subject`, common code paths, write true, export false
- `tdd-test-surface`: role `subject`, common test paths, write true, export false
- `tdd-records`: role `subject`, `docs/tdd/records/**`, write true, export false except README if we split it
- `tdd-record-template`: role `subject`, `docs/tdd/templates/tdd-record.md`, write true, export true
- `tdd-rules`: role `rule`, `docs/tdd/README.md` and `tools/check-tdd-records.sh`, export true
- `tdd-process`: role `process`, `docs/tdd/process/**`, export decision pending

## Key Decisions To Discuss

1. Strictness:
   - Recommended default: strict RED before production code, with explicit human-approved exceptions.
   - Alternative: softer “test-first preferred” mode for legacy / exploratory code.

2. Scope:
   - Recommended default: generic common code/test paths plus install-time manual adjustment.
   - Alternative: make this template rules-only and require the runtime author to add code/test subject paths before use.

3. Records:
   - Recommended default: require a lightweight TDD record for every completed TDD orbit task.
   - Alternative: record only when blocked/failure/abnormal exit occurs.

4. Process export:
   - Recommended default: export stable process docs because installed workers need the workflow.
   - Alternative: keep process docs orchestration-only and export just the rules plus record template.

5. Coverage:
   - Recommended default: use project coverage policy if present; otherwise require meaningful targeted tests, not a global 80% threshold.
   - Alternative: adopt a default coverage threshold, likely 80%, for stronger guardrails.

6. Git checkpoint evidence:
   - Recommended default: record commands/results, but do not require stage commits.
   - Alternative: require `test:` RED and `fix:` GREEN commits when the repo is under Git.

7. E2E:
   - Recommended default: include E2E only for critical user-visible flows or when task scope demands it.
   - Alternative: require unit + integration + E2E for every feature, which is heavier and may overfit web apps.

