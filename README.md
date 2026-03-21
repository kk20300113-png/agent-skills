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

A cost-aware, complex-task orchestration workflow across multiple AI agents.

**Key Features:**
- Numbered role selection system for quick configuration
- Mandatory role confirmation before each task
- Official-source model freshness checking
- Multi-stage review checkpoints

**Role Selection Format:**
```
1. Executor: 1a (Kimi) or 1b (Gemini)
2. Planner: 2a (Claude Opus 4.6)
3. Reviewer: 3a (Gemini), 3b (Claude), or 3c (ChatGPT latest)
```

**Example Usage:**
```
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
