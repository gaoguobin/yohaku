# Uninstall

## Codex App UI

1. Open Codex App.
2. Open **Plugins**.
3. Select **Goal Shaper** from the installed plugins list.
4. Select **Uninstall plugin**.
5. Start a new Codex thread so old thread context is not reused.

## Command Line

```bash
codex plugin remove goal-shaper@yohaku --json
```

If you no longer want Codex to track the `yohaku` marketplace, remove it too:

```bash
codex plugin marketplace remove yohaku --json
```

Restart Codex App or reopen Codex CLI after removing the marketplace. Start a
new Codex thread after uninstalling to avoid old thread context.
