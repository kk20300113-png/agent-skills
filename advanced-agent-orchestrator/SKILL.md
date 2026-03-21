---
name: advanced-agent-orchestrator
description: Use when the user wants a cost-aware, complex-task orchestration workflow across multiple agents with mandatory role confirmation, exact handoff prompts, and an official-source model freshness check before updating defaults.
---

# Advanced Agent Orchestrator

Use this skill only for complex, high-value tasks where planning quality matters more than raw speed.

## Role Confirmation Protocol (MANDATORY)

**Before every task, list and confirm the following roles:**

### 1. Planner (Single choice)
- **1a: Claude Opus 4.6** - Primary planner for complex task decomposition

### 2. Executor (Single choice)
- **2a: Kimi** - Default executor for Kimi Code CLI
- **2b: Gemini** - Alternative executor with different capabilities

### 3. Primary Reviewer (Single choice)
- **3a: Gemini** - Review and critique of execution output
- **3b: Claude Opus** - Alternative reviewer with different perspective
- **3c: ChatGPT (latest frontier model, e.g., 4.5.4)** - Most current frontier model

### 4. Secondary Reviewer (Optional - User requested only)
- **4a: Gemini** - Second independent review (if 3a not selected)
- **4b: Claude Opus** - Second independent review (if 3b not selected)
- **4c: ChatGPT latest** - Second independent review (if 3c not selected)

**User confirmation format:**
- Single review: `"Use roles 1a, 2a, 3c"`
- Dual review: `"Use roles 1a, 2a, 3c, 4b"`

**Reviewer 2 Rule:** Only invoke if user explicitly includes 4a/4b/4c in role selection.

---

## Execution Modes

### Mode 1: Default (Token Efficient)
- **Workflow:** Planner → Executor V1 → Primary Review → Executor V2 → Judge
- **Token Cost:** ~65-90K
- **Best For:** Most tasks, quick iterations, prototyping
- **Reviewers:** 1 (Primary only)

### Mode 2: Deep Review (High Quality)
- **Workflow:** Planner → Executor V1 → Dual Review → Executor V2 → Judge
- **Token Cost:** ~80-115K (+15-25K for second reviewer)
- **Best For:** Critical code, complex systems, high-stakes deliverables
- **Reviewers:** 2 (Primary + Secondary, parallel execution)

### Mode 3: Auto
- **Selection Logic:**
  - Complex tasks (>500 lines expected) → Deep Review Mode
  - Simple tasks (<100 lines) → Default Mode
  - Medium complexity → Ask user preference

**Mode Selection Format:** `"Use mode default/deep/auto"`

---

## Workflow Sequence

### Phase 1: Planning
**Agent:** Planner (Claude Opus 4.6)  
**Input:** Task description, constraints, success criteria  
**Output:** Detailed execution plan  
**Prompt:** `codex-brief-for-claude-plan.md`

### Phase 2: Execution V1
**Agent:** Executor (Kimi/Gemini)  
**Input:** Plan from Phase 1  
**Output:** Working implementation (V1)  
**Prompt:** `executor-implement-plan.md`

### Phase 3A: Primary Review
**Agent:** Primary Reviewer (selected in role 3)  
**Input:** V1 output from Executor  
**Output:** Structured critique of execution  
**Prompt:** `reviewer-primary-critique.md`

### Phase 3B: Secondary Review (Optional - Deep Review Mode only)
**Agent:** Secondary Reviewer (selected in role 4)  
**Input:** V1 output from Executor  
**Output:** Independent structured critique  
**Prompt:** `reviewer-secondary-critique.md`  
**Execution:** Parallel with Phase 3A

### Phase 4: Improvement
**Agent:** Executor (Kimi/Gemini)  
**Input:** V1 output + Review(s)  
**Output:** Improved implementation (V2)  
**Prompt:** `executor-improvement.md`

### Phase 5: Final Judgment
**Agent:** Judge (Kimi as coordinator)  
**Input:** V2 output + Review(s)  
**Output:** Final verdict and deliverables  
**Prompt:** `codex-judge-agent-outputs.md`

---

## Token Optimization Guidelines

### Cost Reduction Strategies

1. **Default Mode First**
   - Start with single reviewer for most tasks
   - Only escalate to Deep Review if quality issues found

2. **Conditional Second Reviewer**
   - Only invoke Reviewer 2 if:
     - User explicitly requests (Deep Review mode)
     - Primary reviewer finds >5 critical issues
     - Task is marked as high-stakes/critical

3. **Parallel Reviews (Deep Mode)**
   - Run Reviewer 1 and Reviewer 2 simultaneously
   - Reduces wall-clock time, not token cost

4. **Review Deduplication**
   - Before Phase 4, merge overlapping feedback
   - Prioritize unique issues
   - Reduces input tokens for Executor V2

5. **Context Management**
   - Pass only relevant code snippets to reviewers
   - Summarize large outputs before review handoff

### Token Budget Guide

| Task Size | Recommended Mode | Est. Tokens |
|-----------|------------------|-------------|
| <100 lines | Default | 65-75K |
| 100-500 lines | Default | 75-90K |
| 500-1000 lines | Deep Review | 90-115K |
| >1000 lines | Deep Review + Chunking | 115K+ |

---

## Review Standards

When reviewing executor output, prioritize:
1. **Correctness bugs** - Does it actually work?
2. **Regressions** - Did anything break?
3. **Hidden assumptions** - Unstated dependencies?
4. **Missing edge cases** - What scenarios weren't considered?
5. **Missing tests** - Is there adequate test coverage?
6. **Unnecessary complexity** - Can it be simpler?

If another agent is correct, say exactly what is strong.  
If another agent is weak, name the failure mode directly.

---

## Start-of-Task Protocol

1. **List and confirm roles** using the 4-role format above
2. **Select mode** (Default/Deep/Auto)
3. **Build a compact brief:**
   - Task
   - Constraints
   - Success criteria
   - Risk areas
4. **Run provider freshness check** before producing handoffs
5. **After freshness check resolved**, produce exact handoff prompt for Phase 1

---

## Local Files to Use When Present

- `AI-COLLAB-START-HERE.md`
- `CLAUDE.md`
- `.gemini/GEMINI.md`
- `ai-collab/config/provider-defaults.json`
- `ai-collab/prompts/codex-brief-for-claude-plan.md`
- `ai-collab/prompts/executor-implement-plan.md`
- `ai-collab/prompts/reviewer-primary-critique.md`
- `ai-collab/prompts/reviewer-secondary-critique.md`
- `ai-collab/prompts/executor-improvement.md`
- `ai-collab/prompts/codex-judge-agent-outputs.md`

---

## Freshness Policy

- The checker uses official provider pages only.
- Without user approval, do not rewrite stored defaults.
- With user approval, update both:
  - `C:\Users\kahye\.codex\skills\advanced-agent-orchestrator\references\provider-defaults.json`
  - The repo-local `ai-collab/config/provider-defaults.json`
- Prefer provider aliases where the provider guarantees they follow the latest model family.

---

## Conflict Resolution

When dual reviewers disagree:
1. **Critical issues** - Always fix if either reviewer mentions
2. **Both mention same issue** - Definitely fix, high confidence
3. **Reviewers contradict** - Executor decides with documented rationale
4. **Unclear priority** - Ask user for clarification

---

## Example User Interaction

**User:**
```
Use advanced-agent-orchestrator skill to build a carbon credit calculator
```

**Kimi:**
```
🎯 Advanced Agent Orchestrator

Select Mode:
- [x] Default (Single reviewer, ~65-90K tokens)
- [ ] Deep Review (Dual reviewers, ~80-115K tokens)
- [ ] Auto (System decides based on complexity)

Select Roles:
1. Planner:
   - 1a: Claude Opus 4.6

2. Executor:
   - 2a: Kimi (You)
   - 2b: Gemini

3. Primary Reviewer:
   - 3a: Gemini
   - 3b: Claude Opus
   - 3c: ChatGPT latest

Add Secondary Reviewer? (+15-25K tokens)
- [ ] 4a: Gemini (only if 3a not selected)
- [ ] 4b: Claude Opus (only if 3b not selected)
- [ ] 4c: ChatGPT latest (only if 3c not selected)

Confirm: Use mode [default/deep/auto], roles [1a], [2a/2b], [3a/3b/3c], [4a/4b/4c or none]
```

**User:**
```
Use mode default, roles 1a, 2a, 3c
```

**Kimi:**
```
✅ Confirmed:
- Mode: Default (Single reviewer)
- Planner: Claude Opus 4.6 (1a)
- Executor: Kimi (2a)
- Primary Reviewer: ChatGPT latest (3c)
- Secondary Reviewer: None

Estimated tokens: 65-90K

[Proceeds with Phase 1: Planning...]
```
