# Automation Architecture Map

## 1. Purpose

This repository is validating a GitHub-native automation factory. The target operating model is:

> Issue → implementation agent → PR → CI → reviewer agent → review-fix agent → final owner decision → later: native auto-merge eligibility.

Every component in this chain must be a standard GitHub primitive or an approved tool. No custom servers, parsers, orchestrators, or merge bots.

---

## 2. Current State

| Step | Artifact | Status |
|---|---|---|
| PR 1 | CLAUDE.md, docs/automation-operating-model.md | Merged |
| PR 2 | Minimal Python scaffold, pytest, scripts/test.sh, scripts/verify.sh | Merged |
| PR 3 | .github/workflows/ci.yml | Merged |
| PR 4 | Issue and PR templates | Merged |
| Labels | claude:ready, claude:blocked, needs:human-decision, type:* | Configured |
| PR 5 | .github/workflows/claude.yml — Claude GitHub Action | Merged |
| Issue #6 | Smoke test: @claude responded without changing files | Passed (~$0.17) |

---

## 3. Target Operating Model

| Role | Component |
|---|---|
| Task intake | GitHub Issues + issue template |
| Scope and STOP conditions | Issue template fields |
| Implementation | Claude Code (local) or Claude GitHub Action (@claude mention) |
| Automated review | Codex (GitHub-native reviewer) |
| Review-fix | Claude GitHub Action (controlled, one pass per PR) |
| Executable gate | GitHub Actions CI (scripts/test.sh, scripts/verify.sh) |
| Routing and safety state | GitHub labels (claude:ready, claude:blocked, needs:human-decision) |
| Final decision | Human owner — until native auto-merge is deliberately enabled |
| Merge gate (later) | Branch protection with required CI and review checks |
| Full automation target (later) | GitHub native auto-merge eligibility after all gates pass |

---

## 4. Automation Maturity Levels

The repo must pass each level safely before advancing.

| Level | Description | Status |
|---|---|---|
| 0 | Local Claude Code creates PRs from human prompts | Done |
| 1 | @claude mention-based GitHub Action responds to comments and issues | Done (PR 5) |
| 2 | Codex reviews PRs; human decides which comments Claude fixes | Next |
| 3 | Controlled automatic Codex-review-to-Claude-fix, max one fix pass per PR | Planned |
| 4 | Branch protection with required CI and review checks | Planned |
| 5 | GitHub native auto-merge eligibility after all gates pass | Long-term target |

The long-term goal is Level 5. Each level is a gate, not a phase to rush through.

---

## 5. Cost Control Principles

- Avoid per-comment Claude runs. One fix pass per PR maximum.
- Batch review comments rather than triggering a Claude run for each one.
- Keep `--max-turns` low (currently 5).
- Keep workflow `timeout-minutes` short (currently 15).
- Keep concurrency controls in place to cancel duplicate runs.
- Avoid scheduled Claude workflow runs.
- Avoid triggering Claude on every `pull_request` opened/synchronize event until there is a clear cost-justified reason.
- Keep issue and PR prompts specific and bounded.
- Keep CLAUDE.md concise — large context docs increase cost per run.

---

## 6. Context Management Strategy

| Context layer | Purpose |
|---|---|
| CLAUDE.md | Persistent project rules, boundaries, and approved toolchain — loaded every session |
| Issue template | Task-specific scope, acceptance criteria, and STOP conditions |
| PR template | Validation record, scope confirmation, and checklist |
| docs/ | Stable operating model and architecture reference |
| Skills | Reusable task recipes — introduced only when a repeated workflow is stable and well-understood |
| Plugins | Packaged skills, agents, and hooks — not available in GitHub Actions runners unless explicitly installed in the workflow |
| Subagents | Local or web context isolation for large research or audits — not required for the core MVP workflow |
| Hooks | Local Claude Code lifecycle guardrails — useful for local safety checks but not a replacement for GitHub Actions automation |
| MCP | External tool or data connector — introduced only when copying information from another system becomes the bottleneck |

---

## 7. Installed Plugin Policy

- User-scope plugins may help local Claude Code sessions on a developer machine.
- GitHub Actions runners do not automatically inherit local user-scope plugin state.
- If a plugin or skill is needed in a GitHub Actions workflow, it must be explicitly installed and configured in that workflow.
- Core repo automation must not depend on a local-only plugin.
- Prefer repo-native docs, templates, and workflows before reaching for plugins.

---

## 8. Why PR 6 Does Not Add More Automation

The Issue #6 smoke test confirmed that Claude GitHub Action runs correctly. However:

- The smoke test cost (~$0.17) suggests that uncontrolled triggers can become expensive at scale.
- Before adding automatic Codex-review-to-Claude-fix behavior, the repo needs to observe actual Codex review event payloads to understand their structure.
- Hardcoding Codex bot usernames or review comment patterns before observing real events would create a fragile parser that may need immediate revision.
- Adding a custom event parser, orchestrator, or merge bot to work around GitHub's native event model is explicitly out of scope.

The next behavior change should be controlled, observable, and reversible.

---

## 9. Next Planned PRs

This roadmap is tentative. Each PR requires human approval before implementation.

| PR | Scope |
|---|---|
| PR 7 | Controlled Codex review-fix pilot design — observe real Codex event payloads, design the one-pass review-fix trigger |
| PR 8 | One-run-per-PR review-fix guardrails — prevent Claude from running more than once per PR automatically |
| PR 9 | Branch protection readiness — define required checks before enabling |
| PR 10 | Native auto-merge eligibility experiment — enable only after PR 9 gates are confirmed stable |

---

## 10. STOP Conditions

Stop and escalate to the repository owner if any of these occur:

- API cost grows unexpectedly across PRs or issues
- Claude runs on every comment or commit without a specific trigger condition
- Claude pushes more than one fix pass per PR automatically
- The automation requires a custom server, parser, or merge bot to function
- A workflow requires secrets beyond the approved repository secrets
- Automation merges PRs without owner-approved GitHub-native gates
- Context documents (CLAUDE.md, issue templates, PR templates) become too large, contradictory, or expensive to load per run
