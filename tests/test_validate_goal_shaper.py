from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import shutil
import tempfile
import unittest
from collections.abc import Iterator
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_goal_shaper.py"

spec = importlib.util.spec_from_file_location("validate_goal_shaper", VALIDATOR_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Unable to load validator from {VALIDATOR_PATH}")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


@contextlib.contextmanager
def copied_repo_fixture() -> Iterator[Path]:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir) / "repo"
        shutil.copytree(REPO_ROOT / ".agents", root / ".agents")
        shutil.copytree(REPO_ROOT / "plugins", root / "plugins")
        yield root


@contextlib.contextmanager
def validator_paths(root: Path):
    plugin_dir = root / "plugins" / "goal-shaper"
    with mock.patch.multiple(
        validator,
        ROOT=root,
        PROJECT_SKILL_DIR=root / ".agents" / "skills" / "goal-shaper",
        PLUGIN_DIR=plugin_dir,
        PLUGIN_SKILL_DIR=plugin_dir / "skills" / "goal-shaper",
        SKILL_DIR=root / ".agents" / "skills" / "goal-shaper",
        MARKETPLACE_PATH=root / ".agents" / "plugins" / "marketplace.json",
        PLUGIN_MANIFEST_PATH=plugin_dir / ".codex-plugin" / "plugin.json",
    ):
        yield


def run_validator(root: Path) -> tuple[int, str]:
    stdout = io.StringIO()
    with validator_paths(root), contextlib.redirect_stdout(stdout):
        status = validator.main()
    return status, stdout.getvalue()


def replace_in_skill_copies(
    root: Path, relative_path: str, old: str, new: str
) -> None:
    for skill_root in [
        root / ".agents" / "skills" / "goal-shaper",
        root / "plugins" / "goal-shaper" / "skills" / "goal-shaper",
    ]:
        path = skill_root / relative_path
        updated = path.read_text(encoding="utf-8").replace(old, new)
        path.write_text(updated, encoding="utf-8")


class ValidatorUnitTests(unittest.TestCase):
    def test_parse_frontmatter_reads_basic_fields(self) -> None:
        parsed = validator.parse_frontmatter(
            "---\nname: goal-shaper\ndescription: Shape goals\n---\n# Body\n"
        )

        self.assertEqual(
            parsed,
            {"name": "goal-shaper", "description": "Shape goals"},
        )

    def test_require_contains_normalizes_whitespace(self) -> None:
        failures: list[str] = []

        validator.require_contains(
            failures,
            "Ask only for missing details\nthat change success.",
            "missing details that change success",
            "SKILL.md",
            "interview rule",
        )

        self.assertEqual(failures, [])


class ValidatorIntegrationTests(unittest.TestCase):
    def test_current_repository_passes_validator(self) -> None:
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            status = validator.main()

        self.assertEqual(status, 0, stdout.getvalue())
        self.assertIn("goal-shaper validation passed", stdout.getvalue())

    def test_copied_repository_fixture_passes_validator(self) -> None:
        with copied_repo_fixture() as root:
            status, output = run_validator(root)

        self.assertEqual(status, 0, output)
        self.assertIn("checked 7 skill files", output)

    def test_entrypoint_boundary_loss_fails_even_when_skill_copies_match(self) -> None:
        with copied_repo_fixture() as root:
            replace_in_skill_copies(
                root,
                "SKILL.md",
                "Do not invent exact validation commands",
                "Avoid made-up validation commands",
            )

            status, output = run_validator(root)

        self.assertEqual(status, 1, output)
        self.assertIn("SKILL.md: missing 'core boundary'", output)
        self.assertIn("Do not invent exact validation commands", output)

    def test_project_and_packaged_skill_drift_fails(self) -> None:
        with copied_repo_fixture() as root:
            plugin_skill = (
                root
                / "plugins"
                / "goal-shaper"
                / "skills"
                / "goal-shaper"
                / "SKILL.md"
            )
            plugin_text = plugin_skill.read_text(encoding="utf-8")
            plugin_skill.write_text(
                plugin_text + "\n<!-- plugin-only drift -->\n", encoding="utf-8"
            )

            status, output = run_validator(root)

        self.assertEqual(status, 1, output)
        self.assertIn("project skill and packaged skill differ", output)
        self.assertIn("content differs: SKILL.md", output)

    def test_plugin_manifest_rejects_unused_runtime_surfaces(self) -> None:
        with copied_repo_fixture() as root:
            manifest_path = (
                root / "plugins" / "goal-shaper" / ".codex-plugin" / "plugin.json"
            )
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["apps"] = {}
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            status, output = run_validator(root)

        self.assertEqual(status, 1, output)
        self.assertIn("unsupported or unnecessary fields present", output)
        self.assertIn("apps", output)

    def test_marketplace_must_point_to_packaged_plugin(self) -> None:
        with copied_repo_fixture() as root:
            marketplace_path = root / ".agents" / "plugins" / "marketplace.json"
            marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
            marketplace["plugins"][0]["source"]["path"] = "./wrong-plugin"
            marketplace_path.write_text(json.dumps(marketplace), encoding="utf-8")

            status, output = run_validator(root)

        self.assertEqual(status, 1, output)
        self.assertIn("source must point to ./plugins/goal-shaper", output)

    def test_missing_required_skill_file_stops_before_deeper_checks(self) -> None:
        with copied_repo_fixture() as root:
            rubric = (
                root
                / ".agents"
                / "skills"
                / "goal-shaper"
                / "references"
                / "rubric.md"
            )
            rubric.unlink()

            status, output = run_validator(root)

        self.assertEqual(status, 1, output)
        self.assertIn("missing required skill file: references/rubric.md", output)


if __name__ == "__main__":
    unittest.main()
