---
name: advanced-agent-orchestrator
description: Use when the user wants a cost-aware, complex-task orchestration workflow across multiple agents with mandatory role confirmation, exact handoff prompts, and an official-source model freshness check before updating defaults.
---

# Advanced Agent Orchestrator

Use this skill only for complex, high-value tasks where planning quality matters more than raw speed.

## Role Confirmation Protocol (MANDATORY)

**Before every task, list and confirm the following roles:**

### 1. Executor (Single choice)
- **1a: Kimi** - Default executor for most tasks
- **1b: Gemini** - Alternative executor with different capabilities

### 2. Planner (Single choice)
- **2a: Claude Opus 4.6** - Primary planner for complex task decomposition

### 3. Plan Reviewer/Critic (Single choice)
- **3a: Gemini** - Review and critique of plans
- **3b: Claude Opus** - Alternative reviewer with different perspective  
- **3c: ChatGPT (latest frontier model, e.g., 4.5.4)** - Most current frontier model

**User confirmation format:** "Use roles 1a, 2a, 3b" or specify each choice.

---

## Workflow defaults

Always start by showing:
- Roles
- Handoffs
- Review checkpoints
- Next action

Never allow more than one writer/executor at a time.

## Start-of-task protocol

1. **List and confirm roles** using the numbered format above
2. Build a compact brief:
   - Task
   - Constraints
   - Success criteria
   - Risk areas
3. Run the provider freshness check before producing handoffs:
   - `python C:\Users\kahye\.codex\skills\advanced-agent-orchestrator\scripts\check_provider_freshness.py --state C:\Users\kahye\.codex\skills\advanced-agent-orchestrator\references\provider-defaults.json --repo-state <repo>\ai-collab\config\provider-defaults.json`
4. If drift is detected:
   - Show the current approved value
   - Show the detected official value
   - Explain why the detected value is more current
   - Ask for approval before updating any stored defaults
5. If the user approves the update, rerun the checker with `--approve`.
6. After the freshness check is resolved, produce the exact next handoff prompt or command for each stage.

## Default execution chain

For every advanced task, use this sequence unless the user overrides a role:
1. Role confirmation (mandatory first step)
2. Brief construction
3. Planner creates plan
4. Reviewer critiques plan
5. Planner challenges/refines based on critique
6. Executor implements the final plan
7. Final review and judgment

## Review standards

When reviewing any agent output, prioritize:
1. Correctness bugs
2. Regressions
3. Hidden assumptions
4. Missing edge cases
5. Missing tests
6. Unnecessary complexity

If another agent is correct, say exactly what is strong.
If another agent is weak, name the failure mode directly.

## Local files to use when present

If the current workspace contains these files, use them:
- `AI-COLLAB-START-HERE.md`
- `CLAUDE.md`
- `.gemini/GEMINI.md`
- `ai-collab/config/provider-defaults.json`
- `ai-collab/prompts/codex-brief-for-claude-plan.md`
- `ai-collab/prompts/gemini-critique-claude-plan.md`
- `ai-collab/prompts/claude-challenge-plan.md`
- `ai-collab/prompts/codex-review-executor-output.md`
- `ai-collab/prompts/codex-judge-agent-outputs.md`

## Freshness policy

- The checker uses official provider pages only.
- Without user approval, do not rewrite stored defaults.
- With user approval, update both:
  - `C:\Users\kahye\.codex\skills\advanced-agent-orchestrator\references\provider-defaults.json`
  - the repo-local `ai-collab/config/provider-defaults.json`
- Prefer provider aliases where the provider guarantees they follow the latest model family. Use provider-specific model IDs where no durable alias exists.

## Persistent setup guidance

For long-term reuse, prefer this stack:
1. ChatGPT Custom Instructions for the short always-on orchestration rule
2. This skill for the full advanced workflow
3. Repo-local Claude and Gemini memory files for project-specific behavior

Read `references/chatgpt-custom-instructions.md` when the user wants the exact text to paste into ChatGPT settings.
