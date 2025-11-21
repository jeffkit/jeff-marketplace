#!/usr/bin/env python3
"""
Journal Manager - Manage journal entries with JSON storage
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class JournalManager:
    def __init__(self, data_file: str = "journals.json"):
        """Initialize journal manager with data file path"""
        self.data_file = Path(data_file)
        self.journals = self._load_journals()

    def _load_journals(self) -> List[Dict]:
        """Load journals from JSON file"""
        if not self.data_file.exists():
            return []

        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Could not parse {self.data_file}, starting fresh", file=sys.stderr)
            return []

    def _save_journals(self):
        """Save journals to JSON file"""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.journals, f, ensure_ascii=False, indent=2)

    def add_entry(self, content: str, category: str = "general",
                  mood: Optional[str] = None, tags: Optional[List[str]] = None) -> Dict:
        """Add a new journal entry"""
        entry = {
            "id": len(self.journals) + 1,
            "content": content,
            "category": category,
            "mood": mood,
            "tags": tags or [],
            "timestamp": datetime.now().isoformat()
        }
        self.journals.append(entry)
        self._save_journals()
        return entry

    def list_entries(self, category: Optional[str] = None,
                     start_date: Optional[str] = None,
                     end_date: Optional[str] = None,
                     mood: Optional[str] = None) -> List[Dict]:
        """List journal entries with optional filters"""
        result = self.journals

        if category:
            result = [j for j in result if j.get("category") == category]

        if mood:
            result = [j for j in result if j.get("mood") == mood]

        if start_date:
            result = [j for j in result if j.get("timestamp", "") >= start_date]

        if end_date:
            result = [j for j in result if j.get("timestamp", "") <= end_date]

        return result

    def update_entry(self, entry_id: int, **kwargs) -> Optional[Dict]:
        """Update a journal entry"""
        for entry in self.journals:
            if entry["id"] == entry_id:
                for key, value in kwargs.items():
                    if value is not None:
                        entry[key] = value
                self._save_journals()
                return entry
        return None

    def delete_entry(self, entry_id: int) -> bool:
        """Delete a journal entry"""
        initial_len = len(self.journals)
        self.journals = [j for j in self.journals if j["id"] != entry_id]
        if len(self.journals) < initial_len:
            self._save_journals()
            return True
        return False

    def search_entries(self, keyword: str) -> List[Dict]:
        """Search journal entries by keyword in content"""
        keyword_lower = keyword.lower()
        return [j for j in self.journals if keyword_lower in j.get("content", "").lower()]


def main():
    """CLI interface for journal manager"""
    if len(sys.argv) < 2:
        print("Usage: journal_manager.py <command> [args...]")
        print("\nCommands:")
        print("  add <content> [--category CAT] [--mood MOOD] [--tags TAG1,TAG2]")
        print("  list [--category CAT] [--start-date DATE] [--end-date DATE] [--mood MOOD]")
        print("  update <id> [--content CONTENT] [--category CAT] [--mood MOOD] [--tags TAG1,TAG2]")
        print("  delete <id>")
        print("  search <keyword>")
        sys.exit(1)

    # Get data file from environment or use default in .assistant directory
    default_file = os.path.join(".assistant", "journals.json")
    data_file = os.environ.get("JOURNAL_DATA_FILE", default_file)
    manager = JournalManager(data_file)

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Error: content required", file=sys.stderr)
            sys.exit(1)

        content = sys.argv[2]
        category = "general"
        mood = None
        tags = None

        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--category" and i + 1 < len(sys.argv):
                category = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--mood" and i + 1 < len(sys.argv):
                mood = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--tags" and i + 1 < len(sys.argv):
                tags = sys.argv[i + 1].split(',')
                i += 2
            else:
                i += 1

        entry = manager.add_entry(content, category, mood, tags)
        print(json.dumps(entry, ensure_ascii=False, indent=2))

    elif command == "list":
        category = None
        start_date = None
        end_date = None
        mood = None

        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--category" and i + 1 < len(sys.argv):
                category = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--start-date" and i + 1 < len(sys.argv):
                start_date = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--end-date" and i + 1 < len(sys.argv):
                end_date = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--mood" and i + 1 < len(sys.argv):
                mood = sys.argv[i + 1]
                i += 2
            else:
                i += 1

        entries = manager.list_entries(category, start_date, end_date, mood)
        print(json.dumps(entries, ensure_ascii=False, indent=2))

    elif command == "update":
        if len(sys.argv) < 3:
            print("Error: entry id required", file=sys.stderr)
            sys.exit(1)

        entry_id = int(sys.argv[2])
        updates = {}

        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--content" and i + 1 < len(sys.argv):
                updates["content"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--category" and i + 1 < len(sys.argv):
                updates["category"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--mood" and i + 1 < len(sys.argv):
                updates["mood"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--tags" and i + 1 < len(sys.argv):
                updates["tags"] = sys.argv[i + 1].split(',')
                i += 2
            else:
                i += 1

        entry = manager.update_entry(entry_id, **updates)
        if entry:
            print(json.dumps(entry, ensure_ascii=False, indent=2))
        else:
            print(f"Error: Journal entry {entry_id} not found", file=sys.stderr)
            sys.exit(1)

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: entry id required", file=sys.stderr)
            sys.exit(1)

        entry_id = int(sys.argv[2])
        if manager.delete_entry(entry_id):
            print(f"Journal entry {entry_id} deleted")
        else:
            print(f"Error: Journal entry {entry_id} not found", file=sys.stderr)
            sys.exit(1)

    elif command == "search":
        if len(sys.argv) < 3:
            print("Error: keyword required", file=sys.stderr)
            sys.exit(1)

        keyword = sys.argv[2]
        entries = manager.search_entries(keyword)
        print(json.dumps(entries, ensure_ascii=False, indent=2))

    else:
        print(f"Error: Unknown command '{command}'", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
