# Blocked And Handoff

Do not keep spending work cycles when the TDD contract cannot be established.
Leave a useful record instead.

## Status Values

Use one of these status values in the TDD record:

- `success`: RED was valid, GREEN was proven, and final validation ran or was
  explicitly scoped.
- `failure`: RED was valid, but GREEN could not be achieved, or validation proved
  the requested behavior cannot be satisfied as stated.
- `blocked`: required context, dependency, environment, fixture, or approval is
  missing.
- `abnormal_exit`: continuing would be misleading or unsafe because the task is
  outside scope, the test target is not meaningful, or the local state cannot
  support the requested work.
- `external_stop`: the human partner or outer runtime stopped the work.

## When To Stop

Stop and record handoff when:

- no meaningful test target can be identified
- the test runner cannot execute because required dependencies or services are
  unavailable
- the target behavior is unclear or contradictory
- the change would exceed the current orbit scope
- the only available RED signal is unrelated setup noise
- the user asks to pause or redirect

## Handoff Minimum

Record:

- what behavior was being targeted
- what files or areas were inspected
- what command failed or could not run
- why the current state is blocked, failed, abnormal, or externally stopped
- the next action that would unblock a future worker

Prefer concise evidence over raw logs. Include paths, commands, and the key error
line rather than long command output.
