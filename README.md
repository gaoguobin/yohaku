# Goal Shaper

Goal Shaper is a Codex skill and plugin package that turns rough requests into
best-practice Codex Goal mode packages.

It helps Codex decide whether Goal mode is appropriate, asks for only the
missing details that change success or safety, drafts a copyable `/goal`, and
then stops.

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

Goal Shaper is also packaged as a Codex plugin:

```text
plugins/goal-shaper/
```

The repo marketplace lives at:

```text
.agents/plugins/marketplace.json
```

Install testing writes to local Codex plugin configuration, so do it only when
you are ready to test local plugin install behavior:

```bash
codex plugin marketplace add <repo-path> --json
codex plugin list --marketplace goal-shaper-local --available --json
codex plugin add goal-shaper@goal-shaper-local --json
```

Start a new Codex thread after installing or reinstalling the plugin.

## Validate

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

- [Validation](docs/validation.md)
- [Plugin packaging](docs/plugin.md)

## License

MIT. See [LICENSE](LICENSE).
