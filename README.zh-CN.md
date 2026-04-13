# orbit-tdd-template

[English README](README.md)

这是一个面向真实代码变更的 Orbit TDD 模板。

当你希望 Agent 处理一个聚焦的功能、修 bug、重构或行为变更，并且严格遵守
TDD 外部合同时，可以使用这个模板：先证明有效 RED，再用最小改动到 GREEN，
只在 GREEN 后重构，如果工作被阻塞，也要留下可交接的证据。

## 为什么用这个 Spec

- 在 TDD 关键点上足够严格：没有有效 RED，就不进入生产代码改动。
- 在日常开发里足够轻：不强推统一覆盖率门槛，也不要求每个任务都写 E2E。
- 卡住时也可恢复：未完成的工作依然会留下结构化交接信息。
- 足够小、足够实用：能装进真实项目，而不是把每次小改动都升级成发布门禁流程。

## 快速使用

在你的 Orbit harness runtime 仓库中执行：

```sh
harness install https://github.com/zack-nova/orbit-tdd-template.git --dry-run
harness install https://github.com/zack-nova/orbit-tdd-template.git
```

然后把一个聚焦的编码任务交给 Agent。安装后的 `tdd` orbit 会引导它：

- 先选择或新增最小相关测试
- 运行目标测试，并确认失败是有效 RED，而不是环境或导入噪音
- 用最小生产代码改动把同一目标推进到 GREEN
- 只在 GREEN 后重构，并保持 GREEN
- 在 `docs/tdd/records/` 中记录 RED/GREEN/REFACTOR 证据

## Spec 画像

下面这张表把当前 `tdd` spec 和精选参考工作流放到同一口径下做了对比。

| Spec | Use Case | Static Load | Startup | 写入边界 | 验证强度 | 恢复/交接 | 最大文件 |
| --- | --- | ---: | ---: | --- | --- | --- | ---: |
| `tdd` | TDD / code change | 2.8k | D2/R4 | 中 (3/7) | 强 + probe | 完整 (4态) | 1.0k |
| `superpowers:tdd` | TDD / code change | 4.0k | D1/R1 | 窄 (2/7) | 强 | 脆弱 (1态) | 2.4k |
| `ecc:tdd` | TDD + coverage | 23.9k | D2/R2 | 中 (3/7) | 强 | 脆弱 (1态) | 16.5k |
| `spec-kit:implement` | Spec-first implementation | 27.6k | D2/R2 | 中 (3/7) | 强 | 可恢复 (3态) | 14.5k |
| `gsd:verify` | Verification / UAT | 27.5k | D1/R1 | 中 (3/7) | 强 | 完整 (4态) | 10.0k |
| `gstack:qa` | QA / fix / ship | 57.2k | D2/R2 | 中 (4/7) | 强 | 完整 (3态) | 32.9k |
| `bmad:testing` | Test generation / QA | 2.1k | D1/R1 | 中 (4/7) | 强 | 脆弱 (1态) | 1.2k |
| `openspec:workflow` | Spec-first change workflow | 16.2k | D2/R2 | 中 (3/7) | 中 | 可恢复 (2态) | 4.8k |
| `omc:entry` | Agent orchestration / TDD | 15.8k | D2/R2 | 中 (4/7) | 强 | 可恢复 (3态) | 11.0k |

- `Static Load`：安装态静态文档集的总 token 数
- `Startup`：`D` = 必经阅读层数，`R` = 开始执行前必读文件数
- `写入边界`：正常任务路径下，7 个通用 surface 中可写的数量
- `验证强度`：基于显式验证动作、final validation 和 cheap probe
- `恢复/交接`：基于结构化非成功状态与交接字段
- `最大文件`：安装态静态文档集中的最大文件

外部参考行基于精选工作流文档集评测，不是对整仓库做泛化扫描。

## 你会得到什么

- 一个用于 test-first 功能、修 bug、重构和行为变更的 `tdd` orbit。
- 一份简洁的 worker brief，让 Agent 快速进入 TDD 循环。
- `docs/tdd/` 下的 TDD 规则与流程文档。
- 一份可复用的 TDD 记录模板，用来保存任务证据。
- `tools/check-tdd-records.sh`，用于快速检查记录是否就绪。

如果你的项目需要不同的写入边界，可以在安装后调整
`.harness/orbits/tdd.yaml` 里的 `tdd` orbit。

## 适合什么场景

- 可以找到明确自动化测试目标的功能、修 bug、重构或行为变更
- 需要显式 regression evidence 的 bug fix
- 团队想要 TDD 纪律，但不想把每个任务都升级成完整 QA 工程

## 不适合什么场景

- 一次性 spike、生成代码或纯配置改动，除非人类伙伴明确批准跳过 TDD
- 完整发布 QA、企业测试治理或合规型验证
- 需求还不清楚，暂时无法转成有意义测试目标的任务

## 设计来源

这个模板吸收了多种强 TDD、验证优先和 spec-first 工作流的经验，最后收口成下面几个原则：

- RED/GREEN/REFACTOR 核心保持严格
- 覆盖率、E2E 扩展和更重的 QA 要求，交给项目规则或升级路径处理
- blocked 工作也必须可观察、可交接
- worker 入口保持简短，让 Agent 更快进入 test-first 循环
