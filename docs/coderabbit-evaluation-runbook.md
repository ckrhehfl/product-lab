# CodeRabbit Evaluation Runbook

This runbook defines the first safe evaluation flow for CodeRabbit in product-lab.

## Purpose

The goal is to evaluate CodeRabbit as a specialist PR review and Autofix tool without building a custom review-fix automation platform.

This evaluation is intentionally limited to low-risk PRs.

## Initial evaluation scope

Allowed initial PR types:

- documentation-only changes
- test-only changes
- lint-only changes

Not allowed during the initial evaluation:

- production logic changes
- trading bot changes
- dependency additions
- GitHub Actions permission changes
- secrets, tokens, or keys
- branch protection changes
- auto-merge changes
- custom parser, controller, validator, sandbox, orchestrator, or merge bot logic

## Expected flow

The initial flow is:

1. Create a small docs-only or tests-only PR.
2. Let CI run.
3. Let CodeRabbit review the PR.
4. Do not use Autofix immediately.
5. Implementation PM reviews the CodeRabbit result.
6. If Autofix is needed, use stacked PR mode only.
7. Re-run CI on the stacked PR.
8. Summarize the result using the AI Merge Summary template.
9. Assign an A/B/C/D risk grade.

## Autofix policy

Allowed during initial evaluation:

```text
@coderabbitai autofix stacked pr
```

Forbidden during initial evaluation:

```text
@coderabbitai autofix
```

The forbidden command modifies the current PR branch directly. Current-branch Autofix is deferred until after evaluation.

## Risk grading

### A — Auto-merge candidate later

- docs, tests, or lint only
- CI passes
- no unresolved review findings
- no secret, workflow, dependency, or trading change
- small change size

### B — Summary approval required

- small code change
- tests included
- review findings resolved
- no risky files

### C — Detailed judgment required

- business logic change
- insufficient tests
- review warnings remain
- large diff

### D — STOP

Escalate immediately if the change includes:

- secrets, tokens, or keys
- GitHub Actions permissions
- branch protection or auto-merge changes
- trading bot implementation
- dependency additions
- automation platform expansion
- custom parser, controller, validator, or sandbox
- cost or security judgment

## First experiment success criteria

The first CodeRabbit experiment is successful if:

- CodeRabbit reviews the PR automatically.
- CI passes.
- No unsafe repository settings are changed.
- No current-branch Autofix is used.
- The Implementation PM can summarize the PR with an A/B/C/D grade.
