# Goal Schema

Use this schema for every task type. Avoid domain-specific special cases unless
they are verifier suggestions.

## Contents

- Suitability
- Canonical Fields
- Interview Priority
- Complexity Levels
- Safety Pause Triggers
- Goal Patterns

## Suitability

Recommend Goal mode when the request has:

- a durable objective
- an evidence-based finish line
- an uncertain multi-step path
- a scope bigger than one prompt but smaller than an open-ended backlog

Recommend a normal prompt when the request is:

- a one-line edit
- a simple explanation
- a short review
- a narrow command lookup
- missing any credible evidence source

Recommend decomposition when the request is a loose backlog, spans unrelated
systems, or would need several independent completion contracts.

## Canonical Fields

Required fields:

- `outcome`: Concrete state that must be true when done.
- `verification_surface`: Tests, commands, benchmark output, generated artifact,
  logs, report, source evidence, or manual check that proves success.
- `constraints`: What must not regress or be changed.
- `boundaries`: Files, folders, repos, systems, environments, tools, data, or
  resources that are in or out of scope.
- `iteration_policy`: How Codex should choose the next attempt after each
  result.
- `blocked_stop_condition`: When Codex should stop and report rather than keep
  trying.
- `initial_materials`: Files, docs, issues, logs, plans, traces, screenshots, or
  references Codex should read first.
- `validation_and_review`: Minimal relevant checks and final review surface.
- `checkpoint_policy`: Short progress log or checkpoint expectation.
- `pause_triggers`: Actions that require stopping or asking for confirmation.

Supporting fields:

- `domain`
- `target_environment`
- `repos_or_files`
- `allowed_tools`
- `forbidden_actions`
- `risk_level`
- `final_artifact`
- `uncertainty_policy`
- `budget_or_time_limit`
- `durable_guidance_candidates`
- `support_spec_required`
- `complexity_level`

## Interview Priority

Ask only when the missing answer changes success, validation, safety, or scope.

1. Verification surface.
2. Success threshold.
3. Scope boundary or target environment.
4. Safety constraint or forbidden action.
5. Blocked stop condition.
6. Initial materials and checkpoint policy.

If the user cannot supply a metric, propose the most honest binary validator
available and ask for confirmation.

## Complexity Levels

`small`: compact `/goal`.

- Clear outcome and verifier.
- Little or no durable context.
- Low safety risk.

`medium`: compact `/goal` plus evidence checklist.

- Several steps or files.
- Verifier and constraints still fit in one goal.

`large`: compact `/goal` plus support spec.

- Long context or many materials.
- Needs milestones, decision log, recovery notes, or safety policy.
- Would approach the 4,000-character goal limit.

`too_broad`: decomposition recommendation.

- Multiple unrelated objectives.
- No single verifier.
- Several independent systems or backlogs.

## Safety Pause Triggers

Include pause triggers when relevant:

- production changes
- credentials or private data
- network access or external writes
- delete, migrate, overwrite, permissions, or ownership changes
- writes outside workspace
- destructive app, MCP, or shell operations
- git history rewrite or shared-branch impact

## Goal Patterns

Compact goal:

```text
/goal <outcome>, verified by <evidence>, while preserving <constraints>. Use <boundaries>. Between iterations, <iteration policy>. If blocked, stop and report <attempted paths, evidence gathered, blocker, and next input needed>.
```

Goal with support spec:

```text
/goal Complete <outcome> according to <support spec path>, verified by <evidence summary>, while preserving <constraints summary>. If blocked, stop with attempted paths, evidence gathered, blocker, and next input needed.
```
