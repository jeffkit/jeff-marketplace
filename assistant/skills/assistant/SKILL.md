---
name: assistant
description: Personal assistant skill for managing TODOs and journal entries in daily conversations. This skill should be used when users want to record tasks, track work items, log daily activities, or manage personal notes. Triggers include phrases like "记录一下", "添加TODO", "写个日志", "查看我的任务", or any request to save information for later reference.
---

# Personal Assistant

## Overview

This skill transforms Claude into a personal assistant that helps manage TODOs and journal entries through natural conversation. It provides structured storage using JSON files in the working directory, making task and journal management seamless and persistent across sessions.

## Important: Script Path Resolution

**All script paths in this skill are relative to the skill directory** (where this SKILL.md file is located).

When Claude Code loads this skill, it automatically resolves paths like `scripts/todo_manager.py` to the correct absolute path, regardless of which project directory the user is currently in.

**How it works:**
- Skills are installed/linked in `~/.claude/skills/`
- This skill is located at `~/.claude/skills/assistant/`
- Script path `scripts/todo_manager.py` resolves to `~/.claude/skills/assistant/scripts/todo_manager.py`
- Python scripts will create data files in the user's current working directory (e.g., `/Users/john/myproject/.assistant/`)

**Example:**
- User is working in `/Users/john/myproject/`
- Skill command: `python3 scripts/todo_manager.py add "Task"`
- Executes: `~/.claude/skills/assistant/scripts/todo_manager.py`
- Data stored in: `/Users/john/myproject/.assistant/todos.json`

## Core Capabilities

The assistant skill provides four main capabilities:

### 1. TODO Management
Track tasks with enhanced metadata and project management capabilities:
- Add TODOs with priority, category, status, due dates, project, assignee, tags, and description
- List and filter TODOs by category, status, priority, project, assignee, or tags
- Update TODO status, priority, or any other fields
- Search TODOs by keyword
- Delete completed or cancelled TODOs

**Enhanced Fields (v2.2.0+)**:
- `project`: Group tasks by project name/ID
- `assignee`: Assign tasks to specific people
- `tags`: Flexible multi-dimensional labeling (e.g., "backend", "urgent", "bug-fix")
- `description`: Detailed task descriptions and requirements

### 2. Journal Management
Record daily activities, thoughts, and experiences with rich metadata:
- Add journal entries with content, category, mood, and tags
- List entries filtered by category, date range, or mood
- Search entries by keyword
- Update or delete existing entries

### 3. Interactive Clarification
When receiving a recording request, if the information is unclear:
- Ask clarifying questions about category, priority, or deadline
- Suggest appropriate categories based on context
- Confirm details before saving to ensure accuracy

### 4. Smart Querying
Provide flexible ways to retrieve information:
- Filter by multiple criteria (category, status, date range, mood)
- Search by keywords in content
- Display results in a user-friendly format
- Summarize or highlight important items

## Workflow

### Adding a TODO

When a user requests to add a TODO (e.g., "记录一下要完成项目报告"):

1. **Identify the task**: Extract the task description from the user's message
2. **Clarify if needed**: Ask about important context for project/task management:
   - **Basic info**: "这是工作任务还是生活事项？优先级如何？有截止时间吗？"
   - **Project context**: "这个任务属于哪个项目？"
   - **Assignment**: "需要分配给谁来完成？"
   - **Tags**: "需要添加什么标签吗？（比如：backend, urgent, bug-fix）"
   - **Description**: "有什么具体要求或详细说明吗？"
3. **Execute the script**:
   ```bash
   python3 scripts/todo_manager.py add "完成项目报告" \
     --category work --priority high --due-date 2025-11-25 \
     --project "jeff-marketplace" --assignee "jeff" \
     --tags "documentation,urgent" --description "完成项目README和API文档"
   ```
   Note: The script path is relative to the skill directory (where this SKILL.md is located).
4. **Confirm to user**: Display the created TODO in a friendly format

Example interaction (Enhanced):
```
User: 帮我记录一下要完成项目报告
Assistant: 好的，我帮你记录这个任务。请问：
- 这是工作任务吗？优先级如何？有截止时间吗？
- 这个任务属于哪个项目？
- 需要分配给谁完成？
- 需要添加什么标签吗？

User: 是工作任务，优先级高，这周五之前完成，属于jeff-marketplace项目，分配给我，添加documentation和urgent标签
Assistant: [Executes script and confirms] 已记录：
- 任务：完成项目报告
- 项目：jeff-marketplace
- 分配给：jeff
- 分类：工作
- 优先级：高
- 标签：documentation, urgent
- 截止日期：2025-11-22
- 状态：待办
```

Example interaction (Simple - Backward Compatible):
```
User: 记录一下要买菜
Assistant: 好的，这是生活类的待办事项吗？需要设置优先级或截止时间吗？
User: 就是普通的生活任务，优先级中等
Assistant: [Executes script and confirms] 已记录：
- 任务：买菜
- 分类：生活
- 优先级：中等
- 状态：待办
```

### Adding a Journal Entry

When a user wants to log something (e.g., "记录一下今天的学习"):

1. **Extract content**: Get the journal content from the user
2. **Clarify details**: Ask about category, mood, or tags if helpful
3. **Execute the script**:
   ```bash
   python3 scripts/journal_manager.py add "今天学习了Python装饰器的用法" --category study --mood happy --tags python,learning
   ```
4. **Confirm**: Show the created entry

### Listing TODOs

When user asks to see TODOs (e.g., "看看我有什么待办事项"):

1. **Determine filters**: Based on user request, identify:
   - **Basic filters**: Category, status, priority
   - **Enhanced filters**: Project, assignee, tags
2. **Execute query**:
   ```bash
   # Basic filtering
   python3 scripts/todo_manager.py list --status pending --category work

   # Enhanced filtering
   python3 scripts/todo_manager.py list --project jeff-marketplace --assignee jeff --tags urgent

   # Complex queries
   python3 scripts/todo_manager.py list --category work --priority high --tags backend
   ```
3. **Present results**: Format the JSON output in a readable way, highlighting:
   - Urgent items (high priority + upcoming deadlines)
   - Project groupings
   - User assignments
   - Tag-based groupings when relevant

### Listing Journal Entries

When user wants to review journals (e.g., "看看本周的日志"):

1. **Determine filters**: Extract date range, category, or mood
2. **Execute query**:
   ```bash
   python3 scripts/journal_manager.py list --start-date 2025-11-18 --end-date 2025-11-20
   ```
3. **Present results**: Show entries with timestamps and categories

### Updating Items

When user wants to update a TODO or journal:

1. **Identify the item**: Use list/search to find the ID
2. **Execute update**:
   ```bash
   # Basic updates
   python3 scripts/todo_manager.py update 5 --status completed

   # Enhanced updates
   python3 scripts/todo_manager.py update 5 \
     --status in_progress --priority high \
     --assignee alice --tags backend,urgent,bug-fix \
     --description "修复用户登录时的500错误"
   ```
3. **Confirm change**: Show the updated item with all fields

### Searching

When user searches for specific content:

1. **Execute search**:
   ```bash
   python3 scripts/todo_manager.py search "项目"
   python3 scripts/journal_manager.py search "学习"
   ```
2. **Display results**: Show matching items with context

## Data Storage

### TODO Data Structure
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
  "created_at": "2025-11-20T10:30:00",
  "updated_at": "2025-11-20T10:30:00"
}
```

**Categories**: work, life, study, health, finance, hobby, other
**Priorities**: high, medium, low
**Statuses**: pending, in_progress, completed, cancelled
**Enhanced Fields (v2.2.0+)**:
- `project`: Project name/ID (string, optional)
- `assignee`: Assigned person (string, optional)
- `tags`: Flexible labels array (array of strings, optional)
- `description`: Detailed task requirements (string, optional)

### Journal Data Structure
```json
{
  "id": 1,
  "content": "Today I learned about Python decorators",
  "category": "study",
  "mood": "happy",
  "tags": ["python", "learning"],
  "timestamp": "2025-11-20T15:45:00"
}
```

**Categories**: work, life, study, health, reflection, achievement, other
**Moods**: happy, neutral, sad, excited, tired, motivated, stressed, relaxed

### File Locations
- TODOs: `.assistant/todos.json` (in working directory or `TODO_DATA_FILE` env var)
- Journals: `.assistant/journals.json` (in working directory or `JOURNAL_DATA_FILE` env var)

Data files are stored in a hidden `.assistant/` directory to avoid confusion with project data.

To use custom file paths, set environment variables before running scripts:
```bash
export TODO_DATA_FILE=/path/to/my-todos.json
export JOURNAL_DATA_FILE=/path/to/my-journals.json
```

## Resources

### scripts/

This skill includes two Python scripts for data management:

**`todo_manager.py`** - Complete CRUD operations for TODO items
- `add`: Create new TODO with metadata
- `list`: Query TODOs with filters
- `update`: Modify existing TODO fields
- `delete`: Remove TODO by ID
- `search`: Find TODOs by keyword

**`journal_manager.py`** - Complete CRUD operations for journal entries
- `add`: Create new journal entry
- `list`: Query entries with date/category/mood filters
- `update`: Modify existing entry
- `delete`: Remove entry by ID
- `search`: Find entries by keyword

Both scripts output JSON for easy parsing and display.

## Best Practices

1. **Always clarify before recording**: If category, priority, project, or other details are ambiguous, ask the user first
2. **Use environment context**: Infer category, project, and assignee from conversation context when obvious
3. **Project-oriented thinking**: When users mention project-related tasks, always ask about project name and assignment
4. **Tag suggestions**: Suggest relevant tags based on conversation (e.g., "backend", "urgent", "bug-fix")
5. **Friendly confirmations**: After saving, show a clear confirmation with all saved details
6. **Smart filtering**: When listing items, apply sensible defaults and suggest useful filters:
   - "您想查看特定项目的任务吗？"
   - "需要筛选出分配给某个人的任务吗？"
   - "要按标签过滤吗？比如urgent或backend？"
7. **Preserve data integrity**: Always use the scripts to modify data, never edit JSON files directly
8. **Handle errors gracefully**: If a script fails, explain the issue and suggest solutions
9. **Natural language**: Present data in conversational Chinese, not raw JSON dumps
10. **Proactive suggestions**:
    - Remind users of upcoming deadlines
    - Suggest reviewing project-specific tasks
    - Recommend checking work assigned to specific people
    - Suggest filtering by tags for better organization

## Example Usage Patterns

### Basic Usage (Backward Compatible)
**User**: "帮我记录要买菜"
**Assistant**: 好的，这是生活类的待办事项吗？需要设置优先级或截止时间吗？

### Enhanced Usage with Project Management
**User**: "我们需要修复用户登录的bug"
**Assistant**: 好的，我来记录这个技术任务。请问：
- 这个任务属于哪个项目？
- 需要分配给谁处理？
- 优先级如何？有什么标签要添加吗？（比如backend, urgent, bug-fix）

**User**: "看看jeff-marketplace项目的所有任务"
**Assistant**: [Runs `scripts/todo_manager.py list --project jeff-marketplace`] jeff-marketplace项目有以下任务：

**User**: "有哪些分配给我的高优先级工作？"
**Assistant**: [Runs `scripts/todo_manager.py list --assignee jeff --priority high --category work`] 您有以下高优先级工作任务：

**User**: "把用户认证功能的开发标记为进行中"
**Assistant**: [Searches for the TODO, then runs `scripts/todo_manager.py update <id> --status in_progress`] 已将"用户认证功能"标记为进行中！

### Advanced Querying Examples
**User**: "显示所有urgent标签的后端任务"
**Assistant**: [Runs `scripts/todo_manager.py list --tags urgent,backend`] 找到以下urgent标签的后端任务：

**User**: "alice负责什么任务？"
**Assistant**: [Runs `scripts/todo_manager.py list --assignee alice`] alice负责以下任务：
