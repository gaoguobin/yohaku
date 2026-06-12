# Goal Shaper Validation

Run this after changing the `goal-shaper` skill package:

```bash
python3 scripts/validate_goal_shaper.py
```

## What It Checks

- Required skill files exist under `.agents/skills/goal-shaper/`.
- `SKILL.md` keeps the core trigger and stop boundaries.
- Schema, rubric, templates, examples, and `agents/openai.yaml` stay aligned.
- Plugin packaging exists under `plugins/goal-shaper/`.
- `.agents/skills/goal-shaper` and
  `plugins/goal-shaper/skills/goal-shaper` stay byte-for-byte in sync.
- `.agents/plugins/marketplace.json` points at `./plugins/goal-shaper`.
- `plugins/goal-shaper/.codex-plugin/plugin.json` keeps installable plugin
  metadata and does not claim unused apps, MCP servers, or hooks.
- The package keeps a small progressive-disclosure shape.
- Validation-command invention, automatic goal execution, automatic support spec
  writes, and durable-guidance mixing remain guarded.
- Manual test scenarios are represented as patterns, not hardcoded project
  fixes.

## What It Does Not Check

- It does not run Codex Goal mode.
- It does not assert model output quality for every possible prompt.
- It does not verify Codex App chip rendering; recheck `$goal-shaper` display
  after global install or plugin packaging.
- It does not replace manual scenario testing for long-context support specs.
- It does not install, reinstall, or remove the plugin from the local Codex
  configuration.

## Additional Plugin Checks

When local system skills are available, run:

```bash
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/goal-shaper
python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" plugins/goal-shaper/skills/goal-shaper
```

## Manual Scenario Checklist

Use these prompts after meaningful behavior changes:

- Too small: explain an unspecified function.
- Too broad: modernize tests, UI, deployment, and docs together.
- Performance: make a homepage faster without a target metric.
- High risk: clean production logs or reclaim disk space.
- Research: decide whether a dependency upgrade is appropriate.
- Durable guidance: require a package manager and dependency policy.
- Long context: generate a compact `/goal` that points to a support spec.

## Manual Scenario Notes

### Long Context Support Spec

Last checked: 2026-06-12

Prompt:

```text
$goal-shaper Help me turn this goal-shaper project into a plugin that can be formally released and installed, and also handle docs, validation, upgrade, and uninstall flow.
```

Expected behavior:

- Classifies the request as `large`.
- Emits a short `/goal` that points to a support spec path.
- Shows a support spec preview instead of stuffing all context into `/goal`.
- Asks before writing `.goal-shaper/specs/...`.
- Preserves the rule that Goal Shaper does not execute the goal.

Observed behavior:

- Passed. The skill produced a compact runnable goal, a support spec preview,
  evidence checklist, assumptions, and durable guidance candidates.
- It paused for confirmation before writing
  `.goal-shaper/specs/2026-06-12-goal-shaper-plugin-release.md`.

Review note:

- Official plugin docs and `codex plugin --help` were listed as materials for
  the future goal runner to verify, not as work already completed by
  Goal Shaper.
