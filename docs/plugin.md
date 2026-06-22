# Yohaku Plugin Packaging

Yohaku packages focused Codex workflow plugins for public marketplace
installation and local development testing.

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
    assets/
    skills/
      goal-shaper/
        SKILL.md
        agents/openai.yaml
        references/
        templates/
  seed/
    .codex-plugin/plugin.json
    assets/
    skills/
      seed/
        SKILL.md
        scripts/
```

The project skill under `.agents/skills/goal-shaper` preserves the plain
`$goal-shaper` development entrypoint. The packaged skill under
`plugins/goal-shaper/skills/goal-shaper` is the plugin distribution copy.
`python3 scripts/validate_goal_shaper.py` checks that both copies stay in sync.

Seed is distributed only as a packaged Yohaku plugin in this repository. Its
source skill currently comes from the Seed skill package and lives under
`plugins/seed/skills/seed`.

Do not replace the project skill with a symlink. In local testing, a symlink
caused Codex to surface the skill as `goal-shaper:goal-shaper` instead of the
plain `$goal-shaper` project skill.

## Validation

Run the repository validator after changing the skill, plugin metadata, or
marketplace metadata:

```bash
python3 scripts/validate_goal_shaper.py
```

If the system `plugin-creator` skill is available, also run the Codex plugin
manifest validator:

```bash
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/goal-shaper
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/seed
```

If the system `skill-creator` skill is available, validate the packaged skill:

```bash
python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" plugins/goal-shaper/skills/goal-shaper
python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" plugins/seed/skills/seed
```

## User Lifecycle

The user-facing lifecycle paths are documented in `INSTALL.md`, `UPDATE.md`,
and `UNINSTALL.md`. Keep those files focused on two user types: UI users and
CLI users. Keep this file focused on packaging and development validation.

The CLI lifecycle is marketplace-first and plugin-second:

```bash
codex plugin marketplace add gaoguobin/yohaku --json
codex plugin list --marketplace yohaku --available --json
codex plugin add <plugin-name>@yohaku --json
```

For Goal Shaper, use `goal-shaper@yohaku`:

```bash
codex plugin add goal-shaper@yohaku --json
```

For Seed, use `seed@yohaku`:

```bash
codex plugin add seed@yohaku --json
```

Start a new Codex thread after installing or reinstalling a plugin so the
plugin and bundled skills are loaded into the fresh thread context. Restart
Codex App or reopen Codex CLI after adding or refreshing a marketplace so the
plugin directory reloads it.

## Local Development Install

These commands write to local Codex plugin configuration. Run them only when
you are ready to install this checkout's repo marketplace into the current
Codex setup.

```bash
codex plugin marketplace add <repo-path> --json
codex plugin list --marketplace yohaku --available --json
codex plugin add goal-shaper@yohaku --json
```

Start a new Codex thread after installation so the plugin and bundled skill are
loaded into the fresh thread context.
Restart Codex App or reopen Codex CLI after adding or refreshing a marketplace
so the plugin directory reloads it.

## Published Update

For published releases, refresh the Git marketplace snapshot and reinstall the
target plugin:

```bash
codex plugin marketplace upgrade yohaku --json
codex plugin add <plugin-name>@yohaku --json
```

For Goal Shaper:

```bash
codex plugin marketplace upgrade yohaku --json
codex plugin add goal-shaper@yohaku --json
```

For release changes, bump `plugins/goal-shaper/.codex-plugin/plugin.json`
`version`, run validation, publish the repository, then verify the update path.

`codex plugin marketplace upgrade` is only for Git marketplace snapshots. It is
not needed for a local repo marketplace and may fail there.

For another Git-backed marketplace, refresh that marketplace before reinstalling:

```bash
codex plugin marketplace upgrade <marketplace-name> --json
codex plugin add <plugin-name>@<marketplace-name> --json
```

For local iteration without a semantic release, use the `plugin-creator`
cachebuster helper when available, then reinstall:

```bash
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/update_plugin_cachebuster.py" plugins/goal-shaper
codex plugin add goal-shaper@yohaku --json
```

Open a new thread after reinstalling.

## Uninstall

Remove one plugin:

```bash
codex plugin remove <plugin-name>@yohaku --json
```

For Goal Shaper:

```bash
codex plugin remove goal-shaper@yohaku --json
```

Only remove the marketplace if it was added only for local testing or if no
other Yohaku plugins are needed:

```bash
codex plugin marketplace remove yohaku --json
```

## Lifecycle Smoke

Use an isolated `CODEX_HOME` to test the local CLI lifecycle without changing
the current user's plugin configuration:

```bash
tmp_root="$(mktemp -d)"
mkdir -p "$tmp_root/codex"
CODEX_HOME="$tmp_root/codex" codex plugin marketplace add "$(pwd)" --json
CODEX_HOME="$tmp_root/codex" codex plugin list --marketplace yohaku --available --json
CODEX_HOME="$tmp_root/codex" codex plugin add goal-shaper@yohaku --json
CODEX_HOME="$tmp_root/codex" codex plugin remove goal-shaper@yohaku --json
CODEX_HOME="$tmp_root/codex" codex plugin marketplace remove yohaku --json
CODEX_HOME="$tmp_root/codex" codex plugin marketplace list --json
rm -rf "$tmp_root"
```

Expected result: the plugin appears as available, installs with the manifest
version, removes cleanly, and the final marketplace list no longer includes
`yohaku`. Start a new Codex thread after installing or reinstalling in a real
user profile.

When `CODEX_HOME` points under `/tmp`, Codex may warn that it is skipping PATH
alias creation. That warning is expected for this smoke; the plugin lifecycle
passes when the JSON results show the marketplace and plugin states above.

## Release Notes

- The official public Plugin Directory flow is separate from repo-local
  marketplace testing.
- `INSTALL.md`, `UPDATE.md`, and `UNINSTALL.md` are the canonical user lifecycle
  docs. Keep this file focused on packaging and development validation.
- This plugin intentionally does not bundle apps, MCP servers, hooks, commands,
  or external service credentials.
- Goal Shaper must keep its hard boundary: shape the `/goal` package, then stop.
