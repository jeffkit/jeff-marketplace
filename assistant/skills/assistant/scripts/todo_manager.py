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
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Could not parse {self.data_file}, starting fresh", file=sys.stderr)
            return []

    def _save_todos(self):
        """Save todos to JSON file"""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.todos, f, ensure_ascii=False, indent=2)

    def add_todo(self, title: str, category: str = "general",
                 priority: str = "medium", due_date: Optional[str] = None) -> Dict:
        """Add a new TODO item"""
        todo = {
            "id": len(self.todos) + 1,
            "title": title,
            "category": category,
            "priority": priority,
            "status": "pending",
            "due_date": due_date,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.todos.append(todo)
        self._save_todos()
        return todo

    def list_todos(self, category: Optional[str] = None,
                   status: Optional[str] = None,
                   priority: Optional[str] = None) -> List[Dict]:
        """List todos with optional filters"""
        result = self.todos

        if category:
            result = [t for t in result if t.get("category") == category]

        if status:
            result = [t for t in result if t.get("status") == status]

        if priority:
            result = [t for t in result if t.get("priority") == priority]

        return result

    def update_todo(self, todo_id: int, **kwargs) -> Optional[Dict]:
        """Update a TODO item"""
        for todo in self.todos:
            if todo["id"] == todo_id:
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
        self.todos = [t for t in self.todos if t["id"] != todo_id]
        if len(self.todos) < initial_len:
            self._save_todos()
            return True
        return False

    def search_todos(self, keyword: str) -> List[Dict]:
        """Search todos by keyword in title"""
        keyword_lower = keyword.lower()
        return [t for t in self.todos if keyword_lower in t.get("title", "").lower()]


def main():
    """CLI interface for TODO manager"""
    if len(sys.argv) < 2:
        print("Usage: todo_manager.py <command> [args...]")
        print("\nCommands:")
        print("  add <title> [--category CAT] [--priority PRI] [--due-date DATE]")
        print("  list [--category CAT] [--status STATUS] [--priority PRI]")
        print("  update <id> [--title TITLE] [--status STATUS] [--priority PRI] [--due-date DATE]")
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
            else:
                i += 1

        todo = manager.add_todo(title, category, priority, due_date)
        print(json.dumps(todo, ensure_ascii=False, indent=2))

    elif command == "list":
        category = None
        status = None
        priority = None

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
            else:
                i += 1

        todos = manager.list_todos(category, status, priority)
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
