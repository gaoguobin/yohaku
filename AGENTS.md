# Repository Guidance

## Scope

Goal Shaper is a dependency-free Codex skill and plugin package. Keep changes
focused on shaping verifiable Goal mode packages, not executing those goals.

## Development Rules

- Preserve the skill contract: draft the `/goal` package, then stop.
- Keep tests and validators dependency-free unless a new dependency is clearly
  necessary and approved first.
- If JavaScript tooling is introduced later, use pnpm only. Do not add npm,
  Yarn, or Bun lockfiles.
- Do not replace `.agents/skills/goal-shaper` with a symlink; the project skill
  and packaged plugin skill must remain byte-for-byte synchronized.
- Keep plugin metadata compatible with the current Codex plugin schema.

## Validation

Run these before handing off changes:

```bash
python3 -m unittest discover -s tests
python3 scripts/validate_goal_shaper.py
```

When local system skills are available, also run:

```bash
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/goal-shaper
python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" .agents/skills/goal-shaper
python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" plugins/goal-shaper/skills/goal-shaper
```
