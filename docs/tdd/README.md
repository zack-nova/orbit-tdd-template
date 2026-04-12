# TDD Orbit

This orbit keeps one code change test-first and observable. It is for features,
bug fixes, refactors, and behavior changes where tests can provide meaningful
evidence.

It is not a release gate, whole-project QA process, enterprise test strategy,
or spec authoring framework. Use the project rules first when they are stricter
or more specific.

## Core Rule

Do not change production code until there is a valid RED signal for the target
behavior.

A valid RED signal means:

- the relevant test target runs or reaches the intended compile-time check
- the new or changed test exercises the target behavior
- the failure is caused by the missing behavior, bug, or contract mismatch
- the failure is not only syntax noise, missing dependencies, bad imports, or
  unrelated broken setup

After RED, make the smallest production change that turns that same target GREEN.
Refactor only after GREEN, and keep the target GREEN after refactor.

## Test Choice

Prefer the cheapest test that proves the behavior:

- unit tests for pure logic, transforms, validators, parsers, utilities, and
  state machines
- integration tests for service boundaries, API behavior, persistence, and
  cross-module contracts
- E2E tests for critical user-visible flows where unit or integration evidence
  would not prove the outcome

Do not require E2E for every change. Do not invent a global coverage threshold
unless the project already has one. If the project has a coverage policy, follow
it and record the command used to check it.

## Bug Fixes

Every bug fix needs regression evidence. Reproduce the bug with a failing test or
a compile-time RED signal, then implement the fix and rerun the same target to
prove GREEN.

## Exceptions

Ask the human partner before skipping TDD for:

- throwaway prototypes
- generated code
- configuration-only changes
- changes where no meaningful automated test target exists
- exploratory spikes that should be discarded before production work begins

If an exception is approved, record the reason and the alternate validation path.

## Evidence Record

Write one record per TDD task in `docs/tdd/records/`, based on
`docs/tdd/templates/tdd-record.md`.

The minimum record is:

- status
- objective
- files touched
- RED command and result
- GREEN command and result
- final validation command and result
- refactor evidence when refactor happened
- gaps, blocked reason, or next handoff step when work cannot complete

The cheap probe `tools/check-tdd-records.sh` only checks record shape. It is not a
replacement for the project test suite.
