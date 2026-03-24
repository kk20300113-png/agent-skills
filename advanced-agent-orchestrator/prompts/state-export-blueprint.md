# State Export: Compile Implicit Knowledge to Explicit Blueprint

## Purpose

Before context window reset, force compilation of ALL implicit knowledge into portable, explicit artifacts. This prevents knowledge loss and enables clean-slate execution/review.

## Critical: This Is Not a Summary

**DO NOT** just summarize. **DO** extract and document every implicit assumption, edge case, and reasoning pattern that lives only in this conversation's context.

## Your Output Must Include

### 1. The Exact Technical Stack & Versions

```
Language: [Version]
Framework: [Version]
Key Libraries: [Name: Version, Name: Version]
Tools: [Build tool, Linter, Formatter, etc.]
Runtime Environment: [Node.js/Python/etc. Version]
```

**Example:**
```
Language: TypeScript 5.3
Framework: React 18.2
Key Libraries: @tanstack/react-query 5.24, MUI 5.15, Vitest 1.2
Tools: Vite 5.0, ESLint 8.56, Prettier 3.2
Runtime Environment: Node.js 20.x
```

### 2. Step-by-Step Implementation Sequence

**Every. Single. Step. In Order.**

```
Step 1: [Action]
- Command to run
- Expected outcome
- Verification method

Step 2: [Action]
- Command to run  
- Expected outcome
- Verification method

[Continue for all steps]
```

**Be precise enough that a developer who wasn't in this conversation could execute it.**

**BAD:** "Set up the project"
**GOOD:** "Run `npm create vite@latest my-app -- --template react-ts`. Verify `npm run dev` starts server on localhost:5173."

### 3. Implicit Knowledge (THIS IS THE CRITICAL PART)

Document everything we discussed but didn't write down. This is the "tribal knowledge" from our conversation.

#### Assumptions We Made
- List every assumption we made about: user behavior, data format, API behavior, environment setup, etc.
- **Why we made this assumption:** [Reasoning]
- **Risk if assumption is wrong:** [What breaks?]
- **How to validate assumption:** [Validation method]

**Example:**
```
Assumption: API returns pagination data in format {data: [], total: n, page: n}
Why: API docs show example response but don't explicitly document all fields
Risk: Wrong field mapping → broken pagination
Validation: Check actual API response structure first call
```

#### Edge Cases We Agreed to Handle
- List every edge case: empty states, error states, boundary conditions, race conditions
- **How we'll handle it:** [Specific implementation]
- **Why this matters:** [User impact]

**Example:**
```
Edge Case: User rapidly clicks "Next Page" button
How: Debounce with 300ms delay + loading state disabling button
Why: Prevents race conditions, reduces unnecessary API calls
```

#### Architectural Patterns We Chose (And Why)
For each pattern/decomposition decision:
- **Pattern chosen:** [e.g., "Custom hook for pagination logic"]
- **Rationale:** [Specific reasoning, not generic best practice]
- **Trade-offs accepted:** [What we gave up]
- **Alternative patterns rejected:** [What we considered and discarded]
- **Why rejected:** [Specific downsides for THIS use case]

**Example:**
```
Pattern: Extract pagination to usePagination hook
Rationale: Reusable across UserTable, ProductTable, OrderTable components
Trade-offs: Slightly more complex than inline logic, but DRY benefit high
Alternatives Considered:
  - Inline logic in UserTable: Rejected → duplication across 3 components
  - Higher-order component: Rejected → More boilerplate, less composable
  - Render prop pattern: Rejected → More verbose, harder to type in TypeScript
```

### 4. Strict Constraints (What Developers Must NOT Do)

**Explicit prohibitions.** These guardrails prevent subtle architectural drift.

```
❌ DO NOT change these decisions without explicit approval:
- Library choices (we chose React Query, do NOT switch to SWR or Axios)
- Component structure (keep UserTable dumb, logic in usePagination)
- API endpoint structure (use /api/users?page=X&limit=Y, do NOT change)
- Error handling approach (use ErrorBoundary at Page level, do NOT inline try/catch)

⚠️ DO NOT introduce these patterns:
- Global mutable state (use React Query cache, not global variables)
- Any class components (functional components only)
- Inline styles (use MUI theme system)

🚫 DO NOT modify these files outside specified steps:
- src/queryClient.js (only modify in Step 1)
- src/hooks/usePagination.js (only modify in Step 2)
```

### 5. Success Criteria Verification Methods

For each success criterion, specify **exactly** how to verify it works.

```
Criterion 1: [Description from requirements]
Verification: [Specific test, command, or manual check]
Acceptable Range: [Pass criteria]

Criterion 2: [Description]
Verification: [Specific method]
Acceptable Range: [Pass criteria]
```

**Example:**
```
Criterion: Table renders in <100ms for 50 rows
Verification: React DevTools Profiler, measure UserTable render time
Acceptable Range: <100ms on M2 Mac, <150ms on average dev machine

Criterion: Handles 10K+ user dataset
Verification: Generate mock data of 15K users, verify pagination loads pages 1, 50, 100
Acceptable Range: No crashes, each page loads in <200ms
```

### 6. Context That Would Help But Isn't Critical

**Optional context for implementation team:**
- Links to relevant resources we found
- Previous similar implementations for reference
- Known quirks of chosen libraries
- Debugging tips for common issues

**Example:**
```
Resource: React Query docs on pagination: https://tanstack.com/query/latest/docs/react/guides/paginated-queries
Reference: Previous usePagination implementation in orders feature (/src/hooks/useOrderPagination.js)
Quirk: MUI DataTable requires `keyField` prop for row selection to work properly
Debug: If pagination jumps to wrong page, check React Query `staleTime` configuration
```

## Output Format

```
# Context Blueprint: [Task Name]

## Technical Stack
[Section 1 content]

## Implementation Sequence
[Section 2 content - exhaustive steps]

## Implicit Knowledge

### Assumptions We Made
[Exhaustive list with rationale, risks, validation]

### Edge Cases Handled
[Exhaustive list with implementation details]

### Architectural Patterns Chosen
[Each pattern with full trade-off analysis]

## Strict Constraints
[What NOT to do - explicit prohibitions]

## Success Criteria Verification
[How to verify each criterion works]

## Helpful Context
[Optional resources, references, tips]

## Blueprint Confidence
Confidence this blueprint captures all implicit knowledge: [0-100]%

Uncertainty areas (what might still be ambiguous): [List]

## Next Phase Handoff
This blueprint is intended for: [Execution / External Review]
```

## Critical Reminder

**If you don't document it here, it will be lost forever when this context window closes.**

The execution/review agent will NOT have access to:
- Our back-and-forth discussion
- Your reasoning process
- The options we considered and discarded
- The subtle trade-offs we debated

**Everything must be explicit in this document or it doesn't exist.**

## Example of Good vs Bad

**BAD (loses critical knowledge):**
```
Assumption: API will work
Edge cases: Handle errors
Pattern: Use custom hook
```

**GOOD (preserves knowledge):**
```
Assumption: API returns consistent response structure (based on staging tests 2024-01-15)
Risk: Production might differ → breaks pagination
Validation: Log first 5 responses in production, alert if structure changes

Edge Case: User navigates away before API responds
Implementation: Cancel request in useEffect cleanup with AbortController
Why: Prevents memory leaks and state updates on unmounted component

Pattern: Extract to usePagination hook (not inline)
Rationale: Reused across 3 table components (User, Product, Order) in current sprint
Trade-off: +1 file, +15 lines, but eliminates 180 lines of duplicated logic
Rejected: Inline (duplication), HOC (unwieldy composition), Render props (boilerplate)
```
