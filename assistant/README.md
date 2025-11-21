# Assistant Plugin

Version: 2.1.0

Personal assistant plugin for Claude Code that manages TODOs and journal entries through natural conversation.

## Features

- **TODO Management**: Track tasks with priority, category, status, and due dates
- **Journal Management**: Record daily activities with mood and tags
- **Interactive Clarification**: Claude asks questions to ensure data accuracy
- **Smart Querying**: Filter and search tasks and journals
- **Local Storage**: All data stored in `.assistant/` directory in your working directory

## Installation

This plugin is part of the jeff-marketplace collection. To use it:

1. Copy the `assistant/` directory to your Claude plugins location
2. Or install via Claude Code's plugin manager (if distributed)

## Usage

Once installed, the `assistant` skill is automatically available. Trigger it with natural language:

**Chinese triggers:**
- "记录一下..." (Record this...)
- "添加TODO..." (Add TODO...)
- "写个日志..." (Write a journal...)
- "查看我的任务" (Check my tasks)

**Example conversations:**

```
User: 帮我记录一下要完成项目报告
Claude: 好的，我帮你记录这个任务。这是工作任务吗？优先级如何？有截止时间吗？
User: 是工作任务，优先级高，这周五之前完成
Claude: 已记录：
- 任务：完成项目报告
- 分类：工作
- 优先级：高
- 截止日期：2025-11-22
```

## Data Storage

All data is stored in `.assistant/` directory in your current working directory:
- `.assistant/todos.json` - TODO items
- `.assistant/journals.json` - Journal entries

The `.assistant/` directory is automatically created when first needed and should be gitignored.

## Customization

You can customize data file locations using environment variables:

```bash
export TODO_DATA_FILE=/path/to/custom-todos.json
export JOURNAL_DATA_FILE=/path/to/custom-journals.json
```

## Migration from v2.0.x

If upgrading from an older version that stored data in the project root:

```bash
# Navigate to your project directory first
cd /path/to/your/project

# Run migration script
python3 ~/.claude/skills/assistant/scripts/migrate_data.py
```

This will migrate `todos.json` and `journals.json` from your project root to `.assistant/` directory.

## Data Schemas

### TODO Item
```json
{
  "id": 1,
  "title": "Task description",
  "category": "work|life|study|health|finance|hobby|other",
  "priority": "high|medium|low",
  "status": "pending|in_progress|completed|cancelled",
  "due_date": "YYYY-MM-DD (optional)",
  "created_at": "ISO 8601 timestamp",
  "updated_at": "ISO 8601 timestamp"
}
```

### Journal Entry
```json
{
  "id": 1,
  "content": "Entry content",
  "category": "work|life|study|health|reflection|achievement|other",
  "mood": "happy|neutral|sad|excited|tired|motivated|stressed|relaxed",
  "tags": ["tag1", "tag2"],
  "timestamp": "ISO 8601 timestamp"
}
```

## Direct Script Usage (Advanced)

You can also use the Python scripts directly from the skill directory:

```bash
# Scripts are located at ~/.claude/skills/assistant/scripts/
cd ~/.claude/skills/assistant/

# Add TODO
python3 scripts/todo_manager.py add "Task title" --category work --priority high

# List TODOs
python3 scripts/todo_manager.py list --status pending

# Add journal
python3 scripts/journal_manager.py add "Today's update" --category work --mood happy

# List journals
python3 scripts/journal_manager.py list --start-date 2025-11-01
```

**Note:**
- Scripts are installed at `~/.claude/skills/assistant/scripts/`
- Data files are created in your current working directory's `.assistant/` folder
- You don't need to navigate to the skill directory to use the skill through Claude

## License

MIT

## Author

jeffkit <bbmyth@gmail.com>
