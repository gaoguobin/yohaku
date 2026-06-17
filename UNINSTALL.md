# Uninstall

Yohaku can contain multiple plugins. Remove the plugin first; remove the
marketplace only when you no longer use any plugins from Yohaku.

## UI Users

1. Open Codex App.
2. Open **Plugins**.
3. Open the installed plugin you want to remove.
4. Select **Uninstall plugin**.
5. Start a new Codex thread so old thread context is not reused.

For Goal Shaper, open **Goal Shaper** from the installed plugins list.

Only remove the `Yohaku` marketplace if you no longer need any plugin from it.
Removing the marketplace affects every plugin installed from that marketplace.

## CLI Users

Remove one plugin:

```bash
codex plugin remove <plugin-name>@yohaku --json
```

For Goal Shaper:

```bash
codex plugin remove goal-shaper@yohaku --json
```

If you no longer want Codex to track the `yohaku` marketplace, remove it too:

```bash
codex plugin marketplace remove yohaku --json
```

Restart Codex App or reopen Codex CLI after removing the marketplace. Start a
new Codex thread after uninstalling to avoid old thread context.
