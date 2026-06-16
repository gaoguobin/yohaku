# Security Policy

Goal Shaper is a local Codex skill and plugin package. It does not require
external service credentials and does not bundle apps, MCP servers, or hooks.

## Reporting

Report security issues privately to the repository owner before opening a
public issue. If the GitHub repository is public, use GitHub private
vulnerability reporting when available.

If private vulnerability reporting is unavailable, open a public issue that
does not include secrets or exploit details and ask for a private contact path.

## Supported Versions

Only the latest released version is supported before `1.0.0`.

## Expectations

- Do not include secrets, tokens, cookies, or production credentials in issues,
  logs, screenshots, or test fixtures.
- Production, deletion, migration, credential, and external-write scenarios
  should remain confirmation-gated in Goal Shaper output.
