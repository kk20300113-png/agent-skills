# Agent Skills Repository

This repository contains custom skills for AI agent orchestration, primarily used with Kimi Code CLI and other agent frameworks.

## Repository Structure

```
├── advanced-agent-orchestrator/    # Advanced multi-agent orchestration workflow
├── agent-orchestrator/             # Basic agent coordination
└── .system/                        # System-managed skills
```

## Getting Started

### Prerequisites
- Git
- Kimi Code CLI or compatible agent framework

### Installation

1. Clone this repository to your skills directory:
```bash
git clone <repository-url> "c:\Users\kahye\.codex\skills"
```

2. Ensure skills are properly loaded by your agent framework.

## Skills Documentation

### Advanced Agent Orchestrator

**Location:** `advanced-agent-orchestrator/SKILL.md`

**Version:** 2.0.0 | 5-phase checkpoint workflow with human verification at each boundary

**Key Features:**
- **Mandatory human checkpoints** at EVERY phase boundary (5 checkpoints total)
- **Single-agent-first architecture** (optimal context preservation)
- **Optional agent reviews** with context loss warnings when switching
- **Transparent token tracking** at each phase
- **Flexible workflow** - skip optional phases, cancel anytime, switch agents

**Workflow Overview:**
```
Phase 0: Select Agent (one primary agent for all phases)
Phase 1: Planning → [CHECKPOINT] →
Phase 2: Plan Review (OPTIONAL) → [CHECKPOINT] →
Phase 3: Execution → [CHECKPOINT] →
Phase 4: Reviewer 1 → [CHECKPOINT] →
Phase 5: Reviewer 2 (OPTIONAL) → [DELIVERY]
```

**Cost & Time Estimates:**
- **Single agent (recommended):** 45-65K tokens, 2-3 minutes
- **+ Plan review:** 65-80K tokens, 3-4 minutes
- **+ External review:** 70-90K tokens, 4-5 minutes
- **Full workflow:** 90-120K tokens, 5-7 minutes

**Usage:**
```
User: Use advanced-agent-orchestrator to build a React component

[Phase 0] Select primary agent:
[1] Kimi - Optimized for coding
[2] Claude Opus - Best for complex reasoning
[3] Gemini 3.1 Pro - Good balance
[4] ChatGPT - Most current knowledge

[Phase 1] Planner creates execution plan

[Checkpoint 1→2] User reviews plan, chooses:
- Proceed to plan review
- Skip review → execute now
- Clarify/replan
- Switch agents

[Phase 2] Plan reviewer validates approach (optional)

[Phase 3] Executor implements solution

[Phase 4] Reviewer 1 checks correctness (same agent = best context)

[Phase 5] Reviewer 2 provides fresh perspective (optional)

[Delivery] Final code with token usage and cost summary
```

**Key Documentation:**
- `advanced-agent-orchestrator/SKILL.md` - Complete workflow guide
- `advanced-agent-orchestrator/CHANGELOG.md` - Version history
- `advanced-agent-orchestrator/workflow_test_results.md` - Test validation

**Key Files:**
- `prompts/planner-create-plan.md` - Planning prompt
- `prompts/plan-reviewer-critique.md` - Plan review prompt
- `prompts/executor-implement-plan.md` - Execution prompt
- `prompts/reviewer-primary-critique.md` - Code review 1 prompt
- `prompts/reviewer-secondary-critique.md` - Code review 2 prompt
- `references/provider-defaults.json` - Agent configuration (schema v2)
```

**When to Use Which Mode:**

| Mode | When to Use | Example |
|------|-------------|---------|
| **Single agent** | Most tasks, prototyping, MVPs | Fix a bug, add a feature |
| **+ Plan review** | Complex architecture, unclear approach | Build new system |
| **+ External review** | Critical code, need fresh eyes | Payment processing |
| **Full workflow** | High-stakes, production code | Core architecture |
```

**New Features in v2.0.0:**
- 5-phase checkpoint workflow (vs 4-phase automatic in v1)
- Human verification at EVERY phase boundary
- Single-agent-first for optimal context preservation
- Optional phases (plan review, reviewer 2) can be skipped
- Agent switching with explicit context loss warnings
- Token tracking at each phase
- Confidence scores at each phase
- Comprehensive prompts for all roles
- Validation test suite (5 scenarios, 100% pass)
```

**Migration from v1:**
- NEW: Checkpoints after every phase (requires user interaction)
- NEW: Single agent recommended by default (vs multi-agent in v1)
- NEW: Optional phases reduce token cost for simple tasks
- UPDATED: Agent selection flows through primary_agent concept
- SAME: Quality standards, safety checks, official model verification
User: "Use roles 1a, 2a, 3c for this task"
Agent: [Confirms roles] → [Executes workflow]
```

## Contributing & Updates

### Making Changes

1. **Edit the skill document:**
```bash
cd "c:\Users\kahye\.codex\skills\advanced-agent-orchestrator"
# Edit SKILL.md with your changes
```

2. **Create a feature branch:**
```bash
git checkout -b update-role-selection
```

3. **Commit your changes:**
```bash
git add advanced-agent-orchestrator/SKILL.md
git commit -m "Description of changes"
```

4. **Push to GitHub:**
```bash
git push origin update-role-selection
```

5. **Create a Pull Request** on GitHub for review

### Version Control Best Practices

- **Always commit changes** to SKILL.md when you update requirements
- **Use descriptive commit messages** explaining what changed and why
- **Create branches** for experimental changes
- **Tag releases** for stable versions: `git tag -a v1.0 -m "Stable role selection format"`

## Syncing Local Changes

### Pulling Updates from GitHub

```bash
cd "c:\Users\kahye\.codex\skills"
git pull origin main
```

### Pushing Local Changes to GitHub

```bash
cd "c:\Users\kahye\.codex\skills"
git add .
git commit -m "Description of your changes"
git push origin main
```

## Next Steps

1. **Create a GitHub repository** for this skills collection
2. **Set up GitHub remote**: `git remote add origin <your-github-repo-url>`
3. **Push initial commit**: `git push -u origin main`
4. **Update this README** with your actual GitHub repository URL

## Troubleshooting

### Skill Not Loading
- Verify the skill is in the correct directory: `c:\Users\kahye\.codex\skills`
- Check that SKILL.md follows the correct format
- Restart your agent framework

### Git Issues
- Ensure you're in the correct directory: `c:\Users\kahye\.codex\skills`
- Check git status: `git status`
- View commit history: `git log --oneline`

## License

[Add your license information here]

## Contact

For questions about these skills or the orchestrator workflow, refer to the individual SKILL.md files or create an issue in this repository.
