# Data Schemas

This document provides detailed schema information for TODO and journal data structures.

## Data Storage Architecture (v1.2.0)

### Dual-File TODO System

- **`active-todos.json`**: Contains active tasks (pending, in_progress, needs_clarification)
- **`archived-todos.json`**: Contains completed and cancelled tasks
- Auto-archiving: Tasks with status `completed` or `cancelled` are automatically moved to archived file

### Daily Markdown Journals

- **Location**: `.assistant/journals/YYYY-MM/YYYY-MM-DD.md`
- **Format**: Markdown with YAML frontmatter
- **Structure**: Organized by time periods (早晨, 下午, 晚上) plus daily summary and agent session records

---

## TODO Schema

### Full Structure (v1.2.0)

```json
{
  "id": 1,
  "title": "Complete project report",
  "category": "work",
  "priority": "high",
  "status": "pending",
  "due_date": "2025-11-25",
  "project": "jeff-marketplace",
  "assignee": "jeff",
  "tags": ["documentation", "urgent", "milestone"],
  "description": "Complete quarterly project report with metrics and analysis",
  "next_action_time": "2025-11-26T09:00:00",
  "needs_clarification": false,
  "clarification_question": "",
  "blockers": [],
  "last_reviewed": "2025-11-20T10:30:00",
  "auto_progress_hint": "Can call code-reviewer agent for PR #123",
  "created_at": "2025-11-20T10:30:00",
  "updated_at": "2025-11-20T10:30:00"
}
```

### Field Definitions

#### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Auto-generated unique identifier |
| `title` | string | Task description or title |
| `category` | string | Task category (see options below) |
| `priority` | string | Task priority level (see options below) |
| `status` | string | Current task status (see options below) |
| `created_at` | string | ISO 8601 timestamp of creation |
| `updated_at` | string | ISO 8601 timestamp of last update |

#### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `due_date` | string | Due date in YYYY-MM-DD format |
| `project` | string | Project name or identifier for grouping tasks |
| `assignee` | string | Person assigned to complete the task |
| `tags` | array[string] | Flexible labels for multi-dimensional categorization |
| `description` | string | Detailed task requirements or notes |

#### New Fields (v1.2.0) - Agent Autonomous Work

| Field | Type | Description |
|-------|------|-------------|
| `next_action_time` | string | ISO 8601 timestamp for when to next follow up on this task |
| `needs_clarification` | boolean | Flag indicating this task requires user input before proceeding |
| `clarification_question` | string | Specific question that needs clarification from user |
| `blockers` | array[string] | List of factors blocking progress on this task |
| `last_reviewed` | string | ISO 8601 timestamp of when agent last reviewed this task |
| `auto_progress_hint` | string | Hint for external agents or automated actions (e.g., "Call code-reviewer for PR #123") |

### Field Value Options

**Categories:**
- `work`: Work-related tasks
- `life`: Personal life tasks
- `study`: Learning and education
- `health`: Health and fitness
- `finance`: Financial matters
- `hobby`: Hobbies and interests
- `other`: Miscellaneous tasks

**Priorities:**
- `high`: Urgent and important tasks
- `medium`: Normal priority tasks
- `low`: Low priority or optional tasks

**Statuses:**
- `pending`: Not yet started
- `in_progress`: Currently being worked on
- `completed`: Finished successfully
- `cancelled`: Abandoned or no longer needed

### Example Scenarios

**Simple TODO (Backward Compatible):**
```json
{
  "id": 1,
  "title": "买菜",
  "category": "life",
  "priority": "medium",
  "status": "pending",
  "created_at": "2025-11-20T10:00:00",
  "updated_at": "2025-11-20T10:00:00"
}
```

**Enhanced TODO with Project Management:**
```json
{
  "id": 2,
  "title": "实现用户认证功能",
  "category": "work",
  "priority": "high",
  "status": "in_progress",
  "due_date": "2025-11-30",
  "project": "jeff-marketplace",
  "assignee": "jeff",
  "tags": ["backend", "security", "auth", "urgent"],
  "description": "添加JWT登录和用户注册功能，包括邮箱验证",
  "created_at": "2025-11-18T09:00:00",
  "updated_at": "2025-11-20T14:30:00"
}
```

---

## Journal Entry Schema

### Full Structure

```json
{
  "id": 1,
  "content": "Today I learned about Python decorators and how they can simplify code",
  "category": "study",
  "mood": "happy",
  "tags": ["python", "learning", "decorators"],
  "timestamp": "2025-11-20T15:45:00"
}
```

### Field Definitions

#### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Auto-generated unique identifier |
| `content` | string | Journal entry content |
| `category` | string | Entry category (see options below) |
| `mood` | string | User's mood when writing (see options below) |
| `timestamp` | string | ISO 8601 timestamp of creation |

#### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `tags` | array[string] | Keywords or topics for categorization |

### Field Value Options

**Categories:**
- `work`: Work-related reflections
- `life`: Personal life events
- `study`: Learning experiences
- `health`: Health and wellness notes
- `reflection`: General reflections and thoughts
- `achievement`: Accomplishments and milestones
- `other`: Miscellaneous entries

**Moods:**
- `happy`: Positive, joyful state
- `neutral`: Calm, balanced state
- `sad`: Negative, down state
- `excited`: Energized, enthusiastic state
- `tired`: Fatigued, exhausted state
- `motivated`: Driven, determined state
- `stressed`: Anxious, overwhelmed state
- `relaxed`: Calm, peaceful state

### Example Scenarios

**Simple Journal Entry:**
```json
{
  "id": 1,
  "content": "今天天气很好，去公园散步了",
  "category": "life",
  "mood": "happy",
  "timestamp": "2025-11-20T16:00:00"
}
```

**Detailed Study Journal:**
```json
{
  "id": 2,
  "content": "深入学习了Python装饰器的原理，理解了闭包和高阶函数的概念。装饰器本质上是一个接受函数作为参数并返回新函数的函数。",
  "category": "study",
  "mood": "motivated",
  "tags": ["python", "decorators", "functional-programming", "advanced"],
  "timestamp": "2025-11-20T20:30:00"
}
```

**Work Achievement:**
```json
{
  "id": 3,
  "content": "成功完成了用户认证模块的开发，所有测试通过。团队对代码质量很满意。",
  "category": "achievement",
  "mood": "excited",
  "tags": ["work", "milestone", "backend", "authentication"],
  "timestamp": "2025-11-20T18:00:00"
}
```

---

## Journal Schema (v1.2.0)

### Daily Markdown Format

**File Location**: `.assistant/journals/YYYY-MM/YYYY-MM-DD.md`

**Structure**:
```markdown
---
date: 2026-01-05
day_of_week: Monday
categories: [work, study]
moods: [happy, motivated]
tags: [python, project]
todos_completed: 3
todos_created: 2
key_achievements: []
---

# 2026年01月05日 星期Monday

## 🌅 早晨 (06:00 - 12:00)

### 09:30 - Meeting with design team
分类：work
心情：neutral
标签：meeting, design

## 🌞 下午 (12:00 - 18:00)

### 14:00 - Code review session
分类：work
心情：happy
标签：code-review, collaboration

## 🌙 晚上 (18:00 - 24:00)

### 20:00 - Study Python decorators
分类：study
心情：motivated
标签：python, learning

## 📊 今日总结

### ✅ 完成的任务
- [x] Design team meeting notes
- [x] Review 3 PRs

### 📝 新增的任务
- [ ] Follow up on design feedback
- [ ] Implement new feature

### 🎯 主要成就
1. Completed code review backlog
2. Learned Python decorator patterns

### 💭 今日反思
Good progress on code reviews. Need to schedule more regular design syncs.

### 🔮 明天计划
- Implement feature based on design feedback
- Schedule weekly design sync

## 🤖 Agent工作记录

### Session: 2026-01-05-09-00
触发方式：scheduled
持续时间：45秒

**执行的动作：**
1. Sent clarification question for TODO #5
2. Called code-reviewer agent for TODO #3
3. Reminded user about overdue TODO #7

**观察和建议：**
User is responsive to morning reminders. Consider scheduling clarifications for afternoon to avoid disrupting morning focus time.

**下次会话：**
2026-01-06 09:00 - Follow up on TODO #5 clarification response
```

### YAML Frontmatter Fields

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | ISO date (YYYY-MM-DD) |
| `day_of_week` | string | Day name (Monday, Tuesday, etc.) |
| `categories` | array[string] | All categories mentioned in entries |
| `moods` | array[string] | All moods mentioned in entries |
| `tags` | array[string] | All tags mentioned in entries |
| `todos_completed` | integer | Count of completed tasks |
| `todos_created` | integer | Count of new tasks created |
| `key_achievements` | array[string] | List of key achievements |

### Journal Entry Sections

Each time-based section contains entries with:
- **Time**: HH:MM format
- **Content**: The main journal entry text
- **分类** (Category): work, life, study, health, reflection, achievement, other
- **心情** (Mood): happy, neutral, sad, excited, tired, motivated, stressed, relaxed
- **标签** (Tags): Flexible keywords for categorization

### Agent Session Records

**Session ID Format**: `YYYY-MM-DD-HH-MM`

**Fields**:
- `触发方式` (trigger): scheduled | user_initiated
- `持续时间` (duration): Execution time
- `执行的动作` (actions): List of actions taken
- `观察和建议` (observations): Agent insights and suggestions
- `下次会话` (next session): When and why to run next session

---

## File Storage Locations (v1.2.0)

### TODO Files
- **Active**: `.assistant/active-todos.json`
- **Archived**: `.assistant/archived-todos.json`

### Journal Files
- **Location**: `.assistant/journals/YYYY-MM/YYYY-MM-DD.md`
- **Example**: `.assistant/journals/2026-01/2026-01-05.md`

### Custom File Paths

Override default locations using environment variables:

```bash
# For active TODOs (default: .assistant/active-todos.json)
export TODO_ACTIVE_FILE=/path/to/custom-active-todos.json

# For archived TODOs (default: .assistant/archived-todos.json)
export TODO_ARCHIVED_FILE=/path/to/custom-archived-todos.json

# For journals (base directory, default: .assistant/journals)
export JOURNAL_BASE_DIR=/path/to/custom-journals
```

### Legacy Data (Pre-v1.2.0)

**Old Format**:
- `.assistant/todos.json` - Single JSON file with all TODOs
- `.assistant/journals.json` - Single JSON file with all journal entries

**Migration**:
- Old data remains in place for reference
- No automatic migration to v1.2.0 format
- New data created in v1.2.0 format going forward
- Can manually view old files if needed

---

## Usage Patterns

### Reading vs Writing

**When Agent Works Autonomously:**
```bash
# ✅ READ: Direct file access
Read .assistant/active-todos.json
Read .assistant/journals/2026-01/2026-01-05.md

# ✅ WRITE: Always through scripts
python3 scripts/todo_manager.py update 5 --status completed
python3 scripts/journal_manager.py add-agent-session --trigger scheduled --actions "..."
```

**When User Interacts:**
```bash
# All operations go through scripts for consistency
python3 scripts/todo_manager.py add "New task" --category work
python3 scripts/journal_manager.py add "Today's progress" --category work --mood happy
```
