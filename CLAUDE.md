# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Jeff Marketplace is a collection of Claude Code plugins designed to enhance personal productivity and autonomous development capabilities. The repository contains two main plugins:

1. **Assistant** (v2.1.0) - Personal assistant for TODO and journal management
2. **Speckit Driver** (v1.1.1) - Autonomous spec-driven development orchestrator

This is a **plugin repository**, not an application codebase. Each plugin is self-contained in its own directory with independent versioning and functionality.

## Repository Structure

```
jeff-marketplace/
├── assistant/                    # Personal assistant plugin
│   ├── .claude-plugin/
│   │   └── plugin.json          # Plugin metadata (v2.1.0)
│   └── skills/
│       └── assistant/
│           ├── SKILL.md         # Skill documentation
│           └── scripts/
│               ├── todo_manager.py      # Python CLI for TODO CRUD
│               └── journal_manager.py   # Python CLI for journal CRUD
│
├── speckit-driver/               # Spec-driven development orchestrator
│   ├── .claude-plugin/
│   │   └── plugin.json          # Plugin metadata (v1.1.1)
│   ├── agents/                  # Sub-agent prompts
│   │   ├── speckit-constitution.md
│   │   ├── speckit-specify.md
│   │   ├── speckit-clarify.md
│   │   ├── speckit-checklist.md
│   │   ├── speckit-plan.md
│   │   ├── speckit-tasks.md
│   │   ├── speckit-analyze.md
│   │   └── speckit-implement.md
│   └── skills/
│       └── speckit-driver/
│           └── SKILL.md         # Main orchestrator skill
│
└── .assistant/                   # Assistant data storage (gitignored)
    ├── todos.json               # Persistent TODO storage
    └── journals.json            # Persistent journal storage
```

## Plugin Architecture

### Assistant Plugin

The Assistant plugin provides personal productivity management through two Python CLI tools:

**Core Components:**
- **todo_manager.py**: Full CRUD operations for TODO items (add, list, update, delete, search)
- **journal_manager.py**: Full CRUD operations for journal entries (add, list, update, delete, search)

**Data Storage:**
- TODOs stored in `.assistant/todos.json` (or `$TODO_DATA_FILE` if set)
- Journals stored in `.assistant/journals.json` (or `$JOURNAL_DATA_FILE` if set)
- Both use JSON format for persistence across sessions
- Data stored in hidden `.assistant/` directory to avoid confusion with project files

**Skill Activation:**
The `assistant` skill is triggered by natural language phrases like:
- "记录一下" (Record this)
- "添加TODO" (Add TODO)
- "写个日志" (Write a journal)
- "查看我的任务" (Check my tasks)

**Workflow Pattern:**
1. User requests to record task/journal
2. Skill clarifies missing details (category, priority, deadline)
3. Execute Python script with appropriate parameters
4. Confirm action to user in conversational format

### Speckit Driver Plugin

The Speckit Driver is an autonomous orchestrator that manages the entire spec-driven development workflow through specialized sub-agents.

**Workflow Phases:**
1. **Constitution** (Phase 0): Establish project principles and governance
2. **Specification** (Phase 1): Convert feature descriptions into detailed specs
3. **Clarification** (Phase 1.5): Resolve ambiguities in specifications
4. **Checklist** (Phase 1.6): Generate quality validation checklists
5. **Planning** (Phase 2): Create technical implementation plans
6. **Tasks** (Phase 3): Break down plans into actionable task lists
7. **Analysis** (Phase 3.5): Cross-artifact consistency validation
8. **Implementation** (Phase 4): Execute tasks with progress monitoring

**Sub-Agents:**
Each agent is defined in `agents/` directory and handles one workflow phase:
- `speckit-constitution`: Creates project principles
- `speckit-specify`: Writes feature specifications
- `speckit-clarify`: Identifies and resolves specification ambiguities
- `speckit-checklist`: Generates quality checklists
- `speckit-plan`: Creates technical implementation plans
- `speckit-tasks`: Breaks plans into actionable tasks
- `speckit-analyze`: Performs cross-artifact consistency analysis
- `speckit-implement`: Executes implementation with monitoring

**Skill Role:**
The `speckit-driver` skill acts as project manager, not executor:
- Delegates work to sub-agents via Task tool
- Reviews sub-agent outputs critically
- Makes continuation decisions
- Handles user interactions and clarifications
- Ensures smooth workflow progression

**Key Quality Gates:**
1. **Clarification Gate**: Resolves ambiguities before planning
2. **Checklist Gate**: Validates requirement quality
3. **Analysis Gate**: Ensures spec/plan/tasks consistency

## Working with This Repository

### Testing Assistant Plugin

**When developing in this repository:**
```bash
# Test TODO management (using relative path from repo root)
python3 assistant/skills/assistant/scripts/todo_manager.py add "Test task" --category work --priority high

# Test journal management
python3 assistant/skills/assistant/scripts/journal_manager.py add "Today's update" --category work --mood happy

# List items
python3 assistant/skills/assistant/scripts/todo_manager.py list --status pending
python3 assistant/skills/assistant/scripts/journal_manager.py list --start-date 2025-11-01
```

**When installed as a plugin:**
```bash
# Skills are installed at ~/.claude/skills/assistant/
# Use absolute path or navigate to skill directory
python3 ~/.claude/skills/assistant/scripts/todo_manager.py add "Test task" --category work

# Or through the skill itself (Claude will resolve paths automatically)
# Just trigger the skill with natural language
```

### Testing Speckit Driver Plugin

The speckit-driver plugin is designed to be used through the Claude Code skill system, not as standalone scripts. To test:

1. Trigger the skill with phrases like "用speckit开发" or "使用speckit构建"
2. Follow the orchestrated workflow from constitution to implementation
3. Review generated artifacts in `.specify/` directory

### Version Updates

When updating plugin versions:

1. Update `version` field in `.claude-plugin/plugin.json`
2. Update version in skill's SKILL.md frontmatter (if applicable)
3. Document changes in CHANGELOG.md (for speckit-driver)
4. Update README.md to reflect new version number

### Plugin Distribution

Each plugin can be distributed independently:
- Copy the entire plugin directory (e.g., `assistant/` or `speckit-driver/`)
- Users install by placing in their `.claude/plugins/` directory
- The `.claude-plugin/plugin.json` file defines plugin metadata

## Important Conventions

### File Naming
- Plugin metadata: `.claude-plugin/plugin.json`
- Skill definitions: `skills/{skill-name}/SKILL.md`
- Agent definitions: `agents/{agent-name}.md`
- Python scripts: Use snake_case (e.g., `todo_manager.py`)

### Data Persistence
- TODOs and journals are stored in `.assistant/` directory by default
- The entire `.assistant/` directory is gitignored to prevent accidental commits
- Use environment variables `TODO_DATA_FILE` and `JOURNAL_DATA_FILE` to customize paths
- The `.assistant/` directory is automatically created when first needed

### Skill Triggers
- Assistant skill: Responds to Chinese phrases for task/journal management
- Speckit Driver skill: Responds to Chinese/English phrases for spec-driven development
- Both skills use natural language triggers, not command-line flags

### Agent Coordination
- Speckit Driver agents are invoked via Task tool, not directly
- Each agent has a specific input/output contract defined in its .md file
- The orchestrator (speckit-driver skill) manages agent sequencing and error handling

## Development Guidelines

### Adding New Features to Assistant

1. Extend Python scripts in `assistant/skills/assistant/scripts/`
2. Update SKILL.md with new workflow patterns
3. Maintain JSON schema compatibility for backward compatibility
4. Test CLI operations independently before integrating with skill

### Modifying Speckit Workflow

1. Edit agent prompts in `speckit-driver/agents/`
2. Update orchestrator logic in `speckit-driver/skills/speckit-driver/SKILL.md`
3. Test workflow progression through all phases
4. Ensure task marking verification works correctly (critical for Phase 4)

### Cross-Plugin Compatibility

Plugins are independent and do not share code or data. Changes to one plugin should not affect the other. However, both follow Claude Code plugin conventions:
- `.claude-plugin/plugin.json` for metadata
- `skills/` directory for skill definitions
- SKILL.md frontmatter for skill metadata

## Architecture Principles

### Assistant Plugin
- **Stateless CLI Tools**: Python scripts are pure functions with no global state
- **JSON Persistence**: All data stored in human-readable JSON format
- **Interactive Clarification**: Always confirm ambiguous details before executing
- **Natural Language Interface**: Users interact through conversation, not commands

### Speckit Driver Plugin
- **Orchestrator Pattern**: Main skill coordinates, sub-agents execute
- **Quality Gates**: Built-in validation at clarification, checklist, and analysis phases
- **Progressive Elaboration**: Each phase adds detail (constitution → spec → plan → tasks)
- **Task Marking Protection**: 4-layer verification ensures task completion tracking accuracy
- **Continuous Workflow**: Minimal user intervention after initial feature description

## Data Schemas

### TODO Schema
```json
{
  "id": 1,
  "title": "string",
  "category": "work|life|study|health|finance|hobby|other",
  "priority": "high|medium|low",
  "status": "pending|in_progress|completed|cancelled",
  "due_date": "YYYY-MM-DD (optional)",
  "project": "string (optional)",
  "assignee": "string (optional)",
  "tags": ["string"] (optional),
  "description": "string (optional)",
  "created_at": "ISO 8601 timestamp",
  "updated_at": "ISO 8601 timestamp"
}
```

**New Fields (v2.2.0)**:
- `project`: Project name/ID for grouping tasks
- `assignee`: Person assigned to the task
- `tags`: Array of flexible labels for multi-dimensional categorization
- `description`: Detailed task description or requirements

### Journal Entry Schema
```json
{
  "id": 1,
  "content": "string",
  "category": "work|life|study|health|reflection|achievement|other",
  "mood": "happy|neutral|sad|excited|tired|motivated|stressed|relaxed",
  "tags": ["string"],
  "timestamp": "ISO 8601 timestamp"
}
```

## CLI Usage Examples

### Basic TODO Operations
```bash
# Add simple TODO (backward compatible)
python3 scripts/todo_manager.py add "完成项目报告"

# Add TODO with new fields
python3 scripts/todo_manager.py add "实现用户认证" \
  --category work --priority high \
  --project jeff-marketplace \
  --assignee jeff \
  --tags backend,security,auth \
  --description "添加JWT登录和用户注册功能"

# List all TODOs
python3 scripts/todo_manager.py list

# Filter by project
python3 scripts/todo_manager.py list --project jeff-marketplace

# Filter by assignee and tags
python3 scripts/todo_manager.py list --assignee jeff --tags backend

# Filter by status and category
python3 scripts/todo_manager.py list --status pending --category work

# Update TODO
python3 scripts/todo_manager.py update 1 --status in_progress --tags backend,security,auth,urgent
```

### Advanced Querying
```bash
# Find all backend tasks for jeff
python3 scripts/todo_manager.py list --assignee jeff --tags backend

# Find all high-priority work tasks
python3 scripts/todo_manager.py list --category work --priority high

# Find all tasks in a project
python3 scripts/todo_manager.py list --project my-project
```

## Common Tasks

### Update Plugin Metadata
```bash
# Edit plugin.json
vim assistant/.claude-plugin/plugin.json
# or
vim speckit-driver/.claude-plugin/plugin.json
```

### Review Skill Documentation
```bash
# Assistant skill
cat assistant/skills/assistant/SKILL.md

# Speckit Driver skill
cat speckit-driver/skills/speckit-driver/SKILL.md
```

### Inspect Agent Definitions
```bash
# List all speckit agents
ls speckit-driver/agents/

# Read specific agent
cat speckit-driver/agents/speckit-specify.md
```

### Check Data Files
```bash
# View TODOs
cat .assistant/todos.json | python3 -m json.tool

# View journals
cat .assistant/journals.json | python3 -m json.tool
```
