# Yohaku Validation

Run the unit tests after changing the validator or its guardrail coverage:

```bash
python3 -m unittest discover -s tests
```

Run this after changing the `goal-shaper` skill package, packaged plugins, or
marketplace metadata:

```bash
python3 scripts/validate_goal_shaper.py
```

## What It Checks

The unit tests exercise the validator's parsing helpers, success path, and
representative failure paths with isolated repository fixtures.

The repository validator checks the current package state:

- Required skill files exist under `.agents/skills/goal-shaper/`.
- `SKILL.md` keeps the core trigger and stop boundaries.
- Schema, rubric, templates, examples, and `agents/openai.yaml` stay aligned.
- Plugin packaging exists under `plugins/goal-shaper/`.
- Seed exists under `plugins/seed/` and keeps its reviewed-artifact stop
  boundary, optional Writing Plan handoff boundary, and conditional
  implementation-quality guidance.
- `.agents/skills/goal-shaper` and
  `plugins/goal-shaper/skills/goal-shaper` stay byte-for-byte in sync.
- `.agents/plugins/marketplace.json` is the `yohaku` marketplace and every
  listed plugin points to a real local plugin package.
- `plugins/goal-shaper/.codex-plugin/plugin.json` keeps installable plugin
  metadata and does not claim unused apps, MCP servers, or hooks.
- Release docs exist, lifecycle commands match the current repository,
  marketplace, and plugin IDs, and `CHANGELOG.md` includes the manifest version.
- The package keeps a small progressive-disclosure shape.
- Validation-command invention, automatic goal execution, automatic support spec
  writes, and durable-guidance mixing remain guarded.
- Manual test scenarios are documented as patterns, not hardcoded project fixes.

## What It Does Not Check

- It does not run Codex Goal mode.
- It does not assert model output quality for every possible prompt.
- It does not verify Codex App chip rendering; recheck `$goal-shaper` display
  after global install or plugin packaging.
- It does not replace manual scenario testing for long-context support specs.
- It does not prove Seed output quality across every possible brainstorm or
  spec request.
- It does not install, reinstall, or remove the plugin from the local Codex
  configuration. For an isolated lifecycle smoke, see
  [Plugin packaging](plugin.md#lifecycle-smoke).

## Additional Plugin Checks

When local system skills are available, run:

```bash
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/goal-shaper
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/seed
python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" plugins/goal-shaper/skills/goal-shaper
python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" plugins/seed/skills/seed
```

## Manual Scenario Checklist

Use [scenario-tests.md](scenario-tests.md) after meaningful behavior changes and
before public releases. It covers install, first use, interview behavior, goal
quality, update, uninstall, and failure recovery.
