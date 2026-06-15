# Examples

Use these as patterns, not as fixed templates.

## Contents

- Too Small
- Too Broad
- Bug Fix
- Performance
- Research
- High Risk
- Long Context
- Durable Guidance

## Too Small

User request:

```text
Explain what this function does.
```

Response direction:

- Do not generate `/goal`.
- Do not explain the `goal-shaper` skill itself unless the user explicitly
  names it as the target.
- If no concrete function, file, selection, or snippet is attached, recommend a
  normal prompt that asks for the missing target:

```text
Explain what this function does. I will provide the file path, selected code, or snippet; cover what it does, where it is called, and any side effects or edge cases worth knowing.
```

## Too Broad

User request:

```text
Modernize the whole platform and improve all tests, docs, UI, and deployment.
```

Response direction:

- Do not generate one giant goal.
- Propose decomposition:
  - test stabilization goal
  - UI migration goal
  - deployment reliability goal
  - docs refresh goal

## Bug Fix

Strong goal shape:

```text
/goal Reproduce and fix the failing checkout retry behavior on the current branch, verified by a failing-then-passing targeted checkout retry test and the existing checkout test command, while preserving public API behavior. Use only checkout service files, related tests, and local logs. Between iterations, record the observed failure, the smallest code change tried, and the test result. If the failure cannot be reproduced or no safe fix remains, stop with attempted paths, evidence gathered, blocker, and next input needed.
```

## Performance

If the target page or metric is unknown, ask before drafting a runnable goal.
If the target is known but no benchmark command is known, propose verifier
options instead of inventing commands.

Strong goal shape:

```text
/goal Reduce checkout API p95 latency below 250 ms on the documented local benchmark across 3 consecutive runs, verified by <known benchmark command or user-confirmed measurement method> and <known relevant test command>, while preserving response schema and error behavior. Use only checkout service code, benchmark fixtures, and related tests. Between iterations, inspect the current bottleneck, make the smallest targeted change, rerun the same benchmark and tests, and record results. If the benchmark cannot run, the test command is unknown, or further improvement needs product guidance, stop with evidence and next input needed.
```

## Research

Strong goal shape:

```text
/goal Produce an evidence-backed audit of <topic>, verified by a final report that separates confirmed findings, approximate support, blocked claims, and remaining uncertainty, while preserving source attribution and avoiding overclaims. Use the listed primary sources first, then reputable secondary sources only when needed. Between iterations, map claims to evidence and label confidence. If key sources are unavailable, stop with the claim inventory, missing sources, and next input needed.
```

## High Risk

If a request involves production, credentials, destructive changes, external
writes, or workspace-external paths, ask for the missing safety boundary before
producing a runnable `/goal`.

Useful question:

```text
Which environment should this goal target: local only, staging with confirmation before writes, or production read-only audit?
```

## Long Context

Use a support spec when a goal needs many materials, milestones, recovery notes,
or safety rules.

Short goal:

```text
/goal Complete the migration described in .goal-shaper/specs/<date>-migration.md, verified by the acceptance checks in that spec, while preserving documented rollback behavior. If blocked, stop with attempted paths, evidence gathered, blocker, and next input needed.
```

## Durable Guidance

User says:

```text
Always use this repository's package manager and never add dependencies without asking.
```

Response direction:

- Do not hide this only inside the goal.
- Add it to `durable_guidance_candidates`:
  - Candidate destination: `AGENTS.md`
  - Suggested rule: "Use the repository's package manager for package commands.
    Ask before adding new production dependencies."
