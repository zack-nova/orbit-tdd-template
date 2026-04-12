# orbit-tdd-template

[English README](README.md)

这是一个面向实际编码任务的 Orbit TDD 模板。

当你希望 Agent 在做功能、修 bug、重构或行为变更时遵守清晰的 TDD 外部合同时，
可以安装这个模板：先建立有效 RED，再用最小实现到 GREEN，只在 GREEN 后重构，
并留下轻量的 RED/GREEN/REFACTOR 证据。

## 快速使用

在你的 Orbit harness runtime 仓库中执行：

```sh
harness install https://github.com/zack-nova/orbit-tdd-template.git --ref orbit-template/tdd --dry-run
harness install https://github.com/zack-nova/orbit-tdd-template.git --ref orbit-template/tdd
orbit enter tdd
```

然后把一个聚焦的编码任务交给 Agent。安装后的 `tdd` orbit 会引导它：

- 先选择或新增最小相关测试
- 运行目标测试，并确认失败是有效 RED，而不是环境或导入噪音
- 用最小生产代码改动把同一目标推进到 GREEN
- 只在 GREEN 后重构，并保持 GREEN
- 在 `docs/tdd/records/` 中记录 RED/GREEN/REFACTOR 证据

## 你会得到什么

- 一个用于 test-first 功能、修 bug、重构和行为变更的 `tdd` orbit。
- 一份简洁的 worker brief，让 Agent 直接进入 TDD 工作合同。
- `docs/tdd/` 下的 TDD 规则和流程说明。
- 一份可复用的 TDD 记录模板，用来记录任务证据。
- `tools/check-tdd-records.sh`，用于快速检查记录是否就绪。
- 默认覆盖常见代码和测试目录，例如 `src/**`、`app/**`、`pkg/**`、
  `tests/**`、`spec/**`、`e2e/**`。

如果你的项目使用不同的源码或测试目录，安装后调整 `.harness/orbits/tdd.yaml`
即可。

## 这份模板参考了哪些经验

这个模板调研并吸收了多种 TDD、test-first、验证优先和 spec-first 的 Agent
工作流。GitHub star 数检查于 2026-04-12。

| 仓库 | Stars | 参考了什么 |
| --- | ---: | --- |
| [obra/superpowers](https://github.com/obra/superpowers) | 147,851 | 严格 TDD 核心最清楚：有效 RED 在前、最小 GREEN、然后重构。本模板保留这个硬内核，同时把 blocked 情况处理得更适合交接。 |
| [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) | 152,062 | TDD agent/workflow 结构完整，强调证据和测试层级。本模板吸收证据记录意识，但不强制统一覆盖率数字。 |
| [github/spec-kit](https://github.com/github/spec-kit) | 87,242 | 很适合参考由项目原则和 spec 清晰度驱动的 test-first 顺序。本模板保留项目自身测试纪律的空间。 |
| [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done) | 51,071 | 验证、gap、blocked/handoff 记录做得好。本模板借鉴了失败或不确定时也能留下可交接证据的做法。 |
| [garrytan/gstack](https://github.com/garrytan/gstack) | 70,314 | 回归测试和覆盖率审计意识强。本模板把 bug fix 与 regression evidence 绑定起来。 |
| [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | 44,347 | QA、ATDD、traceability 视角完整。本模板把它们作为复杂场景的升级方向，而不是每个小任务的默认负担。 |
| [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) | 39,231 | spec-first 纪律适合处理需求不清或不可测试的情况。本模板要求 Agent 在无法建立有效测试目标时先停下并澄清。 |
| [Yeachan-Heo/oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) | 27,919 | keyword/shortcut 进入 TDD 模式的思路很轻。本模板也保持 worker 入口简短，让 Agent 快速进入 test-first 循环。 |

最终目标是：在 TDD 该严格的地方保持严格，同时足够轻量，能被安装进真实项目，
而不是把每次小改动都变成完整 QA 工程。
