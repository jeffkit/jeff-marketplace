#!/usr/bin/env python3
"""
TODO Manager V2 - Dual-file architecture with active/archived separation
Supports new fields for Agent autonomous workflows
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class TodoManager:
    def __init__(self, active_file: str = None, archived_file: str = None):
        """Initialize TODO manager with separate active and archived files"""
        if active_file is None:
            active_file = os.path.join(".assistant", "active-todos.json")
        if archived_file is None:
            archived_file = os.path.join(".assistant", "archived-todos.json")

        self.active_file = Path(active_file)
        self.archived_file = Path(archived_file)

        self.active_todos = self._load_file(self.active_file)
        self.archived_todos = self._load_file(self.archived_file)

    def _load_file(self, filepath: Path) -> List[Dict]:
        """Load todos from JSON file"""
        if not filepath.exists():
            return []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    print(f"Warning: Invalid data format in {filepath}, starting fresh", file=sys.stderr)
                    return []
                valid_todos = [item for item in data if isinstance(item, dict)]
                if len(valid_todos) != len(data):
                    print(f"Warning: Filtered {len(data) - len(valid_todos)} invalid items from {filepath}", file=sys.stderr)
                return valid_todos
        except json.JSONDecodeError:
            print(f"Warning: Could not parse {filepath}, starting fresh", file=sys.stderr)
            return []

    def _save_file(self, filepath: Path, todos: List[Dict]):
        """Save todos to JSON file"""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(todos, f, ensure_ascii=False, indent=2)

    def _get_next_id(self) -> int:
        """Get next available ID across both files"""
        all_todos = self.active_todos + self.archived_todos
        if not all_todos:
            return 1
        return max(todo.get("id", 0) for todo in all_todos) + 1

    def _should_archive(self, todo: Dict) -> bool:
        """Determine if a TODO should be archived"""
        status = todo.get("status", "")
        return status in ["completed", "cancelled"]

    def _move_to_archive(self, todo_id: int):
        """Move a TODO from active to archived"""
        for i, todo in enumerate(self.active_todos):
            if todo.get("id") == todo_id:
                # Remove from active
                archived_todo = self.active_todos.pop(i)
                # Add to archived
                self.archived_todos.append(archived_todo)
                # Save both files
                self._save_file(self.active_file, self.active_todos)
                self._save_file(self.archived_file, self.archived_todos)
                return True
        return False

    def add_todo(self, title: str, category: str = "general",
                 priority: str = "medium", due_date: Optional[str] = None,
                 project: Optional[str] = None, assignee: Optional[str] = None,
                 tags: Optional[List[str]] = None, description: Optional[str] = None,
                 # New fields for Agent workflows
                 next_action_time: Optional[str] = None,
                 needs_clarification: bool = False,
                 clarification_question: Optional[str] = None,
                 blockers: Optional[List[str]] = None,
                 auto_progress_hint: Optional[str] = None) -> Dict:
        """Add a new TODO item (always goes to active file)"""
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
            # New fields
            "next_action_time": next_action_time,
            "needs_clarification": needs_clarification,
            "clarification_question": clarification_question,
            "blockers": blockers or [],
            "last_reviewed": datetime.now().isoformat(),
            "auto_progress_hint": auto_progress_hint,
            # Timestamps
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.active_todos.append(todo)
        self._save_file(self.active_file, self.active_todos)
        return todo

    def list_todos(self, category: Optional[str] = None,
                   status: Optional[str] = None,
                   priority: Optional[str] = None,
                   project: Optional[str] = None,
                   assignee: Optional[str] = None,
                   tags: Optional[List[str]] = None,
                   include_archived: bool = False,
                   needs_attention: bool = False) -> List[Dict]:
        """List todos with optional filters"""
        # Choose which todos to search
        if include_archived:
            result = self.active_todos + self.archived_todos
        else:
            result = self.active_todos.copy()

        # Special filter: needs attention
        if needs_attention:
            now = datetime.now().isoformat()
            result = [t for t in result if (
                t.get("needs_clarification") or
                (t.get("next_action_time") and t.get("next_action_time") <= now) or
                (t.get("due_date") and t.get("due_date") <= now[:10]) or
                len(t.get("blockers", [])) > 0
            )]

        # Standard filters
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
            for tag in tags:
                result = [t for t in result if tag in t.get("tags", [])]

        return result

    def update_todo(self, todo_id: int, **kwargs) -> Optional[Dict]:
        """Update a TODO item and handle archiving if needed"""
        # Try to find in active todos first
        for todo in self.active_todos:
            if todo.get("id") == todo_id:
                # Update fields
                for key, value in kwargs.items():
                    if value is not None:
                        todo[key] = value

                todo["updated_at"] = datetime.now().isoformat()

                # Check if should be archived
                if self._should_archive(todo):
                    self._move_to_archive(todo_id)
                else:
                    self._save_file(self.active_file, self.active_todos)

                return todo

        # Try archived todos (for restoring)
        for todo in self.archived_todos:
            if todo.get("id") == todo_id:
                # Update fields
                for key, value in kwargs.items():
                    if value is not None:
                        todo[key] = value

                todo["updated_at"] = datetime.now().isoformat()

                # If status changed to active, move back to active
                if not self._should_archive(todo):
                    self.archived_todos.remove(todo)
                    self.active_todos.append(todo)
                    self._save_file(self.active_file, self.active_todos)
                    self._save_file(self.archived_file, self.archived_todos)
                else:
                    self._save_file(self.archived_file, self.archived_todos)

                return todo

        return None

    def delete_todo(self, todo_id: int) -> bool:
        """Delete a TODO item from both files"""
        # Try active
        for i, todo in enumerate(self.active_todos):
            if todo.get("id") == todo_id:
                self.active_todos.pop(i)
                self._save_file(self.active_file, self.active_todos)
                return True

        # Try archived
        for i, todo in enumerate(self.archived_todos):
            if todo.get("id") == todo_id:
                self.archived_todos.pop(i)
                self._save_file(self.archived_file, self.archived_todos)
                return True

        return False

    def search_todos(self, keyword: str, include_archived: bool = False) -> List[Dict]:
        """Search todos by keyword in title or description"""
        keyword_lower = keyword.lower()

        if include_archived:
            todos = self.active_todos + self.archived_todos
        else:
            todos = self.active_todos

        return [t for t in todos if (
            keyword_lower in t.get("title", "").lower() or
            keyword_lower in t.get("description", "").lower()
        )]


def main():
    """CLI interface for TODO manager"""
    if len(sys.argv) < 2:
        print("Usage: todo_manager.py <command> [args...]")
        print("\nCommands:")
        print("  add <title> [--category CAT] [--priority PRI] [--due-date DATE]")
        print("              [--project PROJ] [--assignee WHO] [--tags TAG1,TAG2] [--description DESC]")
        print("              [--next-action-time ISO8601] [--needs-clarification]")
        print("              [--clarification-question TEXT] [--blockers B1,B2]")
        print("              [--auto-progress-hint TEXT]")
        print("  list [--category CAT] [--status STATUS] [--priority PRI]")
        print("       [--project PROJ] [--assignee WHO] [--tags TAG1,TAG2]")
        print("       [--include-archived] [--needs-attention]")
        print("  update <id> [--title TITLE] [--status STATUS] [--priority PRI]")
        print("              [--due-date DATE] [--project PROJ] [--assignee WHO]")
        print("              [--tags TAG1,TAG2] [--description DESC]")
        print("              [--next-action-time ISO8601] [--needs-clarification BOOL]")
        print("              [--clarification-question TEXT] [--blockers B1,B2]")
        print("              [--last-reviewed ISO8601] [--auto-progress-hint TEXT]")
        print("  delete <id>")
        print("  search <keyword> [--include-archived]")
        sys.exit(1)

    manager = TodoManager()
    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Error: title required", file=sys.stderr)
            sys.exit(1)

        title = sys.argv[2]
        kwargs = {
            "category": "general",
            "priority": "medium",
            "due_date": None,
            "project": None,
            "assignee": None,
            "tags": None,
            "description": None,
            "next_action_time": None,
            "needs_clarification": False,
            "clarification_question": None,
            "blockers": None,
            "auto_progress_hint": None
        }

        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--category" and i + 1 < len(sys.argv):
                kwargs["category"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--priority" and i + 1 < len(sys.argv):
                kwargs["priority"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--due-date" and i + 1 < len(sys.argv):
                kwargs["due_date"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--project" and i + 1 < len(sys.argv):
                kwargs["project"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--assignee" and i + 1 < len(sys.argv):
                kwargs["assignee"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--tags" and i + 1 < len(sys.argv):
                kwargs["tags"] = [tag.strip() for tag in sys.argv[i + 1].split(",")]
                i += 2
            elif sys.argv[i] == "--description" and i + 1 < len(sys.argv):
                kwargs["description"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--next-action-time" and i + 1 < len(sys.argv):
                kwargs["next_action_time"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--needs-clarification":
                kwargs["needs_clarification"] = True
                i += 1
            elif sys.argv[i] == "--clarification-question" and i + 1 < len(sys.argv):
                kwargs["clarification_question"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--blockers" and i + 1 < len(sys.argv):
                kwargs["blockers"] = [b.strip() for b in sys.argv[i + 1].split(",")]
                i += 2
            elif sys.argv[i] == "--auto-progress-hint" and i + 1 < len(sys.argv):
                kwargs["auto_progress_hint"] = sys.argv[i + 1]
                i += 2
            else:
                i += 1

        todo = manager.add_todo(title, **kwargs)
        print(json.dumps(todo, ensure_ascii=False, indent=2))

    elif command == "list":
        kwargs = {
            "category": None,
            "status": None,
            "priority": None,
            "project": None,
            "assignee": None,
            "tags": None,
            "include_archived": False,
            "needs_attention": False
        }

        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--category" and i + 1 < len(sys.argv):
                kwargs["category"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--status" and i + 1 < len(sys.argv):
                kwargs["status"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--priority" and i + 1 < len(sys.argv):
                kwargs["priority"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--project" and i + 1 < len(sys.argv):
                kwargs["project"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--assignee" and i + 1 < len(sys.argv):
                kwargs["assignee"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--tags" and i + 1 < len(sys.argv):
                kwargs["tags"] = [tag.strip() for tag in sys.argv[i + 1].split(",")]
                i += 2
            elif sys.argv[i] == "--include-archived":
                kwargs["include_archived"] = True
                i += 1
            elif sys.argv[i] == "--needs-attention":
                kwargs["needs_attention"] = True
                i += 1
            else:
                i += 1

        todos = manager.list_todos(**kwargs)
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
            elif sys.argv[i] == "--next-action-time" and i + 1 < len(sys.argv):
                updates["next_action_time"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--needs-clarification" and i + 1 < len(sys.argv):
                updates["needs_clarification"] = sys.argv[i + 1].lower() == "true"
                i += 2
            elif sys.argv[i] == "--clarification-question" and i + 1 < len(sys.argv):
                updates["clarification_question"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--blockers" and i + 1 < len(sys.argv):
                updates["blockers"] = [b.strip() for b in sys.argv[i + 1].split(",")]
                i += 2
            elif sys.argv[i] == "--last-reviewed" and i + 1 < len(sys.argv):
                updates["last_reviewed"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--auto-progress-hint" and i + 1 < len(sys.argv):
                updates["auto_progress_hint"] = sys.argv[i + 1]
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
        include_archived = "--include-archived" in sys.argv

        todos = manager.search_todos(keyword, include_archived)
        print(json.dumps(todos, ensure_ascii=False, indent=2))

    else:
        print(f"Error: Unknown command '{command}'", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
