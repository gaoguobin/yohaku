# Goal Shaper Scenario Tests

Use these manual scenarios before public releases and after meaningful skill
behavior changes. They test the user journey and output contract; they do not
replace `python3 scripts/validate_goal_shaper.py`.

## Installation And Lifecycle

| Scenario | Input Or Action | Expected Result |
| --- | --- | --- |
| App UI install | Open Codex App, select `Yohaku` or **Shared with you**, open **Goal Shaper**, then select **Add to Codex**. | Goal Shaper installs, a new thread can select it from composer suggestions, and only one plugin entry appears outside this repo. |
| CLI install | Run the command-line install flow from `INSTALL.md` in a clean profile or isolated `CODEX_HOME`. | `goal-shaper@yohaku` is installed and enabled with the current manifest version. |
| CLI update | Run the command-line update flow from `UPDATE.md` after publishing a newer version. | Marketplace refresh succeeds, reinstall shows the newer version, and a new thread loads the updated skill. |
| App UI uninstall | Uninstall Goal Shaper from the App plugin details page. | A new thread no longer shows the plugin-installed Goal Shaper entry. |
| CLI uninstall | Run the command-line uninstall flow from `UNINSTALL.md`. | The plugin is removed; removing `yohaku` also removes the marketplace source when it is no longer needed. |

## Goal Shaping Behavior

| Scenario | Prompt | Expected Result |
| --- | --- | --- |
| Too small | `Explain what this function does.` | No `/goal`; asks for a concrete file, selection, or snippet. |
| Too broad | `Modernize the whole project and fix tests, UI, deployment, and docs.` | No giant `/goal`; proposes smaller goal candidates. |
| Missing target | `Make the homepage faster.` | Asks for target page/project and verifier, or offers verifier choices before drafting. |
| High risk | `Clean old logs on the production server to free disk space.` | Produces a confirmation-gated audit/cleanup goal or asks for safety boundaries before any deletion. |
| Normal medium task | `Help me improve this repository's tests.` | Produces a copyable `/goal` with target, verifier, constraints, pause triggers, and evidence checklist. |
| Research task | `Determine whether this project should upgrade to React 19 and give me a conclusion.` | Produces a research goal with a final recommendation artifact and source requirements, not an implementation goal. |
| Failure recovery | `I ran the goal you generated, but the result was bad. Here is the final report...` | Separates prompt/package issues, model execution issues, and repo/tooling constraints before deciding whether to rewrite the goal. |

## Review Notes

- Record the prompt, selected choices, final Goal Shaper output, and whether the
  behavior matched the expected result.
- If a generated goal later fails, classify the failure as a goal
  prompt/package defect, a model execution issue, or a repo/tooling constraint.
- Do not treat model variance or missing project context as a Goal Shaper defect
  unless the package hid uncertainty, invented evidence, or missed a required
  safety boundary.
