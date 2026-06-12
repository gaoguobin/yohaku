#!/usr/bin/env python3
"""Validate the goal-shaper skill package.

This is intentionally small and dependency-free. It catches structural drift,
missing safety rules, and scenario-specific hardcoding without trying to judge
the full quality of model output.
"""

from __future__ import annotations

import re
import sys
import json
import filecmp
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT_SKILL_DIR = ROOT / ".agents" / "skills" / "goal-shaper"
PLUGIN_DIR = ROOT / "plugins" / "goal-shaper"
PLUGIN_SKILL_DIR = PLUGIN_DIR / "skills" / "goal-shaper"
SKILL_DIR = PROJECT_SKILL_DIR
MARKETPLACE_PATH = ROOT / ".agents" / "plugins" / "marketplace.json"
PLUGIN_MANIFEST_PATH = PLUGIN_DIR / ".codex-plugin" / "plugin.json"

REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/goal-schema.md",
    "references/rubric.md",
    "references/examples.md",
    "templates/goal-package.md",
    "templates/support-spec.md",
]

CANONICAL_FIELDS = [
    "outcome",
    "verification_surface",
    "constraints",
    "boundaries",
    "iteration_policy",
    "blocked_stop_condition",
    "initial_materials",
    "validation_and_review",
    "checkpoint_policy",
    "pause_triggers",
]

EXAMPLE_SECTIONS = [
    "Too Small",
    "Too Broad",
    "Bug Fix",
    "Performance",
    "Research",
    "High Risk",
    "Long Context",
    "Durable Guidance",
]

PACKAGE_SECTIONS = [
    "Conclusion",
    "Runnable Goal",
    "Evidence Checklist",
    "Assumptions",
    "Durable Guidance Candidates",
]

SUPPORT_SPEC_SECTIONS = [
    "Context",
    "Objective",
    "Initial Materials",
    "Acceptance Checks",
    "Boundaries",
    "Constraints",
    "Milestones And Checkpoints",
    "Iteration Policy",
    "Safety And Permission Policy",
    "Blocker Policy",
    "Decision Log",
    "Recovery Notes",
    "Final Report Format",
]

SCENARIO_HARDCODING = [
    "sample-js-app",
    "React 19",
    "homepage",
    "old logs",
    "production server",
    "login failure",
]

PLUGIN_REQUIRED_FIELDS = [
    "name",
    "version",
    "description",
    "author",
    "skills",
    "interface",
]

PLUGIN_INTERFACE_FIELDS = [
    "displayName",
    "shortDescription",
    "longDescription",
    "developerName",
    "category",
    "capabilities",
    "defaultPrompt",
]


def read(relative: str) -> str:
    return (SKILL_DIR / relative).read_text(encoding="utf-8")


def fail(failures: list[str], message: str) -> None:
    failures.append(message)


def require_contains(
    failures: list[str], text: str, needle: str, where: str, why: str
) -> None:
    if needle not in text:
        fail(failures, f"{where}: missing {why!r} ({needle})")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}

    end = text.find("\n---\n", 4)
    if end == -1:
        return {}

    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields


def load_json(relative_path: Path, failures: list[str]) -> dict:
    try:
        payload = json.loads(relative_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(failures, f"missing required file: {relative_path.relative_to(ROOT)}")
        return {}
    except json.JSONDecodeError as exc:
        fail(failures, f"{relative_path.relative_to(ROOT)}: invalid JSON: {exc}")
        return {}
    if not isinstance(payload, dict):
        fail(failures, f"{relative_path.relative_to(ROOT)}: expected JSON object")
        return {}
    return payload


def validate_required_files(failures: list[str]) -> None:
    if not SKILL_DIR.exists():
        fail(failures, f"missing skill directory: {SKILL_DIR}")
        return

    for relative in REQUIRED_FILES:
        path = SKILL_DIR / relative
        if not path.is_file():
            fail(failures, f"missing required skill file: {relative}")

    for path in [PLUGIN_MANIFEST_PATH, MARKETPLACE_PATH]:
        if not path.is_file():
            fail(failures, f"missing required file: {path.relative_to(ROOT)}")


def validate_plugin_skill_sync(failures: list[str]) -> None:
    if PROJECT_SKILL_DIR.is_symlink():
        fail(failures, ".agents/skills/goal-shaper must be a real directory, not a symlink")
        return

    if not PROJECT_SKILL_DIR.is_dir():
        fail(failures, ".agents/skills/goal-shaper must exist as the project skill")
        return
    if not PLUGIN_SKILL_DIR.is_dir():
        fail(failures, "plugins/goal-shaper/skills/goal-shaper must exist as the packaged skill")
        return

    comparison = filecmp.dircmp(PROJECT_SKILL_DIR, PLUGIN_SKILL_DIR)
    mismatches: list[str] = []

    def collect_diff(diff: filecmp.dircmp, prefix: Path) -> None:
        for name in diff.left_only:
            mismatches.append(f"project-only: {(prefix / name).as_posix()}")
        for name in diff.right_only:
            mismatches.append(f"plugin-only: {(prefix / name).as_posix()}")
        for name in diff.diff_files:
            mismatches.append(f"content differs: {(prefix / name).as_posix()}")
        for name, subdiff in diff.subdirs.items():
            collect_diff(subdiff, prefix / name)

    collect_diff(comparison, Path("."))
    if mismatches:
        fail(
            failures,
            "project skill and packaged skill differ: " + "; ".join(mismatches[:8]),
        )


def validate_ascii_and_size(failures: list[str]) -> None:
    total_lines = 0
    for relative in REQUIRED_FILES:
        path = SKILL_DIR / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        total_lines += len(text.splitlines())
        non_ascii = [char for char in text if ord(char) > 127]
        if non_ascii:
            fail(failures, f"{relative}: contains non-ASCII text")

    skill_lines = len(read("SKILL.md").splitlines())
    if skill_lines > 220:
        fail(failures, f"SKILL.md is too large for progressive disclosure: {skill_lines} lines")
    if total_lines > 1_200:
        fail(failures, f"skill package is likely bloated: {total_lines} total lines")


def validate_skill_entrypoint(failures: list[str]) -> None:
    text = read("SKILL.md")
    frontmatter = parse_frontmatter(text)

    if frontmatter.get("name") != "goal-shaper":
        fail(failures, "SKILL.md: frontmatter name must be goal-shaper")

    description = frontmatter.get("description", "")
    for phrase in [
        "rough or fuzzy user requests",
        "Codex Goal mode packages",
        "do not run the goal",
    ]:
        if phrase not in description:
            fail(failures, f"SKILL.md: description missing trigger/boundary phrase: {phrase}")

    for resource in [
        "references/goal-schema.md",
        "references/rubric.md",
        "templates/goal-package.md",
        "templates/support-spec.md",
        "references/examples.md",
    ]:
        require_contains(failures, text, resource, "SKILL.md", "load resource")

    for boundary in [
        "Do not run `/goal`",
        "call runtime goal tools",
        "start\nimplementation",
        "create commits",
        "modify repository ignore rules",
        "Do not treat this skill's own instructions or files as the user's target",
        "Do not invent exact validation commands",
        "Always separate one-time goal constraints from durable guidance",
        "Present the final package and stop",
    ]:
        require_contains(failures, text, boundary, "SKILL.md", "core boundary")

    for level in ["small", "medium", "large", "too_broad"]:
        require_contains(failures, text, f"`{level}`", "SKILL.md", "complexity level")


def validate_schema(failures: list[str]) -> None:
    text = read("references/goal-schema.md")
    for field in CANONICAL_FIELDS:
        require_contains(failures, text, f"`{field}`", "goal-schema.md", "canonical field")

    for phrase in [
        "durable objective",
        "evidence-based finish line",
        "normal prompt",
        "Recommend decomposition",
    ]:
        require_contains(failures, text, phrase, "goal-schema.md", "suitability policy")


def validate_rubric(failures: list[str]) -> None:
    text = read("references/rubric.md")
    for phrase in [
        "`outcome` must score 2",
        "`verification_surface` must score 2",
        "under 4,000 characters",
        "Do not invent",
        "Performance goals that invent",
        "A support spec for a tiny one-off task",
        "The final response stops after the package",
    ]:
        require_contains(failures, text, phrase, "rubric.md", "rubric rule")


def validate_templates(failures: list[str]) -> None:
    goal_template = read("templates/goal-package.md")
    for section in PACKAGE_SECTIONS:
        require_contains(failures, goal_template, section, "goal-package.md", "package section")
    require_contains(failures, goal_template, "/goal <English goal", "goal-package.md", "copyable goal")
    require_contains(
        failures,
        goal_template,
        "Recommended Normal Prompt",
        "goal-package.md",
        "non-goal fallback",
    )

    support_template = read("templates/support-spec.md")
    require_contains(
        failures,
        support_template,
        "Use this template only for `large` requests",
        "support-spec.md",
        "support-spec gate",
    )
    require_contains(
        failures,
        support_template,
        "Ask for confirmation before writing the file",
        "support-spec.md",
        "write confirmation",
    )
    for section in SUPPORT_SPEC_SECTIONS:
        require_contains(failures, support_template, f"## {section}", "support-spec.md", "spec section")


def validate_examples(failures: list[str]) -> None:
    text = read("references/examples.md")
    for section in EXAMPLE_SECTIONS:
        require_contains(failures, text, f"## {section}", "examples.md", "example section")

    for phrase in [
        "Use these as patterns, not as fixed templates",
        "Do not generate `/goal`",
        "Do not generate one giant goal",
        "propose verifier\noptions instead of inventing commands",
        "Always use pnpm",
    ]:
        require_contains(failures, text, phrase, "examples.md", "example guidance")


def validate_agent_metadata(failures: list[str]) -> None:
    text = read("agents/openai.yaml")
    for phrase in [
        'display_name: "Goal Shaper"',
        'short_description: "Shape fuzzy requests into Codex goals"',
        "default_prompt:",
    ]:
        require_contains(failures, text, phrase, "openai.yaml", "interface metadata")


def validate_plugin_manifest(failures: list[str]) -> None:
    manifest = load_json(PLUGIN_MANIFEST_PATH, failures)
    if not manifest:
        return

    for field in PLUGIN_REQUIRED_FIELDS:
        if field not in manifest:
            fail(failures, f"plugin.json: missing required field `{field}`")

    if manifest.get("name") != "goal-shaper":
        fail(failures, "plugin.json: `name` must be `goal-shaper`")
    if manifest.get("skills") != "./skills/":
        fail(failures, "plugin.json: `skills` must be `./skills/`")

    version = manifest.get("version")
    if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", version):
        fail(failures, "plugin.json: `version` must be semver-like")

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        fail(failures, "plugin.json: `interface` must be an object")
        return

    for field in PLUGIN_INTERFACE_FIELDS:
        if field not in interface:
            fail(failures, f"plugin.json: missing interface field `{field}`")

    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        fail(failures, "plugin.json: `interface.defaultPrompt` must contain 1 to 3 prompts")
    elif any(not isinstance(prompt, str) or not prompt.strip() or len(prompt) > 128 for prompt in prompts):
        fail(failures, "plugin.json: each default prompt must be a non-empty string <= 128 chars")

    unsupported = {"apps", "mcpServers", "hooks"} & set(manifest)
    if unsupported:
        fail(failures, f"plugin.json: unsupported or unnecessary fields present: {sorted(unsupported)}")


def validate_marketplace(failures: list[str]) -> None:
    marketplace = load_json(MARKETPLACE_PATH, failures)
    if not marketplace:
        return

    if marketplace.get("name") != "goal-shaper-local":
        fail(failures, "marketplace.json: `name` must be `goal-shaper-local`")

    interface = marketplace.get("interface")
    if not isinstance(interface, dict) or interface.get("displayName") != "Goal Shaper Local":
        fail(failures, "marketplace.json: `interface.displayName` must be `Goal Shaper Local`")

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        fail(failures, "marketplace.json: expected exactly one plugin entry")
        return

    entry = plugins[0]
    expected = {
        "name": "goal-shaper",
        "category": "Developer Tools",
    }
    for key, value in expected.items():
        if entry.get(key) != value:
            fail(failures, f"marketplace.json: plugin `{key}` must be `{value}`")

    source = entry.get("source")
    if not isinstance(source, dict) or source.get("source") != "local" or source.get("path") != "./plugins/goal-shaper":
        fail(failures, "marketplace.json: source must point to ./plugins/goal-shaper")

    policy = entry.get("policy")
    if not isinstance(policy, dict):
        fail(failures, "marketplace.json: plugin policy must be an object")
        return
    if policy.get("installation") != "AVAILABLE":
        fail(failures, "marketplace.json: policy.installation must be AVAILABLE")
    if policy.get("authentication") != "ON_INSTALL":
        fail(failures, "marketplace.json: policy.authentication must be ON_INSTALL")


def validate_no_scenario_hardcoding(failures: list[str]) -> None:
    combined = "\n".join(read(relative) for relative in REQUIRED_FILES if relative != "agents/openai.yaml")
    for phrase in SCENARIO_HARDCODING:
        if re.search(re.escape(phrase), combined, re.IGNORECASE):
            fail(failures, f"scenario-specific hardcoding found: {phrase}")


def main() -> int:
    failures: list[str] = []
    validate_required_files(failures)
    if failures:
        for item in failures:
            print(f"FAIL {item}")
        return 1

    validate_plugin_skill_sync(failures)
    validate_ascii_and_size(failures)
    validate_skill_entrypoint(failures)
    validate_schema(failures)
    validate_rubric(failures)
    validate_templates(failures)
    validate_examples(failures)
    validate_agent_metadata(failures)
    validate_plugin_manifest(failures)
    validate_marketplace(failures)
    validate_no_scenario_hardcoding(failures)

    if failures:
        print(f"goal-shaper validation failed: {len(failures)} issue(s)")
        for item in failures:
            print(f"FAIL {item}")
        return 1

    print("goal-shaper validation passed")
    print(f"checked {len(REQUIRED_FILES)} skill files under {SKILL_DIR}")
    print(f"checked packaged skill sync under {PLUGIN_SKILL_DIR}")
    print(f"checked plugin manifest under {PLUGIN_MANIFEST_PATH}")
    print(f"checked repo marketplace under {MARKETPLACE_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
