---
name: seed
description: "Use before implementation to brainstorm, clarify requirements, compare approaches, shape rough ideas into reviewed specs, PRDs, design docs, decision artifacts, or optional Writing Plans for complex implementation handoff; trigger on think through, requirements analysis, solution design, write a spec, draft a PRD, before coding, no code yet, and Chinese prompts like 头脑风暴、讨论、聊聊、梳理想法、需求澄清/分析、方案设计/对比、技术方案、产品方案、写spec/PRD、先不实现、先别写代码; stop after the reviewed artifact and do not code."
---

# Seed Ideas Into Reviewed Artifacts

Turn rough ideas into reviewed specs, decisions, or compact handoff plans before
implementation. Seed owns the spec or decision artifact. Goal Shaper owns the
later `/goal` package.

<HARD-GATE>
Do NOT invoke implementation skills, write implementation code, scaffold a
project, call Goal Shaper, run `/goal`, or start implementation execution or
automatic handoff. Stop after the reviewed artifact.
</HARD-GATE>

A Writing Plan is a handoff artifact, not an execution mode. It is approved
context for a future handoff, not approval to begin that handoff automatically.
Do not produce a Writing Plan before the spec or decision is coherent and the
user wants an implementation handoff.

## Artifact Triage

Choose the smallest artifact that makes the next decision reliable:

- **Decision note**: when the user needs to choose between directions.
- **Lightweight spec**: when the idea is simple but still needs scope and
  success criteria.
- **Full spec / PRD / design doc**: when the work affects product behavior,
  architecture, users, data, integrations, or multiple files/modules.
- **Writing Plan**: optional after the spec is understood, only for complex,
  risky, cross-module, migration, performance, or operations work that needs a
  handoff to implementation or Goal Shaper.

If the request is too broad for one artifact, decompose it and shape only the
first coherent sub-project. If it is a tiny explanation or one-answer question,
do not force a spec; answer normally and say Seed is not needed.

## Checklist

Create and complete task items in this order:

1. **Explore context**: inspect available project files, docs, and constraints.
2. **Triage artifact and scope**: choose decision note, lightweight spec, full
   spec, or optional Writing Plan.
3. **Offer Visual Companion if useful**: only when visual comparison would help;
   use a separate message. See `visual-companion.md`.
4. **Ask clarifying questions**: one at a time; prefer multiple choice when it
   lowers friction.
5. **Compare 2-3 approaches**: lead with the recommended path and trade-offs.
6. **Present the artifact draft**: section by section when non-trivial, scaled
   to complexity.
7. **Self-review**: fix placeholders, contradictions, ambiguity, scope creep,
   and unjustified complexity.
8. **User review gate**: ask the user to review; revise if requested.
9. **Deliver final artifact and STOP**: report the artifact path or final inline
   artifact. Do not continue into implementation or Goal Shaper.

## Interview Rules

- Ask only one question per message.
- Ask questions that change scope, success criteria, constraints, user value,
  architecture, validation, risk, or handoff quality.
- Avoid asking for details already clear from context.
- For existing codebases, inspect current structure before proposing changes and
  follow local patterns.
- Do not propose unrelated refactors or speculative future features.

## Shared Quality Kernel

Apply this kernel only when the artifact will guide implementation, maintenance,
migration, performance, or operations work. Do not apply it to pure explanation,
research summaries, or tiny one-answer tasks.

- Prefer not building what does not need to exist.
- Prefer standard library, platform-native features, existing project patterns,
  and already-installed dependencies before custom implementation.
- Keep future implementation surgical and traceable to the user's request.
- Avoid speculative features, single-use abstractions, unrelated refactors, and
  future-proofing not required by the current goal.
- Require observable proof: tests, checks, metrics, screenshots, artifacts, or
  explicit user review.
- Never simplify away security, permissions, accessibility, data-loss
  prevention, trust-boundary validation, or explicitly requested behavior.

## Artifact Shapes

### Decision Note

Use when the main output is a choice:

- Context
- Decision to make
- Options considered
- Recommendation
- Trade-offs
- What would change the decision
- Next step

### Spec / PRD / Design Doc

Scale sections to complexity:

- Context and goal
- Users or stakeholders
- In scope
- Out of scope
- Requirements
- Proposed approach
- Key flows or data flow
- Edge cases and risks
- Validation
- Open assumptions

For repository work, write the reviewed spec to
`docs/seed/YYYY-MM-DD-<topic>-design.md` unless the user requested a different
path. For pure discussion or a small decision, an inline artifact is acceptable
if writing a file would add clutter.

### Writing Plan

Offer a Writing Plan only after the spec or decision is coherent and the user
wants an implementation handoff. Keep it concise.

- Implementation objective
- Minimal reliable route
- Existing capabilities to prefer before new code
- Explicit non-goals and anti-bloat constraints
- Files or areas likely in scope
- Validation order
- Risk checkpoints and pause triggers
- Handoff note for Goal Shaper, if the user later wants a `/goal`

Do not include a runnable `/goal` in Seed. If the user wants one, stop and tell
them to use Goal Shaper with the reviewed Seed artifact.

## Self-Review

Before presenting the final artifact, check:

1. No `TBD`, `TODO`, placeholders, or hidden assumptions.
2. No internal contradictions.
3. Scope fits one decision, spec, or handoff.
4. Requirements are concrete enough to prevent a wrong implementation.
5. The quality kernel appears only when implementation-facing.
6. The artifact does not claim approval to implement.

If a fresh spec-review pass is useful, use `spec-document-reviewer-prompt.md` as
the reviewer prompt template. Treat its output as advisory; fix only issues that
would materially affect future planning or implementation.

## Stop Condition

The terminal state is delivering the reviewed artifact. STOP. Do not invoke any
other skill, do not call Goal Shaper, do not write implementation code, and do
not begin a `/goal` package. The user decides the next workflow.
