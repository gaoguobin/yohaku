# Contributing

Thanks for improving Goal Shaper. Keep contributions small, evidence-backed,
and aligned with the existing skill contract.

## Local Checks

Run:

```bash
python3 -m unittest discover -s tests
python3 scripts/validate_goal_shaper.py
```

If the Codex system skills are installed locally, also run:

```bash
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/goal-shaper
python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" .agents/skills/goal-shaper
python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" plugins/goal-shaper/skills/goal-shaper
```

## Change Guidelines

- Keep the skill focused on shaping Goal mode packages.
- Do not make the skill run `/goal`, implement the user's target task, or write
  support specs without confirmation.
- Keep the project skill and packaged skill synchronized.
- Prefer data-driven validator checks over one-off branches.
- Do not add dependencies without explaining why existing tooling is
  insufficient and getting approval first.
