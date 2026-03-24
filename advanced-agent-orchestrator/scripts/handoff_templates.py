"""
Checkpoint Template Functions for Advanced Agent Orchestrator v4

These functions generate consistent checkpoint prompts for phase transitions.
Every checkpoint includes:
  1. Phase output summary for user review
  2. MANDATORY agent selection for the next phase
  3. Explicit Run/Skip decision for optional phases (Phase 2, Phase 5)
"""

AGENT_MENU = """[1] Kimi (Moonshot — Kimi K2 Thinking)
[2] Claude Opus 4.6 (Anthropic)
[3] Gemini 3.1 Pro (Google)
[4] ChatGPT / GPT-5.2-Codex (OpenAI)
[5] Custom agent (specify provider:model)"""


def checkpoint_1_to_2(plan_data):
    """
    Phase 1 → 2: Plan Review Decision (MANDATORY agent selection + Run/Skip)

    Args:
        plan_data: dict with keys:
            - agent_name: str
            - confidence: int (0-100)
            - tokens: int
            - summary: str
            - key_decisions: list of dicts with 'decision' and 'rationale'
            - risks: dict with 'high', 'medium', 'low' lists
            - phase0_reviewer_pref: str (user's Phase 0 reviewer preference)
            - phase0_executor_pref: str (user's Phase 0 executor preference)
    """
    decisions_str = "\n".join([
        f"  {i+1}. {d['decision']} → {d['rationale'][:80]}..."
        for i, d in enumerate(plan_data.get('key_decisions', [])[:3])
    ])

    risks_str = ""
    if plan_data.get('risks', {}).get('high'):
        risks_str += "High: " + ", ".join(plan_data['risks']['high'][:2]) + "\n"
    if plan_data.get('risks', {}).get('medium'):
        risks_str += "Medium: " + ", ".join(plan_data['risks']['medium'][:2])

    reviewer_pref = plan_data.get('phase0_reviewer_pref', 'Not declared')
    executor_pref = plan_data.get('phase0_executor_pref', 'Not declared')

    return f"""═══════════════════════════════════════════════════════════
📋 PHASE 1 COMPLETE: Plan Created
═══════════════════════════════════════════════════════════

Planner: {plan_data.get('agent_name', 'Unknown')}
Confidence: {plan_data.get('confidence', 0)}% | Tokens: {plan_data.get('tokens', 0)}

╔══════════════════════════════════════════════════════════╗
║  PLAN SUMMARY                                            ║
╚══════════════════════════════════════════════════════════╝
{plan_data.get('summary', 'No summary provided')[:500]}...

╔══════════════════════════════════════════════════════════╗
║  KEY DECISIONS                                           ║
╚══════════════════════════════════════════════════════════╝
{decisions_str}

╔══════════════════════════════════════════════════════════╗
║  RISK ASSESSMENT                                         ║
╚══════════════════════════════════════════════════════════╝
{risks_str}

═══════════════════════════════════════════════════════════
📖 REVIEW THE PLAN ABOVE before proceeding.
═══════════════════════════════════════════════════════════

╔══════════════════════════════════════════════════════════╗
║  STEP 1: Run or Skip Phase 2 (Plan Review)?             ║
╚══════════════════════════════════════════════════════════╝

[A] ✅ Run Phase 2 (Plan Review)
     → Validate plan before execution
     → +15-25K tokens, +60-90 seconds

[B] ⏭️  Skip Phase 2 → Go directly to Phase 3 (Execution)
     → Plan is straightforward, no review needed

[C] 📝 Clarify blueprint → Stay in Phase 1

[D] ♻️  Replan from scratch → Restart Phase 1

[E] ⏹️  Cancel task → Clean exit

Your choice (A-E): ___

╔══════════════════════════════════════════════════════════╗
║  STEP 2: Select Agent for Next Phase (REQUIRED)          ║
╚══════════════════════════════════════════════════════════╝

If [A]: Select Plan Reviewer agent.
If [B]: Select Executor agent for Phase 3.

{AGENT_MENU}

Your Phase 0 preference: {reviewer_pref} (reviewer) / {executor_pref} (executor)
Confirm or change (1-5): ___"""


def checkpoint_2_to_3(review_data):
    """
    Phase 2 → 3: Execution Decision (MANDATORY agent selection)

    Args:
        review_data: dict with keys:
            - agent_name: str
            - score: int (0-60)
            - verdict: str
            - tokens: int
            - agreement_areas: list
            - critical_issues: list
            - improvements: list
            - phase0_executor_pref: str
    """
    agreement = "\n".join([f"   • {area}" for area in review_data.get('agreement_areas', [])])

    critical = "\n".join([
        f"   {i+1}. {issue.get('desc', '')[:100]}..."
        for i, issue in enumerate(review_data.get('critical_issues', [])[:2])
    ])

    executor_pref = review_data.get('phase0_executor_pref', 'Not declared')

    return f"""═══════════════════════════════════════════════════════════
🔍 PHASE 2 COMPLETE: Plan Reviewed
═══════════════════════════════════════════════════════════

Plan Reviewer: {review_data.get('agent_name', 'Unknown')}
Score: {review_data.get('score', 0)}/60 | Verdict: {review_data.get('verdict', 'Unknown')}
Tokens: {review_data.get('tokens', 0)}

╔══════════════════════════════════════════════════════════╗
║  AGREEMENT AREAS                                         ║
╚══════════════════════════════════════════════════════════╝
Both planner and reviewer agree:
{agreement}

╔══════════════════════════════════════════════════════════╗
║  ISSUES IDENTIFIED                                       ║
╚══════════════════════════════════════════════════════════╝
Critical Issues: {len(review_data.get('critical_issues', []))}
Improvements: {len(review_data.get('improvements', []))}

Top critical issues:
{critical}

═══════════════════════════════════════════════════════════
📖 REVIEW THE FINDINGS ABOVE before proceeding.
═══════════════════════════════════════════════════════════

╔══════════════════════════════════════════════════════════╗
║  STEP 1: What would you like to do?                      ║
╚══════════════════════════════════════════════════════════╝

[A] ✅ Proceed to Phase 3 (Execution)
     → Use reviewed plan with issues addressed

[B] 📝 Return to planner → Address critical issues first
     → Back to Phase 1 with review feedback

[C] ⏭️  Override review → Ignore feedback, use original plan

[D] ⏹️  Cancel → Critical blockers

Your choice (A-D): ___

╔══════════════════════════════════════════════════════════╗
║  STEP 2: Select Executor Agent for Phase 3 (REQUIRED)    ║
╚══════════════════════════════════════════════════════════╝

{AGENT_MENU}

Your Phase 0 Executor preference: {executor_pref}
Confirm or change (1-5): ___"""


def checkpoint_3_to_4(execution_data):
    """
    Phase 3 → 4: Code Review Decision (MANDATORY agent selection)

    Args:
        execution_data: dict with keys:
            - agent_name: str
            - confidence: int
            - tokens: int
            - loc: int (lines of code)
            - files_changed: int
            - tests_passed: int
            - tests_total: int
            - phase0_reviewer_pref: str
    """
    test_results = f"{execution_data.get('tests_passed', 0)}/{execution_data.get('tests_total', 0)} passed"
    reviewer_pref = execution_data.get('phase0_reviewer_pref', 'Not declared')

    return f"""═══════════════════════════════════════════════════════════
🛠️  PHASE 3 COMPLETE: Implementation Finished
═══════════════════════════════════════════════════════════

Executor: {execution_data.get('agent_name', 'Unknown')}
Confidence: {execution_data.get('confidence', 0)}% | Tokens: {execution_data.get('tokens', 0)}
Lines of Code: {execution_data.get('loc', 0)} | Files: {execution_data.get('files_changed', 0)}
Tests: {test_results}

═══════════════════════════════════════════════════════════
📖 REVIEW THE IMPLEMENTATION ABOVE before proceeding.
═══════════════════════════════════════════════════════════

╔══════════════════════════════════════════════════════════╗
║  STEP 1: What would you like to do?                      ║
╚══════════════════════════════════════════════════════════╝

[A] ✅ Proceed to Phase 4 (Reviewer 1) — Get code review
     → Blind judge: sees Requirements + Code only

[B] ⏭️  Skip review → Deliver now
     → Save ~15K tokens + 60 seconds

[C] 📝 Request fixes — Issues need to be fixed first
     → Return to Phase 3 with feedback

[D] ⏹️  Accept as-is — Ready for delivery

Your choice (A-D): ___

╔══════════════════════════════════════════════════════════╗
║  STEP 2: Select Reviewer 1 Agent for Phase 4 (REQUIRED)  ║
╚══════════════════════════════════════════════════════════╝

{AGENT_MENU}

Your Phase 0 Reviewer preference: {reviewer_pref}
Confirm or change (1-5): ___"""


def checkpoint_4_to_5(review_data):
    """
    Phase 4 → 5: Second Review Decision (MANDATORY Run/Skip + agent selection)

    Args:
        review_data: dict with keys:
            - agent_name: str
            - confidence: int
            - verdict: str
            - tokens: int
            - critical_issues: list
            - improvements: list
            - phase0_reviewer_pref: str
    """
    critical = len(review_data.get('critical_issues', []))
    improvements = len(review_data.get('improvements', []))
    reviewer_pref = review_data.get('phase0_reviewer_pref', 'Not declared')
    reviewer1_agent = review_data.get('agent_name', 'Unknown')

    return f"""═══════════════════════════════════════════════════════════
🔍 PHASE 4 COMPLETE: Reviewer 1 Finished
═══════════════════════════════════════════════════════════

Reviewer 1: {reviewer1_agent}
Confidence: {review_data.get('confidence', 0)}% | Verdict: {review_data.get('verdict', 'Unknown')}
Tokens: {review_data.get('tokens', 0)}

╔══════════════════════════════════════════════════════════╗
║  REVIEW FINDINGS                                         ║
╚══════════════════════════════════════════════════════════╝
Critical Issues: {critical}
Improvements: {improvements}

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
     → +18-25K tokens, +60-90 seconds

[B] 📝 Return to Executor — Fix critical issues first
     → Back to Phase 3 with review feedback

[C] ⏭️  Skip to delivery — Accept with known issues

[D] ⏹️  Deliver now — Reviewer 1 feedback is sufficient

Your choice (A-D): ___

╔══════════════════════════════════════════════════════════╗
║  STEP 2: Select Reviewer 2 Agent for Phase 5 (REQUIRED)  ║
║  (Only if you chose [A] above)                           ║
╚══════════════════════════════════════════════════════════╝

{AGENT_MENU}

Your Phase 0 Reviewer preference: {reviewer_pref}
Reviewer 1 used: {reviewer1_agent}
Confirm or change (1-5): ___

Note: Using a different model from Reviewer 1 provides a
genuinely different perspective from different training data."""


def agent_switch_warning(agent_from, agent_to):
    """
    Warning displayed when switching agents between phases.

    Args:
        agent_from: str (current agent name)
        agent_to: str (next agent name)
    """
    return f"""═══════════════════════════════════════════════════════════
⚠️  AGENT SWITCH: {agent_from} → {agent_to}
═══════════════════════════════════════════════════════════

Context Note: Different agents have different training and
reasoning patterns. The State Export Blueprint ensures
explicit knowledge is preserved, but implicit reasoning
style will differ.

Proceeding with {agent_to}..."""


def final_delivery_summary(workflow_data):
    """
    Final summary after all phases complete.

    Args:
        workflow_data: dict with keys:
            - phases_run: int
            - reviews_conducted: int
            - loc: int
            - files_changed: int
            - agents_used: dict mapping phase name to agent name
            - tokens_phase_1: int
            - tokens_phase_2: int (optional)
            - tokens_phase_3: int
            - tokens_phase_4: int
            - tokens_phase_5: int (optional)
            - total_tokens: int
    """
    total = workflow_data.get('total_tokens', 0)
    cost_range = f"${total * 0.00001:.2f}-${total * 0.00003:.2f}"

    agents = workflow_data.get('agents_used', {})
    agents_str = "\n".join([
        f"  {phase}: {agent}"
        for phase, agent in agents.items()
    ])

    return f"""═══════════════════════════════════════════════════════════
✅ ALL PHASES COMPLETE - Ready for Delivery
═══════════════════════════════════════════════════════════

Completed Phases: {workflow_data.get('phases_run', 0)}/5
Reviews Conducted: {workflow_data.get('reviews_conducted', 0)}

╔══════════════════════════════════════════════════════════╗
║  AGENTS USED (User-Selected)                             ║
╚══════════════════════════════════════════════════════════╝
{agents_str}

╔══════════════════════════════════════════════════════════╗
║  SUMMARY OF WORK                                         ║
╚══════════════════════════════════════════════════════════╝
Execution:     {workflow_data.get('loc', 0)} lines across {workflow_data.get('files_changed', 0)} files

╔══════════════════════════════════════════════════════════╗
║  TOKEN USAGE & COST                                      ║
╚══════════════════════════════════════════════════════════╝
Phase 1 (Plan):        {workflow_data.get('tokens_phase_1', 0)}K tokens
Phase 2 (Plan Rev):    {workflow_data.get('tokens_phase_2', 0)}K tokens
Phase 3 (Execute):     {workflow_data.get('tokens_phase_3', 0)}K tokens
Phase 4 (Review 1):    {workflow_data.get('tokens_phase_4', 0)}K tokens
Phase 5 (Review 2):    {workflow_data.get('tokens_phase_5', 0)}K tokens
───────────────────────────────────────────────────────────
TOTAL:                 {total}K tokens
Estimated Cost:        {cost_range}

╔══════════════════════════════════════════════════════════╗
║  FINAL DELIVERABLE                                       ║
╚══════════════════════════════════════════════════════════╝

[IMPLEMENTATION CODE/FILES]

═══════════════════════════════════════════════════════════
🎉 Task Complete
═══════════════════════════════════════════════════════════
"""


# Export all functions
__all__ = [
    'checkpoint_1_to_2',
    'checkpoint_2_to_3',
    'checkpoint_3_to_4',
    'checkpoint_4_to_5',
    'agent_switch_warning',
    'final_delivery_summary',
]
