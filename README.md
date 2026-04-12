# orbit-tdd-template

TDD workflow template for Orbit source-branch publishing.

This repository is the source-branch authoring sandbox for the `tdd` Orbit
template. The template exercises a test-first development lane with a narrow
write surface, publishable Orbit metadata, and lightweight RED/GREEN/REFACTOR
evidence.

## Purpose

- Validate the full Orbit source-branch template flow.
- Keep the authoring repo small enough to inspect by hand.
- Capture experience notes while improving the workflow.

## Source Branch Shape

- `.harness/manifest.yaml` marks this branch as `kind: source`.
- `.harness/orbits/tdd.yaml` is the authored OrbitSpec and worker brief truth.
- `docs/tdd/**` and `tools/check-tdd-records.sh` are the exported template
  content.
- `authoring/**`, `references/**`, and root `AGENTS.md` are source-only
  authoring material.
- The published branch is `orbit-template/tdd`, produced with
  `orbit template publish --orbit tdd`.

## Reference Set

Refresh the local reference snapshot with:

```sh
authoring/fetch-reference-docs.sh
```

The snapshot lives under `references/repo-docs-latest/` and is ignored by Git.
It is evidence for authoring, not template payload.

| Repository | Reference files | Takeaway |
| --- | --- | --- |
| `obra/superpowers` | `README.md`, `skills/test-driven-development/SKILL.md` | Strongest strict TDD contract: valid RED before production code, minimal GREEN, then refactor. |
| `affaan-m/everything-claude-code` | `README.md`, `agents/tdd-guide.md`, `skills/tdd-workflow/SKILL.md`, `commands/tdd.md`, `.opencode/prompts/agents/tdd-guide.txt`, `.kiro/agents/tdd-guide.md` | Complete TDD agent/skill/command model with evidence, test layers, and RED/GREEN/REFACTOR flow. |
| `github/spec-kit` | `README.md`, `spec-driven.md`, `templates/commands/implement.md`, `templates/commands/tasks.md`, `templates/commands/constitution.md`, `docs/quickstart.md` | Good model for spec/constitution-driven test-first ordering, while keeping tests conditional on task policy. |
| `gsd-build/get-shit-done` | `README.md`, `get-shit-done/workflows/add-tests.md`, `get-shit-done/workflows/verify-work.md`, `get-shit-done/workflows/verify-phase.md`, `get-shit-done/references/verification-patterns.md` | Strong verification, gap, and blocked-state recording patterns; not a strict default TDD flow. |
| `garrytan/gstack` | `README.md`, `qa/SKILL.md`, `ship/SKILL.md` | Useful regression-test, coverage-audit, and ship-gate language; more QA-heavy than TDD-first. |
| `bmad-code-org/BMAD-METHOD` | `docs/reference/testing.md`, `docs/reference/modules.md` | Useful QA/ATDD/traceability escalation model for larger systems. |
| `Fission-AI/OpenSpec` | `README.md`, `docs/concepts.md`, `docs/workflows.md`, `docs/commands.md`, `docs/getting-started.md` | Useful spec-first discipline when a behavior is not testable or clear enough yet. |
| `Yeachan-Heo/oh-my-claudecode` | `AGENTS.md`, `docs/REFERENCE.md` | Useful keyword/shortcut routing pattern for entering a TDD mode quickly. |

## Development Approach

- Keep the Orbit source truth in `.harness/orbits/tdd.yaml`.
- Keep installed-worker instructions concise in `meta.agents_template`; keep
  deeper authoring rationale in `authoring/**` and this README.
- Preserve the strict core rule: establish a valid RED before changing
  production code, rerun the same target to reach GREEN, then refactor only
  while GREEN stays green.
- Require a small TDD record for evidence, but avoid imposing a universal
  coverage threshold or full unit/integration/E2E stack on every project.
- Use the reference snapshot to compare patterns and then write original,
  Orbit-specific template content. Do not copy long third-party docs into the
  template payload.
