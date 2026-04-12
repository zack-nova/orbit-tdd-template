# Red Green Refactor Process

Use this flow for one behavior at a time.

## 1. Identify The Behavior

State the smallest behavior that must change. If the requirement is unclear,
pause and ask for clarification before writing code.

Good targets are externally observable:

- input validation accepts or rejects a value
- a parser returns a specific structure
- an API returns a documented status and body
- a UI flow reaches a visible outcome
- a state transition produces a defined next state

## 2. Write Or Update The Test

Choose the smallest test layer that proves the behavior. Match the project's
existing test style, naming, setup helpers, and runner.

The test should assert behavior, not implementation details. Use mocks only when
the real dependency would make the test slow, flaky, unsafe, or impractical.

## 3. Verify RED

Run the relevant target and record the command.

Accept RED only when the failure proves the target behavior is missing or wrong.
If the failure is syntax noise, a bad import, missing dependency, or unrelated
setup issue, fix the test setup and rerun until RED is meaningful.

If the test passes immediately, it is not RED for the target behavior. Rewrite the
test, choose a narrower behavior, or record why the behavior is already covered.

## 4. Make GREEN

Change the smallest production surface needed to pass the RED test. Avoid
unrelated refactors, extra features, and broad rewrites.

Run the same relevant target again and record the result. GREEN means the target
that was RED now passes.

## 5. Refactor After GREEN

Only refactor after GREEN. Keep behavior unchanged, then rerun the relevant tests.
If refactor breaks GREEN, fix the refactor or revert the refactor.

## 6. Final Validation

Run the narrow target first. Then run the broader project command when it is
available and reasonably scoped, such as the package test, lint, or CI-equivalent
command used by the repository.

Update the TDD record before leaving the orbit.
