# Install

Yohaku is a Codex plugin marketplace published by this repository. It can host
multiple plugins over time. Goal Shaper is the first public plugin.

## Prerequisites

- Codex App or Codex CLI is installed and signed in.
- `https://github.com/gaoguobin/yohaku` is public and reachable.
- After installing a plugin, start a new Codex thread so Codex loads the newly
  installed plugin and its skills.
- After adding or changing a marketplace, restart Codex App or reopen Codex CLI
  so the plugin directory reloads the marketplace.

If the GitHub repository is not public yet, use the local development flow in
`docs/plugin.md` instead.

## UI Users

Use this path if you prefer to manage plugins from the Codex App.

### Add The Marketplace

1. Open Codex App.
2. Open **Plugins**.
3. Add a plugin marketplace.
4. Use `gaoguobin/yohaku` as the source.
5. Restart Codex App if the `Yohaku` marketplace does not appear immediately.

If `Yohaku` is already visible in the plugin directory, skip this step.

### Install A Plugin

1. Open **Plugins**.
2. Select the `Yohaku` marketplace or **Shared with you**.
3. Open the plugin you want to install.
4. Select **Add to Codex**.
5. Start a new Codex thread.

For Goal Shaper, open **Goal Shaper** from the `Yohaku` marketplace.

### Use A Plugin In Codex App

Yohaku can contain multiple plugins, and each plugin can contain one or more
skills. In a new thread, pick the entry that matches the plugin or skill you
want to use.

- Type `/` to open the slash command list. Enabled skills can appear there;
  search for a skill such as `Goal Shaper`, select it, then enter the request
  you want shaped.
- Type `@` to choose an installed plugin or one of its bundled capabilities.
  Use this when you want to steer Codex toward a specific installed plugin from
  the marketplace.
- Type `$` for an explicit skill mention, such as `$goal-shaper`. This is the
  most precise form when you know the skill name.
- You can also describe the task naturally and let Codex choose an installed
  plugin or skill, but release smoke tests should use `/`, `@`, or `$` so the
  selected entry is clear.

### Verify In The App

Open **Plugins**, select `Yohaku`, and confirm the target plugin is installed.
For Goal Shaper, confirm the details page shows the expected version. Then
start a new thread and confirm Goal Shaper appears through `/`, `@`, or `$`.

## CLI Users

Use this path if you are comfortable with terminal commands or need a
repeatable install.

### Latest Channel

Add the Yohaku marketplace once:

```bash
codex plugin marketplace add gaoguobin/yohaku --json
```

List available plugins:

```bash
codex plugin list --marketplace yohaku --available --json
```

Install a plugin from the marketplace:

```bash
codex plugin add <plugin-name>@yohaku --json
```

For Goal Shaper:

```bash
codex plugin marketplace add gaoguobin/yohaku --json
codex plugin list --marketplace yohaku --available --json
codex plugin add goal-shaper@yohaku --json
```

Restart Codex App or reopen Codex CLI after adding the marketplace. Open a new
Codex thread after installation so the bundled skills are loaded into fresh
context.

### Pinned Release

Use a pinned release when you need a reproducible install:

```bash
codex plugin marketplace add gaoguobin/yohaku --ref v0.1.6 --json
codex plugin list --marketplace yohaku --available --json
codex plugin add goal-shaper@yohaku --json
```

Replace `v0.1.6` with the release tag you want to run. Open a new Codex thread
after installation so the bundled skills are loaded into fresh context.

### Verify From The CLI

```bash
codex plugin list --marketplace yohaku --json
```

For Goal Shaper, the installed entry should show `goal-shaper@yohaku`,
`installed: true`, and the version from
`plugins/goal-shaper/.codex-plugin/plugin.json`.
