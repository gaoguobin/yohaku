# Goal Quality Rubric

Run this self-check before final output.

## Scoring

Score each core field:

- `0`: missing
- `1`: present but vague or assumed
- `2`: concrete and auditable

Pass criteria:

- `outcome` must score 2.
- `verification_surface` must score 2.
- Other required fields may score 1 only when the assumption is explicit.
- The `/goal` objective must be non-empty and under 4,000 characters.
- Support spec must be used only when complexity justifies it.

## Field Checks

- Outcome: names the concrete end state, not an activity.
- Verification: names a check, artifact, benchmark, report, source evidence, or
  manual review that can decide completion.
- Verification commands: exact commands must be user-provided, discovered in
  the target project, or already known from reliable context. Do not invent
  paths such as virtualenv locations, npm scripts, make targets, or benchmark
  commands.
- Constraints: says what must not regress or change.
- Boundaries: says what Codex may and may not use or modify.
- Iteration: says how to choose the next attempt after each result.
- Blocked stop: says when to stop and what to report.
- Initial materials: names what to read first, or explicitly says none known.
- Validation and review: names the smallest relevant verification and review
  surface.
- Checkpoint: asks for compact progress logs only, not verbose per-step
  preambles.
- Pause triggers: covers high-risk actions.
- Durable guidance: separates reusable repo/team rules from this one goal, and
  includes only rules traceable to the current request or target evidence.

## Anti-Patterns

Reject or repair these before final output:

- "Make it better."
- "Improve performance" with no metric or benchmark.
- Performance goals that invent a benchmark command, test command, target
  threshold, or tool path without labeling it as an assumption or asking for
  confirmation.
- "Refactor this" with no expected behavior, tests, or boundaries.
- "Keep investigating" with no decision or evidence standard.
- Several unrelated backlog items in one goal.
- A goal that hides uncertainty instead of naming unavailable evidence.
- A support spec for a tiny one-off task.
- Requiring long upfront plans or verbose status in every continuation turn.

## Repair Strategy

- If outcome is vague, ask which user-visible or artifact state should be true.
- If verification is missing, ask which test, command, artifact, or review
  should decide success.
- If performance verification is missing, ask for the metric and measurement
  method, or propose 2 or 3 verifier options and ask the user to pick one.
- If scope is too broad, propose 2 or 3 smaller goal candidates.
- If risk is high, ask for environment, forbidden actions, rollback, or pause
  triggers before producing a runnable goal.
- If a detail is low impact, record it as an assumption instead of asking.

## Final Consistency Check

Before responding, verify:

- The user-language summary and English `/goal` describe the same objective.
- The evidence checklist matches the verifier in the `/goal`.
- Assumptions are not hidden inside success criteria.
- Durable guidance candidates are not necessary for this single goal to make
  sense, and are not inherited from prior examples or surrounding instructions.
- The final response stops after the package or after asking for support spec
  file confirmation.
