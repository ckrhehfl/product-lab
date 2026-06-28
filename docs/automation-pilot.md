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

Posted as a PR comment by a **trusted post-Claude workflow step** (`Post one-pass marker`) when the pass completes. The marker check runs before Claude is invoked, enforcing the one-pass limit even if the workflow fires again.

The trusted marker step does **not** receive `ANTHROPIC_API_KEY`. It uses only `GH_TOKEN` (the standard `GITHUB_TOKEN`). Claude is explicitly instructed not to post any PR comment — the marker step handles it.

The marker step posts the completion marker only when:
1. The Claude action exited successfully (`steps.claude.outcome == 'success'`), **and**
2. The local HEAD matches the remote HEAD of the PR branch (verifying that any fix commits were actually pushed).

If either condition fails, the marker step posts a `BLOCKED:` marker instead and exits non-zero (failing the job). This prevents the completion marker from being posted while fixes were not actually delivered to the branch.

## Codex actor status

**Confirmed.**

The GitHub bot login that submits Codex reviews on this repository is:

```
chatgpt-codex-connector[bot]
```

The job-level `if:` condition guards on both the actor and the repository:

```yaml
if: >
  github.event.review.user.login == 'chatgpt-codex-connector[bot]' &&
  github.event.pull_request.head.repo.full_name == github.repository
```

The workflow runs only when the review is submitted by `chatgpt-codex-connector[bot]` **and** the PR is from the same repository. Fork PRs are intentionally skipped — this pilot does not support fork-originated PRs and does not use custom fork remotes or tokens.

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

The triggering Codex review is fetched by a **trusted pre-Claude workflow step** (`Fetch triggering Codex review context`) that runs before the Claude action. This step uses `GH_TOKEN` but does **not** receive `ANTHROPIC_API_KEY`.

It writes two local files:
- `.claude-review-context/review.json` — the triggering review body and metadata
- `.claude-review-context/comments.json` — inline comments scoped to this review only

Claude reads these local files instead of calling `gh api`. Claude does not have `gh` Bash access.

Using `github.event.review.id` scopes the fetch to the single review that triggered the workflow, avoiding stale feedback from older Codex reviews. No custom parser is introduced; Claude reads the raw JSON directly.

`gh pr view --json reviewComments` is not used because `reviewComments` is not a supported field.

## Test script isolation

The Claude review-fix workflow intentionally does not run `scripts/test.sh` or `scripts/verify.sh`. This job runs with `ANTHROPIC_API_KEY` and write-capable GitHub credentials (`contents: write`, `pull-requests: write`). Executing PR-controlled shell scripts in that context would allow a labeled same-repo PR to run arbitrary code while secrets are present.

Tests and verification are delegated entirely to the existing CI workflow, which runs after the Claude job pushes any fix commits to the PR branch. No sandbox, trusted test runner, or custom controller is introduced — the separation is enforced purely by removing script execution from Claude's allowed tools and adding an explicit hard constraint in the prompt.

The Python/pytest setup steps that previously appeared in this workflow have been removed for the same reason.

## Claude Code CLI permission scope

The Claude action runs with scoped CLI flags:

```
--permission-mode acceptEdits
--allowedTools Read,Edit,Write,
  Bash(git status*),Bash(git diff*),Bash(git add*),Bash(git commit*),
  Bash(git push*),Bash(git config*)
```

`--dangerously-skip-permissions`, `--permission-mode bypassPermissions`, `Bash(*)`, `Bash(gh api*)`, `Bash(gh pr comment*)`, and any broad shell access are not used. The tool list covers only what is needed for: reading/editing files, committing, and pushing. `gh` commands are not permitted inside the Claude action — review context is fetched by a trusted pre-Claude step, and the marker is posted by a trusted post-Claude step. Both trusted steps use `GH_TOKEN` only and do not receive `ANTHROPIC_API_KEY`. Repository test scripts are also excluded — see [Test script isolation](#test-script-isolation).

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
| Sandbox / trusted test runner | Not present — test isolation is achieved by removing script execution from allowed tools |
| PR-controlled script execution in Claude job | Not permitted — `scripts/test.sh` and `scripts/verify.sh` are excluded from allowed tools and explicitly forbidden in the prompt |
| `gh` Bash access for Claude | Not permitted — `gh api` and `gh pr comment` are removed from Claude's allowed tools; review context and marker posting are handled by trusted steps without `ANTHROPIC_API_KEY` |

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
