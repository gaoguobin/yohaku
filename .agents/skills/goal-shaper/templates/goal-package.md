# Compact Goal Package Template

Use this template for `small` and `medium` requests.

## Response Shape

Use the user's language for headings and explanations. Keep the `/goal` in
English unless the user explicitly asks otherwise.

````markdown
**Conclusion**
<User-language summary of whether Goal mode fits and why.>

**Runnable Goal**
```text
/goal <English goal under 4,000 characters>
```

**Evidence Checklist**
- <Evidence that should prove completion>
- <Validation or review surface>

**Assumptions**
- <Explicit low-risk assumptions, or "None">

**Durable Guidance Candidates**
- <Rules that belong in AGENTS.md, a skill, config, or team docs, or "None">
````

## If Goal Mode Is Not Appropriate

Use this shape instead:

````markdown
**Conclusion**
This request is not a good fit for Goal mode: <reason>.

**Recommended Normal Prompt**
```text
<A concise normal Codex prompt>
```

**Reason**
- <Why it is too small, too broad, or lacks verification>
````

## Constraints

- Keep the `/goal` command copyable.
- Keep user-facing explanation concise.
- Do not add implementation steps beyond what is needed for the goal contract.
- Do not tell the user the goal has been run.
