# Release Checklist

Use this checklist before publishing or sharing Goal Shaper as a Codex plugin.

## 1. Repository Shape

- Root `README.md` explains skill usage, plugin usage, validation, and install
  boundaries.
- `LICENSE` exists.
- `.internal/` stays ignored and is not required for installation.
- `.agents/skills/goal-shaper/` exists for project-scope development use.
- `plugins/goal-shaper/` exists as the installable plugin package.
- `.agents/plugins/marketplace.json` points at `./plugins/goal-shaper`.

## 2. Version And Metadata

- `plugins/goal-shaper/.codex-plugin/plugin.json` has the intended version.
- Manifest fields describe the current plugin behavior.
- Manifest does not include unused `apps`, `mcpServers`, `hooks`, or commands.
- Project skill and packaged skill are intentionally identical.

## 3. Local Validation

Run:

```bash
python3 scripts/validate_goal_shaper.py
```

When system validation helpers are available, also run:

```bash
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/goal-shaper
python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" .agents/skills/goal-shaper
python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" plugins/goal-shaper/skills/goal-shaper
```

## 4. Manual Skill Scenarios

Run focused prompt checks after meaningful skill behavior changes:

- Too small: explain an unspecified function.
- Too broad: modernize tests, UI, deployment, and docs together.
- Performance: make a homepage faster without a target metric.
- High risk: clean production logs or reclaim disk space.
- Research: decide whether a dependency upgrade is appropriate.
- Durable guidance: require a package manager and dependency policy.
- Long context: generate a compact `/goal` that points to a support spec.

## 5. GitHub Preparation

- Initialize git only after the repository contents are ready.
- Confirm GitHub account and repo-local git author identity before committing.
- Push to the intended GitHub repository.
- Prefer testing plugin install from the GitHub repository URL after push.

## 6. Install Test

These commands write local Codex plugin configuration. Run only when ready to
test install behavior:

```bash
codex plugin marketplace add <repo-path> --json
codex plugin list --marketplace goal-shaper-local --available --json
codex plugin add goal-shaper@goal-shaper-local --json
```

For GitHub-backed testing after push, use `codex plugin marketplace add` with
the GitHub repo or URL and any needed sparse paths, then install
`goal-shaper@<marketplace-name>`.

After install:

- Start a new Codex thread.
- Confirm the plugin appears in the plugin list.
- Confirm the bundled skill can be invoked.
- Recheck the Codex App chip label for `Goal Shaper` versus `$goal-shaper`.

## 7. Update Test

After a release change:

```bash
python3 scripts/validate_goal_shaper.py
codex plugin marketplace upgrade goal-shaper-local --json
codex plugin add goal-shaper@goal-shaper-local --json
```

Start a new Codex thread after reinstalling.

## 8. Uninstall Test

```bash
codex plugin remove goal-shaper@goal-shaper-local --json
codex plugin marketplace remove goal-shaper-local --json
```

Only remove the marketplace if it was added only for Goal Shaper local testing.

## 9. Release Decision

Mark the release `go` only when:

- All validation commands pass.
- Manual scenarios still match expected behavior.
- Install, update, and uninstall behavior are tested or explicitly deferred.
- Known limitations are documented.
- No local-only paths remain in user-facing GitHub install instructions.
