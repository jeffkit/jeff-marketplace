---
name: assistant
description: Personal assistant for TODO and journal management in daily conversations. Use when users want to record tasks, track work items, log activities, or manage notes. Triggers include phrases like "记录一下", "添加TODO", "写个日志", "查看我的任务", "add todo", "log this", "check my tasks", or any request to save information for later reference.
---

# Personal Assistant

## Overview

This skill transforms Claude into a personal assistant that helps manage TODOs and journal entries through natural conversation. Data is stored in JSON files in `.assistant/` directory of the current working directory, making task and journal management seamless and persistent across sessions.

## Core Capabilities

1. **TODO Management**: Track tasks with priority, category, status, due dates, project, assignee, tags, and descriptions
2. **Journal Management**: Record daily activities with content, category, mood, and tags
3. **Interactive Clarification**: Ask questions when details are unclear before saving
4. **Smart Querying**: Filter and search by multiple criteria, present results in friendly format

## Workflow

### Adding a TODO

When user requests to add a TODO (e.g., "记录一下要完成项目报告"):

1. **Extract task description** from user's message
2. **Clarify if needed**: Ask about category, priority, deadline, project, assignee, tags, or description
3. **Execute script**:
   ```bash
   python3 scripts/todo_manager.py add "完成项目报告" \
     --category work --priority high --due-date 2025-11-25 \
     --project "jeff-marketplace" --assignee "jeff" \
     --tags "documentation,urgent" --description "完成项目README和API文档"
   ```
4. **Confirm**: Display the created TODO in friendly format

**Example:**
```
User: 帮我记录一下要完成项目报告
Assistant: 好的。这是工作任务吗？优先级如何？有截止时间吗？属于哪个项目？
User: 工作任务，高优先级，周五前完成，jeff-marketplace项目
Assistant: [Executes script] 已记录：完成项目报告 (工作/高优先级/2025-11-22/jeff-marketplace)
```

### Adding a Journal Entry

1. **Extract content** from user
2. **Clarify** category, mood, or tags if helpful
3. **Execute**:
   ```bash
   python3 scripts/journal_manager.py add "今天学习了Python装饰器" --category study --mood happy --tags python,learning
   ```
4. **Confirm**: Show the created entry

### Listing and Querying

**TODOs:**
```bash
# Basic filtering
python3 scripts/todo_manager.py list --status pending --category work

# Enhanced filtering
python3 scripts/todo_manager.py list --project jeff-marketplace --assignee jeff --tags urgent
```

**Journals:**
```bash
python3 scripts/journal_manager.py list --start-date 2025-11-18 --end-date 2025-11-20
```

**Present results** in readable format, highlighting urgent items, project groupings, and assignments.

### Updating and Searching

**Update:**
```bash
python3 scripts/todo_manager.py update 5 --status completed
python3 scripts/journal_manager.py update 3 --mood motivated
```

**Search:**
```bash
python3 scripts/todo_manager.py search "项目"
python3 scripts/journal_manager.py search "学习"
```

## Data Storage (v1.2.0)

**File Locations:**
- Active TODOs: `.assistant/active-todos.json`
- Archived TODOs: `.assistant/archived-todos.json`
- Journals: `.assistant/journals/YYYY-MM/YYYY-MM-DD.md` (daily markdown files)

**TODO Fields:**
- Required: `title`, `category`, `priority`, `status`
- Optional: `due_date`, `project`, `assignee`, `tags`, `description`
- **New (v1.2.0)**: `next_action_time`, `needs_clarification`, `clarification_question`, `blockers`, `last_reviewed`, `auto_progress_hint`
- Categories: work, life, study, health, finance, hobby, other
- Priorities: high, medium, low
- Statuses: pending, in_progress, completed, cancelled

**Journal Format:**
- Daily markdown files with YAML frontmatter
- Sections: 早晨, 下午, 晚上, 今日总结, Agent工作记录
- Frontmatter includes: date, categories, moods, tags, todos_completed, key_achievements

**For detailed schemas**: See [references/data-schemas.md](references/data-schemas.md)

## Scripts

**`scripts/todo_manager.py`** - TODO CRUD operations
- Commands: `add`, `list`, `update`, `delete`, `search`
- Outputs JSON for easy parsing

**`scripts/journal_manager.py`** - Journal CRUD operations
- Commands: `add`, `list`, `update`, `delete`, `search`
- Outputs JSON for easy parsing

**For complete CLI reference**: See [references/cli-reference.md](references/cli-reference.md)

## Best Practices

1. **Always clarify ambiguity**: Ask about category, priority, project when unclear
2. **Use conversation context**: Infer details from ongoing discussion when obvious
3. **Project-oriented**: For work tasks, always confirm project and assignee
4. **Friendly confirmations**: Show clear success messages with saved details
5. **Smart defaults**: Apply sensible filters and suggest useful queries
6. **Preserve integrity**: Always use scripts, never edit JSON directly
7. **Natural presentation**: Present data conversationally, not as raw JSON
8. **Agent self-awareness** (v1.2.0): When working autonomously, directly read data files for planning, use scripts only for updates

**For detailed examples**: See [references/examples.md](references/examples.md)
**For autonomous agent workflows**: See [references/agent-workflows.md](references/agent-workflows.md)
