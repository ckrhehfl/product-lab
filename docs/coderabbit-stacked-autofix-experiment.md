# CodeRabbit Stacked Autofix Experiment

This document defines the second CodeRabbit evaluation in product-lab.

## Purpose

The goal is to evaluate CodeRabbit Autofix in stacked PR mode without allowing current-branch Autofix.

This experiment remains intentionally low risk.

## Allowed change types

Allowed initial change types:

- documentation-only changes
- test-only changes

## Experiment flow

The flow for this experiment is:

1. Create a small docs-only PR.
2. Let CI run.
3. Let CodeRabbit review the PR.
4. Request Autofix using stacked PR mode only.
5. Inspect the stacked PR.
6. Re-run CI.
7. Assign an A/B/C/D risk grade.
8. Merge only if the result is A.

## Autofix commands

Allowed command:

```text
@coderabbitai autofix stacked pr
```

Forbidden command:

```text
@coderabbitai autofix
```

The forbidden command modifies the current PR branch directly.

## Deliberate review target

This section intentionally says the experiment allows docs-only or lint-only changes.

That sentence should be aligned with the allowed change types above before this experiment is considered complete.

## Merge policy

The stacked PR may be merged only if:

- it is docs-only
- CI passes
- CodeRabbit has no unresolved actionable findings
- no current-branch Autofix was used
- no workflow, secret, dependency, permission, branch protection, auto-merge, trading bot, or automation-platform file changed

## Failure policy

Close the stacked PR instead of merging if:

- it changes anything outside documentation
- CI fails
- it uses current-branch Autofix
- it introduces workflow, secret, dependency, permission, branch protection, auto-merge, trading bot, or automation-platform changes
- the fix is not obviously safe
