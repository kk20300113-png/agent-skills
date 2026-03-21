# Executor Improvement Handoff (V1 → V2)

## Your Original Output (V1)

[INSERT_EXECUTOR_V1_OUTPUT]

## Review Feedback

### Primary Reviewer ([REVIEWER_1_NAME]) Feedback

[INSERT_PRIMARY_REVIEW]

### Secondary Reviewer ([REVIEWER_2_NAME]) Feedback

[INSERT_SECONDARY_REVIEW or "No secondary review for this task"]

## Your Role

You are the **Executor**. Address the review feedback and produce an improved V2 implementation.

## Conflict Resolution Guide

When reviewers disagree or provide conflicting feedback:

1. **Critical Issues First**
   - Always fix issues marked as "Critical" by either reviewer
   - Safety/correctness issues take priority

2. **Consensus Issues**
   - If both reviewers mention the same issue → Definitely fix
   - High confidence that it's a real problem

3. **Conflicting Feedback**
   - Reviewers contradict each other → Use your judgment
   - Document your decision and rationale
   - Prefer correctness over style when in doubt

4. **Unclear Priority**
   - If unsure whether to implement a suggestion → Ask for clarification
   - When in doubt, implement the safer option

5. **Trade-offs**
   - You don't need to implement every suggestion
   - Prioritize based on: correctness > maintainability > style
   - Document which suggestions you rejected and why

## Improvement Priorities

### P0 - Critical (Must Fix)
- [ ] Critical Issue 1
- [ ] Critical Issue 2

### P1 - High Priority (Should Fix)
- [ ] High priority improvement 1
- [ ] High priority improvement 2

### P2 - Medium Priority (Fix if Time)
- [ ] Medium priority item 1
- [ ] Medium priority item 2

### P3 - Suggestions (Optional)
- [ ] Suggestion 1
- [ ] Suggestion 2

## Output Requirements

### 1. Improved Implementation (V2)
- All code/files updated
- Address P0 and P1 items
- Document any rejected feedback

### 2. Changelog
- List of changes made
- Rationale for each change
- Items considered but rejected (with reason)

### 3. Test Results
- Re-run tests
- Verify critical issues resolved
- New test cases if needed

### 4. Response to Reviews
- Address each critical issue
- Acknowledge improvements made
- Explain rejected suggestions

## Output Format

```
## Implementation V2

[Updated code/files]

## Changelog

### Changes Made
1. [Change 1] - [Rationale]
2. [Change 2] - [Rationale]

### Rejected Suggestions
1. [Suggestion] - [Reason for rejection]
2. [Suggestion] - [Reason for rejection]

## Test Results (V2)

- Test 1: [PASS/FAIL] - [Description]
- Test 2: [PASS/FAIL] - [Description]
- New Test: [PASS/FAIL] - [Description]

## Response to Review Feedback

### Critical Issues Addressed
1. [Issue 1]: [How it was fixed]
2. [Issue 2]: [How it was fixed]

### Improvements Implemented
1. [Improvement 1]: [What changed]
2. [Improvement 2]: [What changed]

### Conflict Resolutions
1. [Conflict]: [Decision made] - [Rationale]

## Verification Checklist

- [ ] All P0 (Critical) issues resolved
- [ ] All P1 (High) issues resolved or consciously deferred
- [ ] Tests pass
- [ ] Success criteria still met
- [ ] No regressions introduced
- [ ] Documentation updated

## Ready for Final Review

V2 is complete and ready for final judgment.
```

Produce V2 now by addressing the review feedback.
