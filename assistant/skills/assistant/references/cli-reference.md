# CLI Reference

Complete command-line interface reference for `todo_manager.py` and `journal_manager.py`.

## TODO Manager (`todo_manager.py`)

### Add TODO

Create a new TODO item with optional metadata.

**Usage:**
```bash
python3 scripts/todo_manager.py add <title> [OPTIONS]
```

**Options:**
- `--category CATEGORY`: Task category (work, life, study, health, finance, hobby, other)
- `--priority PRIORITY`: Priority level (high, medium, low)
- `--status STATUS`: Initial status (pending, in_progress, completed, cancelled)
- `--due-date DATE`: Due date in YYYY-MM-DD format
- `--project PROJECT`: Project name/identifier
- `--assignee ASSIGNEE`: Person assigned to the task
- `--tags TAGS`: Comma-separated list of tags
- `--description DESC`: Detailed task description

**Examples:**
```bash
# Simple TODO
python3 scripts/todo_manager.py add "买菜" --category life --priority medium

# Enhanced TODO with project management
python3 scripts/todo_manager.py add "实现用户认证" \
  --category work --priority high --due-date 2025-11-30 \
  --project jeff-marketplace --assignee jeff \
  --tags backend,security,auth --description "添加JWT登录和注册功能"

# Minimal TODO (uses defaults)
python3 scripts/todo_manager.py add "阅读文档"
```

**Output:**
```json
{
  "success": true,
  "todo": {
    "id": 1,
    "title": "实现用户认证",
    "category": "work",
    "priority": "high",
    "status": "pending",
    "due_date": "2025-11-30",
    "project": "jeff-marketplace",
    "assignee": "jeff",
    "tags": ["backend", "security", "auth"],
    "description": "添加JWT登录和注册功能",
    "created_at": "2025-11-20T10:00:00",
    "updated_at": "2025-11-20T10:00:00"
  }
}
```

---

### List TODOs

Query TODOs with optional filters.

**Usage:**
```bash
python3 scripts/todo_manager.py list [OPTIONS]
```

**Options:**
- `--category CATEGORY`: Filter by category
- `--status STATUS`: Filter by status
- `--priority PRIORITY`: Filter by priority
- `--project PROJECT`: Filter by project name
- `--assignee ASSIGNEE`: Filter by assignee
- `--tags TAGS`: Filter by tags (comma-separated, matches ANY)

**Examples:**
```bash
# List all pending TODOs
python3 scripts/todo_manager.py list --status pending

# List high-priority work tasks
python3 scripts/todo_manager.py list --category work --priority high

# List tasks in a specific project
python3 scripts/todo_manager.py list --project jeff-marketplace

# List tasks assigned to a person
python3 scripts/todo_manager.py list --assignee jeff

# List tasks with specific tags
python3 scripts/todo_manager.py list --tags urgent,backend

# Complex query
python3 scripts/todo_manager.py list --category work --priority high \
  --project jeff-marketplace --tags backend
```

**Output:**
```json
{
  "success": true,
  "todos": [
    { "id": 1, "title": "...", ... },
    { "id": 2, "title": "...", ... }
  ],
  "count": 2
}
```

---

### Update TODO

Modify an existing TODO by ID.

**Usage:**
```bash
python3 scripts/todo_manager.py update <id> [OPTIONS]
```

**Options:**
- `--title TITLE`: Update title
- `--category CATEGORY`: Update category
- `--priority PRIORITY`: Update priority
- `--status STATUS`: Update status
- `--due-date DATE`: Update due date
- `--project PROJECT`: Update project
- `--assignee ASSIGNEE`: Update assignee
- `--tags TAGS`: Update tags (replaces existing)
- `--description DESC`: Update description

**Examples:**
```bash
# Mark as completed
python3 scripts/todo_manager.py update 5 --status completed

# Update priority and assignee
python3 scripts/todo_manager.py update 5 --priority high --assignee alice

# Update multiple fields
python3 scripts/todo_manager.py update 5 \
  --status in_progress --priority high \
  --tags backend,urgent,bug-fix \
  --description "修复用户登录时的500错误"
```

**Output:**
```json
{
  "success": true,
  "todo": {
    "id": 5,
    "title": "...",
    "status": "completed",
    ...
  }
}
```

---

### Delete TODO

Remove a TODO by ID.

**Usage:**
```bash
python3 scripts/todo_manager.py delete <id>
```

**Example:**
```bash
python3 scripts/todo_manager.py delete 5
```

**Output:**
```json
{
  "success": true,
  "message": "TODO deleted successfully"
}
```

---

### Search TODOs

Search for TODOs by keyword in title or description.

**Usage:**
```bash
python3 scripts/todo_manager.py search <keyword>
```

**Example:**
```bash
python3 scripts/todo_manager.py search "项目"
python3 scripts/todo_manager.py search "bug"
```

**Output:**
```json
{
  "success": true,
  "todos": [
    { "id": 1, "title": "完成项目报告", ... },
    { "id": 3, "title": "项目部署", ... }
  ],
  "count": 2
}
```

---

## Journal Manager (`journal_manager.py`)

### Add Journal Entry

Create a new journal entry.

**Usage:**
```bash
python3 scripts/journal_manager.py add <content> [OPTIONS]
```

**Options:**
- `--category CATEGORY`: Entry category (work, life, study, health, reflection, achievement, other)
- `--mood MOOD`: Mood when writing (happy, neutral, sad, excited, tired, motivated, stressed, relaxed)
- `--tags TAGS`: Comma-separated list of tags

**Examples:**
```bash
# Simple entry
python3 scripts/journal_manager.py add "今天天气很好" --category life --mood happy

# Detailed study entry
python3 scripts/journal_manager.py add "学习了Python装饰器的原理" \
  --category study --mood motivated --tags python,decorators,learning

# Work achievement
python3 scripts/journal_manager.py add "完成了用户认证模块" \
  --category achievement --mood excited --tags work,milestone
```

**Output:**
```json
{
  "success": true,
  "journal": {
    "id": 1,
    "content": "学习了Python装饰器的原理",
    "category": "study",
    "mood": "motivated",
    "tags": ["python", "decorators", "learning"],
    "timestamp": "2025-11-20T15:45:00"
  }
}
```

---

### List Journal Entries

Query journal entries with optional filters.

**Usage:**
```bash
python3 scripts/journal_manager.py list [OPTIONS]
```

**Options:**
- `--category CATEGORY`: Filter by category
- `--mood MOOD`: Filter by mood
- `--start-date DATE`: Filter entries from this date (YYYY-MM-DD)
- `--end-date DATE`: Filter entries until this date (YYYY-MM-DD)
- `--tags TAGS`: Filter by tags (comma-separated, matches ANY)

**Examples:**
```bash
# List all entries
python3 scripts/journal_manager.py list

# List entries from a date range
python3 scripts/journal_manager.py list --start-date 2025-11-01 --end-date 2025-11-30

# List study entries
python3 scripts/journal_manager.py list --category study

# List happy mood entries
python3 scripts/journal_manager.py list --mood happy

# List entries with specific tags
python3 scripts/journal_manager.py list --tags python,learning

# Complex query
python3 scripts/journal_manager.py list --category study --mood motivated \
  --start-date 2025-11-01
```

**Output:**
```json
{
  "success": true,
  "journals": [
    { "id": 1, "content": "...", ... },
    { "id": 2, "content": "...", ... }
  ],
  "count": 2
}
```

---

### Update Journal Entry

Modify an existing journal entry by ID.

**Usage:**
```bash
python3 scripts/journal_manager.py update <id> [OPTIONS]
```

**Options:**
- `--content CONTENT`: Update content
- `--category CATEGORY`: Update category
- `--mood MOOD`: Update mood
- `--tags TAGS`: Update tags (replaces existing)

**Examples:**
```bash
# Update mood
python3 scripts/journal_manager.py update 3 --mood motivated

# Update category and tags
python3 scripts/journal_manager.py update 3 --category achievement --tags milestone,success

# Update content
python3 scripts/journal_manager.py update 3 --content "更新后的内容"
```

**Output:**
```json
{
  "success": true,
  "journal": {
    "id": 3,
    "content": "...",
    "mood": "motivated",
    ...
  }
}
```

---

### Delete Journal Entry

Remove a journal entry by ID.

**Usage:**
```bash
python3 scripts/journal_manager.py delete <id>
```

**Example:**
```bash
python3 scripts/journal_manager.py delete 3
```

**Output:**
```json
{
  "success": true,
  "message": "Journal entry deleted successfully"
}
```

---

### Search Journal Entries

Search for entries by keyword in content.

**Usage:**
```bash
python3 scripts/journal_manager.py search <keyword>
```

**Example:**
```bash
python3 scripts/journal_manager.py search "学习"
python3 scripts/journal_manager.py search "Python"
```

**Output:**
```json
{
  "success": true,
  "journals": [
    { "id": 1, "content": "今天学习了Python", ... },
    { "id": 5, "content": "继续学习Python装饰器", ... }
  ],
  "count": 2
}
```

---

## Environment Variables

Both scripts support custom data file paths:

```bash
# Set custom TODO data file
export TODO_DATA_FILE=/path/to/custom-todos.json

# Set custom journal data file
export JOURNAL_DATA_FILE=/path/to/custom-journals.json

# Then run scripts normally
python3 scripts/todo_manager.py list
python3 scripts/journal_manager.py list
```

## Error Handling

All commands return JSON with `success` field:

**Success:**
```json
{
  "success": true,
  "todo": { ... }
}
```

**Error:**
```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

Common errors:
- Invalid ID: "TODO with ID X not found"
- Invalid category/priority/status: "Invalid category: xyz"
- Missing arguments: "Title is required"
- File access issues: "Unable to read/write data file"
