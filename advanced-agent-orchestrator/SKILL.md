---
name: advanced-agent-orchestrator
description: Use when the user asks for advanced agent orchestration, advanced agents orchestration, or says "use advanced agent orchestration skill to solve [task]". Runs a 5-phase workflow with mandatory human checkpoints, mandatory agent selection per phase, clean-slate context management, and explicit run/skip decisions for optional phases.
---

# Advanced Agent Orchestrator v4 (Mandatory User Selection Architecture)

## Trigger Phrases (Implicit Invocation)

This skill should activate when users say phrases like:
- "use advanced agent orchestration skill to solve [task]"
- "use advanced agents orchestration for this"
- "run advanced-agent-orchestrator"

**CRITICAL: This skill uses clean-slate context management at EVERY phase boundary to prevent self-confirmation bias.**

**CRITICAL: The user MUST explicitly select which agent to use at EVERY phase. No defaults, no auto-selection, no carry-forward without explicit confirmation.**

**CRITICAL: The user MUST review the output of each phase BEFORE deciding to proceed to the next phase.**

---

## Clean Slate Architecture: How It Works

### The Problem We're Solving

**Self-Confirmation Bias (The Silent Killer)**
- When same agent reviews its own work in same context window, it's mathematically biased to agree with past logic
- "Lost in the Middle" phenomenon: Important requirements pushed to edge of context window lose attention weight
- Agent becomes weighed down by conversational baggage, leading to repetitive loops and forgotten constraints

### Our Solution: Same Model, Clean Slate

```
Phase 1: Planning (Window A)
    ↓
[STATE EXPORT PROMPT] → Forces compilation of ALL implicit knowledge
    ↓
Close Window A (DROP all prior context)
    ↓
Phase 2: Execution (Window B - Fresh)
    ↓
[STATE EXPORT + CODE] → Provides fresh context with compiled knowledge
    ↓
Close Window B
    ↓
Phase 3: Review (Window C - Fresh)
    ↓
Agent evaluates code as "blind judge" - sees requirements + code only
```

**What This Achieves:**
- Zero context loss (implicit knowledge made explicit via State Export)
- Zero semantic drift (same model across all phases, if user chooses)
- Broken self-confirmation bias (reviewer has no memory of execution)
- Full user control at every checkpoint — YOU choose the agent, every time

---

## Workflow Overview

```
Phase 0: Role Preference Declaration
    ↓  (User declares preferred agents per role)
    ↓
Phase 1: Planning (Window A)
    ↓  [User selects/confirms Planner agent]
    ↓
[Checkpoint 1→2: USER REVIEWS Plan]
    ↓  [User decides: Run or Skip Phase 2?]
    ↓  [If Run: User selects Plan Reviewer agent]
    ↓
State Export Prompt → Compile implicit knowledge → CLOSE WINDOW A
    ↓
Phase 2: Plan Review (Window B) — User chose to Run
    ↓
[Checkpoint 2→3: USER REVIEWS Plan Review Findings]
    ↓  [User selects Executor agent]
    ↓
State Export → [Blueprint + Requirements] → CLOSE WINDOW B
    ↓
Phase 3: Execution (Window C - Fresh)
    ↓
[Checkpoint 3→4: USER REVIEWS Implementation]
    ↓  [User selects Reviewer 1 agent]
    ↓
State Export + Final Code → CLOSE WINDOW C
    ↓
Phase 4: Reviewer 1 (Window D - Fresh, Blind Judge)
    ↓
[Checkpoint 4→5: USER REVIEWS Review Findings]
    ↓  [User decides: Run or Skip Phase 5?]
    ↓  [If Run: User selects Reviewer 2 agent]
    ↓
Phase 5: Reviewer 2 (Window E - Fresh Context)
    ↓
[USER REVIEWS Final Output]
    ↓
[FINAL DELIVERY]
```

**At each checkpoint, you MUST:**
1. **Review the output** of the completed phase
2. **Explicitly select** which agent runs the next phase
3. **Explicitly choose** Run or Skip for optional phases (Phase 2, Phase 5)
4. Approve and proceed, go back to fix issues, or cancel

---

## When Different Models Add Value (Context for Your Decision)

### Using the Same Model Across Phases

**Advantages:**
- Zero semantic drift — same terminology throughout
- Optimal context preservation — 15-25% token savings vs switching
- Predictable costs — no hidden "rewriting context" overhead

**Good for:**
- Straightforward tasks (<500 lines expected)
- Standard web/mobile/backend development
- CRUD operations, UI components, API endpoints
- Well-understood problem domains

---

### Using Different Models Across Phases

**Advantages:**
- Different training corpora = different "world models" and pattern libraries
- Catches vendor-specific blind spots
- Different vulnerability pattern detection (security)

**Good for:**
1. **Complex System Architecture** — Microservices, distributed systems, CAP theorem
2. **Security-Critical Code** — Auth, payments, crypto, PII handling
3. **Technology Selection** — Different models have different tech stack biases
4. **Novel Problem Domains** — Medical AI, financial systems, scientific computing
5. **Cross-Cutting Production Concerns** — Scalability, compliance, disaster recovery

---

## Phase 0: Role Preference Declaration (MANDATORY)

Before the workflow begins, declare your preferred agent for each role. These are **starting preferences only** — you will confirm or change at each phase entry.

```
═══════════════════════════════════════════════════════════
📋 PHASE 0: Role Preference Declaration
═══════════════════════════════════════════════════════════

Declare your preferred agent for each workflow role.
These are starting preferences — you will confirm or 
override at each phase boundary.

╔══════════════════════════════════════════════════════════╗
║  AVAILABLE AGENTS                                        ║
╚══════════════════════════════════════════════════════════╝

[1] Kimi (Moonshot — Kimi K2 Thinking)
    Strengths: Code generation, CLI tasks, technical implementation
    
[2] Claude Opus 4.6 (Anthropic)
    Strengths: Complex reasoning, architecture design, strategic thinking

[3] Gemini 3.1 Pro (Google)
    Strengths: Balanced speed/quality, comprehensive review, gap analysis

[4] ChatGPT / GPT-5.2-Codex (OpenAI)
    Strengths: Current knowledge, general-purpose coding, code review

[5] Custom agent
    Specify: [provider:model]

╔══════════════════════════════════════════════════════════╗
║  ROLE PREFERENCES                                        ║
╚══════════════════════════════════════════════════════════╝

Planner (Phase 1):       Your choice (1-5): ___
Executor (Phase 3):      Your choice (1-5): ___
Reviewer (Phase 4, 5):   Your choice (1-5): ___

Shortcut: Enter "same" to use one agent for all roles.
          You must specify which agent. Example: "same: 2"

═══════════════════════════════════════════════════════════
NOTE: Phase 2 (Plan Review) inherits from your Reviewer 
preference. You will confirm at the checkpoint.
═══════════════════════════════════════════════════════════
```

**After user declares preferences, confirm and proceed to Phase 1.**

---

## Phase 1: Planning (Window A)

**Agent:** User's declared Planner preference (confirmed at Phase 0)

**Output:** Context Blueprint (detailed execution plan)

**Prompt:** `prompts/planner-create-plan.md`

**Includes:**
- Executive summary
- Phase breakdown (steps, dependencies, estimates)
- Key decisions with rationale
- Risk assessment (high/medium/low)
- Dependencies & prerequisites
- Confidence score (0-100%)
- Recommendation (PROCEED/PROCEED_WITH_CAVEATS/CLARIFY)

---

## Checkpoint 1→2: Review Plan & Decide Next Steps

After Phase 1 completes, **display this exactly**:

```
═══════════════════════════════════════════════════════════
📋 PHASE 1 COMPLETE: Context Blueprint Created (Window A)
═══════════════════════════════════════════════════════════

Planner: [AGENT_NAME] | Confidence: [X]% | Tokens: [N] | Time: [M]s

╔══════════════════════════════════════════════════════════╗
║  BLUEPRINT SUMMARY                                       ║
╚══════════════════════════════════════════════════════════╝
[2-3 paragraph summary of approach]

╔══════════════════════════════════════════════════════════╗
║  KEY TECHNICAL DECISIONS                                 ║
╚══════════════════════════════════════════════════════════╝
1. [Decision 1] → [Rationale]
2. [Decision 2] → [Rationale]
3. [Decision 3] → [Rationale]

[View full blueprint: show 500 more lines]

╔══════════════════════════════════════════════════════════╗
║  CONTEXT MANAGEMENT                                      ║
╚══════════════════════════════════════════════════════════╝
✓ Implicit knowledge compiled into explicit blueprint
✓ Next phase: Clean slate (new window)
✓ Zero context loss (blueprint preserves all reasoning)

═══════════════════════════════════════════════════════════
📖 REVIEW THE PLAN ABOVE before proceeding.
═══════════════════════════════════════════════════════════

╔══════════════════════════════════════════════════════════╗
║  STEP 1: Run or Skip Phase 2 (Plan Review)?             ║
╚══════════════════════════════════════════════════════════╝

Phase 2 sends this blueprint to a reviewer in a fresh context
for independent validation before execution.

[A] ✅ Run Phase 2 (Plan Review)
     → Validate plan before execution
     → Catches planning errors early
     → +15-25K tokens, +60-90 seconds

[B] ⏭️  Skip Phase 2 → Go directly to Execution (Phase 3)
     → Plan is straightforward, no review needed

[C] 📝 Clarify blueprint → Stay in Phase 1
     → Need planner to expand on specific areas

[D] ♻️  Replan from scratch → Restart Phase 1
     → Current approach is wrong

[E] ⏹️  Cancel task → Clean exit

Your choice (A-E): ___

╔══════════════════════════════════════════════════════════╗
║  STEP 2: Select Agent for Next Phase                     ║
╚══════════════════════════════════════════════════════════╝

If you chose [A] (Run Phase 2), select the Plan Reviewer agent:
If you chose [B] (Skip Phase 2), select the Executor agent for Phase 3:

[1] Kimi (Moonshot — Kimi K2 Thinking)
[2] Claude Opus 4.6 (Anthropic)
[3] Gemini 3.1 Pro (Google)
[4] ChatGPT / GPT-5.2-Codex (OpenAI)
[5] Custom agent (specify provider:model)

Your Phase 0 preference for this role: [SHOW_PREFERENCE]
Confirm or change (1-5): ___
```

**After user selects option A, trigger State Export Prompt:**

```
═══════════════════════════════════════════════════════════
📝 STATE EXPORT: Compiling Implicit Knowledge
═══════════════════════════════════════════════════════════

Prompt: prompts/state-export-blueprint.md

**The planner is being forced to compile:**
- Exact technical stack & versions
- Step-by-step implementation sequence  
- ALL implicit assumptions (with risks & validation)
- ALL edge cases (with handling strategy)
- Architectural patterns (with full trade-off analysis)
- STRICT constraints (what NOT to do)
- Success criteria verification methods

This process takes 30-60 seconds but ensures zero knowledge loss.

% Executing State Export...
```

**Wait for planner to output complete Context Blueprint.**

**Then display:**

```
═══════════════════════════════════════════════════════════
✓ STATE EXPORT COMPLETE
═══════════════════════════════════════════════════════════

Blueprint size: [N] lines
Implicit assumptions documented: [N]
Edge cases specified: [N]
Architectural decisions captured: [N]

**This blueprint is now the single source of truth.**
**Closing Window A. Opening fresh window for next phase.**

Press Enter to continue...
```

---

## Phase 2: Plan Review (Window B) — User Chose to Run

**Purpose:** Catch planning errors before expensive execution

**Agent:** User-selected at Checkpoint 1→2

**Process:**
1. Provide State Export Blueprint to reviewer
2. Reviewer evaluates in clean context (no memory of planning)
3. Prevents planner's assumptions from biasing reviewer

**Output:** Structured critique of blueprint

**Prompt:** `prompts/plan-reviewer-critique.md`

**Evaluates:**
- Completeness (all requirements addressed?)
- Soundness (logic valid?)
- Optimality (best approach?)
- Risk assessment (accurate?)
- Feasibility (can it be built?)
- Edge case coverage (what's missing?)

**Scores:** Each 0-10 | Total: 0-60
**Verdict:** Approve / Approve with fixes / Request replanning

---

## Checkpoint 2→3: Review Plan Review & Select Executor

After Phase 2 completes (or is skipped), **display this exactly**:

```
═══════════════════════════════════════════════════════════
🔍 REVIEW COMPLETE: Blueprint Validated
═══════════════════════════════════════════════════════════

Plan Reviewer: [AGENT_NAME] | Score: [XX]/60 | Verdict: [VERDICT]
Tokens: [N] | Time: [M]s

╔══════════════════════════════════════════════════════════╗
║  REVIEW FINDINGS                                         ║
╚══════════════════════════════════════════════════════════╝

Critical Issues: [N]
Improvements: [N]
Strengths: [N]

Top Critical Issues:
1. [Issue 1]
2. [Issue 2]

[View full review: show 400 more lines]

═══════════════════════════════════════════════════════════
📖 REVIEW THE FINDINGS ABOVE before proceeding.
═══════════════════════════════════════════════════════════

╔══════════════════════════════════════════════════════════╗
║  CONTEXT HANDOFF TO EXECUTOR                             ║
╚══════════════════════════════════════════════════════════╝

The executor will receive:
✓ Original Context Blueprint (from State Export)
✓ Review feedback (if Phase 2 ran)
✓ Original requirements
✓ Clean slate context (new conversation window)

Benefits:
✓ No self-confirmation bias (can't remember planning reasoning)
✓ Must follow blueprint (can't infer from past conversation)
✓ Must address critical review issues (explicitly documented)

╔══════════════════════════════════════════════════════════╗
║  STEP 1: What would you like to do?                      ║
╚══════════════════════════════════════════════════════════╝

[A] ✅ Proceed to Phase 3 (Execution) 
     → Use validated blueprint
     → Executor receives all context materials

[B] 📝 Return to planner → Address critical issues
     → Critical issues make blueprint unsafe
     → Back to Phase 1 with review feedback

[C] ⏭️  Override review → Ignore feedback, use original blueprint
     → You disagree with reviewer's assessment

[D] ⏹️  Cancel → Critical blockers

Your choice (A-D): ___

╔══════════════════════════════════════════════════════════╗
║  STEP 2: Select Executor Agent for Phase 3               ║
╚══════════════════════════════════════════════════════════╝

[1] Kimi (Moonshot — Kimi K2 Thinking)
[2] Claude Opus 4.6 (Anthropic)
[3] Gemini 3.1 Pro (Google)
[4] ChatGPT / GPT-5.2-Codex (OpenAI)
[5] Custom agent (specify provider:model)

Your Phase 0 Executor preference: [SHOW_PREFERENCE]
Confirm or change (1-5): ___
```

---

## Phase 3: Execution (Window C - Clean Slate)

**Agent:** User-selected at Checkpoint 2→3 (Senior Implementation Engineer)

**Purpose:** Build exactly what the blueprint specifies

**Input:**
- Context Blueprint (from State Export)
- Original requirements  
- Plan review feedback (if Phase 2 was run — critical issues override blueprint)

**Context:** Clean slate conversation. Agent cannot see planning discussion or reviewer conversation.

**Key Constraint:** Executor MUST follow blueprint. If blueprint is ambiguous, they MUST ask for clarification (not decide).

**Output:**
- Complete working implementation
- Documentation of deviations (should be rare)
- Test results
- Confidence score
- Handoff notes for reviewer

**Prompt:** `prompts/executor-implement-plan.md`

**Critical mechanism:** By removing planning conversation from context, executor cannot "read between the lines" or infer unstated requirements. Must rely ONLY on explicit blueprint.

---

## Checkpoint 3→4: Review Implementation & Select Reviewer

After Phase 3 completes, **display this exactly**:

```
═══════════════════════════════════════════════════════════
🛠️  PHASE 3 COMPLETE: Execution Finished
═══════════════════════════════════════════════════════════

Executor: [AGENT_NAME] | Confidence: [X]% | Tokens: [N]
Lines of Code: [N] | Files Created/Modified: [N]
Test Results: [N]/[N] passed

╔══════════════════════════════════════════════════════════╗
║  IMPLEMENTATION SUMMARY                                  ║
╚══════════════════════════════════════════════════════════╝
[Key implementation details, files created, approach taken]

═══════════════════════════════════════════════════════════
📖 REVIEW THE IMPLEMENTATION ABOVE before proceeding.
═══════════════════════════════════════════════════════════

╔══════════════════════════════════════════════════════════╗
║  CONTEXT MANAGEMENT FOR REVIEW                           ║
╚══════════════════════════════════════════════════════════╝

Now compiling materials for blind review:
✓ Original requirements (from Phase 1)
✓ Final codebase (what was built)
✓ Closing execution context (Window C)
✓ Opening fresh review context (Window D)

Benefits of this approach:
✓ Reviewer has NO memory of execution
✓ Cannot be influenced by "how it was built"
✓ Evaluates purely on: requirements → code
✓ Prevents self-confirmation bias

╔══════════════════════════════════════════════════════════╗
║  STEP 1: What would you like to do?                      ║
╚══════════════════════════════════════════════════════════╝

[A] ✅ Proceed to Phase 4 (Reviewer 1) — Get code review
     → Technical correctness, bug check, quality review
     → Agent sees: Requirements + Code only (blind judge)

[B] ⏭️  Skip review → Deliver now
     → Implementation is sufficient for needs
     → Save ~15K tokens + 60 seconds

[C] 📝 Request fixes — Issues need to be fixed first
     → Return to Phase 3 with feedback

[D] ⏹️  Accept as-is — Ready for delivery
     → Don't need formal review process

Your choice (A-D): ___

╔══════════════════════════════════════════════════════════╗
║  STEP 2: Select Reviewer 1 Agent for Phase 4             ║
╚══════════════════════════════════════════════════════════╝

[1] Kimi (Moonshot — Kimi K2 Thinking)
[2] Claude Opus 4.6 (Anthropic)
[3] Gemini 3.1 Pro (Google)
[4] ChatGPT / GPT-5.2-Codex (OpenAI)
[5] Custom agent (specify provider:model)

Your Phase 0 Reviewer preference: [SHOW_PREFERENCE]
Confirm or change (1-5): ___
```

---

## Phase 4: Reviewer 1 (Window D - Fresh Context, Blind Judge)

**Agent:** User-selected at Checkpoint 3→4

**Context:** Brand new conversation. Agent sees ONLY:
1. Original task requirements
2. Final implementation codebase
3. (Optional) Context Blueprint

**What they CANNOT see:**
- Planning discussion
- Why architectural decisions were made
- Any reasoning from previous phases
- Plan review feedback (if Phase 2 ran)

**Output:** Structured critique addressing:
1. **Security vulnerabilities** (CRITICAL)
2. **Architectural flaws** (long-term risks)
3. **Plan adherence** (did they build what was spec'd?)
4. **Correctness & bugs** (does it actually work?)
5. **Code quality** (maintainability)
6. **Success criteria verification** (requirements met?)

**Prompt:** `prompts/reviewer-primary-critique.md`

**Why "Blind Judge" works:**
- No self-confirmation bias (doesn't remember execution reasoning)
- Forced to evaluate against requirements objectively
- Catches hidden assumptions executor made
- Identifies gaps between "what was planned" vs "what was built"

---

## Checkpoint 4→5: Review Findings & Decide on Second Review

After Phase 4 completes, **display this exactly**:

```
═══════════════════════════════════════════════════════════
🔍 PHASE 4 REVIEW COMPLETE
═══════════════════════════════════════════════════════════

Reviewer 1: [AGENT_NAME] (Fresh context, blind review)
Verdict: [APPROVE/APPROVE_WITH_CHANGES/NEEDS_REVISION]
Critical Issues: [N] | Improvements: [N] | Confidence: [X]%

╔══════════════════════════════════════════════════════════╗
║  CRITICAL ISSUES FOUND                                   ║
╚══════════════════════════════════════════════════════════╝
[Top 3 critical issues]

╔══════════════════════════════════════════════════════════╗
║  IMPROVEMENTS SUGGESTED                                  ║
╚══════════════════════════════════════════════════════════╝
[Top 3 improvements]

[View full review: show 400 more lines]

═══════════════════════════════════════════════════════════
📖 REVIEW THE FINDINGS ABOVE before proceeding.
═══════════════════════════════════════════════════════════

╔══════════════════════════════════════════════════════════╗
║  STEP 1: Run or Skip Phase 5 (Second Review)?           ║
╚══════════════════════════════════════════════════════════╝

A second review in a fresh context catches additional blind spots.
Using a different model adds a genuinely different perspective.

[A] ✅ Run Phase 5 (Reviewer 2) — Fresh perspective review
     → Catches what Reviewer 1 missed
     → +18-25K tokens, +60-90 seconds

[B] 📝 Return to Executor — Fix critical issues first
     → Critical issues must be fixed before delivery
     → Back to Phase 3 with review feedback

[C] ⏭️  Skip to delivery — Accept with known issues
     → Issues are acceptable for current scope

[D] ⏹️  Deliver now — Reviewer 1 feedback is sufficient
     → Stop here, no second review

Your choice (A-D): ___

╔══════════════════════════════════════════════════════════╗
║  STEP 2: Select Reviewer 2 Agent for Phase 5             ║
║  (Only if you chose [A] above)                           ║
╚══════════════════════════════════════════════════════════╝

[1] Kimi (Moonshot — Kimi K2 Thinking)
[2] Claude Opus 4.6 (Anthropic)
[3] Gemini 3.1 Pro (Google)
[4] ChatGPT / GPT-5.2-Codex (OpenAI)
[5] Custom agent (specify provider:model)

Your Phase 0 Reviewer preference: [SHOW_PREFERENCE]
Confirm or change (1-5): ___

Note: Using a different model from Reviewer 1 ([REVIEWER_1_AGENT])
provides a genuinely different perspective from different training data.

⚠️ If switching models: ~30-40% of implicit reasoning context may differ.
   This is expected and is the VALUE of using a different model for review.
```

---

## Phase 5: Reviewer 2 (Window E - Fresh Context) — User Chose to Run

**Purpose:** Fresh perspective, catch blind spots, strategic view

**Agent:** User-selected at Checkpoint 4→5

**Mission:**
1. Validate Reviewer 1's findings (correct? priority right?)
2. Find what Reviewer 1 MISSED (primary value)
3. Challenge assumptions (question accepted decisions)
4. Strategic viewpoint (architecture, alternatives)

**Important:** Do NOT duplicate Reviewer 1's feedback. Focus on NEW insights.

**Output:** Independent second critique

**Prompt:** `prompts/reviewer-secondary-critique.md`

---

## Final Checkpoint: Delivery

After all phases complete, **display this exactly**:

```
═══════════════════════════════════════════════════════════
✅ ALL PHASES COMPLETE - Ready for Delivery
═══════════════════════════════════════════════════════════

Completed Phases: [N]/5
Checkpoint Reviews: [N]
Context Window Resets: [N]

╔══════════════════════════════════════════════════════════╗
║  AGENTS USED                                             ║
╚══════════════════════════════════════════════════════════╝
Phase 1 (Planner):     [AGENT_NAME]
Phase 2 (Plan Review): [AGENT_NAME or SKIPPED]
Phase 3 (Executor):    [AGENT_NAME]
Phase 4 (Reviewer 1):  [AGENT_NAME]
Phase 5 (Reviewer 2):  [AGENT_NAME or SKIPPED]

╔══════════════════════════════════════════════════════════╗
║  TOKEN USAGE BREAKDOWN                                   ║
╚══════════════════════════════════════════════════════════╝
Phase 1 (Planning):           [N]K tokens
Phase 1a (State Export):      [N]K tokens
Phase 2 (Plan Review):        [N]K tokens [if run]
Phase 3 (Execution):          [N]K tokens
Phase 4 (Reviewer 1):         [N]K tokens
Phase 5 (Reviewer 2):         [N]K tokens [if run]
───────────────────────────────────────────────────────────
TOTAL:                        [N]K tokens
Estimated Cost:               $[X.XX] - $[Y.YY]

╔══════════════════════════════════════════════════════════╗
║  CLEAN SLATE ARCHITECTURE BENEFITS                       ║
╚══════════════════════════════════════════════════════════╝
✓ Zero context loss (implicit knowledge → explicit blueprint)
✓ Self-confirmation bias broken (fresh context each phase)
✓ User controlled every agent selection
✓ User reviewed every phase output before proceeding

╔══════════════════════════════════════════════════════════╗
║  FINAL DELIVERABLE                                       ║
╚══════════════════════════════════════════════════════════╝

[IMPLEMENTATION CODE/FILES]

[REVIEW FINDINGS SUMMARY]

═══════════════════════════════════════════════════════════
🎉 Task Complete - Ready for production or further iteration
═══════════════════════════════════════════════════════════

Key outcomes:
• [Outcome 1 - e.g., "Fresh-context reviews caught 3 critical issues"]
• [Outcome 2 - e.g., "State Export preserved all architectural reasoning"]
• [Outcome 3 - e.g., "User selected optimal agents per phase"]
```

---

## Cost & Time Reference

| Scenario | Phases | Tokens | Time | Use When |
|----------|--------|--------|------|----------|
| **Fast Path** | 1, 3, 4 (skip 2,5) | 45-55K | 2-3 min | Prototypes, MVPs, internal tools, simple features |
| **Standard** | 1, 3, 4, 5 | 65-80K | 4-5 min | Most production code, important features |
| **With Plan Review** | 1, 2, 3, 4 | 65-80K | 3-4 min | Complex planning, architecture decisions |
| **Full Workflow** | 1, 2, 3, 4, 5 | 90-120K | 5-7 min | High-stakes tasks, critical systems |

---

## Common Patterns (Examples — Not Prescriptions)

These are examples showing how different users have configured the workflow. Your choices depend on your task and preferences.

### Pattern 1: Single Agent, All Phases
```
- Phase 0: User declares same agent for all roles
- Phase 1: [Agent X] plans → State Export → Close Window
- Phase 3: [Agent X] executes (fresh context, blueprint only) → Close Window  
- Phase 4: [Agent X] reviews (fresh context, blind judge)
- Phase 5: [Agent X] reviews again (another fresh context)
Cost: ~65-80K tokens
Note: Fresh contexts still break self-confirmation bias
```

### Pattern 2: Multi-Agent Configuration
```
- Phase 0: User declares different agents per role
- Phase 1: [Agent A] plans → State Export
- Phase 3: [Agent B] executes (clean slate)
- Phase 4: [Agent C] reviews (fresh context)
- Phase 5: [Agent A] reviews (different perspective from executor)
Cost: ~85-110K tokens
Note: Different models catch different blind spots
```

### Pattern 3: Fast Path (Skip Optional Phases)
```
- Phase 0: User declares preferences
- Phase 1: [Agent] plans → State Export
- Checkpoint 1→2: User skips Phase 2
- Phase 3: [Agent] executes (clean slate)
- Checkpoint 3→4: User proceeds to Phase 4
- Phase 4: [Agent] reviews (fresh context)
- Checkpoint 4→5: User skips Phase 5
Cost: ~45-55K tokens
Note: User explicitly chose to skip Phases 2 and 5
```

### Pattern 4: Full Workflow with Plan Validation
```
- Phase 0: User declares preferences
- Phase 1: [Agent A] plans → State Export
- Phase 2: [Agent B] reviews plan (gap analysis)
- Phase 3: [Agent A] executes (clean slate)
- Phase 4: [Agent A] reviews (fresh context)
- Phase 5: [Agent B] reviews (different perspective)
Cost: ~90-120K tokens
Note: Plan review catches issues before expensive execution
```

---

## Agent Switch Warning

When an agent switch occurs between phases, display this:

```
═══════════════════════════════════════════════════════════
⚠️  AGENT SWITCH: [AGENT_FROM] → [AGENT_TO]
═══════════════════════════════════════════════════════════

Context Note: Different agents have different training and
reasoning patterns. The State Export Blueprint ensures 
explicit knowledge is preserved, but implicit reasoning 
style will differ.

Proceeding with [AGENT_TO] for [PHASE_NAME]...
```

---

## Troubleshooting Scenarios

### Scenario: User asks "Why so many phase boundaries?"
**Response:**
```
Each boundary provides a checkpoint AND resets context to prevent bias.

Without clean-slate resets:
- Reviewer would see execution reasoning → biased to agree
- Requirements pushed to context edge → forgotten
- Agent weighed down by conversation → repetitive loops
```

**Alternative:** Remind them they can skip optional phases (2 and 5) at the explicit checkpoint — they just need to actively choose "Skip."

---

### Scenario: User concerned about token costs
**Response:**
```
Clean-slate architecture typically saves tokens vs. continuous conversation:

Continuous chat problems:
- Context window fills with back-and-forth
- Agent repeats itself
- Important details buried
- Eventually hits token limit, needs summarization

Clean slate benefits:
- Compact blueprint replaces long conversation
- Each phase focused on one task
- No conversational cruft
- More predictable token usage

Typical savings: 15-25% vs. equivalent continuous conversation
```

**Offer:** Show them Fast Path pattern (45-55K tokens).

---

### Scenario: Executor makes assumptions instead of asking
**Root cause:** Ambiguity handling not enforced.

**Fix at runtime:**
```
Interceptor detects assumption → HALT execution
Template to executor:
"⚠️ You made an assumption: [assumption]

Blueprint says: '[exact blueprint text]'

You must:
1. STOP execution
2. Ask for clarification
3. Wait for explicit answer

Clarification request template:
'Blueprint says \"[ambiguous part]\". What does this mean? [Options].'"
```

---

### Scenario: User wants to "keep same context" for speed
**Explain the trade-off:**
```
Same context risks:
- Self-confirmation bias in reviews
- Requirements forgotten over long conversations
- Agent becomes "creatively fatigued"
- Less objective evaluation

Clean slate benefits:
- Reviews are genuinely objective
- Requirements refreshed at each phase
- Agent maintains peak performance
- Better catches hidden assumptions

Cost difference: Minimal (State Export adds ~5% tokens)
Quality difference: Significant (catches 20-30% more issues)
```

---

## Fresh Perspective Simulation (Cheap Alternative)

**Before committing to Phase 5 (Reviewer 2), you can ask Reviewer 1:**

```
"Review your previous critique, but do so as if you were a different AI
with different training and perspective. Focus on:

1. What would a security expert flag that you missed?
2. What architectural concerns would a principal engineer raise?
3. What blind spots do you think your training might have?
4. If you had to bet $1000 on one issue being real, what would it be?

Be brutally honest. Catch what you missed the first time."
```

**Cost:** ~3-5K tokens (vs 18-25K for actual Phase 5)
**Effectiveness:** ~40-50% of full second review value
**Advantage:** Zero context loss, immediate availability

---

## Example: Real Workflow with Mandatory Selection

### Task: "Build a React component for user data table with pagination"

```
═══════════════════════════════════════════════════════════
[Phase 0] Role Preference Declaration
═══════════════════════════════════════════════════════════

User declares:
  Planner:  [2] Claude Opus 4.6
  Executor: [1] Kimi
  Reviewer: [3] Gemini 3.1 Pro

═══════════════════════════════════════════════════════════
[Phase 1: Planning — Claude Opus 4.6 (Window A)]
═══════════════════════════════════════════════════════════

→ Creates detailed Context Blueprint
→ Key decisions: React Query v5.24, MUI DataTable, custom usePagination
→ Assumptions: API pagination format, 50 rows/page
→ Blueprint confidence: 88%

═══════════════════════════════════════════════════════════
[Checkpoint 1→2] User reviews plan output
═══════════════════════════════════════════════════════════

→ User reviews blueprint summary and key decisions
→ Step 1: User chooses [A] Run Phase 2 (Plan Review)
→ Step 2: User confirms Reviewer preference → [3] Gemini 3.1 Pro

→ State Export compiles 247 lines of explicit knowledge
→ Window A closed

═══════════════════════════════════════════════════════════
[Phase 2: Plan Review — Gemini 3.1 Pro (Window B)]
═══════════════════════════════════════════════════════════

→ Clean context, sees blueprint only
→ Score: 52/60 | Verdict: APPROVE_WITH_FIXES
→ Finds gaps: missing API rate limit handling, no error boundary
→ Improvements: suggests optimistic updates

═══════════════════════════════════════════════════════════
[Checkpoint 2→3] User reviews plan review findings
═══════════════════════════════════════════════════════════

→ User reviews critical issues and improvements
→ Step 1: User chooses [A] Proceed to execution
→ Step 2: User confirms Executor preference → [1] Kimi

→ Window B closed

═══════════════════════════════════════════════════════════
[Phase 3: Execution — Kimi (Window C)]
═══════════════════════════════════════════════════════════

→ Clean slate, follows blueprint exactly
→ Addresses review issues: adds rate limit handling, error boundary
→ Discovers one ambiguity: asks "What timeout for rate limit retries?"
→ Gets answer: "3 seconds with exponential backoff"
→ Builds: 342 lines, 5 files, 8/8 tests pass
→ Confidence: 92%

═══════════════════════════════════════════════════════════
[Checkpoint 3→4] User reviews implementation
═══════════════════════════════════════════════════════════

→ User reviews code output, test results, files created
→ Step 1: User chooses [A] Proceed to Phase 4 (Review)
→ Step 2: User confirms Reviewer preference → [3] Gemini 3.1 Pro

→ Window C closed

═══════════════════════════════════════════════════════════
[Phase 4: Review — Gemini 3.1 Pro (Window D, Blind Judge)]
═══════════════════════════════════════════════════════════

→ Clean slate, sees Requirements + Code only
→ Finds 2 critical: race condition in rapid paging, missing PropTypes
→ Finds 1 improvement: extract magic number (page size = 50)
→ Verdict: APPROVE_WITH_CHANGES

═══════════════════════════════════════════════════════════
[Checkpoint 4→5] User reviews review findings
═══════════════════════════════════════════════════════════

→ User reviews critical issues and improvements
→ Step 1: User chooses [A] Run Phase 5 (Second Review)
→ Step 2: User selects [2] Claude Opus 4.6 (different from Reviewer 1)

→ Window D closed

═══════════════════════════════════════════════════════════
[Phase 5: Review 2 — Claude Opus 4.6 (Window E, Fresh)]
═══════════════════════════════════════════════════════════

→ Clean slate, different model from Reviewer 1
→ Catches: ARIA accessibility issue (Gemini missed it)
→ Validates Reviewer 1's critical issues (confirms they're real)
→ Verdict: APPROVE_WITH_CHANGES (add ARIA labels)

═══════════════════════════════════════════════════════════
[Final Delivery]
═══════════════════════════════════════════════════════════

Agents Used:
  Phase 1: Claude Opus 4.6
  Phase 2: Gemini 3.1 Pro
  Phase 3: Kimi
  Phase 4: Gemini 3.1 Pro
  Phase 5: Claude Opus 4.6

✓ 342 lines across 5 files
✓ All critical issues identified and addressed
✓ Token usage: 95K
✓ Time: 5.8 minutes
✓ User reviewed output at every checkpoint
✓ User selected agent at every phase
```

---

## Core Principles

### 1. User Controls Everything

**Users MUST:**
- Declare role preferences upfront (Phase 0)
- Confirm or change agent at every phase boundary
- Explicitly choose Run or Skip for optional phases
- Review every phase output before proceeding

**The orchestrator MUST NOT:**
- Auto-select agents
- Silently skip phases
- Present any agent as "recommended" or "default"
- Proceed to the next phase without user review and approval

---

### 2. You Control State, Not The Agent

**Agents cannot manage their own environment.** You (orchestrator) must:
- Explicitly trigger State Export prompt
- Close conversation windows
- Open fresh contexts
- Hand compiled materials to next phase

**Agents will happily continue in same context forever** unless you force the reset.

---

### 3. Implicit Knowledge Must Be Explicit

**The cardinal sin:** "The agent knows that, we discussed it earlier."

**Reality:** Once context closes, implicit knowledge is LOST forever.

**Solution:** Force State Export at EVERY phase boundary.

---

### 4. Fresh Context Breaks Bias

**Biased review (same context):**
- "Well, they chose React Query for caching, that makes sense based on our earlier discussion about API latency..."

**Blind review (fresh context):**
- "Where's the caching strategy? This will hit the API on every render. CRITICAL ISSUE."

**Same model. Different results. Just from context reset.**

---

### 5. Checkpoints Are Non-Negotiable

**Every phase boundary requires:**
- User reviews phase output
- User selects agent for next phase (or confirms preference)
- User explicitly chooses Run/Skip for optional phases
- State Export (if implicit knowledge exists)
- Context window close
- Fresh context open
- Compiled materials handoff

**No silent handoffs.** Each phase is a contract between the user and the orchestrator.

---

## Final Principle

**This architecture treats LLMs as what they are:** stateless function approximators with attention mechanisms, not magical reasoning engines.

- **Stateless:** They don't remember unless you pass state explicitly
- **Attention-limited:** Context edges lose weight over time
- **Bias-prone:** They confirm their own output (sycophancy)
- **Pattern-matchers:** Different training = different patterns

**Clean Slate Architecture works WITH these mechanics, not against them.**

**Mandatory User Selection ensures YOU, not the system, decide which tool to use for each job.**
