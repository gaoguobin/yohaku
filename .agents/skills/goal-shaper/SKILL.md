---
name: goal-shaper
description: Turn rough or fuzzy user requests into best-practice Codex Goal mode packages through adaptive interview, goal suitability triage, /goal drafting, optional support spec generation, evidence checklist, assumptions, and durable-guidance separation. Use when the user asks to create, shape, draft, refine, or evaluate a Codex /goal prompt, convert a short requirement into Goal mode, prepare a long-running Codex task, or decide whether Goal mode is appropriate; stop after producing the goal package and do not run the goal.
---

# Goal Shaper

## Overview

Shape a user's rough request into an auditable Codex Goal mode package. Produce
the goal package, then stop. Do not run `/goal`, call runtime goal tools, start
implementation, create commits, or modify repository ignore rules.

Do not treat this skill's own instructions or files as the user's target unless
the user explicitly asks about `goal-shaper` itself. If the user asks a small
task such as "explain this function" without attaching a concrete file,
selection, or snippet, classify it as not suitable for Goal mode and provide a
normal prompt that asks for the missing target.

## Load Resources

- Read `references/goal-schema.md` before classifying suitability or drafting a
  goal.
- Read `references/rubric.md` before final output.
- Read `templates/goal-package.md` before producing a compact goal package.
- Read `templates/support-spec.md` before producing or writing a support spec.
- Read `references/examples.md` when classification, interview depth, or output
  shape is uncertain.

## Workflow

1. Restate the request as a candidate outcome in concrete terms.
2. Decide whether Goal mode is appropriate:
   - If the task is too small, recommend a normal prompt and provide it.
   - If the task is too broad, recommend decomposition into smaller goals.
   - If the task has no credible verifier, ask for evidence or recommend a
     planning/research prompt instead.
   - If the request depends on "this" but no target artifact is attached, do
     not infer the skill file as the target; ask for the file/selection/snippet
     in a normal prompt.
3. Extract the canonical fields from the user's request. Use the same field
   model for bugs, performance, research, migration, docs, and operations.
4. Ask only for missing details that would change success, validation, safety,
   or scope. Ask one question at a time. Prefer 2 or 3 choices with short
   tradeoffs when the current surface supports it; otherwise ask one concise
   plain-text question.
   Do not invent exact validation commands. Use exact commands only when they
   are provided by the user, visible in the target project, or already known
   from reliable context; otherwise ask for the verifier or mark the command as
   a confirmation-needed assumption.
5. Classify complexity:
   - `small`: compact `/goal` only.
   - `medium`: compact `/goal` plus evidence checklist.
   - `large`: compact `/goal` plus support spec.
   - `too_broad`: decomposition recommendation instead of a single goal.
6. Draft the output:
   - User-facing explanation should follow the user's language.
   - The `/goal` and support spec should default to English for Codex
     execution stability.
   - Preserve the user's original intent in a short local-language summary when
     useful.
7. Run the rubric self-check. Outcome and verification must score 2. Other
   fields may score 1 only when the assumption is explicit.
8. Present the final package and stop.

## Support Spec Policy

Use a support spec only when the goal is complex, long, high-risk, needs
restartable context, or would approach the 4,000-character `/goal` limit.

Default support spec path:

```text
.goal-shaper/specs/YYYY-MM-DD-<slug>.md
```

Before writing a support spec file, confirm the exact path with the user. Do
not automatically create or edit `.gitignore`; if ignore behavior matters,
state the implication and ask separately.

## Safety Policy

Always separate one-time goal constraints from durable guidance. Put reusable
repo/team rules into a `durable_guidance_candidates` section and suggest
`AGENTS.md`, a skill, config, or team docs as the destination.
Include durable guidance only when it is explicit in the current request or
directly evidenced by the target repo/workspace. Do not carry it forward from
examples, earlier conversation, outer instructions, or installed-skill context.

Treat these as pause or confirmation triggers inside generated goals/specs:

- production environment changes
- credentials, tokens, secrets, cookies, or private data
- network access or external writes
- delete, migrate, overwrite, permission, or ownership changes
- writes outside the workspace
- destructive app, MCP, or shell actions
- git history rewrites or shared-branch impact

## Final Output Rules

- Provide a copyable `/goal` command only when Goal mode is appropriate.
- Keep the `/goal` objective non-empty and under 4,000 characters.
- Include evidence checklist, assumptions, and durable guidance candidates.
- For support specs, provide a preview and ask before writing unless the user
  already explicitly approved writing the file.
- Do not continue into implementation planning after delivering the package.
