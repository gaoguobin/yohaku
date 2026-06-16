# Install

Goal Shaper installs from the `yohaku` Codex marketplace published by this
repository.

## Prerequisites

- Codex App or Codex CLI is installed and signed in.
- `https://github.com/gaoguobin/goal-shaper` is public and reachable.
- The install should be tested in a new Codex thread after completion.
- After adding or changing a marketplace, restart Codex App or reopen Codex CLI
  so the plugin directory reloads the marketplace.

If the GitHub repository is not public yet, use the local development flow in
`docs/plugin.md` instead.

## Option 1: Codex App UI

Use this path for normal users when `Yohaku` is already visible in the Codex
App plugin directory, for example because the plugin was shared with the
workspace or the marketplace was already added on that machine.

1. Open Codex App.
2. Open **Plugins**.
3. Select the `Yohaku` marketplace or **Shared with you**.
4. Open **Goal Shaper**.
5. Select **Add to Codex**.
6. Start a new Codex thread.
7. Select Goal Shaper from the composer suggestions and ask it to shape a
   request into a verifiable Goal mode package.

If `Yohaku` is not visible yet, use the command-line path once to add the
marketplace, restart Codex App, then return to the App UI for normal install
and management.

## Option 2: Command Line

Use this path for first installs from the public GitHub repository, automation,
or terminal-first users.

### Latest Channel

Use the latest channel when you want Codex to follow the repository's default
branch:

```bash
codex plugin marketplace add gaoguobin/goal-shaper --json
codex plugin list --marketplace yohaku --available --json
codex plugin add goal-shaper@yohaku --json
```

Restart Codex App or reopen Codex CLI after adding the marketplace. Open a new
Codex thread after installation so the bundled skill is loaded into fresh
context.

### Pinned Release

Use a pinned release when you need a reproducible install:

```bash
codex plugin marketplace add gaoguobin/goal-shaper --ref v0.1.4 --json
codex plugin list --marketplace yohaku --available --json
codex plugin add goal-shaper@yohaku --json
```

Open a new Codex thread after installation so the bundled skill is loaded into
fresh context.

## Verify

From the CLI:

```bash
codex plugin list --marketplace yohaku --json
```

The installed entry should show `goal-shaper@yohaku`, `installed: true`, and
the version from `plugins/goal-shaper/.codex-plugin/plugin.json`.

In the App, open **Plugins**, select **Yohaku**, and confirm **Goal Shaper** is
installed. Then start a new thread and confirm Goal Shaper appears in composer
suggestions.
