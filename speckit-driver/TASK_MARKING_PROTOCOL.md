# Task Marking Protocol

**Critical quality assurance mechanism for speckit-driver workflow**

## Problem Statement

Task marking (`[X]`) in tasks.md is crucial for:
- Progress tracking and recovery
- Accurate completion status
- Preventing duplicate work
- Enabling resumable workflows

**Common failure mode**: Tasks get completed but not marked, leading to:
- Inaccurate progress reports
- Re-execution of completed tasks on resume
- Loss of work tracking
- Confusion about project state

## Four-Layer Protection System

### Layer 1: Sub-Agent Mandatory Workflow

**Location**: `agents/speckit-implement.md`

**Rule**: EVERY completed task MUST be marked BEFORE proceeding.

**Enforced workflow**:
```
1. Execute task
2. Mark task [X] in tasks.md (MANDATORY)
3. Verify marking succeeded
4. ONLY THEN report completion
```

**Key requirements**:
- Use Edit tool to change `- [ ]` to `- [X]`
- Verify edit succeeded by reading line again
- Include "Marked: ✓" in completion report

**Wrong patterns (caught by this layer)**:
```
❌ Execute → Report → Next task (forgot to mark)
❌ Execute multiple → Mark all at end (if errors occur, marks lost)
❌ Report "done" without file update
```

### Layer 2: Mandatory Output Format

**Location**: `agents/speckit-implement.md` → "Your Output" section

**Rule**: Task completion reports MUST include marking confirmation.

**Required format**:
```markdown
✓ T012 Create User model in src/models/user.py
  - Implementation: [what was done]
  - Marked: ✓ Updated tasks.md (T012 marked [X])
  - Status: Complete
```

**Enforcement**: If sub-agent cannot write "Marked: ✓", it has NOT properly completed the task.

**Benefits**:
- Forces sub-agent to confirm marking
- Makes missing marks immediately visible
- Creates audit trail in conversation

### Layer 3: Main Agent Active Monitoring

**Location**: `skills/speckit-driver/SKILL.md` → Phase 4

**Rule**: Main agent actively verifies each task completion includes marking confirmation.

**Monitoring protocol**:

1. **Per-task verification**:
   ```
   For each task report:
     IF "Marked: ✓" present:
       ✓ Accept completion
     ELSE:
       ⚠️ Alert and block next task
       Require immediate marking
   ```

2. **Periodic audits** (every 5-10 tasks):
   ```
   Request status table from sub-agent
   Verify [X] count matches completion count
   IF mismatch:
     List missing marks
     Require correction before continuing
   ```

3. **Active intervention**:
   ```
   IF marking missing:
     Main Agent: "⚠️ T005 completed but NOT marked"
     Main Agent: "Mark T005 as [X] in tasks.md NOW"
     Wait for: "✓ T005 marked" confirmation
     THEN: Allow next task
   ```

**Benefits**:
- Catches omissions in real-time
- Prevents cascade of unmarked tasks
- Maintains accurate state throughout

### Layer 4: Final Audit on Completion

**Location**: `skills/speckit-driver/SKILL.md` → Phase 4, Step 4

**Rule**: After implementation, main agent MUST perform marking audit.

**Audit protocol**:

```bash
# Step 1: Read tasks.md directly
Read tasks.md

# Step 2: Count tasks
Total tasks: grep -c "^- \[" tasks.md
Completed: grep -c "^- \[X\]" tasks.md (check both [X] and [x])

# Step 3: Compare with sub-agent report
Sub-agent claimed: N tasks complete
File shows: M tasks marked [X]

# Step 4: If mismatch (N != M)
IF N > M:
  ⚠️ MISMATCH: Some tasks unmarked
  Identify which: diff completed list vs marked list
  Fix: Mark missing tasks
  Verify: Re-count
ELSE:
  ✓ Audit passed
```

**Benefits**:
- Final safety net before completion
- Corrects any missed marks
- Ensures clean final state
- Enables confident resume later

## Implementation Examples

### Example 1: Correct Execution

```markdown
Main Agent: Invoking speckit-implement...

Sub-agent: Starting implementation...

Sub-agent:
✓ T001 Initialize project structure
  - Implementation: Created src/, tests/, docs/ directories
  - Marked: ✓ Updated tasks.md (T001 marked [X])
  - Status: Complete

Main Agent: ✓ Verified T001 marked

Sub-agent:
✓ T002 Install dependencies
  - Implementation: Ran npm install, 47 packages installed
  - Marked: ✓ Updated tasks.md (T002 marked [X])
  - Status: Complete

Main Agent: ✓ Verified T002 marked

[After 10 tasks]

Main Agent: Requesting status audit...

Sub-agent:
| Task ID | Description | Status | Marked |
|---------|-------------|--------|--------|
| T001 | Init structure | ✓ Done | ✓ [X] |
| T002 | Install deps | ✓ Done | ✓ [X] |
...
| T010 | Create service | ✓ Done | ✓ [X] |

Main Agent: ✓ Audit passed (10/10 marked)

[After all tasks]

Main Agent: Performing final audit...
Main Agent: Reading tasks.md...
Main Agent: Total: 42 tasks, Marked [X]: 42 tasks
Main Agent: ✓ All tasks properly marked
Main Agent: ✓ Implementation complete and verified
```

### Example 2: Catching Missing Mark (Layer 3)

```markdown
Sub-agent:
✓ T015 Implement auth middleware
  - Implementation: Created middleware in src/middleware/auth.js
  - Status: Complete

Main Agent: ⚠️ WARNING - Marking confirmation missing

Main Agent: "T015 is reported complete but I don't see 'Marked: ✓' in your report.
Did you update tasks.md? If not, do it NOW before continuing."

Sub-agent: You're right, I forgot. Marking now...
[Uses Edit tool to mark T015]

Sub-agent: ✓ Corrected: T015 now marked [X] in tasks.md

Main Agent: ✓ Verified. You may continue.
```

### Example 3: Final Audit Catches Omissions (Layer 4)

```markdown
Sub-agent: Implementation complete! All 35 tasks finished.

Main Agent: Performing final audit...
Main Agent: [Reads tasks.md]
Main Agent: Counting marks...

Main Agent: ⚠️ TASK MARKING MISMATCH DETECTED

Sub-agent reported: 35 tasks complete
Tasks.md shows: 32 tasks marked [X]
Missing marks: 3 tasks

Main Agent: Identifying unmarked tasks...
Main Agent: Missing marks found:
- T012 (reported done but [ ] in file)
- T018 (reported done but [ ] in file)
- T029 (reported done but [ ] in file)

Main Agent: Fixing now...
[Marks T012, T018, T029 as [X]]

Main Agent: Re-counting...
Main Agent: ✓ Now showing 35/35 tasks marked
Main Agent: ✓ Audit passed
```

## Recovery Scenarios

### Scenario A: Implementation Interrupted Mid-Way

```markdown
[Implementation runs, then crashes at T025]

[User restarts later]

Main Agent: Resuming implementation...
Main Agent: [Invokes speckit-implement]

Sub-agent: [Reads tasks.md]
Sub-agent: Found 24 tasks marked [X] (T001-T024)
Sub-agent: Resuming from T025...

✓ T025 Create API endpoint
  - Implementation: Created /api/users endpoint
  - Marked: ✓ Updated tasks.md (T025 marked [X])
  - Status: Complete

[Continues from T025...]
```

**Why this works**: All completed tasks are marked [X], so sub-agent knows exactly where to resume.

### Scenario B: Manual Task Completion

```markdown
[User manually completes T042 outside of workflow]

User: "I manually implemented the logging feature (T042)"

Main Agent: "Let me mark that in tasks.md..."
[Marks T042 as [X]]

Main Agent: "✓ T042 marked as complete. Continuing with remaining tasks..."
```

## Failure Mode Analysis

### Without Protection

```markdown
Sub-agent executes T001-T010
Sub-agent reports "10 tasks done"
But tasks.md still shows:
  - [ ] T001
  - [ ] T002
  ...
  - [ ] T010

[If workflow restarts]
Sub-agent: "No completed tasks found, starting from T001"
→ Duplicate work!
```

### With 4-Layer Protection

```markdown
Layer 1: Sub-agent MUST mark each task
Layer 2: Sub-agent MUST report "Marked: ✓"
Layer 3: Main agent VERIFIES each report
Layer 4: Main agent AUDITS final state

Result: tasks.md accurately reflects:
  - [X] T001
  - [X] T002
  ...
  - [X] T010

[If workflow restarts]
Sub-agent: "Found 10 completed tasks, resuming from T011"
→ Correct behavior!
```

## Best Practices for Sub-Agent Developers

1. **Never batch mark**: Mark tasks immediately, not at end
2. **Always verify**: Read back the line after Edit to confirm [X]
3. **Always report**: Include "Marked: ✓" in every completion report
4. **Never skip on error**: Only mark [X] if task truly succeeded
5. **Use consistent format**: `- [X]` (not `- [x]` unless both are checked)

## Best Practices for Main Agent Orchestration

1. **Verify every report**: Check for "Marked: ✓" confirmation
2. **Audit periodically**: Don't wait until end to check
3. **Intervene immediately**: Block next task if marking missing
4. **Final audit mandatory**: Always verify final state
5. **Fix before finish**: Correct any omissions before reporting done

## Testing the Protocol

### Unit Test for Sub-Agent

```markdown
Test: Task marking is enforced
Given: A task T001 to execute
When: Sub-agent completes T001
Then:
  - tasks.md line changes from "- [ ] T001" to "- [X] T001"
  - Report includes "Marked: ✓ Updated tasks.md"
  - Cannot proceed to T002 without marking T001
```

### Integration Test for Full Workflow

```markdown
Test: End-to-end marking verification
Given: tasks.md with 10 tasks
When: Sub-agent executes all 10 tasks
Then:
  - All 10 reports include "Marked: ✓"
  - Main agent audit finds 10/10 marked
  - tasks.md grep shows 10 [X] marks
  - No tasks left in [ ] state
```

### Recovery Test

```markdown
Test: Resume after interruption
Given:
  - tasks.md with tasks T001-T020
  - T001-T012 marked [X]
  - Workflow interrupted
When: Workflow resumes
Then:
  - Sub-agent detects 12 completed
  - Resumes from T013
  - Does not re-execute T001-T012
```

## Metrics and Success Criteria

**Success metrics**:
- Marking accuracy: 100% (all completed tasks marked)
- Marking timeliness: Immediate (within same task execution)
- Audit pass rate: 100% (final audit always passes)
- Recovery accuracy: 100% (resume at correct task)

**Failure indicators**:
- Any task reported done without [X] mark
- Final audit finds unmarked tasks
- Resume starts from wrong task
- Duplicate work on resume

## Summary

The four-layer protection system ensures task marking integrity:

1. **Layer 1** (Sub-agent): Mandatory workflow prevents forgetting
2. **Layer 2** (Output format): Forces confirmation in reports
3. **Layer 3** (Active monitoring): Catches omissions in real-time
4. **Layer 4** (Final audit): Safety net before completion

**Result**: Robust, resumable, accurate progress tracking throughout the entire speckit workflow.
