# Changelog

## Unreleased

- Add Seed as a second Yohaku marketplace plugin.
- Validate marketplace entries as real local plugin packages instead of only
  checking the Goal Shaper entry.
- Update public docs to describe Yohaku as a multi-plugin marketplace.
- Generalize localized UI guides for installing and invoking any Yohaku plugin.
- Upgrade Seed 0.1.5 to support decision artifacts, optional reviewed Writing
  Plans, and conditional implementation-quality guidance without starting
  implementation.
- Switch Yohaku to a plugin-first repository layout by removing the duplicate
  Goal Shaper project skill entry and validating the packaged plugin skill as
  the canonical source.

## 0.1.8 - 2026-06-18

- Guard large support-spec flows so Goal Shaper does not present a copyable
  `/goal` that references an unwritten support spec file.
- Make Codex App update guidance conservative: restart and check the plugin
  details page, then use the CLI update flow if the version stays old.
- Add regression coverage for the unwritten support-spec guard.

## 0.1.7 - 2026-06-17

- Add English, Simplified Chinese, and Japanese Codex App UI guides with real
  marketplace, plugin detail, and composer entrypoint screenshots.
- Clarify the UI guide distinction between `/`, `@`, and `$` entrypoints for
  installed Yohaku plugins and bundled skills.
- Update Goal Shaper starter prompts to sound like realistic user actions
  rather than abstract product copy.

## 0.1.6 - 2026-06-17

- Clarify that users should copy only the `/goal` code block to run a shaped
  goal, while the evidence, assumptions, and durable guidance sections are for
  review.
- Require execution-critical constraints to appear inside the `/goal`, not only
  in review sections.
- Clarify that selecting or invoking Goal Shaper is not target selection, so
  missing function/code targets ask for the target without explaining the
  selected skill.
- Add validator and unittest guardrails for these output and missing-target
  boundaries.

## 0.1.5 - 2026-06-16

- Rename the public marketplace source from `gaoguobin/goal-shaper` to
  `gaoguobin/yohaku` so Codex App marketplace source input matches the Yohaku
  marketplace identity.
- Update plugin metadata, install docs, update docs, and release checks to use
  the Yohaku marketplace repository.

## 0.1.4 - 2026-06-16

- Rename the repo marketplace catalog to `yohaku`.
- Add plugin icon, website, privacy, and terms metadata.
- Keep the Yohaku catalog extensible by validating the `goal-shaper` entry
  without rejecting future sibling plugins.
- Add public release, install, update, uninstall, security, and contribution
  documentation.
- Add GitHub Actions validation for tests and repository guardrails.

## 0.1.3 - 2026-06-16

- Add website metadata and water-ink brand color.
- Use `verifiable` wording for plugin presentation.

## 0.1.2 - 2026-06-16

- Add initial plugin icon metadata and local App smoke validation.

## 0.1.1 - 2026-06-15

- Add dependency-free unittest coverage for validator and packaging guardrails.

## 0.1.0 - 2026-06-12

- Initial Goal Shaper skill and Codex plugin package.
