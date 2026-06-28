# CodeRabbit Evaluation Results

This document records the initial CodeRabbit evaluation results for product-lab.

## Summary

The initial CodeRabbit evaluation passed.

Both review-only and stacked Autofix workflows were tested using low-risk documentation-only pull requests.

The evaluation confirmed that CodeRabbit can:

- review a pull request automatically
- generate actionable comments
- re-review after a follow-up commit
- create a stacked Autofix pull request
- keep the current PR branch unchanged when stacked PR mode is used

The evaluation did not use current-branch Autofix.

## Evaluated flow

The evaluated flow was:

Issue or implementation request
→ Claude creates a documentation-only PR
→ CI runs
→ CodeRabbit reviews the PR
→ Implementation PM assigns A/B/C/D risk grade
→ Claude applies manual follow-up fixes when needed
→ CodeRabbit re-reviews
→ CodeRabbit stacked Autofix is tested separately
→ A-grade PRs are merged

## PR #10 — CodeRabbit review evaluation

URL:

- https://github.com/ckrhehfl/product-lab/pull/10

Result:

- CodeRabbit reviewed the PR automatically.
- CodeRabbit generated 2 actionable comments.
- Claude manually fixed both comments with a normal local commit.
- CodeRabbit re-review generated no actionable comments.
- CI passed.
- Autofix was not used.
- Final risk grade: A.

Decision:

- Merged.

## PR #11 — Stacked Autofix original experiment PR

URL:

- https://github.com/ckrhehfl/product-lab/pull/11

Result:

- CodeRabbit reviewed the PR automatically.
- CodeRabbit detected the deliberate documentation inconsistency.
- The allowed stacked Autofix command was used:

```text
@coderabbitai autofix stacked pr
```

- The forbidden current-branch command was not used:

```text
@coderabbitai autofix
```

- The original PR was merged after the stacked Autofix PR was validated.
- Final risk grade: A.

Decision:

- Merged.

## PR #12 — CodeRabbit stacked Autofix PR

URL:

- https://github.com/ckrhehfl/product-lab/pull/12

Result:

- CodeRabbit created a stacked PR.
- The stacked PR changed only:

```text
docs/coderabbit-stacked-autofix-experiment.md
```

- CI verify passed.
- CodeRabbit status succeeded.
- CodeRabbit pre-merge checks passed 5/5.
- The change was documentation-only.
- Final risk grade: A.

Decision:

- Merged.

## Risk assessment

The initial CodeRabbit evaluation is considered successful.

### Confirmed safe

- CodeRabbit automatic PR review
- Claude manual follow-up fixes
- CodeRabbit re-review after follow-up commits
- CodeRabbit stacked Autofix for documentation-only changes
- A/B/C/D implementation PM risk grading
- Squash merge after A-grade confirmation

### Still prohibited

Current-branch Autofix remains prohibited:

```text
@coderabbitai autofix
```

This command directly modifies the current PR branch and has not been approved for product-lab.

### Still deferred

The following remain deferred:

- branch protection changes
- GitHub native auto-merge
- automatic merge rules
- AI agent write-token workflows
- current-branch Autofix
- custom review-fix automation platform work

## Operating decision

CodeRabbit is approved for continued evaluation as a specialist review tool.

CodeRabbit stacked Autofix is approved only for low-risk documentation-only or test-only experiments, and only when explicitly requested with:

```text
@coderabbitai autofix stacked pr
```

The Implementation PM must continue assigning an A/B/C/D risk grade before merge.

## Current status

The project should continue with specialist agent evaluation rather than custom review-fix automation.

Do not build:

- custom review-thread parsers
- marker-based orchestration
- custom controllers
- validators
- sandboxes
- orchestrators
- merge bots
- Claude automatic commit/push workflows using secret or write credentials
