#!/usr/bin/env python3
"""
TODO Manager - Manage TODO items with JSON storage
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class TodoManager:
    def __init__(self, data_file: str = "todos.json"):
        """Initialize TODO manager with data file path"""
        self.data_file = Path(data_file)
        self.todos = self._load_todos()

    def _load_todos(self) -> List[Dict]:
        """Load todos from JSON file"""
        if not self.data_file.exists():
            return []

        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Ensure we have a list and all items are dictionaries
                if not isinstance(data, list):
                    print(f"Warning: Invalid data format in {self.data_file}, starting fresh", file=sys.stderr)
                    return []
                # Filter out any non-dict items
                valid_todos = [item for item in data if isinstance(item, dict)]
                if len(valid_todos) != len(data):
                    print(f"Warning: Filtered {len(data) - len(valid_todos)} invalid items from {self.data_file}", file=sys.stderr)
                return valid_todos
        except json.JSONDecodeError:
            print(f"Warning: Could not parse {self.data_file}, starting fresh", file=sys.stderr)
            return []

    def _save_todos(self):
        """Save todos to JSON file"""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.todos, f, ensure_ascii=False, indent=2)

    def _get_next_id(self) -> int:
        """Get next available ID safely"""
        valid_todos = [t for t in self.todos if isinstance(t, dict)]
        if not valid_todos:
            return 1
        return max(todo.get("id", 0) for todo in valid_todos) + 1

    def add_todo(self, title: str, category: str = "general",
                 priority: str = "medium", due_date: Optional[str] = None,
                 project: Optional[str] = None, assignee: Optional[str] = None,
                 tags: Optional[List[str]] = None, description: Optional[str] = None) -> Dict:
        """Add a new TODO item"""
        todo = {
            "id": self._get_next_id(),
            "title": title,
            "category": category,
            "priority": priority,
            "status": "pending",
            "due_date": due_date,
            "project": project,
            "assignee": assignee,
            "tags": tags or [],
            "description": description,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.todos.append(todo)
        self._save_todos()
        return todo

    def list_todos(self, category: Optional[str] = None,
                   status: Optional[str] = None,
                   priority: Optional[str] = None,
                   project: Optional[str] = None,
                   assignee: Optional[str] = None,
                   tags: Optional[List[str]] = None) -> List[Dict]:
        """List todos with optional filters"""
        # Filter out any non-dict items that might have corrupted the data
        result = [t for t in self.todos if isinstance(t, dict)]

        if category:
            result = [t for t in result if t.get("category") == category]

        if status:
            result = [t for t in result if t.get("status") == status]

        if priority:
            result = [t for t in result if t.get("priority") == priority]

        if project:
            result = [t for t in result if t.get("project") == project]

        if assignee:
            result = [t for t in result if t.get("assignee") == assignee]

        if tags:
            # Filter todos that contain ALL specified tags
            for tag in tags:
                result = [t for t in result if tag in t.get("tags", [])]

        return result

    def update_todo(self, todo_id: int, **kwargs) -> Optional[Dict]:
        """Update a TODO item"""
        for todo in self.todos:
            if isinstance(todo, dict) and todo.get("id") == todo_id:
                for key, value in kwargs.items():
                    if value is not None:
                        todo[key] = value
                todo["updated_at"] = datetime.now().isoformat()
                self._save_todos()
                return todo
        return None

    def delete_todo(self, todo_id: int) -> bool:
        """Delete a TODO item"""
        initial_len = len(self.todos)
        self.todos = [t for t in self.todos if not (isinstance(t, dict) and t.get("id") == todo_id)]
        if len(self.todos) < initial_len:
            self._save_todos()
            return True
        return False

    def search_todos(self, keyword: str) -> List[Dict]:
        """Search todos by keyword in title"""
        keyword_lower = keyword.lower()
        valid_todos = [t for t in self.todos if isinstance(t, dict)]
        return [t for t in valid_todos if keyword_lower in t.get("title", "").lower()]


def main():
    """CLI interface for TODO manager"""
    if len(sys.argv) < 2:
        print("Usage: todo_manager.py <command> [args...]")
        print("\nCommands:")
        print("  add <title> [--category CAT] [--priority PRI] [--due-date DATE]")
        print("              [--project PROJ] [--assignee WHO] [--tags TAG1,TAG2] [--description DESC]")
        print("  list [--category CAT] [--status STATUS] [--priority PRI]")
        print("            [--project PROJ] [--assignee WHO] [--tags TAG1,TAG2]")
        print("  update <id> [--title TITLE] [--status STATUS] [--priority PRI] [--due-date DATE]")
        print("             [--project PROJ] [--assignee WHO] [--tags TAG1,TAG2] [--description DESC]")
        print("  delete <id>")
        print("  search <keyword>")
        sys.exit(1)

    # Get data file from environment or use default in .assistant directory
    default_file = os.path.join(".assistant", "todos.json")
    data_file = os.environ.get("TODO_DATA_FILE", default_file)
    manager = TodoManager(data_file)

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Error: title required", file=sys.stderr)
            sys.exit(1)

        title = sys.argv[2]
        category = "general"
        priority = "medium"
        due_date = None
        project = None
        assignee = None
        tags = None
        description = None

        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--category" and i + 1 < len(sys.argv):
                category = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--priority" and i + 1 < len(sys.argv):
                priority = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--due-date" and i + 1 < len(sys.argv):
                due_date = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--project" and i + 1 < len(sys.argv):
                project = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--assignee" and i + 1 < len(sys.argv):
                assignee = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--tags" and i + 1 < len(sys.argv):
                tags = [tag.strip() for tag in sys.argv[i + 1].split(",")]
                i += 2
            elif sys.argv[i] == "--description" and i + 1 < len(sys.argv):
                description = sys.argv[i + 1]
                i += 2
            else:
                i += 1

        todo = manager.add_todo(title, category, priority, due_date, project, assignee, tags, description)
        print(json.dumps(todo, ensure_ascii=False, indent=2))

    elif command == "list":
        category = None
        status = None
        priority = None
        project = None
        assignee = None
        tags = None

        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--category" and i + 1 < len(sys.argv):
                category = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--status" and i + 1 < len(sys.argv):
                status = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--priority" and i + 1 < len(sys.argv):
                priority = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--project" and i + 1 < len(sys.argv):
                project = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--assignee" and i + 1 < len(sys.argv):
                assignee = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--tags" and i + 1 < len(sys.argv):
                tags = [tag.strip() for tag in sys.argv[i + 1].split(",")]
                i += 2
            else:
                i += 1

        todos = manager.list_todos(category, status, priority, project, assignee, tags)
        print(json.dumps(todos, ensure_ascii=False, indent=2))

    elif command == "update":
        if len(sys.argv) < 3:
            print("Error: todo id required", file=sys.stderr)
            sys.exit(1)

        todo_id = int(sys.argv[2])
        updates = {}

        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--title" and i + 1 < len(sys.argv):
                updates["title"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--status" and i + 1 < len(sys.argv):
                updates["status"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--priority" and i + 1 < len(sys.argv):
                updates["priority"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--category" and i + 1 < len(sys.argv):
                updates["category"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--due-date" and i + 1 < len(sys.argv):
                updates["due_date"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--project" and i + 1 < len(sys.argv):
                updates["project"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--assignee" and i + 1 < len(sys.argv):
                updates["assignee"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--tags" and i + 1 < len(sys.argv):
                updates["tags"] = [tag.strip() for tag in sys.argv[i + 1].split(",")]
                i += 2
            elif sys.argv[i] == "--description" and i + 1 < len(sys.argv):
                updates["description"] = sys.argv[i + 1]
                i += 2
            else:
                i += 1

        todo = manager.update_todo(todo_id, **updates)
        if todo:
            print(json.dumps(todo, ensure_ascii=False, indent=2))
        else:
            print(f"Error: TODO {todo_id} not found", file=sys.stderr)
            sys.exit(1)

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: todo id required", file=sys.stderr)
            sys.exit(1)

        todo_id = int(sys.argv[2])
        if manager.delete_todo(todo_id):
            print(f"TODO {todo_id} deleted")
        else:
            print(f"Error: TODO {todo_id} not found", file=sys.stderr)
            sys.exit(1)

    elif command == "search":
        if len(sys.argv) < 3:
            print("Error: keyword required", file=sys.stderr)
            sys.exit(1)

        keyword = sys.argv[2]
        todos = manager.search_todos(keyword)
        print(json.dumps(todos, ensure_ascii=False, indent=2))

    else:
        print(f"Error: Unknown command '{command}'", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
