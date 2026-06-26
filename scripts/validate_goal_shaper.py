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
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_DIR = ROOT / "plugins" / "goal-shaper"
PLUGIN_SKILL_DIR = PLUGIN_DIR / "skills" / "goal-shaper"
SEED_PLUGIN_DIR = ROOT / "plugins" / "seed"
SEED_SKILL_DIR = SEED_PLUGIN_DIR / "skills" / "seed"
SEED_PLUGIN_MANIFEST_PATH = SEED_PLUGIN_DIR / ".codex-plugin" / "plugin.json"
SKILL_DIR = PLUGIN_SKILL_DIR
MARKETPLACE_PATH = ROOT / ".agents" / "plugins" / "marketplace.json"
PLUGIN_MANIFEST_PATH = PLUGIN_DIR / ".codex-plugin" / "plugin.json"
CHANGELOG_PATH = ROOT / "CHANGELOG.md"

REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/goal-schema.md",
    "references/rubric.md",
    "references/examples.md",
    "templates/goal-package.md",
    "templates/support-spec.md",
]

RELEASE_FILES = [
    "README.md",
    "INSTALL.md",
    "UPDATE.md",
    "UNINSTALL.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "LICENSE",
    "docs/plugin.md",
    "docs/privacy.md",
    "docs/terms.md",
    "docs/validation.md",
    "docs/release-checklist.md",
    "docs/scenario-tests.md",
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

PLUGIN_REQUIRED_FIELDS = [
    "name",
    "version",
    "description",
    "author",
    "license",
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
    "websiteURL",
    "privacyPolicyURL",
    "termsOfServiceURL",
    "composerIcon",
    "logo",
]


def read(relative: str) -> str:
    return (SKILL_DIR / relative).read_text(encoding="utf-8")


def fail(failures: list[str], message: str) -> None:
    failures.append(message)


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def require_contains(
    failures: list[str], text: str, needle: str, where: str, why: str
) -> None:
    if normalize_text(needle) not in normalize_text(text):
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
    if not payload:
        fail(
            failures,
            f"{relative_path.relative_to(ROOT)}: expected non-empty JSON object",
        )
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

    for relative in RELEASE_FILES:
        path = ROOT / relative
        if not path.is_file():
            fail(failures, f"missing required release file: {relative}")


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
        "verifiable Codex Goal mode packages",
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
        "start implementation",
        "create commits",
        "modify repository ignore rules",
        "Selecting or invoking this skill is not target selection",
        "Do not treat this skill's own instructions or files as the user's target",
        "Do not add a fallback explanation of this skill",
        "without explaining the selected skill",
        "Do not invent exact validation commands",
        "Separate prompt/package issues, model execution issues, and repo/tooling constraints",
        "copy only the `/goal` code block",
        "execution-critical constraints are inside the `/goal`",
        "Always separate one-time goal constraints from durable guidance",
        "Do not carry it forward from examples",
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
        "traceable to the current request or target evidence",
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
        "Copy only the `/goal` code block to run it",
        "goal-package.md",
        "copy instruction",
    )
    require_contains(
        failures,
        goal_template,
        "Do not leave execution-critical constraints only in the review sections",
        "goal-package.md",
        "execution constraint placement",
    )
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
    require_contains(
        failures,
        support_template,
        "Before the support spec file exists, do not include a copyable `/goal` block",
        "support-spec.md",
        "unwritten spec guard",
    )
    require_contains(
        failures,
        support_template,
        "After the support spec has been written, provide the final runnable goal",
        "support-spec.md",
        "post-write runnable goal",
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
        "Do not add an optional fallback explanation of the selected skill",
        "propose verifier options instead of inventing commands",
        "repository's package manager",
        "If no durable rule is explicit in the current request or target evidence",
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


def validate_seed_skill_contract(failures: list[str]) -> None:
    skill_path = SEED_SKILL_DIR / "SKILL.md"
    if not skill_path.is_file():
        fail(failures, f"missing required file: {skill_path.relative_to(ROOT)}")
        return

    text = skill_path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text)
    if frontmatter.get("name") != "seed":
        fail(failures, "seed SKILL.md: frontmatter name must be seed")

    description = frontmatter.get("description", "")
    for phrase in [
        "reviewed specs",
        "decision artifacts",
        "optional Writing Plans",
        "stop after the reviewed artifact",
        "do not code",
    ]:
        if phrase not in description:
            fail(failures, f"seed SKILL.md: description missing trigger/boundary phrase: {phrase}")

    for boundary in [
        "Seed owns the spec or decision artifact",
        "Goal Shaper owns the later `/goal` package",
        "Do NOT invoke implementation skills",
        "call Goal Shaper",
        "run `/goal`",
        "Stop after the reviewed artifact",
        "A Writing Plan is a handoff artifact, not an execution mode",
        "not approval to begin that handoff automatically",
        "Do not produce a Writing Plan before the spec or decision is coherent",
        "Choose the smallest artifact",
        "Decision note",
        "Lightweight spec",
        "Full spec / PRD / design doc",
        "Writing Plan",
        "If the request is too broad for one artifact",
        "do not force a spec",
        "Apply this kernel only when the artifact will guide implementation",
        "Do not apply it to pure explanation",
        "Prefer standard library, platform-native features",
        "Do not include a runnable `/goal` in Seed",
        "The terminal state is delivering the reviewed artifact",
    ]:
        require_contains(failures, text, boundary, "seed SKILL.md", "seed contract")


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
    if manifest.get("license") != "MIT":
        fail(failures, "plugin.json: `license` must be `MIT`")

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

    for field, expected in {
        "websiteURL": "https://github.com/gaoguobin/yohaku",
        "privacyPolicyURL": "https://github.com/gaoguobin/yohaku/blob/main/docs/privacy.md",
        "termsOfServiceURL": "https://github.com/gaoguobin/yohaku/blob/main/docs/terms.md",
        "brandColor": "#1F1B16",
    }.items():
        if interface.get(field) != expected:
            fail(failures, f"plugin.json: `interface.{field}` must be `{expected}`")

    for field, expected_path in {
        "composerIcon": "./assets/icon.png",
        "logo": "./assets/icon.png",
    }.items():
        if interface.get(field) != expected_path:
            fail(failures, f"plugin.json: `interface.{field}` must be `{expected_path}`")
            continue
        if not (PLUGIN_DIR / expected_path[2:]).is_file():
            fail(failures, f"plugin.json: `interface.{field}` points to a missing file")

    unsupported = {"apps", "mcpServers", "hooks"} & set(manifest)
    if unsupported:
        fail(failures, f"plugin.json: unsupported or unnecessary fields present: {sorted(unsupported)}")


def validate_seed_plugin_manifest(failures: list[str]) -> None:
    manifest = load_json(SEED_PLUGIN_MANIFEST_PATH, failures)
    if not manifest:
        return

    if manifest.get("name") != "seed":
        fail(failures, "seed plugin.json: `name` must be `seed`")
    if manifest.get("skills") != "./skills/":
        fail(failures, "seed plugin.json: `skills` must be `./skills/`")

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        fail(failures, "seed plugin.json: `interface` must be an object")
        return

    for field in ["displayName", "shortDescription", "longDescription", "defaultPrompt", "composerIcon", "logo"]:
        if field not in interface:
            fail(failures, f"seed plugin.json: missing interface field `{field}`")

    long_description = interface.get("longDescription")
    if isinstance(long_description, str):
        for phrase in ["reviewed spec or decision artifact", "Writing Plan", "stop before coding"]:
            if phrase not in long_description:
                fail(failures, f"seed plugin.json: longDescription missing `{phrase}`")

    for field, expected_path in {
        "composerIcon": "./assets/icon.png",
        "logo": "./assets/icon.png",
    }.items():
        if interface.get(field) != expected_path:
            fail(failures, f"seed plugin.json: `interface.{field}` must be `{expected_path}`")
            continue
        if not (SEED_PLUGIN_DIR / expected_path[2:]).is_file():
            fail(failures, f"seed plugin.json: `interface.{field}` points to a missing file")

    unsupported = {"apps", "mcpServers", "hooks"} & set(manifest)
    if unsupported:
        fail(failures, f"seed plugin.json: unsupported or unnecessary fields present: {sorted(unsupported)}")


def validate_marketplace(failures: list[str]) -> None:
    marketplace = load_json(MARKETPLACE_PATH, failures)
    if not marketplace:
        return

    if marketplace.get("name") != "yohaku":
        fail(failures, "marketplace.json: `name` must be `yohaku`")

    interface = marketplace.get("interface")
    if not isinstance(interface, dict) or interface.get("displayName") != "Yohaku":
        fail(failures, "marketplace.json: `interface.displayName` must be `Yohaku`")

    plugin_entries = marketplace.get("plugins")
    if not isinstance(plugin_entries, list):
        fail(failures, "marketplace.json: `plugins` must be a list")
        return

    for index, entry in enumerate(plugin_entries):
        validate_marketplace_entry(failures, entry, index)

    matching_entries = [
        entry
        for entry in plugin_entries
        if isinstance(entry, dict) and entry.get("name") == "goal-shaper"
    ]
    if len(matching_entries) != 1:
        fail(failures, "marketplace.json: expected exactly one goal-shaper plugin entry")
        return

    entry = matching_entries[0]
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


def validate_marketplace_entry(failures: list[str], entry: object, index: int) -> None:
    if not isinstance(entry, dict):
        fail(failures, f"marketplace.json: plugin entry {index} must be an object")
        return

    name = entry.get("name")
    if not isinstance(name, str) or not name.strip():
        fail(failures, f"marketplace.json: plugin entry {index} must have a name")
        return
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        fail(failures, f"marketplace.json: plugin `{name}` name must be kebab-case")
        return

    if entry.get("category") != "Developer Tools":
        fail(failures, f"marketplace.json: plugin `{name}` category must be Developer Tools")

    source = entry.get("source")
    expected_path = f"./plugins/{name}"
    if (
        not isinstance(source, dict)
        or source.get("source") != "local"
        or source.get("path") != expected_path
    ):
        fail(failures, f"marketplace.json: source must point to {expected_path}")
        return

    plugin_root = ROOT / expected_path[2:]
    manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    manifest = load_json(manifest_path, failures)
    if manifest and manifest.get("name") != name:
        fail(failures, f"marketplace.json: plugin `{name}` manifest name must match entry")

    policy = entry.get("policy")
    if not isinstance(policy, dict):
        fail(failures, f"marketplace.json: plugin `{name}` policy must be an object")
        return
    if policy.get("installation") != "AVAILABLE":
        fail(failures, f"marketplace.json: plugin `{name}` policy.installation must be AVAILABLE")
    if policy.get("authentication") != "ON_INSTALL":
        fail(failures, f"marketplace.json: plugin `{name}` policy.authentication must be ON_INSTALL")


def validate_release_metadata(failures: list[str]) -> None:
    manifest = load_json(PLUGIN_MANIFEST_PATH, failures)
    marketplace = load_json(MARKETPLACE_PATH, failures)
    if not manifest or not marketplace:
        return

    version = manifest.get("version")
    changelog = CHANGELOG_PATH.read_text(encoding="utf-8")
    if isinstance(version, str) and f"## {version} -" not in changelog:
        fail(failures, f"CHANGELOG.md: missing heading for plugin version {version}")

    plugin_name = manifest.get("name")
    marketplace_name = marketplace.get("name")
    repository = manifest.get("repository", "")
    repo_match = re.fullmatch(r"https://github\.com/([^/\s]+/[^/\s]+?)(?:\.git)?", repository)
    if not repo_match:
        fail(failures, "plugin.json: `repository` must be a GitHub repository URL")
        return

    repo_shorthand = repo_match.group(1)
    plugin_selector = f"{plugin_name}@{marketplace_name}"
    expected_commands = {
        "INSTALL.md": [
            f"codex plugin marketplace add {repo_shorthand} --json",
            f"codex plugin list --marketplace {marketplace_name} --available --json",
            f"codex plugin add {plugin_selector} --json",
        ],
        "README.md": [
            f"codex plugin marketplace add {repo_shorthand} --json",
            f"codex plugin add {plugin_selector} --json",
        ],
        "UPDATE.md": [
            f"codex plugin marketplace upgrade {marketplace_name} --json",
            f"codex plugin add {plugin_selector} --json",
        ],
        "UNINSTALL.md": [
            f"codex plugin remove {plugin_selector} --json",
            f"codex plugin marketplace remove {marketplace_name} --json",
        ],
        "docs/plugin.md": [
            f"codex plugin marketplace add {repo_shorthand} --json",
            f"codex plugin add {plugin_selector} --json",
            f"codex plugin remove {plugin_selector} --json",
        ],
    }
    for relative, commands in expected_commands.items():
        text = (ROOT / relative).read_text(encoding="utf-8")
        for command in commands:
            require_contains(failures, text, command, relative, "lifecycle command")

    stale_markers = ["goal-shaper-local", "codex plugin install"]
    for relative in ["README.md", "INSTALL.md", "UPDATE.md", "UNINSTALL.md", "docs/plugin.md"]:
        text = (ROOT / relative).read_text(encoding="utf-8")
        for marker in stale_markers:
            if marker in text:
                fail(failures, f"{relative}: stale lifecycle marker `{marker}` must not appear")


def main() -> int:
    failures: list[str] = []
    validate_required_files(failures)
    if failures:
        for item in failures:
            print(f"FAIL {item}")
        return 1

    validate_ascii_and_size(failures)
    validate_skill_entrypoint(failures)
    validate_schema(failures)
    validate_rubric(failures)
    validate_templates(failures)
    validate_examples(failures)
    validate_agent_metadata(failures)
    validate_seed_skill_contract(failures)
    validate_plugin_manifest(failures)
    validate_seed_plugin_manifest(failures)
    validate_marketplace(failures)
    validate_release_metadata(failures)

    if failures:
        print(f"goal-shaper validation failed: {len(failures)} issue(s)")
        for item in failures:
            print(f"FAIL {item}")
        return 1

    print("goal-shaper validation passed")
    print(f"checked {len(REQUIRED_FILES)} skill files under {SKILL_DIR}")
    print(f"checked plugin manifest under {PLUGIN_MANIFEST_PATH}")
    print(f"checked Seed plugin contract under {SEED_SKILL_DIR}")
    print(f"checked repo marketplace under {MARKETPLACE_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
