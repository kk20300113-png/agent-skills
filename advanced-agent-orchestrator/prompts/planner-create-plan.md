# Create Comprehensive Execution Plan

## Original Task Brief

**Task**: [INSERT_TASK_DESCRIPTION]

**Constraints**: [LIST_CONSTRAINTS]

**Success Criteria**: [LIST_SUCCESS_CRITERIA]

## Additional Context

[IF_AVAILABLE: LOCAL_KNOWLEDGE_FILES]
[IF_AVAILABLE: RELEVANT_CODE_SNIPPETS]
[IF_AVAILABLE: EXISTING_CODEBASE_STRUCTURE]

## Your Role

You are the **Planner**. Create a detailed, actionable execution plan that will be reviewed (possibly by another agent) and then executed.

**Be explicit about your reasoning.** If another agent reviews this plan, they need to understand your thinking, not just your conclusions.

## Output Requirements

### 1. Executive Summary (2-3 paragraphs)

Brief overview of:
- Approach and high-level strategy
- Key decisions made
- Expected outcomes and deliverables
- Any major risks or concerns

### 2. Phase Breakdown

Numbered phases with details:

```
Phase 1: [Name]
- Objective: What this phase accomplishes
- Actions: Specific steps to take
- Files to Create/Modify: [list]
- Dependencies: What must be done first
- Estimated Lines: Rough estimate
- Time Estimate: Rough estimate

Phase 2: [Name]
[Same structure]

[Continue for all phases]
```

**For coding tasks, include:**
- Components to create
- Functions to implement
- API endpoints to modify
- Database changes needed
- Tests to write

### 3. Key Decisions with Rationale

For each major decision, document:

**Decision:** What you decided

**Rationale:** Why this is the best approach
- Technical reasons
- Trade-offs considered
- Alignment with constraints/success criteria

**Alternatives Considered:** What else you thought of

**Why Rejected:** Why those alternatives are worse
- Limitations of alternatives
- Cost/benefit analysis

**Example:**
```
Decision: Use React Query for data fetching
Rationale: Built-in caching reduces API calls by ~70%, matches requirement 
for responsive UI. Stale-while-revalidate strategy fits user mental model.
Alternatives Considered: Axios + manual cache, SWR
Why Rejected: Axios requires custom cache implementation (more code to 
maintain). SWR less mature ecosystem.
```

### 4. Risk Assessment

**High Risk** (could block task or cause major issues):
- [Risk description]
- [Mitigation strategy]
- [Contingency plan if mitigation fails]

**Medium Risk** (may cause complications):
- [Risk description]
- [Mitigation strategy]

**Low Risk** (minor inconvenience, easily worked around):
- [Risk description]
- [Workaround]

**Example:**
```
High Risk: External API rate limits (100 req/min) may throttle data import
Mitigation: Implement exponential backoff with jitter
Contingency: Batch processing with 500ms delays between batches
```

### 5. Dependencies & Prerequisites

**External:**
- APIs, libraries, services needed
- Versions required
- Setup/configuration needed

**Internal:**
- Existing code dependencies
- Database schemas
- Environment variables

**Access:**
- Permissions needed
- Credentials required
- Who to contact for access

### 6. Confidence Score

Rate your confidence in this plan: **[0-100]%**

**Factors contributing to confidence:**
- Familiarity with technology
- Clarity of requirements
- Known vs unknown elements
- Similar tasks completed successfully

**Factors reducing confidence:**
- [Specific uncertainty]
- [Ambiguity in requirements]
- [Technical unknowns]
- [External dependencies]

**Example:** "Confidence: 85% - Familiar with React Query, clear requirements, but unclear on API pagination structure."

### 7. Recommendation

**Verdict:**
- [ ] **PROCEED** - Plan is solid, ready for execution
- [ ] **PROCEED_WITH_CAVEATS** - Good overall, but note concerns above
- [ ] **CLARIFY_REQUIREMENTS** - Need more information before proceeding

**Why:** [Explain your recommendation]

If clarifying: **What specific information do you need?**

### 8. Questions for Reviewer

**If this plan will be reviewed, what should the reviewer focus on?**

- [Area you're uncertain about]
- [Area where alternative approaches might exist]
- [Technical decision that could be controversial]

---

## Formatting Rules

**Be specific and concrete:**
- ❌ "Implement user interface"
- ✅ "Create UserTable.jsx with columns: ID, Name, Email, Actions. Use MUI DataTable with pagination controls."

**Include examples where helpful:**
```
API endpoint expected format:
GET /api/users?page=1&limit=50
Response: { users: [...], total: 125, page: 1, pages: 3 }
```

**Quantify when possible:**
- ❌ "Handle errors appropriately"
- ✅ "Add error boundaries at Page level. Log to console. Show user-friendly message with retry button."

**Be explicit about edge cases:**
- ❌ "Handle empty state"
- ✅ "If no users: show 'No users found' message with 'Create User' button. If API error: show error banner."

---

## Example Output Structure

```
## Executive Summary
Build a reusable UserTable component with server-side pagination.
Key decisions: React Query for caching, MUI DataTable for base, custom usePagination hook.
Expected outcome: Component can handle 10K+ users, <100ms response time.

## Phase Breakdown
Phase 1: Setup React Query
- Objective: Configure data fetching library
- Actions: Install @tanstack/react-query, setup QueryClient, wrap App
- Files: src/main.jsx (modify), src/queryClient.js (create)
- Estimated: 15 lines

Phase 2: Create usePagination hook
- Objective: Reusable pagination logic
- Actions: Custom hook managing page state, fetch calls
- Files: src/hooks/usePagination.js (create)
- Dependencies: Phase 1 complete
- Estimated: 80 lines

[More phases...]

## Key Decisions
Decision: Use React Query over SWR
Rationale: Better caching, devtools, used successfully in 3 past projects
Alternatives: SWR, custom fetch hook
Why Rejected: SWR lacks devtools, custom hook = more code to maintain

[More decisions...]

## Risk Assessment
High Risk: API pagination structure unknown
Mitigation: Create adapter layer to map API response to expected format
Contingency: If API changes, only adapter needs update

Medium Risk: Large dataset performance
Mitigation: Use React Query's built-in windowing

## Dependencies
External: @tanstack/react-query v5.x
Internal: User API must support pagination
Access: API docs at https://api-docs.example.com

## Confidence Score
85% - Familiar with React Query, clear requirements, but API pagination schema unclear

## Recommendation
PROCEED_WITH_CAVEATS - Plan is solid but need to confirm API pagination format
```

---

## Final Check

Before outputting, verify:
- [ ] All requirements from task brief are addressed
- [ ] Constraints are respected in plan
- [ ] Success criteria can be met
- [ ] Each phase is specific and actionable
- [ ] Key decisions include rationale
- [ ] Risks are identified with mitigations
- [ ] Confidence score is honest (not overly optimistic)
- [ ] Recommendation is clear

**Remember:** This plan will be reviewed and executed. Ambiguity causes failure. Be explicit.
