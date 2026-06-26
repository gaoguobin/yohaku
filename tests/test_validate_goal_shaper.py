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
        for relative in validator.RELEASE_FILES:
            source = REPO_ROOT / relative
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        yield root


@contextlib.contextmanager
def validator_paths(root: Path):
    plugin_dir = root / "plugins" / "goal-shaper"
    with mock.patch.multiple(
        validator,
        ROOT=root,
        PLUGIN_DIR=plugin_dir,
        PLUGIN_SKILL_DIR=plugin_dir / "skills" / "goal-shaper",
        SEED_PLUGIN_DIR=root / "plugins" / "seed",
        SEED_SKILL_DIR=root / "plugins" / "seed" / "skills" / "seed",
        SEED_PLUGIN_MANIFEST_PATH=root
        / "plugins"
        / "seed"
        / ".codex-plugin"
        / "plugin.json",
        SKILL_DIR=plugin_dir / "skills" / "goal-shaper",
        MARKETPLACE_PATH=root / ".agents" / "plugins" / "marketplace.json",
        PLUGIN_MANIFEST_PATH=plugin_dir / ".codex-plugin" / "plugin.json",
        CHANGELOG_PATH=root / "CHANGELOG.md",
    ):
        yield


def replace_in_file(root: Path, relative_path: str, old: str, new: str) -> None:
    path = root / relative_path
    updated = path.read_text(encoding="utf-8").replace(old, new)
    path.write_text(updated, encoding="utf-8")


def run_validator(root: Path) -> tuple[int, str]:
    stdout = io.StringIO()
    with validator_paths(root), contextlib.redirect_stdout(stdout):
        status = validator.main()
    return status, stdout.getvalue()


def replace_in_goal_shaper_skill(
    root: Path, relative_path: str, old: str, new: str
) -> None:
    path = root / "plugins" / "goal-shaper" / "skills" / "goal-shaper" / relative_path
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
            replace_in_goal_shaper_skill(
                root,
                "SKILL.md",
                "Do not invent exact validation commands",
                "Avoid made-up validation commands",
            )

            status, output = run_validator(root)

        self.assertEqual(status, 1, output)
        self.assertIn("SKILL.md: missing 'core boundary'", output)
        self.assertIn("Do not invent exact validation commands", output)

    def test_goal_template_requires_copy_instruction(self) -> None:
        with copied_repo_fixture() as root:
            replace_in_goal_shaper_skill(
                root,
                "templates/goal-package.md",
                "Copy only the `/goal` code block to run it",
                "Copy the generated goal",
            )

            status, output = run_validator(root)

        self.assertEqual(status, 1, output)
        self.assertIn("goal-package.md: missing 'copy instruction'", output)

    def test_support_spec_template_blocks_unwritten_spec_goal(self) -> None:
        with copied_repo_fixture() as root:
            replace_in_goal_shaper_skill(
                root,
                "templates/support-spec.md",
                "Before the support spec file exists, do not include a copyable `/goal` block",
                "Preview the runnable goal before writing the support spec",
            )

            status, output = run_validator(root)

        self.assertEqual(status, 1, output)
        self.assertIn("support-spec.md: missing 'unwritten spec guard'", output)

    def test_entrypoint_requires_missing_target_skill_boundary(self) -> None:
        with copied_repo_fixture() as root:
            replace_in_goal_shaper_skill(
                root,
                "SKILL.md",
                "Selecting or invoking this skill is not target selection",
                "Selecting this skill provides context",
            )

            status, output = run_validator(root)

        self.assertEqual(status, 1, output)
        self.assertIn("SKILL.md: missing 'core boundary'", output)
        self.assertIn("not target selection", output)

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

    def test_empty_plugin_manifest_fails(self) -> None:
        with copied_repo_fixture() as root:
            manifest_path = (
                root / "plugins" / "goal-shaper" / ".codex-plugin" / "plugin.json"
            )
            manifest_path.write_text("{}", encoding="utf-8")

            status, output = run_validator(root)

        self.assertEqual(status, 1, output)
        self.assertIn("expected non-empty JSON object", output)

    def test_plugin_manifest_requires_icon_assets(self) -> None:
        with copied_repo_fixture() as root:
            icon_path = root / "plugins" / "goal-shaper" / "assets" / "icon.png"
            icon_path.unlink()

            status, output = run_validator(root)

        self.assertEqual(status, 1, output)
        self.assertIn("interface.composerIcon", output)
        self.assertIn("missing file", output)

    def test_plugin_manifest_requires_website_url(self) -> None:
        with copied_repo_fixture() as root:
            manifest_path = (
                root / "plugins" / "goal-shaper" / ".codex-plugin" / "plugin.json"
            )
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["interface"]["websiteURL"] = "https://example.com"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            status, output = run_validator(root)

        self.assertEqual(status, 1, output)
        self.assertIn("interface.websiteURL", output)

    def test_seed_skill_requires_writing_plan_handoff_boundary(self) -> None:
        with copied_repo_fixture() as root:
            replace_in_file(
                root,
                "plugins/seed/skills/seed/SKILL.md",
                "A Writing Plan is a handoff artifact, not an execution mode",
                "A Writing Plan is an implementation plan",
            )

            status, output = run_validator(root)

        self.assertEqual(status, 1, output)
        self.assertIn("seed SKILL.md: missing 'seed contract'", output)
        self.assertIn("Writing Plan is a handoff artifact", output)

    def test_seed_skill_requires_conditional_quality_kernel(self) -> None:
        with copied_repo_fixture() as root:
            replace_in_file(
                root,
                "plugins/seed/skills/seed/SKILL.md",
                "Apply this kernel only when the artifact will guide implementation",
                "Apply this kernel to every Seed artifact",
            )

            status, output = run_validator(root)

        self.assertEqual(status, 1, output)
        self.assertIn("seed SKILL.md: missing 'seed contract'", output)
        self.assertIn("Apply this kernel only", output)

    def test_seed_manifest_rejects_unused_runtime_surfaces(self) -> None:
        with copied_repo_fixture() as root:
            manifest_path = root / "plugins" / "seed" / ".codex-plugin" / "plugin.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["hooks"] = {}
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            status, output = run_validator(root)

        self.assertEqual(status, 1, output)
        self.assertIn("seed plugin.json: unsupported or unnecessary fields present", output)

    def test_marketplace_allows_other_yohaku_plugins(self) -> None:
        with copied_repo_fixture() as root:
            future_plugin = root / "plugins" / "future-plugin"
            future_manifest = future_plugin / ".codex-plugin" / "plugin.json"
            future_manifest.parent.mkdir(parents=True)
            future_manifest.write_text('{"name": "future-plugin"}', encoding="utf-8")

            marketplace_path = root / ".agents" / "plugins" / "marketplace.json"
            marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
            marketplace["plugins"].append(
                {
                    "name": "future-plugin",
                    "source": {
                        "source": "local",
                        "path": "./plugins/future-plugin",
                    },
                    "policy": {
                        "installation": "AVAILABLE",
                        "authentication": "ON_INSTALL",
                    },
                    "category": "Developer Tools",
                }
            )
            marketplace_path.write_text(json.dumps(marketplace), encoding="utf-8")

            status, output = run_validator(root)

        self.assertEqual(status, 0, output)

    def test_marketplace_rejects_missing_plugin_entry_path(self) -> None:
        with copied_repo_fixture() as root:
            marketplace_path = root / ".agents" / "plugins" / "marketplace.json"
            marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
            marketplace["plugins"].append(
                {
                    "name": "missing-plugin",
                    "source": {
                        "source": "local",
                        "path": "./plugins/missing-plugin",
                    },
                    "policy": {
                        "installation": "AVAILABLE",
                        "authentication": "ON_INSTALL",
                    },
                    "category": "Developer Tools",
                }
            )
            marketplace_path.write_text(json.dumps(marketplace), encoding="utf-8")

            status, output = run_validator(root)

        self.assertEqual(status, 1, output)
        self.assertIn("missing required file: plugins/missing-plugin/.codex-plugin/plugin.json", output)

    def test_marketplace_rejects_non_kebab_plugin_name(self) -> None:
        with copied_repo_fixture() as root:
            marketplace_path = root / ".agents" / "plugins" / "marketplace.json"
            marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
            marketplace["plugins"][0]["name"] = "../goal-shaper"
            marketplace_path.write_text(json.dumps(marketplace), encoding="utf-8")

            status, output = run_validator(root)

        self.assertEqual(status, 1, output)
        self.assertIn("name must be kebab-case", output)

    def test_marketplace_must_point_to_packaged_plugin(self) -> None:
        with copied_repo_fixture() as root:
            marketplace_path = root / ".agents" / "plugins" / "marketplace.json"
            marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
            marketplace["plugins"][0]["source"]["path"] = "./wrong-plugin"
            marketplace_path.write_text(json.dumps(marketplace), encoding="utf-8")

            status, output = run_validator(root)

        self.assertEqual(status, 1, output)
        self.assertIn("source must point to ./plugins/goal-shaper", output)

    def test_empty_marketplace_fails(self) -> None:
        with copied_repo_fixture() as root:
            marketplace_path = root / ".agents" / "plugins" / "marketplace.json"
            marketplace_path.write_text("{}", encoding="utf-8")

            status, output = run_validator(root)

        self.assertEqual(status, 1, output)
        self.assertIn("expected non-empty JSON object", output)

    def test_manifest_version_must_have_changelog_heading(self) -> None:
        with copied_repo_fixture() as root:
            manifest_path = (
                root / "plugins" / "goal-shaper" / ".codex-plugin" / "plugin.json"
            )
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["version"] = "9.9.9"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            status, output = run_validator(root)

        self.assertEqual(status, 1, output)
        self.assertIn("CHANGELOG.md: missing heading for plugin version 9.9.9", output)

    def test_install_docs_must_match_marketplace_name(self) -> None:
        with copied_repo_fixture() as root:
            install_path = root / "INSTALL.md"
            install_path.write_text(
                install_path.read_text(encoding="utf-8").replace(
                    "goal-shaper@yohaku", "goal-shaper@wrong-market"
                ),
                encoding="utf-8",
            )

            status, output = run_validator(root)

        self.assertEqual(status, 1, output)
        self.assertIn("INSTALL.md: missing 'lifecycle command'", output)
        self.assertIn("codex plugin add goal-shaper@yohaku", output)

    def test_missing_required_skill_file_stops_before_deeper_checks(self) -> None:
        with copied_repo_fixture() as root:
            rubric = (
                root
                / "plugins"
                / "goal-shaper"
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
