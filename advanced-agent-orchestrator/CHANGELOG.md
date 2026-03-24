# Advanced Agent Orchestrator Changelog

## Version 4.0.0 - 2026-03-24

### 🎉 Major Update: Mandatory User Agent Selection Architecture

**Breaking Changes:**
- User MUST explicitly select an agent at EVERY phase — no defaults, no auto-selection, no carry-forward without confirmation
- Phase 0 rewritten: Role Preference Declaration (Planner/Executor/Reviewer) replaces single "primary agent" selection
- All `⭐ RECOMMENDED` labels and recommendation bias removed from every file
- Optional phases (Phase 2: Plan Review, Phase 5: Reviewer 2) now require explicit "Run" or "Skip" decision — no silent skipping
- Every checkpoint now has two mandatory steps: (1) review output, (2) select agent for next phase
- `provider-defaults.json` schema bumped to v3: `"default": "primary_agent"` replaced with `"user_selection": "required"`; `"use_when"` replaced with neutral `"strengths"`; `"recommended"` field removed from workflow config
- `handoff_templates.py` rewritten: all checkpoint functions include mandatory agent selection menu and explicit Run/Skip prompts; `context_loss_warning()` renamed to `agent_switch_warning()` with neutral framing

### Features Added

**Phase 0: Role Preference Declaration (NEW)**
- Users declare preferred agent for each role: Planner, Executor, Reviewer
- "Same agent for all" shortcut available but must be explicitly stated
- Preferences are confirmed or overridden at each phase boundary

**Mandatory Agent Selection at Every Phase**
- Every checkpoint displays full agent menu with numbered options
- Shows user's Phase 0 preference for easy confirmation
- No agent is pre-selected or marked as default/recommended
- All agents listed equally with factual strength descriptions

**Explicit Run/Skip for Optional Phases**
- Phase 2 (Plan Review): User must choose [A] Run or [B] Skip at Checkpoint 1→2
- Phase 5 (Reviewer 2): User must choose [A] Run or [D] Skip at Checkpoint 4→5
- No phase is silently skipped or automatically included

**Review-Before-Proceed at Every Checkpoint**
- Each checkpoint displays phase output summary with "📖 REVIEW THE [OUTPUT] ABOVE before proceeding" prompt
- User reviews output BEFORE being offered proceed/skip/fix options
- Ensures informed decision-making at every boundary

### Files Changed
- `SKILL.md` — Complete rewrite (v4): Phase 0 role declaration, all checkpoints with mandatory agent selection + explicit Run/Skip, neutral language throughout, updated examples and patterns
- `references/provider-defaults.json` — Schema v3: removed `recommended`, removed `default: primary_agent`, added `user_selection: required`, renamed `use_when` to `strengths`
- `scripts/handoff_templates.py` — Rewritten: mandatory agent menu in all checkpoints, Phase 0 preference display, explicit Run/Skip prompts, removed all recommendation bias
- `CHANGELOG.md` — This entry

### Files NOT Changed (No Changes Needed)
- `scripts/api_executor.py` — Already requires `--provider` flag on every execution, no default fallback
- `scripts/cli_executor.py` — Same: requires explicit provider
- `prompts/` — All prompt files are model-agnostic, no changes needed
- `agents/openai.yaml` — VS Code agent config, not workflow-related

---

## Version 2.0.0 - 2026-03-21

### 🎉 Major Update: 5-Phase Checkpoint Workflow

**Breaking Changes:**
- Complete workflow redesign with mandatory human checkpoints at each phase boundary
- Single-agent-first architecture (multi-agent still supported as override)
- New prompt structure for all phases

### Features Added

**Phase 0: Initial Agent Selection**
- User selects ONE primary agent for all phases (optimal context preservation)
- Can override at any checkpoint with explicit approval

**Phase 1: Planning**
- New comprehensive planner prompt with:
  - Executive summary
  - Detailed phase breakdown
  - Key decisions with rationale
  - Risk assessment (high/medium/low)
  - Confidence score
  - Proceed/caveats/clarify recommendation

**Checkpoint 1→2: Plan Review Decision**
- Shows plan summary, key decisions, risks
- 6 options: proceed to review, skip review, clarify, replan, switch agent, cancel
- User maintains full control

**Phase 2: Plan Review (OPTIONAL)**
- New comprehensive plan reviewer prompt with:
  - 6-dimension scoring (Completeness, Soundness, Optimality, Risk, Feasibility, Edge Cases)
  - Critical issues table (must fix)
  - Improvements table (should fix)
  - Alternative approaches
  - 0-60 total score with grade
  - Notes for executor

**Checkpoint 2→3: Execution Decision**
- Shows plan vs review comparison
- Agreement areas highlighted
- Issues identified (critical vs improvements)
- 5 options: proceed, return to planner, override review, switch agent, cancel

**Phase 3: Execution**
- Updated executor prompt with plan review reconciliation
- PRIORITY ORDER: Critical issues > Improvements > Original plan > Your judgment
- Requirements:
  - Address critical issues from review
  - Implement improvements if time permits
  - Document deviations
  - Confidence score
  - Response to plan review section

**Checkpoint 3→4: Code Review Decision**
- Shows implementation summary, LOC, files changed, test results
- 5 options: proceed to review, skip review, request fixes, switch agent, deliver
- Recommends same agent for review (best context)
- Shows context loss warning if agent switch selected

**Phase 4: Reviewer 1**
- Updated prompt with self-review note
- Focus areas: correctness, plan adherence, code quality, bug hunt, testing
- If reviewing own work: self-review enhancement questions

**Checkpoint 4→5: Second Review Decision**
- Shows Reviewer 1 findings (critical, improvements, strengths)
- 4 options: proceed to Reviewer 2, return to executor, skip to delivery, deliver now
- Explains Reviewer 2 value (catches 20-30% blind spots)
- Shows context loss warning for agent switch

**Phase 5: Reviewer 2 (OPTIONAL)**
- Updated prompt with fresh perspective mission
- Must NOT duplicate Reviewer 1's work
- MUST find what Reviewer 1 missed
- Focus: architecture, strategy, alternatives, challenging assumptions

**Final Delivery:**
- Comprehensive summary
- Token usage breakdown by phase
- Cost estimates
- Final deliverable code/files

### Agent Configuration

**New: primary_agent workflow**
- User selects ONE agent at start (used for all phases by default)
- Each phase can override with alternatives
- Clear recommendations for when to use which agent

**Provider defaults updated:**
- schema_version: 2
- Token estimates for each mode (single, +plan review, +external review, full)
- Agent strengths documented

### Context Loss Prevention

**When agent switches occur:**
- Explicit warning displayed
- Explains why context loss happens (30-40%)
- Shows cost/time impact
- Requires explicit Y/N confirmation

**Context preservation protocol:**
- Original task brief always included
- Decision rationale preserved
- Confidence scores tracked
- Escalation protocol defined

### Cost Optimization

**Four modes documented:**

| Mode | Phases | Tokens | Time | When to Use |
|------|--------|--------|------|-------------|
| Single Agent | 1,3,4 | 45-65K | 2-3 min | Most tasks (recommended) |
| + Plan Review | 1,2,3,4 | 65-80K | 3-4 min | Complex planning |
| + External Review | 1,3,4,5 | 70-90K | 4-5 min | Critical code |
| Full Workflow | 1,2,3,4,5 | 90-120K | 5-7 min | High-stakes tasks |

### Testing

**5 test scenarios validated:**
1. ✅ Single agent mode (Kimi - cheapest)
2. ✅ Multi-agent mode (all phases)
3. ✅ Skip optional phases (2, 5)
4. ✅ Agent switching with warnings
5. ✅ Cancel workflow cleanly

**Result:** 5/5 tests passed (100%)

### Documentation

**Files updated:**
- SKILL.md (complete rewrite with checkpoint templates)
- prompts/planner-create-plan.md (new)
- prompts/plan-reviewer-critique.md (new)
- prompts/executor-implement-plan.md (updated)
- prompts/reviewer-primary-critique.md (updated)
- prompts/reviewer-secondary-critique.md (updated)
- references/provider-defaults.json (schema v2)
- scripts/handoff_templates.py (new)
- scripts/test_workflow.py (new)

**New files:**
- CHANGELOG.md (this file)
- workflow_test_results.md (test validation results)

## Migration Guide

### From v1 to v2:

**Old workflow (v1):**
```
Planner → Executor V1 → Review → Executor V2 → Judge
(automatic progression, no checkpoints)
```

**New workflow (v2):**
```
Planning → [USER CHECK] → Plan Review (opt) → [USER CHECK] →
Execution → [USER CHECK] → Review 1 → [USER CHECK] → Review 2 (opt) → Delivery
(stops at EVERY boundary for human verification)
```

### Key Differences:

1. **Human checkpoints at every phase** (previously automatic)
2. **Single agent by default** (previously multi-agent rigid)
3. **Optional phases** (2 and 5 can be skipped)
4. **Agent switching with warnings** (previously silent)
5. **Plan review phase** (new - catches issues before execution)
6. **Fresh perspective reviewer** (Reviewer 2 different from Reviewer 1)
7. **Token transparency** (costs shown at each phase)

### For Users:

**Most tasks:** Use single agent mode (Kimi or Claude for all phases)
- Simpler, cheaper, faster
- 95% as good as multi-agent for most work

**Complex/critical tasks:** Add optional phases as needed
- Plan review: If architecture unclear
- External reviewer: If need fresh perspective

### Performance:

**Token costs:**
- Simple fix (v1): ~40K tokens
- Simple fix (v2): ~40K tokens (similar)
- Complex task (v1): ~90K tokens
- Complex task (v2): ~90-120K tokens (similar to slightly higher)

**Time:**
- v1: 3-4 minutes average
- v2: 2-7 minutes depending on options chosen (similar to faster)

## Known Limitations

1. **Checkpoint overhead:** Adds interaction time (benefit: user control)
2. **Context loss:** 30-40% when switching agents (warning displayed)
3. **No auto-detection:** System doesn't auto-skip phases based on complexity (future enhancement)
4. **Learning curve:** Users need to understand when to use optional phases (documentation helps)

## Future Enhancements (v2.x)

- Auto-detect task complexity and suggest optional phases
- Remember user preferences (which agents they prefer for which phases)
- A/B testing mode: run both single and multi-agent, compare results
- Performance metrics: track which phase finds most issues
- Confidence-based auto-escalation: add reviewers if confidence low

## Contributors

- Implementation: Advanced Agents Orchestrator Team
- Testing: Automated test suite (5 scenarios)
- Documentation: Inline docs and examples

## License

Same as parent project
