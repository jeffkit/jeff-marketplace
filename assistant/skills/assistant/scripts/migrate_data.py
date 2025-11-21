#!/usr/bin/env python3
"""
Data Migration Script - Migrate old data files to .assistant directory
"""

import json
import os
import shutil
from pathlib import Path


def migrate_file(old_path: str, new_path: str, file_type: str):
    """Migrate a data file from old location to new location"""
    old_file = Path(old_path)
    new_file = Path(new_path)

    if not old_file.exists():
        print(f"✓ No old {file_type} file found at {old_path}, nothing to migrate")
        return

    # Create .assistant directory if it doesn't exist
    new_file.parent.mkdir(parents=True, exist_ok=True)

    # Check if new file already exists
    if new_file.exists():
        print(f"⚠ Warning: {new_path} already exists")
        response = input(f"Do you want to merge with {old_path}? (y/n): ")
        if response.lower() == 'y':
            # Load both files
            with open(old_file, 'r', encoding='utf-8') as f:
                old_data = json.load(f)
            with open(new_file, 'r', encoding='utf-8') as f:
                new_data = json.load(f)

            # Merge (new_data takes precedence for ID conflicts)
            old_ids = {item['id'] for item in old_data}
            new_ids = {item['id'] for item in new_data}

            # Add old items that don't conflict
            merged_data = new_data.copy()
            for item in old_data:
                if item['id'] not in new_ids:
                    merged_data.append(item)

            # Save merged data
            with open(new_file, 'w', encoding='utf-8') as f:
                json.dump(merged_data, f, ensure_ascii=False, indent=2)

            print(f"✓ Merged {len(old_data)} old items with {len(new_data)} new items")
            print(f"  Total items: {len(merged_data)}")
        else:
            print(f"✗ Skipped merging {old_path}")
            return
    else:
        # Simply copy the file
        shutil.copy2(old_file, new_file)
        print(f"✓ Migrated {old_path} → {new_path}")

    # Ask if user wants to delete the old file
    response = input(f"Delete old file {old_path}? (y/n): ")
    if response.lower() == 'y':
        old_file.unlink()
        print(f"✓ Deleted {old_path}")
    else:
        print(f"✓ Kept {old_path} (you can delete it manually later)")


def main():
    """Main migration process"""
    print("=" * 60)
    print("Assistant Plugin Data Migration")
    print("=" * 60)
    print()
    print("This script will migrate your data files from the project root")
    print("to the .assistant/ directory.")
    print()

    # Migrate TODOs
    print("1. Migrating TODOs...")
    old_todo = os.environ.get("TODO_DATA_FILE", "todos.json")
    new_todo = ".assistant/todos.json"
    migrate_file(old_todo, new_todo, "TODOs")
    print()

    # Migrate Journals
    print("2. Migrating Journals...")
    old_journal = os.environ.get("JOURNAL_DATA_FILE", "journals.json")
    new_journal = ".assistant/journals.json"
    migrate_file(old_journal, new_journal, "journals")
    print()

    print("=" * 60)
    print("Migration Complete!")
    print("=" * 60)
    print()
    print("Your data files are now in the .assistant/ directory:")
    print(f"  - {new_todo}")
    print(f"  - {new_journal}")
    print()
    print("The .assistant/ directory is gitignored to prevent accidental commits.")
    print()


if __name__ == "__main__":
    main()
