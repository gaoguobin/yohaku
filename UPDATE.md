# Update

Use this flow after a newer `yohaku` marketplace version is available.

## Codex App UI

1. Open Codex App.
2. Open **Plugins**.
3. Select the `Yohaku` marketplace.
4. Open **Goal Shaper**.
5. Update or reinstall the plugin if Codex shows a newer version.
6. Start a new Codex thread.

## Command Line

For latest-channel installs:

```bash
codex plugin marketplace upgrade yohaku --json
codex plugin add goal-shaper@yohaku --json
codex plugin list --marketplace yohaku --json
```

Restart Codex App or reopen Codex CLI after refreshing the marketplace. Open a
new Codex thread after updating or reinstalling.

For pinned-release installs, switch the marketplace to the new tag and then
reinstall:

```bash
codex plugin marketplace remove yohaku --json
codex plugin marketplace add gaoguobin/yohaku --ref v0.1.5 --json
codex plugin add goal-shaper@yohaku --json
codex plugin list --marketplace yohaku --json
```

Replace `v0.1.5` with the release tag you want to run.

## Local Development

For local development iteration without a semantic release, use the Codex
plugin cachebuster helper when available, then reinstall from the local
marketplace:

```bash
python3 scripts/validate_goal_shaper.py
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/update_plugin_cachebuster.py" plugins/goal-shaper
codex plugin add goal-shaper@yohaku --json
```

Do not use `codex plugin marketplace upgrade` for the repo-local development
marketplace. That command is for Git marketplace snapshots.
