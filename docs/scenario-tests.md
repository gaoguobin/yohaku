# Yohaku Scenario Tests

Use these manual scenarios before public releases and after meaningful skill,
metadata, or lifecycle-documentation changes. They test the user journey and
output contract; they do not replace `python3 scripts/validate_goal_shaper.py`.

## UI User Lifecycle

| Scenario | Input Or Action | Expected Result |
| --- | --- | --- |
| UI marketplace add | In Codex App, open **Plugins**, add marketplace source `gaoguobin/yohaku`, and restart the App if needed. | `Yohaku` appears as a marketplace source. |
| UI plugin list | Select `Yohaku`. | The marketplace can show multiple plugins, including Goal Shaper and Seed. |
| UI plugin install | Select `Yohaku`, open **Goal Shaper** or **Seed**, then select **Add to Codex**. | The selected plugin installs and shows the current release version. |
| UI slash entrypoint | In a new Codex App thread, type `/`, search for `Goal Shaper`, select the skill, and ask it to shape a short request. | The selected skill runs and produces the expected Goal Shaper behavior without relying on implicit invocation. |
| UI plugin entrypoint | In a new Codex App thread, type `@`, select the Yohaku plugin or its bundled Goal Shaper capability, and ask it to shape a short request. | Codex steers to the installed Yohaku plugin/capability and does not confuse marketplace selection with the request target. |
| UI skill mention | In a new Codex App thread, type `$goal-shaper` followed by a short request. | Goal Shaper is explicitly invoked and follows the same output contract as the slash entrypoint. |
| UI update check | After a newer release exists, restart Codex App and open the installed plugin details page. | The details page shows the newer version, then a new thread loads it. If it stays old after restart, use the CLI update flow from `UPDATE.md`. |
| UI plugin uninstall | Uninstall the selected Yohaku plugin from the App plugin details page. | A new thread no longer shows that plugin-installed entry. |
| UI marketplace removal | Remove `Yohaku` only after uninstalling or no longer needing every plugin from that marketplace. | Yohaku no longer appears as a marketplace source, and no installed Yohaku plugins are expected to remain available. |
| UI localized guides | Review `docs/ui-guide.en.md`, `docs/ui-guide.zh-CN.md`, and `docs/ui-guide.ja-JP.md` after screenshot or lifecycle changes. | The three guides describe the same UI lifecycle, link to existing screenshots, and do not contradict the canonical lifecycle docs. |

## CLI User Lifecycle

| Scenario | Input Or Action | Expected Result |
| --- | --- | --- |
| CLI marketplace add | Run `codex plugin marketplace add gaoguobin/yohaku --json` in a clean profile or isolated `CODEX_HOME`. | The `yohaku` marketplace is configured. |
| CLI plugin list | Run `codex plugin list --marketplace yohaku --available --json`. | Yohaku lists Goal Shaper and Seed, split between installed and available as appropriate. |
| CLI plugin install | Run `codex plugin add <plugin-name>@yohaku --json`. | The selected Yohaku plugin is installed and enabled with the current manifest version. |
| CLI update | Run the latest-channel update flow from `UPDATE.md` after publishing a newer version. | Marketplace refresh succeeds, reinstall shows the newer version, and a new thread loads the updated skill. |
| CLI pinned release | Run the pinned release flow from `INSTALL.md` or `UPDATE.md` with the selected tag. | The installed plugin resolves to the requested release tag version. |
| CLI plugin uninstall | Run `codex plugin remove <plugin-name>@yohaku --json`. | The plugin is removed while the `yohaku` marketplace can remain configured for other plugins. |
| CLI marketplace removal | Run `codex plugin marketplace remove yohaku --json` only when no Yohaku plugins are still needed. | The marketplace source is removed. |

## Goal Shaping Behavior

| Scenario | Prompt | Expected Result |
| --- | --- | --- |
| Too small | `Explain what this function does.` | No `/goal`; asks for a concrete file, selection, or snippet; does not explain the selected skill. |
| Too broad | `Modernize the whole project and fix tests, UI, deployment, and docs.` | No giant `/goal`; proposes smaller goal candidates. |
| Missing target | `Make the homepage faster.` | Asks for target page/project and verifier, or offers verifier choices before drafting. |
| High risk | `Clean old logs on the production server to free disk space.` | Produces a confirmation-gated audit/cleanup goal or asks for safety boundaries before any deletion. |
| Long context support spec | `Help me modernize this large project; write a support spec first if needed.` | Presents a support spec preview and asks before writing it; does not provide a copyable `/goal` that references an unwritten spec file. |
| Normal medium task | `Help me improve this repository's tests.` | Produces a copyable `/goal` with target, verifier, constraints, pause triggers, and evidence checklist. |
| Research task | `Determine whether this project should upgrade to React 19 and give me a conclusion.` | Produces a research goal with a final recommendation artifact and source requirements, not an implementation goal. |
| Failure recovery | `I ran the goal you generated, but the result was bad. Here is the final report...` | Separates prompt/package issues, model execution issues, and repo/tooling constraints before deciding whether to rewrite the goal. |

## Seed Behavior

| Scenario | Prompt | Expected Result |
| --- | --- | --- |
| Too small | `Explain what this short helper function does.` | Does not force a spec; gives a normal answer or asks for the missing code target. |
| Decision shaping | `Help me decide whether this should be a CLI or a web UI before we build it.` | Produces or drafts a decision artifact with options, recommendation, trade-offs, and review gate. |
| Lightweight spec | `I want a small settings page; think it through before coding.` | Produces a concise spec with scope, requirements, validation, and stop condition. |
| Complex implementation handoff | `Plan how we should migrate this service safely, but do not code yet.` | Offers or produces a reviewed Writing Plan only after the spec/decision is coherent; does not start implementation. |
| Seed-to-Goal boundary | `Now turn this Seed spec into a /goal.` | Stops and tells the user to use Goal Shaper with the reviewed artifact; Seed itself does not emit a runnable `/goal`. |
| Quality kernel scope | `Summarize this research idea before I discuss it with the team.` | Does not inject implementation anti-bloat rules unless the artifact will guide implementation work. |

## Review Notes

- Record the prompt, selected choices, final Goal Shaper output, and whether the
  behavior matched the expected result.
- If a generated goal later fails, classify the failure as a goal
  prompt/package defect, a model execution issue, or a repo/tooling constraint.
- Do not treat model variance or missing project context as a Goal Shaper defect
  unless the package hid uncertainty, invented evidence, or missed a required
  safety boundary.
