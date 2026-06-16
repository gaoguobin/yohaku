# Release Checklist

Use this checklist before tagging or sharing a public release.

## Metadata

- `plugins/goal-shaper/.codex-plugin/plugin.json` has a clean semver version.
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
python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" .agents/skills/goal-shaper
python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" plugins/goal-shaper/skills/goal-shaper
git diff --check
```

Run the manual scenario checklist in `docs/scenario-tests.md` for any release
that changes skill behavior, install metadata, or lifecycle docs.

## Lifecycle Smoke

Run the isolated lifecycle smoke from `docs/plugin.md`, then test a real Codex
App install/update/uninstall flow in a new thread.

Before calling a release public-ready, verify both user installation paths:

- Codex App UI: `Yohaku` or the shared Goal Shaper entry is visible, Goal Shaper
  installs from the details page, and a new thread can select the skill. If the
  marketplace was added on the same machine, restart Codex App before checking
  the directory.
- Command line: `codex plugin marketplace add gaoguobin/yohaku`,
  `codex plugin add goal-shaper@yohaku`, and uninstall all work from a clean
  profile or isolated `CODEX_HOME`.
- Pinned command line works from a clean profile or isolated `CODEX_HOME`:

```bash
codex plugin marketplace add gaoguobin/yohaku --ref v0.1.5
```
