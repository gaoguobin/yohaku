# Release Checklist

Use this checklist before tagging or sharing a public release.

## Metadata

- Every plugin under `plugins/` has a clean semver version in
  `.codex-plugin/plugin.json`.
- `CHANGELOG.md` includes the release version.
- `README.md`, `INSTALL.md`, `UPDATE.md`, and `UNINSTALL.md` mention the current
  marketplace name.
- `homepage`, `repository`, `websiteURL`, `privacyPolicyURL`, and
  `termsOfServiceURL` point to public, working URLs.
- Anonymous users can read the release source:

```bash
git ls-remote https://github.com/gaoguobin/yohaku.git HEAD
curl -I -L https://github.com/gaoguobin/yohaku
```

## Validation

```bash
python3 -m unittest discover -s tests
python3 scripts/validate_goal_shaper.py
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/goal-shaper
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/seed
python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" plugins/goal-shaper/skills/goal-shaper
python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" plugins/seed/skills/seed
git diff --check
```

Run the manual scenario checklist in `docs/scenario-tests.md` for any release
that changes skill behavior, install metadata, or lifecycle docs.

## Lifecycle Smoke

Run the isolated lifecycle smoke from `docs/plugin.md`, then test real Codex
App and CLI lifecycle flows in new threads.

Before calling a release public-ready, verify both user types:

- UI users: `Yohaku` is visible, the expected plugins appear in the marketplace,
  the target plugin installs from its details page, and a new thread can select
  the target plugin or skill via
  `/`, `@`, or `$`. If the marketplace was added on the same machine, restart
  Codex App before checking the directory. When testing an update, restart the
  App, check the details page version, and use the CLI update flow if the App
  still shows the older version.
- Localized UI guides: English, Simplified Chinese, and Japanese walkthroughs
  render on GitHub, screenshots load, and screenshots do not expose accounts,
  hostnames, local paths, tokens, or private project names.
- Command line: `codex plugin marketplace add gaoguobin/yohaku`,
  `codex plugin list --marketplace yohaku --available --json`,
  `codex plugin add <plugin-name>@yohaku`, and uninstall all work from a clean
  profile or isolated `CODEX_HOME`.
- Pinned command line works from a clean profile or isolated `CODEX_HOME`:

```bash
codex plugin marketplace add gaoguobin/yohaku --ref v0.1.8
```
