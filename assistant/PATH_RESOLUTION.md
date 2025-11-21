# Path Resolution Guide

This document explains how paths work in the Assistant plugin.

## Understanding the Two Directories

### 1. Skill Installation Directory (Read-Only)
- **Location**: `~/.claude/skills/assistant/`
- **Contents**: SKILL.md, Python scripts, documentation
- **Purpose**: Where the skill code lives
- **Used by**: Claude Code to load the skill and execute scripts

### 2. User's Working Directory (Data Storage)
- **Location**: Where the user runs their project (e.g., `/Users/john/myproject/`)
- **Contents**: `.assistant/todos.json`, `.assistant/journals.json`
- **Purpose**: Where user data is stored
- **Used by**: Python scripts to read/write TODO and journal data

## Path Resolution Examples

### Example 1: User Working in Project A

**Setup:**
- Skill installed at: `~/.claude/skills/assistant/`
- User's project: `/Users/john/project-a/`
- User working directory: `/Users/john/project-a/`

**When skill executes:**
```bash
python3 scripts/todo_manager.py add "Task"
```

**What happens:**
1. Claude resolves `scripts/todo_manager.py` to `~/.claude/skills/assistant/scripts/todo_manager.py`
2. Script executes from skill directory
3. Script creates data at `/Users/john/project-a/.assistant/todos.json`

### Example 2: User Switches to Project B

**Setup:**
- Same skill: `~/.claude/skills/assistant/` (unchanged)
- User's project: `/Users/john/project-b/`
- User working directory: `/Users/john/project-b/`

**When skill executes:**
```bash
python3 scripts/todo_manager.py add "Task"
```

**What happens:**
1. Same script: `~/.claude/skills/assistant/scripts/todo_manager.py`
2. Different data: `/Users/john/project-b/.assistant/todos.json`

**Result:** Each project has independent TODO/journal data!

## Path Types Used

### 1. In SKILL.md (Script Paths)
```bash
python3 scripts/todo_manager.py
```
- **Type**: Relative to SKILL.md location
- **Resolved by**: Claude Code
- **Final path**: `~/.claude/skills/assistant/scripts/todo_manager.py`

### 2. In Python Scripts (Data Paths)
```python
default_file = os.path.join(".assistant", "todos.json")
```
- **Type**: Relative to current working directory (CWD)
- **Resolved by**: Python's os module
- **Final path**: `{CWD}/.assistant/todos.json`

### 3. Environment Variables (Optional Custom Paths)
```bash
export TODO_DATA_FILE="/custom/path/todos.json"
```
- **Type**: Absolute path
- **Overrides**: Default `.assistant/` location
- **Use case**: Special storage requirements

## Testing Path Resolution

### Test 1: Verify Script Location
```bash
# Should show ~/.claude/skills/assistant/scripts/
ls -la ~/.claude/skills/assistant/scripts/
```

### Test 2: Verify Data Storage
```bash
# Navigate to test project
cd /tmp/test-project

# Add a TODO
python3 ~/.claude/skills/assistant/scripts/todo_manager.py add "Test"

# Check data location (should be in /tmp/test-project/.assistant/)
ls -la .assistant/
cat .assistant/todos.json
```

### Test 3: Verify Independence
```bash
# Project A
cd /tmp/project-a
python3 ~/.claude/skills/assistant/scripts/todo_manager.py add "Task A"

# Project B
cd /tmp/project-b
python3 ~/.claude/skills/assistant/scripts/todo_manager.py add "Task B"

# Verify different data
cat /tmp/project-a/.assistant/todos.json  # Contains "Task A"
cat /tmp/project-b/.assistant/todos.json  # Contains "Task B"
```

## Common Pitfalls

### ❌ Wrong: Using absolute paths in SKILL.md
```bash
python3 ~/.claude/skills/assistant/scripts/todo_manager.py
```
This is too specific and may break if skill is installed elsewhere.

### ✓ Correct: Using relative paths in SKILL.md
```bash
python3 scripts/todo_manager.py
```
Claude Code resolves this correctly regardless of installation location.

### ❌ Wrong: Using skill directory for data storage
```python
# In Python script
data_file = "~/.claude/skills/assistant/data/todos.json"
```
This stores all users' data in one location (bad!).

### ✓ Correct: Using working directory for data storage
```python
# In Python script
data_file = os.path.join(".assistant", "todos.json")
```
Each project gets its own data directory (good!).

## Summary

**Scripts:** Always in `~/.claude/skills/assistant/scripts/` (one location)
**Data:** Always in `{project}/.assistant/` (per-project location)
**Result:** One skill installation serves many projects with isolated data
