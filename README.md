# orbit-tdd-template

[中文 README](README.zh-CN.md)

An Orbit template for practical test-driven coding work.

Use it when you want an agent to make a feature, bug fix, refactor, or behavior
change with a clear TDD contract: create a valid RED first, make the smallest
GREEN change, refactor only after GREEN, and leave lightweight evidence for the
cycle.

## Quick Start

In an Orbit harness runtime repository:

```sh
harness install https://github.com/zack-nova/orbit-tdd-template.git --dry-run
harness install https://github.com/zack-nova/orbit-tdd-template.git
orbit enter tdd
```

Then give the agent one focused coding task. The installed orbit guides it to:

- choose or add the smallest relevant test first
- run the target and confirm the failure is a real RED, not setup noise
- make the minimal production change to reach GREEN
- keep GREEN during any refactor
- record RED/GREEN/REFACTOR evidence under `docs/tdd/records/`

## What You Get

- A `tdd` orbit for test-first feature, bug fix, refactor, and behavior-change
  work.
- A concise worker brief that points the agent to the TDD contract.
- TDD rule and process docs under `docs/tdd/`.
- A reusable TDD record template for task evidence.
- A cheap record-readiness probe at `tools/check-tdd-records.sh`.

If your project needs a narrower or broader write surface, adjust the installed
`tdd` orbit in `.harness/orbits/tdd.yaml` after installation.

## Research Behind This Template

This template was shaped by comparing several strong TDD, test-first,
verification, and spec-first agent workflows. GitHub stars were checked on
2026-04-12.

| Repository | Stars | What it contributed |
| --- | ---: | --- |
| [superpowers](https://github.com/obra/superpowers) | 147,851 | A strict TDD core: valid RED before production code, minimal GREEN, then refactor. This template keeps that core while using a calmer handoff style for blocked cases. |
| [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) | 152,062 | A complete TDD agent/workflow shape with evidence and test-layer awareness. This template borrows the evidence mindset without forcing a universal coverage number. |
| [github/spec-kit](https://github.com/github/spec-kit) | 87,242 | A useful model for test-first work driven by project policy and spec clarity. This template keeps room for project-specific testing discipline. |
| [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done) | 51,071 | Strong verification and handoff habits. This template adopts explicit blocked/gap recording so failed or uncertain TDD cycles remain useful. |
| [garrytan/gstack](https://github.com/garrytan/gstack) | 70,314 | Regression-test and coverage-audit instincts. This template reflects that by making bug fixes prove the regression path. |
| [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | 44,347 | Broader QA, ATDD, and traceability framing. This template treats those as escalation paths rather than requirements for every small task. |
| [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) | 39,231 | Spec-first discipline for unclear behavior. This template tells agents to stop and clarify when a valid test target cannot be established. |
| [Yeachan-Heo/oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) | 27,919 | A compact TDD entry-mode idea. This template keeps the installed worker entry short so the agent can get to the test-first loop quickly. |

The result is intentionally focused: strict where TDD needs to be strict, but
lightweight enough to install into real projects without turning every change
into a full QA program.
