# CLAUDE.md — Agent Operating Contract

This file is the operating contract for Claude Code sessions in this repository. Read it before taking any action.

## Repository Identity

`product-lab` is a clean-start public repository for validating an automation factory MVP using Claude Code and GitHub-native workflows. It is not a custom automation platform. There is no legacy system to port.

## Hard Boundaries

Do not inspect, reference, or copy from any prior automation repository (including l5-adf).

Do not propose or implement any of the following, in any PR:
- Custom orchestrator
- Custom validator
- Review-thread parser
- Merge controller
- Secret scanner
- Automation server
- Dashboard
- Merge bot
- Evidence packet system

If a user prompt implies any of the above, stop and explain why it is out of scope.

## Approved Toolchain

Only these tools may be used in this repository:

- Claude Code
- AI-Builder-Club/skills
- GitHub Issues
- GitHub Pull Requests
- GitHub Actions CI
- GitHub branch protection
- GitHub native auto-merge eligibility
- Issue templates
- PR templates
- Labels
- `CLAUDE.md`
- `scripts/test.sh`
- `scripts/verify.sh`

No other runtime, server, framework, or custom tooling is permitted without an explicit decision recorded in a PR.

## PR Discipline

- Each PR must have a single, clearly scoped purpose.
- A PR that adds source code must not also add documentation restructures, and vice versa.
- PR titles must be specific: describe what changes, not what the PR does generically.
- Every PR must be implementable end-to-end without depending on a future PR to make it coherent.
- Do not add source code, tests, scripts, CI, GitHub Actions, issue templates, PR templates, labels, branch protection config, `.github/`, or any automation runtime unless the PR scope explicitly includes it.

## Planning-First Rule

Before writing any code or configuration, state the plan in one short paragraph. If the plan touches more than one logical concern (e.g., CI and documentation), stop and split into separate PRs. Do not proceed until the user confirms the plan.

## Human Decision Boundaries

Humans decide:
- Whether a PR is ready to merge
- Whether branch protection rules change
- Whether the approved toolchain expands
- Whether a STOP condition has been resolved
- The rollout order of PRs

Claude Code does not make these decisions unilaterally.

## STOP Conditions

Stop immediately and ask a human if:
- The task requires a tool or pattern not in the approved toolchain
- The task would affect more than one PR scope at once
- There is ambiguity about whether an action falls inside the hard boundaries
- A CI check fails and the fix is not obvious from the error output
- The branch diverges from `main` in a way that is not straightforwardly resolvable

Do not attempt to work around a STOP condition by choosing an adjacent action.

## What Belongs in Later PRs

The following are explicitly deferred and must not appear in early PRs:
- `scripts/test.sh` and `scripts/verify.sh`
- GitHub Actions workflows
- Branch protection configuration
- Issue and PR templates
- Labels
- Any source code

Each will arrive in its own scoped PR, in the rollout order defined in `docs/automation-operating-model.md`.
