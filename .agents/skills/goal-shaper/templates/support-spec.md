# Support Spec Template

Use this template only for `large` requests or when a short `/goal` should point
to a durable support file.

Default path:

```text
.goal-shaper/specs/YYYY-MM-DD-<slug>.md
```

Ask for confirmation before writing the file.

## Goal Package Response Shape

Use the user's language for headings and explanations. Keep the `/goal` and
support spec content in English unless the user explicitly asks otherwise.

````markdown
**Conclusion**
This request fits Goal mode, but needs a support spec for long context and
recovery information.

**Suggested Path**
`.goal-shaper/specs/<date>-<slug>.md`

**Runnable Goal**
```text
/goal Complete <outcome> according to .goal-shaper/specs/<date>-<slug>.md, verified by <evidence summary>, while preserving <constraints summary>. If blocked, stop with attempted paths, evidence gathered, blocker, and next input needed.
```

**Support Spec Preview**
<Show the spec content or a concise preview, depending on length.>

Ask in the user's language whether to write the support spec at the suggested
path.
````

## Support Spec File Shape

```markdown
# <Title>

Date: <YYYY-MM-DD>
Status: draft for Codex Goal mode

## Context

<What Codex needs to know before starting.>

## Objective

<Concrete desired end state.>

## Initial Materials

- <Files, docs, issues, logs, screenshots, plans, or sources to read first>

## Acceptance Checks

- <Tests, commands, artifacts, benchmark targets, reports, or review criteria>

## Boundaries

- In scope: <allowed files, systems, tools, data, environments>
- Out of scope: <forbidden or deferred areas>

## Constraints

- <What must not regress or change>

## Milestones And Checkpoints

- <Milestone or checkpoint>
- Keep progress logs compact: current checkpoint, evidence checked, remaining
  work, blocked status.

## Iteration Policy

<How Codex should choose the next best action after each result.>

## Safety And Permission Policy

- Pause before: <network, production, credentials, deletion, external writes,
  workspace-external writes, destructive tools, git history rewrite, etc.>

## Blocker Policy

Stop and report when <blocked condition>. Include attempted paths, evidence
gathered, blocker, and next input needed.

## Decision Log

- <Initial decision and rationale>

## Recovery Notes

<What a later thread should know to resume from this spec alone.>

## Final Report Format

- Summary
- Evidence checked
- Changes or artifacts produced
- Remaining uncertainty
- Follow-up needed
```
