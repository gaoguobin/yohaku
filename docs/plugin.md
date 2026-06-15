# Goal Shaper Plugin Packaging

Goal Shaper is packaged as a Codex plugin for local or repo marketplace
installation.

## Package Layout

```text
.agents/
  plugins/
    marketplace.json
  skills/
    goal-shaper/
plugins/
  goal-shaper/
    .codex-plugin/plugin.json
    skills/
      goal-shaper/
        SKILL.md
        agents/openai.yaml
        references/
        templates/
```

The project skill under `.agents/skills/goal-shaper` preserves the plain
`$goal-shaper` development entrypoint. The packaged skill under
`plugins/goal-shaper/skills/goal-shaper` is the plugin distribution copy.
`python3 scripts/validate_goal_shaper.py` checks that both copies stay in sync.

Do not replace the project skill with a symlink. In local testing, a symlink
caused Codex to surface the skill as `goal-shaper:goal-shaper` instead of the
plain `$goal-shaper` project skill.

## Validation

Run the repository validator after changing the skill or plugin metadata:

```bash
python3 scripts/validate_goal_shaper.py
```

If the system `plugin-creator` skill is available, also run the Codex plugin
manifest validator:

```bash
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/goal-shaper
```

If the system `skill-creator` skill is available, validate the packaged skill:

```bash
python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" plugins/goal-shaper/skills/goal-shaper
```

## Local Install

These commands write to local Codex plugin configuration. Run them only when
you are ready to install the repo marketplace into the current Codex setup.

```bash
codex plugin marketplace add <repo-path> --json
codex plugin list --marketplace goal-shaper-local --available --json
codex plugin add goal-shaper@goal-shaper-local --json
```

Start a new Codex thread after installation so the plugin and bundled skill are
loaded into the fresh thread context.

## Update

For release changes, bump `plugins/goal-shaper/.codex-plugin/plugin.json`
`version`, run validation, then refresh the installed marketplace and reinstall:

```bash
python3 scripts/validate_goal_shaper.py
codex plugin marketplace upgrade goal-shaper-local --json
codex plugin add goal-shaper@goal-shaper-local --json
```

For local iteration without a semantic release, use the `plugin-creator`
cachebuster helper when available, then reinstall:

```bash
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/update_plugin_cachebuster.py" plugins/goal-shaper
codex plugin add goal-shaper@goal-shaper-local --json
```

Open a new thread after reinstalling.

## Uninstall

```bash
codex plugin remove goal-shaper@goal-shaper-local --json
codex plugin marketplace remove goal-shaper-local --json
```

Only remove the marketplace if it was added only for Goal Shaper local testing.

## Release Notes

- The official public Plugin Directory flow is separate from repo-local
  marketplace testing.
- This plugin intentionally does not bundle apps, MCP servers, hooks, commands,
  or external service credentials.
- Goal Shaper must keep its hard boundary: shape the `/goal` package, then stop.
