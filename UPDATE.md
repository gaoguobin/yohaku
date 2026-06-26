# Update

Use this flow after a newer Yohaku marketplace version or plugin release is
available. Yohaku can contain multiple plugins, so confirm the marketplace and
plugin version you intend to use.

## UI Users

Restart Codex App after a published Yohaku update, then check the plugin
details page. In App testing, Git-backed marketplace metadata may continue to
show the older version until the App restarts.

1. Restart Codex App.
2. Open **Plugins**.
3. Select the `Yohaku` marketplace.
4. Open the plugin details page and confirm the version.
5. Start a new Codex thread.

If the version is still old after a restart, use the CLI flow below.

## CLI Users

The CLI path is the reliable update path for Git-backed marketplaces.

### Latest Channel

Refresh the Yohaku marketplace snapshot:

```bash
codex plugin marketplace upgrade yohaku --json
```

Reinstall the plugin you want to update:

```bash
codex plugin add <plugin-name>@yohaku --json
```

Verify the result:

```bash
codex plugin list --marketplace yohaku --json
```

For Goal Shaper:

```bash
codex plugin marketplace upgrade yohaku --json
codex plugin add goal-shaper@yohaku --json
codex plugin list --marketplace yohaku --json
```

Restart Codex App or reopen Codex CLI after refreshing the marketplace. Open a
new Codex thread after updating or reinstalling.

### Pinned Release Or Rollback

Pinned installs follow an explicit release tag. To switch tags, remove the
configured marketplace, add it again with the desired tag, then reinstall the
plugin:

```bash
codex plugin marketplace remove yohaku --json
codex plugin marketplace add gaoguobin/yohaku --ref v0.1.8 --json
codex plugin add goal-shaper@yohaku --json
codex plugin list --marketplace yohaku --json
```

Replace `v0.1.8` with the release tag you want to run.

## Local Development

For local development iteration without a semantic release, use the Codex
plugin cachebuster helper when available, then reinstall from the local
marketplace:

```bash
python3 scripts/validate_goal_shaper.py
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/update_plugin_cachebuster.py" plugins/goal-shaper
codex plugin add goal-shaper@yohaku --json
```

Do not use `codex plugin marketplace upgrade` for a local repo marketplace.
That command is for Git marketplace snapshots.
