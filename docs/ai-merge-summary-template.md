# AI Merge Summary Template

Use this summary before deciding whether a PR is safe to merge.

## PR summary

- PR title:
- Author/tool:
- Change type:
- Files changed:
- CI status:
- Review status:

## What changed

Briefly summarize the change in plain language.

## Review findings

- CodeRabbit findings:
- Claude findings, if any:
- Human findings, if any:

## Autofix status

- Autofix used:
- Autofix mode:
- Stacked PR link:
- Current branch modified directly: yes/no

Current branch Autofix is not allowed during the initial evaluation phase.

## Risk checklist

Answer yes/no.

- Docs/test/lint only:
- Code changed:
- Business logic changed:
- GitHub Actions changed:
- Secrets/tokens/keys changed:
- Dependencies changed:
- Trading bot touched:
- Automation platform logic added:
- Custom parser/controller/validator/sandbox added:
- CI passed:
- Unresolved review findings remain:

## Risk grade

Choose one:

- A — Auto-merge candidate later
- B — Summary approval required
- C — Detailed judgment required
- D — STOP / escalate to Strategy PM

## Final recommendation

Merge / do not merge / escalate.
