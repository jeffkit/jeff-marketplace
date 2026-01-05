#!/usr/bin/env python3
"""
Journal Manager V2 - Manage journal entries with Markdown + YAML frontmatter
Each day is a separate markdown file with structured metadata
"""

import os
import sys
import re
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional
import json


class JournalManager:
    def __init__(self, base_dir: str = None):
        """Initialize journal manager with base directory for markdown files"""
        if base_dir is None:
            base_dir = os.path.join(".assistant", "journals")
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _get_journal_path(self, target_date: date) -> Path:
        """Get path to journal file for a specific date"""
        year_month = target_date.strftime("%Y-%m")
        filename = target_date.strftime("%Y-%m-%d.md")
        month_dir = self.base_dir / year_month
        month_dir.mkdir(parents=True, exist_ok=True)
        return month_dir / filename

    def _parse_frontmatter(self, content: str) -> tuple[Dict, str]:
        """Parse YAML frontmatter from markdown content"""
        if not content.startswith("---\n"):
            return {}, content

        # Find the end of frontmatter
        match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
        if not match:
            return {}, content

        frontmatter_text = match.group(1)
        body = match.group(2)

        # Simple YAML parsing (limited to our use case)
        frontmatter = {}
        for line in frontmatter_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()

                # Parse lists
                if value.startswith('[') and value.endswith(']'):
                    value = [v.strip() for v in value[1:-1].split(',') if v.strip()]
                # Parse numbers
                elif value.isdigit():
                    value = int(value)

                frontmatter[key] = value

        return frontmatter, body

    def _serialize_frontmatter(self, frontmatter: Dict) -> str:
        """Serialize frontmatter dict to YAML format"""
        lines = ["---"]
        for key, value in frontmatter.items():
            if isinstance(value, list):
                value_str = f"[{', '.join(value)}]"
            else:
                value_str = str(value)
            lines.append(f"{key}: {value_str}")
        lines.append("---")
        return '\n'.join(lines)

    def _create_daily_journal(self, target_date: date) -> str:
        """Create a new daily journal file with template"""
        day_name = target_date.strftime("%A")
        cn_date = target_date.strftime("%Y年%m月%d日")

        frontmatter = {
            "date": target_date.isoformat(),
            "day_of_week": day_name,
            "categories": [],
            "moods": [],
            "tags": [],
            "todos_completed": 0,
            "todos_created": 0,
            "key_achievements": []
        }

        content = f"""{self._serialize_frontmatter(frontmatter)}

# {cn_date} 星期{day_name}

## 🌅 早晨 (06:00 - 12:00)


---

## 🌞 下午 (12:00 - 18:00)


---

## 🌙 晚上 (18:00 - 24:00)


---

## 📊 今日总结

### ✅ 完成的任务


### 📝 新增的任务


### 🎯 主要成就


### 💭 今日反思


### 🔮 明天计划


---

## 🤖 Agent工作记录

"""
        return content

    def _update_frontmatter(self, frontmatter: Dict, category: str, mood: str, tags: List[str]) -> Dict:
        """Update frontmatter with new entry metadata"""
        # Add category if not present
        if category and category not in frontmatter.get('categories', []):
            if 'categories' not in frontmatter:
                frontmatter['categories'] = []
            frontmatter['categories'].append(category)

        # Add mood if not present
        if mood and mood not in frontmatter.get('moods', []):
            if 'moods' not in frontmatter:
                frontmatter['moods'] = []
            frontmatter['moods'].append(mood)

        # Add tags
        if tags:
            if 'tags' not in frontmatter:
                frontmatter['tags'] = []
            for tag in tags:
                if tag not in frontmatter['tags']:
                    frontmatter['tags'].append(tag)

        return frontmatter

    def _format_entry(self, content: str, category: str, mood: str, tags: List[str]) -> str:
        """Format a journal entry"""
        now = datetime.now()
        time_str = now.strftime("%H:%M")

        entry_lines = [f"### {time_str} - {content}"]

        if category:
            entry_lines.append(f"分类：{category}")
        if mood:
            entry_lines.append(f"心情：{mood}")
        if tags:
            entry_lines.append(f"标签：{', '.join(tags)}")

        entry_lines.append("")  # Blank line after entry

        return '\n'.join(entry_lines)

    def _insert_entry(self, content: str, new_entry: str) -> str:
        """Insert entry into appropriate time section"""
        now = datetime.now()
        hour = now.hour

        # Determine which section to add to
        if 6 <= hour < 12:
            section_marker = "## 🌅 早晨"
        elif 12 <= hour < 18:
            section_marker = "## 🌞 下午"
        else:
            section_marker = "## 🌙 晚上"

        # Find the section and next separator
        lines = content.split('\n')
        insert_pos = None

        for i, line in enumerate(lines):
            if line.startswith(section_marker):
                # Find next section or separator
                for j in range(i + 1, len(lines)):
                    if lines[j].startswith('---') or lines[j].startswith('## '):
                        insert_pos = j
                        break
                break

        if insert_pos:
            lines.insert(insert_pos, new_entry)
            lines.insert(insert_pos, "")  # Add blank line before entry
        else:
            # Append to end if section not found
            lines.append(new_entry)

        return '\n'.join(lines)

    def add_entry(self, content: str, category: str = None, mood: str = None,
                  tags: List[str] = None, entry_date: date = None) -> Dict:
        """Add a journal entry to today's (or specified date's) journal"""
        target_date = entry_date or date.today()
        filepath = self._get_journal_path(target_date)

        # Create or read existing journal
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                existing_content = f.read()
        else:
            existing_content = self._create_daily_journal(target_date)

        # Parse frontmatter
        frontmatter, body = self._parse_frontmatter(existing_content)

        # Update frontmatter
        frontmatter = self._update_frontmatter(frontmatter, category, mood, tags or [])

        # Format new entry
        new_entry = self._format_entry(content, category, mood, tags or [])

        # Insert entry
        body = self._insert_entry(body, new_entry)

        # Combine and save
        new_content = self._serialize_frontmatter(frontmatter) + '\n' + body

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return {
            "success": True,
            "date": target_date.isoformat(),
            "file": str(filepath),
            "entry": new_entry
        }

    def add_agent_session(self, trigger: str, actions: List[str], observations: str,
                         next_hint: str = None, session_date: date = None) -> Dict:
        """Add Agent work session record to today's journal"""
        target_date = session_date or date.today()
        filepath = self._get_journal_path(target_date)

        # Create or read existing journal
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = self._create_daily_journal(target_date)

        # Find Agent section
        now = datetime.now()
        session_id = now.strftime("%Y-%m-%d-%H-%M")
        duration = "执行中"

        session_entry = f"""
### Session: {session_id}
触发方式：{trigger}
持续时间：{duration}

**执行的动作：**
"""
        for i, action in enumerate(actions, 1):
            session_entry += f"{i}. {action}\n"

        session_entry += f"""
**观察和建议：**
{observations}
"""

        if next_hint:
            session_entry += f"""
**下次会话：**
{next_hint}
"""

        # Append to Agent section
        if "## 🤖 Agent工作记录" in content:
            content = content.replace("## 🤖 Agent工作记录\n", f"## 🤖 Agent工作记录\n{session_entry}\n")
        else:
            content += f"\n\n## 🤖 Agent工作记录\n{session_entry}\n"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return {
            "success": True,
            "session_id": session_id,
            "file": str(filepath)
        }

    def show(self, target_date: date = None) -> Dict:
        """Show journal for a specific date"""
        target_date = target_date or date.today()
        filepath = self._get_journal_path(target_date)

        if not filepath.exists():
            return {
                "success": False,
                "error": f"No journal found for {target_date.isoformat()}"
            }

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        frontmatter, body = self._parse_frontmatter(content)

        return {
            "success": True,
            "date": target_date.isoformat(),
            "file": str(filepath),
            "frontmatter": frontmatter,
            "content": content
        }

    def list_recent(self, days: int = 7) -> List[str]:
        """List recent journal files"""
        files = []
        for month_dir in sorted(self.base_dir.iterdir(), reverse=True):
            if month_dir.is_dir():
                for journal_file in sorted(month_dir.glob("*.md"), reverse=True):
                    files.append(str(journal_file))
                    if len(files) >= days:
                        return files
        return files

    def search(self, keyword: str, days: int = 30) -> List[Dict]:
        """Search recent journals for keyword"""
        results = []
        files = self.list_recent(days)

        keyword_lower = keyword.lower()

        for filepath in files:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            if keyword_lower in content.lower():
                # Extract matching lines
                matches = []
                for line in content.split('\n'):
                    if keyword_lower in line.lower():
                        matches.append(line.strip())

                results.append({
                    "file": filepath,
                    "date": Path(filepath).stem,
                    "matches": matches[:5]  # Limit to 5 matches per file
                })

        return results


def main():
    """CLI interface for journal manager"""
    if len(sys.argv) < 2:
        print("Usage: journal_manager.py <command> [args...]")
        print("\nCommands:")
        print("  add <content> [--category CAT] [--mood MOOD] [--tags TAG1,TAG2] [--date YYYY-MM-DD]")
        print("  add-agent-session --trigger TYPE --actions 'action1;action2' --observations 'text' [--next-hint 'text']")
        print("  show [--date YYYY-MM-DD]")
        print("  list [--recent N]")
        print("  search <keyword> [--days N]")
        sys.exit(1)

    manager = JournalManager()
    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Error: content required", file=sys.stderr)
            sys.exit(1)

        content = sys.argv[2]
        category = None
        mood = None
        tags = None
        entry_date = None

        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--category" and i + 1 < len(sys.argv):
                category = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--mood" and i + 1 < len(sys.argv):
                mood = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--tags" and i + 1 < len(sys.argv):
                tags = [t.strip() for t in sys.argv[i + 1].split(',')]
                i += 2
            elif sys.argv[i] == "--date" and i + 1 < len(sys.argv):
                entry_date = date.fromisoformat(sys.argv[i + 1])
                i += 2
            else:
                i += 1

        result = manager.add_entry(content, category, mood, tags, entry_date)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "add-agent-session":
        trigger = "manual"
        actions = []
        observations = ""
        next_hint = None

        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--trigger" and i + 1 < len(sys.argv):
                trigger = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--actions" and i + 1 < len(sys.argv):
                actions = sys.argv[i + 1].split(';')
                i += 2
            elif sys.argv[i] == "--observations" and i + 1 < len(sys.argv):
                observations = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--next-hint" and i + 1 < len(sys.argv):
                next_hint = sys.argv[i + 1]
                i += 2
            else:
                i += 1

        result = manager.add_agent_session(trigger, actions, observations, next_hint)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "show":
        target_date = None

        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--date" and i + 1 < len(sys.argv):
                target_date = date.fromisoformat(sys.argv[i + 1])
                i += 2
            else:
                i += 1

        result = manager.show(target_date)
        if result['success']:
            print(result['content'])
        else:
            print(result['error'], file=sys.stderr)
            sys.exit(1)

    elif command == "list":
        days = 7

        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--recent" and i + 1 < len(sys.argv):
                days = int(sys.argv[i + 1])
                i += 2
            else:
                i += 1

        files = manager.list_recent(days)
        print(json.dumps(files, ensure_ascii=False, indent=2))

    elif command == "search":
        if len(sys.argv) < 3:
            print("Error: keyword required", file=sys.stderr)
            sys.exit(1)

        keyword = sys.argv[2]
        days = 30

        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--days" and i + 1 < len(sys.argv):
                days = int(sys.argv[i + 1])
                i += 2
            else:
                i += 1

        results = manager.search(keyword, days)
        print(json.dumps(results, ensure_ascii=False, indent=2))

    else:
        print(f"Error: Unknown command '{command}'", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
