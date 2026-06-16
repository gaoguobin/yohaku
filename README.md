# Yohaku Codex Plugins

Yohaku is a Codex plugin marketplace. Its first public plugin is Goal Shaper, a
Codex skill and plugin package that turns rough requests into verifiable Codex
Goal mode packages.

When adding the marketplace in Codex App or CLI, use this repository as the
marketplace source:

```text
gaoguobin/yohaku
```

After Codex loads the marketplace, it appears as `Yohaku`, and the installable
plugin appears as `Goal Shaper`.

## What It Does

- Shapes fuzzy requirements into auditable `/goal` commands.
- Separates outcome, verification, scope, constraints, assumptions, and safety
  pause points.
- Recommends a normal prompt when Goal mode is too heavy.
- Recommends decomposition when a request is too broad for one goal.
- Produces support spec previews for long or high-risk goals and asks before
  writing files.

## What It Does Not Do

- It does not run `/goal`.
- It does not call Codex runtime goal tools.
- It does not implement the requested task.
- It does not commit code.
- It does not write support specs before asking for confirmation.

## Use As A Repo Skill

From this repository, invoke the project skill:

```text
$goal-shaper Help me turn this request into a Codex Goal mode package.
```

The project-scope skill lives at:

```text
.agents/skills/goal-shaper/
```

## Use As A Plugin

Goal Shaper is packaged as a Codex plugin in the `yohaku` marketplace:

```text
plugins/goal-shaper/
```

Normal users should install with either the Codex App UI or the CLI. See
[Install](INSTALL.md) for both paths.

Command-line install:

```bash
codex plugin marketplace add gaoguobin/yohaku --json
codex plugin list --marketplace yohaku --available --json
codex plugin add goal-shaper@yohaku --json
```

Start a new Codex thread after installing or reinstalling the plugin.

## Validate

Run the unit tests after changing the validator or its guardrail coverage:

```bash
python3 -m unittest discover -s tests
```

Run the repository validator after changing the skill, plugin metadata, or
marketplace metadata:

```bash
python3 scripts/validate_goal_shaper.py
```

When the local system skills are available, also run:

```bash
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/goal-shaper
python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" .agents/skills/goal-shaper
python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" plugins/goal-shaper/skills/goal-shaper
```

## Documentation

- [Install](INSTALL.md)
- [Update](UPDATE.md)
- [Uninstall](UNINSTALL.md)
- [Validation](docs/validation.md)
- [Scenario tests](docs/scenario-tests.md)
- [Plugin packaging](docs/plugin.md)
- [Release checklist](docs/release-checklist.md)

## License

MIT. See [LICENSE](LICENSE).
