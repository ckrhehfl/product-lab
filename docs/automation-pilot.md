# Automation Pilot: Guarded Claude Review-Fix Pass

## Purpose

This document describes the controlled pilot for Option B: one guarded Claude review-fix pass after a Codex review is submitted on a PR.

## Workflow file

`.github/workflows/claude-review-fix-once.yml`

## Trigger

`pull_request_review` → `submitted`

Only fires when a PR review is submitted. Does not fire on:
- issue comments
- pull_request opened/synchronize
- scheduled events
- individual review comments (pull_request_review_comment)
- issues opened

## Guard conditions (all must pass)

| Guard | Condition |
|-------|-----------|
| Codex actor | Review must be submitted by the confirmed Codex GitHub actor (see status below) |
| Required label | PR must have `claude:ready` |
| Blocking label | PR must NOT have `claude:blocked` |
| Blocking label | PR must NOT have `needs:human-decision` |
| One-pass marker | PR must NOT contain a comment with `<!-- claude-review-fix-pass:v1 -->` |

If any guard fails the job exits immediately without invoking Claude.

## Marker

`<!-- claude-review-fix-pass:v1 -->`

Posted as a PR comment by Claude when the pass completes (success or blocked). The marker check runs before Claude is invoked, enforcing the one-pass limit even if the workflow fires again.

## Codex actor status

**Confirmed.**

The GitHub bot login that submits Codex reviews on this repository is:

```
chatgpt-codex-connector[bot]
```

The workflow `if:` condition is set to this exact actor. The workflow will fire only when a review is submitted by `chatgpt-codex-connector[bot]`. All other review actors (humans, other bots) are rejected by the actor guard before any further checks run.

## Claude action bot allowance

`allowed_bots: chatgpt-codex-connector[bot]`

Set narrowly to the exact Codex bot. The `anthropics/claude-code-action@v1` action in agent mode (i.e. when `prompt` is supplied) requires non-User actors to be listed in `allowed_bots`. Wildcard (`"*"`) is explicitly not used. No other bots are permitted.

## Checkout safety

The checkout step checks out the PR head branch and repository directly:

```yaml
repository: ${{ github.event.pull_request.head.repo.full_name }}
ref: ${{ github.event.pull_request.head.ref }}
```

This ensures Claude's commits land on the PR head branch, not a detached merge commit or the workflow's default merge ref, which could cause the commit/push to fail or go to the wrong branch.

## Marker guard — fail-closed behavior

The marker guard uses `set -euo pipefail` before fetching PR comments. If the `gh api` call fails (e.g. network error, permission error), the step exits non-zero and the job fails before Claude is invoked. Only the `grep` no-match case (marker absent) is treated as non-fatal, which correctly sets `proceed=true`. A `gh api` failure is never silently treated as "marker absent".

## Review fetch commands

Claude fetches the Codex review via two supported GitHub API endpoints:

- Review submissions: `gh api "repos/{owner}/{repo}/pulls/{number}/reviews" --paginate`
- Inline review comments: `gh api "repos/{owner}/{repo}/pulls/{number}/comments" --paginate`

`gh pr view --json reviewComments` is not used because `reviewComments` is not a supported field. No custom parser is introduced; Claude reads the raw JSON from these endpoints directly.

## Non-goals

| Non-goal | Status |
|----------|--------|
| Merge | Claude is explicitly instructed not to merge |
| Auto-merge | Claude is explicitly instructed not to enable auto-merge |
| Branch protection changes | Not touched |
| Scheduled trigger | Not present |
| Per-comment trigger | Not present |
| pull_request opened/synchronize trigger | Not present |
| Repeated Claude fix passes | Prevented by marker guard |
| Codex↔Claude loop | Prevented by actor guard + marker guard |
| l5-adf reuse | Explicitly forbidden in Claude instructions |
| Custom orchestrator/validator/parser | Not present |

## STOP conditions

Work stops and a human is consulted if:
- The Codex actor is unknown and the workflow needs to be enabled
- Claude posts a BLOCKED comment — a human must read the reason and decide next steps
- The `needs:human-decision` label is applied — the workflow will skip on any future trigger
- CI fails after a Claude fix pass — a human must review

## Concurrency

One Claude pass per PR at a time. Concurrent triggers for the same PR number are queued, not cancelled, so no pass is silently dropped. However, the marker guard ensures only one pass ever runs.

## Permissions

Minimum required for the Claude GitHub Action to operate:
- `contents: write` — commit changes to the branch
- `pull-requests: write` — post PR comments
- `issues: write` — post issue-style PR comments
- `id-token: write` — OIDC for action authentication
- `actions: read` — read workflow context

No new secrets are added. Uses existing `ANTHROPIC_API_KEY`.

## Timeout

15 minutes maximum (`timeout-minutes: 15`). Claude is limited to `--max-turns 5`.
