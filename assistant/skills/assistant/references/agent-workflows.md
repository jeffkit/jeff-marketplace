# Agent Autonomous Workflows

This document provides detailed guidance for Claude when working autonomously (triggered by scheduled tasks or external events) with the assistant skill.

## Table of Contents

1. [Core Principles](#core-principles)
2. [Data Access Pattern](#data-access-pattern)
3. [Scheduled Trigger Workflow](#scheduled-trigger-workflow)
4. [User-Initiated Workflow](#user-initiated-workflow)
5. [External Agent Integration](#external-agent-integration)
6. [Human-in-the-Loop (HIL) Communication](#human-in-the-loop-hil-communication)
7. [Best Practices](#best-practices)

---

## Core Principles

### Read vs Write Pattern

**IMPORTANT:** When working autonomously, Claude should:
- ✅ **Read data files directly** using the `Read` tool
- ✅ **Write data using scripts** to ensure data integrity

**Rationale:**
- **Reading**: `active-todos.json` and journal markdown files are pure data - Claude can read them directly without script overhead
- **Writing**: All modifications must go through scripts to maintain data consistency, handle archiving, and validate fields

### Example

```markdown
# ❌ WRONG: Using script to read
python3 scripts/todo_manager.py list --status pending

# ✅ CORRECT: Direct read
Read .assistant/active-todos.json

# ✅ CORRECT: Using script to write
python3 scripts/todo_manager.py update 5 --status completed
```

---

## Data Access Pattern

### File Locations

```
.assistant/
├── active-todos.json           # Read directly ✅
├── archived-todos.json         # Read directly ✅ (when needed)
└── journals/
    └── 2026-01/
        └── 2026-01-05.md      # Read directly ✅
```

### Reading Active TODOs

```markdown
# Step 1: Read the active todos file
Read .assistant/active-todos.json

# Step 2: Parse and analyze
The file contains a JSON array of TODO objects with fields:
- id, title, status, priority, category
- project, assignee, tags, description
- next_action_time, needs_clarification, clarification_question
- blockers, auto_progress_hint, last_reviewed
- created_at, updated_at, due_date

# Step 3: Identify TODOs that need attention
Look for:
1. next_action_time <= current time
2. needs_clarification = true
3. due_date approaching or overdue
4. blockers array not empty
```

### Reading Today's Journal

```markdown
# Read today's journal
Read .assistant/journals/2026-01/2026-01-05.md

# Parse frontmatter for metadata
# Read Agent work log section to see what was done earlier
```

---

## Scheduled Trigger Workflow

### Typical Scenario

External system triggers Claude at scheduled time (e.g., 9:00 AM daily). Claude should:

1. **Initialize and assess**
2. **Identify action items**
3. **Execute actions**
4. **Record work**

### Detailed Step-by-Step

#### Step 1: Read Current State

```markdown
1. Read .assistant/active-todos.json
2. Read .assistant/journals/YYYY-MM/YYYY-MM-DD.md (today's journal)
3. Parse both files to understand current context
```

#### Step 2: Identify TODOs Needing Attention

```python
# Pseudo-logic for filtering
current_time = now()

needs_attention = []

for todo in active_todos:
    if todo.needs_clarification:
        needs_attention.append({
            "todo_id": todo.id,
            "action": "clarify_with_user",
            "reason": todo.clarification_question
        })

    elif todo.next_action_time and todo.next_action_time <= current_time:
        if todo.auto_progress_hint:
            needs_attention.append({
                "todo_id": todo.id,
                "action": "call_external_agent",
                "hint": todo.auto_progress_hint
            })
        else:
            needs_attention.append({
                "todo_id": todo.id,
                "action": "follow_up",
                "reason": "Scheduled action time reached"
            })

    elif todo.due_date and todo.due_date <= today:
        needs_attention.append({
            "todo_id": todo.id,
            "action": "remind_user",
            "reason": "Due date approaching/overdue"
        })

    elif len(todo.blockers) > 0:
        needs_attention.append({
            "todo_id": todo.id,
            "action": "check_blockers",
            "blockers": todo.blockers
        })
```

#### Step 3: Execute Actions

For each item in `needs_attention`, choose appropriate action:

**Action Type: clarify_with_user**
```markdown
Use mcp__hil__send_and_wait_reply tool:

mcp__hil__send_and_wait_reply(
    message: f"关于TODO #{todo_id} '{todo.title}'，{clarification_question}",
    project_name: "assistant-autonomous"
)

Wait for user response, then update TODO:
python3 scripts/todo_manager.py update {todo_id} \
    --needs-clarification false \
    --description "{user's answer}"
```

**Action Type: call_external_agent**
```markdown
Use mcp__a2a-client__call_external_agent tool:

# Example: Calling code-reviewer agent
mcp__a2a-client__call_external_agent(
    agentUrl: "https://example.com/agents/code-reviewer",
    agentName: "Code Reviewer",
    message: f"Check the status of PR #123 related to TODO: {todo.title}",
    useTask: false
)

Based on agent response, update TODO:
python3 scripts/todo_manager.py update {todo_id} \
    --auto-progress-hint "Code review completed, ready to merge" \
    --next-action-time "{tomorrow_9am}"
```

**Action Type: remind_user**
```markdown
Use mcp__hil__send_message_only tool:

mcp__hil__send_message_only(
    message: f"⏰ 提醒：TODO #{todo_id} '{todo.title}' 的截止日期是 {due_date}，请及时处理。",
    project_name: "assistant-autonomous"
)

Update last_reviewed:
python3 scripts/todo_manager.py update {todo_id} \
    --last-reviewed "{now}"
```

#### Step 4: Record Agent Work Session

```markdown
python3 scripts/journal_manager.py add-agent-session \
    --trigger "scheduled" \
    --actions "发送澄清问题给用户(TODO #5);调用code-reviewer检查PR #123(TODO #3);提醒用户TODO #7即将到期" \
    --observations "用户对jeff-marketplace项目进度比较关注" \
    --next-hint "明天09:00继续跟进用户对TODO #5的回复"
```

---

## User-Initiated Workflow

### Scenario: User Contacts Agent with TODO Request

```markdown
User: "帮我记录一个任务：修复用户登录bug"

Agent workflow:
1. Extract task description
2. Ask clarifying questions (project, assignee, priority, etc.)
3. Assess if immediate clarification is needed or can wait
4. Create TODO with appropriate fields
5. Confirm to user

Example:
User: "帮我记录：修复用户登录bug"
Agent: "好的，让我确认几个细节：
- 这是哪个项目的任务？
- 需要分配给谁？
- 优先级如何？
- 具体的bug现象是什么？"

User: "jeff-marketplace项目，分配给alice，高优先级，用户在登录时返回500错误"

Agent decision:
- Still needs clarification: 具体的复现步骤是什么？
- But can defer this to avoid blocking user
- Set needs_clarification = true with question

Agent executes:
python3 scripts/todo_manager.py add "修复用户登录bug" \
    --project jeff-marketplace \
    --assignee alice \
    --category work \
    --priority high \
    --description "用户在登录时返回500错误" \
    --needs-clarification \
    --clarification-question "具体的复现步骤是什么？浏览器控制台有什么错误信息？" \
    --next-action-time "2026-01-06T14:00:00"

Agent response:
"已记录！这个bug任务已分配给alice。我注意到还需要一些技术细节（复现步骤、错误信息等），我会在明天下午2点跟进这些信息。"

# Record journal entry
python3 scripts/journal_manager.py add "用户报告jeff-marketplace项目的登录bug，已创建TODO并分配给alice" \
    --category work \
    --mood neutral \
    --tags jeff-marketplace,bug,user-request
```

---

## External Agent Integration

### Available External Agents

**How to find available agents:**

Check Claude Code's available MCP tools and A2A agents. Currently available:
- `mcp__a2a-client__call_external_agent`: Call any A2A-compatible agent

**Agent Discovery:**
- User should configure available external agents in their environment
- Claude can ask user: "我可以调用哪些外部agent来帮助处理这个任务？"

### Example: Code Review Agent

```markdown
# Scenario: TODO has auto_progress_hint about checking PR

TODO:
{
  "id": 3,
  "title": "优化数据库查询性能",
  "auto_progress_hint": "Call code-reviewer agent to check PR #456 status",
  "next_action_time": "2026-01-05T10:00:00"
}

# Agent executes:
result = mcp__a2a-client__call_external_agent(
    agentUrl: "{configured_agent_url}",
    agentName: "Code Reviewer",
    message: "Please check the review status of PR #456 for database query optimization",
    useTask: false
)

# Based on result, update TODO:
if "approved" in result:
    python3 scripts/todo_manager.py update 3 \
        --status in_progress \
        --auto_progress_hint "PR approved, ready to merge" \
        --next-action-time "2026-01-06T09:00:00"
elif "changes requested" in result:
    python3 scripts/todo_manager.py update 3 \
        --blockers "Code review requested changes" \
        --auto_progress_hint "Address review comments first"
```

### When to Use External Agents

Use external agents when:
1. **auto_progress_hint** explicitly suggests calling an agent
2. **Task type** is technical and can benefit from specialized agents (code review, testing, deployment)
3. **Blocking condition** can be resolved by an external system check

---

## Human-in-the-Loop (HIL) Communication

### Available HIL Tools

**Primary tool:** `mcp__hil__send_and_wait_reply`
- Sends message to user via WeChat Work (企业微信)
- Waits for user response (user must @mention the bot)
- Returns user's reply

**Secondary tool:** `mcp__hil__send_message_only`
- Sends message without waiting for reply
- Use for notifications, reminders, status updates

### When to Use send_and_wait_reply

```markdown
✅ Use send_and_wait_reply when:
1. TODO has needs_clarification = true
2. User input is required to proceed
3. Decision is needed from user

❌ Do NOT use ask_user_question tool
The skill should use HIL tools for user communication, not ask_user_question
```

### Example: Async Clarification

```markdown
# Scenario: TODO needs clarification

TODO:
{
  "id": 5,
  "title": "优化数据库查询",
  "needs_clarification": true,
  "clarification_question": "是优化所有查询还是只针对慢查询？",
  "next_action_time": "2026-01-05T14:00:00"
}

# At 14:00, agent executes:
response = mcp__hil__send_and_wait_reply(
    message: "关于TODO #5 '优化数据库查询'，需要确认一下：是优化所有查询还是只针对慢查询（>1s）？",
    project_name: "assistant-autonomous"
)

# User replies: "只针对慢查询，超过1秒的"

# Update TODO:
python3 scripts/todo_manager.py update 5 \
    --needs-clarification false \
    --description "优化数据库查询：只针对慢查询（>1s）" \
    --last-reviewed "{now}"

# Record in journal:
python3 scripts/journal_manager.py add "TODO #5 澄清完成：用户确认只优化慢查询" \
    --category work \
    --mood neutral \
    --tags database,clarification
```

### Message Formatting Best Practices

```markdown
# ✅ GOOD: Clear, actionable message
"关于TODO #5 '优化数据库查询'：
需要确认具体范围：
1. 优化所有查询？
2. 只优化慢查询（>1s）？
3. 其他标准？

请回复序号或具体说明。"

# ❌ BAD: Vague message
"有个问题想确认一下"
```

---

## Best Practices

### 1. Efficient Data Reading

```markdown
# ✅ GOOD: Read file once, analyze in memory
Read .assistant/active-todos.json
# Parse and filter in one pass
needs_attention = filter_todos(todos, criteria)

# ❌ BAD: Multiple script calls
python3 scripts/todo_manager.py list --status pending
python3 scripts/todo_manager.py list --priority high
# (Each call loads file from disk)
```

### 2. Batching Updates

```markdown
# ✅ GOOD: Update TODO once with all changes
python3 scripts/todo_manager.py update 5 \
    --needs-clarification false \
    --description "新描述" \
    --last-reviewed "{now}"

# ❌ BAD: Multiple updates
python3 scripts/todo_manager.py update 5 --needs-clarification false
python3 scripts/todo_manager.py update 5 --description "新描述"
python3 scripts/todo_manager.py update 5 --last-reviewed "{now}"
```

### 3. Context Awareness

```markdown
# Before taking action, always read:
1. Today's journal - What happened earlier today?
2. Active TODOs - Full context of all active work
3. User's recent interactions - Last session's observations

# This prevents:
- Redundant questions
- Conflicting actions
- Missing context
```

### 4. Graceful Degradation

```markdown
# If external agent call fails:
1. Log the failure
2. Set TODO blocker
3. Notify user if critical

# Example:
try:
    result = call_external_agent(...)
except:
    python3 scripts/todo_manager.py update {id} \
        --blockers "External agent unavailable" \
        --next-action-time "{retry_time}"

    mcp__hil__send_message_only(
        message: f"TODO #{id}: 外部agent调用失败，将在{retry_time}重试"
    )
```

### 5. Recording Work Sessions

**ALWAYS record agent sessions** to maintain continuity:

```markdown
After completing autonomous work session:

python3 scripts/journal_manager.py add-agent-session \
    --trigger "scheduled" \
    --actions "{semicolon-separated list of actions}" \
    --observations "{insights about user needs or project status}" \
    --next-hint "{when and why to run next session}"
```

### 6. Respecting User Time

```markdown
# ✅ GOOD: Defer non-urgent clarifications
- If it's late at night: Set next_action_time for next morning
- If user is busy: Batch multiple questions together
- If not critical: Wait for user to initiate contact

# ❌ BAD: Interrupting user immediately
- Don't send messages at midnight
- Don't ask trivial questions when user is focused
```

---

## Complete Example: Daily Morning Routine

```markdown
# 9:00 AM - Scheduled trigger

## Step 1: Read current state
Read .assistant/active-todos.json
Read .assistant/journals/2026-01/2026-01-05.md

## Step 2: Analyze
active_todos = 12
needs_clarification = 2 (TODO #5, #7)
overdue = 1 (TODO #3)
next_action_due = 3 (TODO #8, #9, #11)

## Step 3: Execute actions

### Action 1: Handle overdue TODO
mcp__hil__send_message_only(
    message: "⏰ 提醒：TODO #3 '完成项目文档' 已逾期2天，请及时处理。"
)

### Action 2: Clarify TODO #5
response = mcp__hil__send_and_wait_reply(
    message: "关于TODO #5 '数据库优化'，需要确认：优化所有查询还是只针对慢查询？"
)

python3 scripts/todo_manager.py update 5 \
    --needs-clarification false \
    --description "优化慢查询（用户回复：{response})"

### Action 3: Call external agent for TODO #8
result = mcp__a2a-client__call_external_agent(
    agentUrl: "{code_reviewer_url}",
    message: "Check PR #123 status"
)

python3 scripts/todo_manager.py update 8 \
    --auto-progress_hint "PR review: {result}"

### Action 4: Batch clarification for TODO #7
# Defer to avoid too many interruptions
python3 scripts/todo_manager.py update 7 \
    --next_action_time "2026-01-05T14:00:00"

## Step 4: Record session
python3 scripts/journal_manager.py add-agent-session \
    --trigger "scheduled" \
    --actions "提醒逾期TODO #3;澄清TODO #5数据库优化范围;调用code-reviewer检查TODO #8的PR状态;推迟TODO #7到下午" \
    --observations "用户对项目文档进度关注，需要加快TODO #3" \
    --next-hint "2026-01-05 14:00 跟进TODO #7的澄清"
```

---

## Summary Checklist

When working autonomously, always:

- ✅ Read `active-todos.json` and journal files directly
- ✅ Use scripts only for writing/updating data
- ✅ Check `next_action_time`, `needs_clarification`, `due_date`, `blockers`
- ✅ Use `mcp__hil__send_and_wait_reply` for user communication (NOT ask_user_question)
- ✅ Use `mcp__a2a-client__call_external_agent` for external agent calls
- ✅ Record every autonomous session in journal
- ✅ Batch actions to minimize user interruptions
- ✅ Consider user's time (don't message at midnight)
- ✅ Maintain context awareness (read previous sessions)
- ✅ Handle failures gracefully (set blockers, retry later)
