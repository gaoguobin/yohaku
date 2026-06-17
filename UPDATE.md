# Update

Use this flow after a newer Yohaku marketplace version or plugin release is
available. Yohaku can contain multiple plugins, so update the marketplace first,
then update the specific plugin you use.

## UI Users

Codex App can install and uninstall plugins from the plugin directory. Current
official docs do not confirm that the App UI can refresh a Git-backed
marketplace snapshot by itself, so treat UI-only update as a best-effort flow
until it is verified on a future release.

### If The App Shows An Update Or Reinstall Action

1. Open Codex App.
2. Open **Plugins**.
3. Select the `Yohaku` marketplace.
4. Open the plugin you want to update.
5. Use the App's update or reinstall action if it is shown.
6. Restart Codex App if the version does not refresh immediately.
7. Start a new Codex thread.

For Goal Shaper, confirm the details page shows the expected version.

### UI-Only Fallback

Use this when the App does not show an update action and the plugin details
page still shows an older version.

1. Open **Plugins** and uninstall the target plugin.
2. If the version still stays stale, remove the `Yohaku` marketplace only if
   you are ready to reinstall any other Yohaku plugins you use.
3. Add the marketplace again with source `gaoguobin/yohaku`.
4. Install the target plugin again.
5. Restart Codex App.
6. Start a new Codex thread.

Removing the marketplace affects all plugins installed from that marketplace,
not only Goal Shaper.

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
codex plugin marketplace add gaoguobin/yohaku --ref v0.1.7 --json
codex plugin add goal-shaper@yohaku --json
codex plugin list --marketplace yohaku --json
```

Replace `v0.1.7` with the release tag you want to run.

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
