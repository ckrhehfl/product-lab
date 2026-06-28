# Review-Fix Automation Pivot

## Decision

We will not build a custom Codex→Claude automatic review-fix automation platform.

The product-lab direction is pivoting toward evaluating existing specialist agent tools, starting with CodeRabbit.

## Why Option B is being discontinued

Option B attempted to build an automatic review-fix loop using Codex review output, Claude follow-up fixes, labels, markers, workflows, and automatic branch updates.

This direction is discontinued because it introduces unnecessary platform complexity and security risk.

Specific concerns:

- AI agents with secret or write credentials can accidentally modify repository state.
- Automatic commit/push behavior increases blast radius.
- Review-thread parsing and marker-based orchestration are brittle.
- Custom controller, parser, validator, sandbox, orchestrator, and merge bot logic would turn product-lab into an automation platform.
- Building the review-fix platform distracts from validating the product operating model.

## New operating model

The target flow is:

Issue
→ Claude or Copilot creates a PR
→ CI runs
→ CodeRabbit performs specialist review
→ CodeRabbit Autofix creates a stacked PR
→ CI reruns
→ AI Merge Summary is produced
→ Implementation PM assigns A/B/C/D risk grade
→ Only A-grade changes may later become GitHub native auto-merge candidates

## Tool roles

### Claude

Claude remains useful for:

- implementation assistance
- small follow-up changes
- summaries
- risk interpretation
- PR result explanation for non-developers

Claude should not automatically commit or push using secret/write credentials from GitHub Actions.

Local user-invoked Claude Code sessions may create commits and PRs when explicitly instructed by the repository owner.

### CodeRabbit

CodeRabbit is the first specialist review tool to evaluate.

CodeRabbit Autofix should initially be used only in stacked PR mode.

Allowed:

```text
@coderabbitai autofix stacked pr
```

Not allowed during the initial evaluation:

```text
@coderabbitai autofix
```

Current-branch Autofix is prohibited until reviewed later.

### GitHub Copilot

Copilot remains a GitHub-native comparison candidate.

It may be evaluated as an alternative implementation or review assistant.

### Codex Review

Codex review should be treated as optional, supplemental, or paused during this phase to avoid duplicate review noise.

## Deferred decisions

The following are deferred until after tool evaluation:

- branch protection changes
- GitHub native auto-merge
- automatic merge rules
- current-branch Autofix
- AI agent write-token workflows

## A/B/C/D risk grading

### A — Auto-merge candidate later

- docs, tests, or lint only
- CI passes
- no unresolved review findings
- no secret, workflow, dependency, or trading changes
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

## First evaluation PR

After CodeRabbit is installed by the repository owner, the first experiment PR must be docs-only or tests-only.

The first Autofix experiment must use stacked PR mode only.

## Evaluation results

See `docs/coderabbit-evaluation-results.md` for the initial evaluation results.
