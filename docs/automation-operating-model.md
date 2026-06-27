# Automation Operating Model

## Purpose

This document describes how automation is structured in `product-lab`. It exists so that contributors, reviewers, and agents share a single, stable mental model of what is automated, what is not, and where the boundaries are.

## Guiding Constraint: GitHub-Native Automation Only

All automation in this repository must be expressible using GitHub's built-in primitives: Issues, Pull Requests, Actions, branch protection, labels, and auto-merge eligibility. No custom servers, orchestrators, or runtime processes are permitted. If a workflow cannot be implemented with these primitives, it is out of scope.

## Intended Workflow

Each unit of work follows this sequence:

```
GitHub Issue
  → Claude Code implementation on a feature branch
  → Pull Request opened
  → GitHub Actions CI runs
  → Claude Code reviews the PR
  → At most one review-fix cycle
  → Branch protection gates satisfied
  → GitHub native auto-merge eligibility reached
  → Human approves merge
```

"At most one review-fix cycle" is a hard constraint. If a PR requires more than one round of Claude-driven fixes, it is a signal that the PR scope is too large or the implementation plan was insufficiently validated before writing.

## Automation Levels

| Level | Description | Status |
|-------|-------------|--------|
| 0 | Manual: all actions performed by a human | Baseline |
| 1 | Claude Code drafts implementation; human reviews and merges | Current target |
| 2 | CI validates on every push; branch protection blocks merge on failure | Planned |
| 3 | Claude Code reviews the PR automatically after CI passes | Planned |
| 4 | Auto-merge eligibility triggered when branch protection gates are satisfied | Planned |
| 5 | Issue-to-merged-PR flow completes without human writing code | Future |

Levels are additive. Each level is introduced in its own PR. No level may be skipped.

## What Claude Code May Do

- Read any file in the repository
- Create and edit files within the PR scope
- Run `scripts/test.sh` and `scripts/verify.sh`
- Open a pull request for completed work
- Post a review on a pull request
- Request changes on a pull request
- Suggest a plan and wait for human confirmation before implementing

## What GitHub Actions May Do

- Run `scripts/test.sh` on push and pull request events
- Run `scripts/verify.sh` on pull request events
- Report pass/fail status checks to a PR
- Block merge when status checks fail (via branch protection)
- Trigger auto-merge eligibility when all checks pass and approvals are present

GitHub Actions may not post comments, open issues, push commits, or modify repository settings.

## What Humans Must Decide

- Whether a PR is ready to merge
- Whether branch protection rules should change
- Whether the approved toolchain should expand
- The rollout order and timing of PRs
- Whether a STOP condition has been resolved

No automation in this repository replaces these decisions.

## Explicit Non-Goals

The following will not be built in this repository:

- Custom orchestrator or automation server
- Custom validator or review parser
- Merge controller or merge bot
- Secret scanner
- Evidence packet system
- Dashboard or observability layer
- Any runtime process that runs outside GitHub's built-in primitives

If a proposed change requires any of the above, it is out of scope.

## PR Size Discipline

Each PR must be independently coherent and mergeable. A PR that adds source code must not also restructure documentation. A PR that adds CI must not also add branch protection configuration. When in doubt, split.

A PR is too large if:
- It cannot be reviewed in a single sitting
- It touches more than one logical concern
- Reverting it would require undoing unrelated work

## STOP Conditions

Work stops and a human is consulted if:
- A required tool or pattern is not in the approved toolchain
- A PR would need to span more than one logical concern to be coherent
- CI fails and the fix is not derivable from the error output alone
- A branch diverges from `main` in a way that is not straightforwardly resolvable
- There is ambiguity about whether an action falls inside the hard boundaries

STOP conditions are not blockers to work around; they are signals that a human decision is required.

## Current Rollout Order

| PR | Scope |
|----|-------|
| PR 1 | `CLAUDE.md` and this operating model document |
| PR 2 | `scripts/test.sh` and `scripts/verify.sh` |
| PR 3 | GitHub Actions CI workflow |
| PR 4 | Issue templates and PR template |
| PR 5 | Labels |
| PR 6 | Branch protection configuration |
| PR 7 | Auto-merge eligibility wiring |
| PR 8+ | First substantive feature work |

This order is not final. Humans decide if it changes.
