# orbit-tdd-template

[中文 README](README.zh-CN.md)

Strict TDD for real code changes in Orbit.

Use this template when you want an agent to handle one focused feature, bug fix,
refactor, or behavior change with a clear contract: prove a valid RED first,
make the smallest GREEN change, refactor only after GREEN, and leave useful
evidence if the work gets blocked.

## Why This Spec

- Strict where TDD matters: no production change before a meaningful RED.
- Lightweight in daily work: no forced global coverage target and no mandatory
  E2E for every task.
- Recoverable when blocked: incomplete work still leaves structured handoff
  evidence.
- Small enough to install into real projects without turning each change into a
  release-gate workflow.

## Quick Start

In an Orbit harness runtime repository:

```sh
harness install https://github.com/zack-nova/orbit-tdd-template.git --dry-run
harness install https://github.com/zack-nova/orbit-tdd-template.git
```

Then give the agent one focused coding task. The installed `tdd` orbit guides it
to:

- choose or add the smallest relevant test first
- run the target and confirm the failure is a real RED, not setup noise
- make the minimum production change that turns the same target GREEN
- keep GREEN through any refactor
- record RED/GREEN/REFACTOR evidence under `docs/tdd/records/`

## Spec Snapshot

This table compares the installed `tdd` spec with curated reference workflows.

| Spec | Use Case | Static Load | Startup | Write Boundary | Validation | Recovery/Handoff | Max File |
| --- | --- | ---: | ---: | --- | --- | --- | ---: |
| `tdd` | TDD / code change | 2.8k | D2/R4 | Medium (3/7) | Strong + probe | Complete (4 states) | 1.0k |
| `superpowers:tdd` | TDD / code change | 4.0k | D1/R1 | Narrow (2/7) | Strong | Fragile (1 state) | 2.4k |
| `ecc:tdd` | TDD + coverage | 23.9k | D2/R2 | Medium (3/7) | Strong | Fragile (1 state) | 16.5k |
| `spec-kit:implement` | Spec-first implementation | 27.6k | D2/R2 | Medium (3/7) | Strong | Recoverable (3 states) | 14.5k |
| `gsd:verify` | Verification / UAT | 27.5k | D1/R1 | Medium (3/7) | Strong | Complete (4 states) | 10.0k |
| `gstack:qa` | QA / fix / ship | 57.2k | D2/R2 | Medium (4/7) | Strong | Complete (3 states) | 32.9k |
| `bmad:testing` | Test generation / QA | 2.1k | D1/R1 | Medium (4/7) | Strong | Fragile (1 state) | 1.2k |
| `openspec:workflow` | Spec-first change workflow | 16.2k | D2/R2 | Medium (3/7) | Medium | Recoverable (2 states) | 4.8k |
| `omc:entry` | Agent orchestration / TDD | 15.8k | D2/R2 | Medium (4/7) | Strong | Recoverable (3 states) | 11.0k |

- `Static Load`: total tokens in the install-time static doc set
- `Startup`: `D` = required reading depth, `R` = required files before work starts
- `Write Boundary`: writable surfaces / 7 normalized surfaces in the normal task path
- `Validation`: based on explicit checks, final validation, and cheap probe presence
- `Recovery/Handoff`: based on structured non-success states and handoff fields
- `Max File`: largest file in the install-time static doc set

Reference rows are measured from curated workflow document sets, not from whole
repositories.

## What You Get

- A `tdd` orbit for test-first feature, bug fix, refactor, and behavior-change
  work.
- A concise worker brief that gets the agent into the TDD loop quickly.
- TDD rule and process docs under `docs/tdd/`.
- A reusable TDD record template for task evidence.
- A cheap record-readiness probe at `tools/check-tdd-records.sh`.

If your project needs a different write boundary, adjust the installed `tdd`
orbit in `.harness/orbits/tdd.yaml` after installation.

## When To Use It

- feature, bug-fix, refactor, or behavior-change work with a meaningful
  automated test target
- bug fixes that need explicit regression evidence
- teams that want TDD discipline without promoting every task into a full QA
  program

## When Not To Use It

- throwaway spikes, generated code, or configuration-only work unless the human
  partner approves skipping TDD
- full release QA, enterprise testing strategy, or compliance-heavy validation
- unclear requests where the behavior cannot yet be turned into a meaningful
  test target

## Design Lineage

This template was shaped by several strong TDD, verification-first, and
spec-first workflows. The distilled result is simple:

- keep the RED/GREEN/REFACTOR core strict
- treat broader QA, coverage policy, and E2E expansion as project-specific or
  escalation paths
- make blocked work observable instead of silently abandoned
- keep the worker entry short so the agent reaches the test-first loop quickly
