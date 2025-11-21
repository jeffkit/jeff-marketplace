# Speckit Driver Plugin for Claude Code

Autonomous Spec-Driven Development orchestrator for Claude Code that enables intelligent, continuous workflow execution with minimal user intervention.

## Overview

Speckit Driver is a Claude Code plugin that transforms how you use [speckit](https://github.com/github/spec-kit) for spec-driven development. Instead of manually executing each speckit command and constantly prompting Claude to continue, this plugin provides:

- **Autonomous orchestration**: Main agent acts as project manager, delegating to specialized sub-agents
- **Continuous workflow**: Executes entire workflows (constitution → specify → plan → tasks → implement) without constant prompting
- **Intelligent decision-making**: Reviews sub-agent outputs and decides when to continue vs. ask for user input
- **Smart interactions**: Stops for clarifications and confirmations only when necessary

## The Problem It Solves

When using speckit in Claude Code manually:

1. You need to repeatedly type speckit commands (`/speckit.specify`, `/speckit.plan`, etc.)
2. Claude does a few tasks and stops, requiring you to say "continue" constantly
3. No intelligent review of outputs before proceeding to next phase
4. Manual coordination between different workflow phases
5. Loses context between phases

## The Solution

Speckit Driver provides:

1. **Single entry point**: Just invoke the `speckit-driver` skill
2. **Autonomous execution**: Sub-agents execute tasks while main agent orchestrates
3. **Critical review**: Main agent reviews sub-agent outputs before proceeding
4. **Smart pausing**: Stops only when user input is actually needed
5. **Maintained context**: Main agent tracks entire workflow progression

## How It Works

### Architecture

```
User Request
     ↓
Main Agent (Orchestrator)
     ↓
     ├── speckit-constitution (sub-agent) → Creates project principles
     ├── speckit-specify (sub-agent) → Creates feature specs
     ├── speckit-plan (sub-agent) → Generates technical plans
     ├── speckit-tasks (sub-agent) → Breaks down into tasks
     └── speckit-implement (sub-agent) → Executes implementation
```

### Workflow Phases (Enhanced with Quality Gates)

1. **Phase 0 - Constitution** (optional, first-time only)
   - Main agent guides you through defining project principles
   - Invokes `speckit-constitution` sub-agent to create constitution
   - Reviews and confirms with you

2. **Phase 1 - Specification**
   - Main agent asks clarifying questions about your feature
   - Once clear, invokes `speckit-specify` sub-agent
   - Reviews spec quality and handles any clarifications
   - Confirms readiness before proceeding

3. **Phase 1.5 - Clarification** ⭐ NEW (optional but recommended)
   - Invokes `speckit-clarify` sub-agent to identify ambiguities
   - Agent asks up to 5 targeted questions
   - Updates spec with resolved answers
   - **Quality gate**: Prevents downstream rework

4. **Phase 1.6 - Quality Checklist** ⭐ NEW (optional)
   - Invokes `speckit-checklist` sub-agent for requirement validation
   - Generates domain-specific checklists (UX, API, security, etc.)
   - Creates "unit tests for requirements"
   - **Quality gate**: Validates spec completeness and clarity

5. **Phase 2 - Technical Planning**
   - Invokes `speckit-plan` sub-agent
   - **Critical review**: Validates technology choices, architecture, security
   - Flags concerns for your review if needed
   - Confirms plan before proceeding

6. **Phase 3 - Task Breakdown**
   - Invokes `speckit-tasks` sub-agent
   - Reviews task structure and dependencies
   - Presents summary and confirms before analysis

7. **Phase 3.5 - Cross-Artifact Analysis** ⭐ NEW (highly recommended)
   - Invokes `speckit-analyze` sub-agent for consistency check
   - Analyzes spec.md, plan.md, tasks.md alignment
   - Identifies inconsistencies, coverage gaps, constitution violations
   - **Quality gate**: BLOCKS implementation if CRITICAL issues found
   - Reports severity-ranked findings

8. **Phase 4 - Implementation**
   - Invokes `speckit-implement` sub-agent
   - Monitors progress continuously
   - Handles errors and asks for guidance when needed
   - Reports completion and recommends next steps

## Installation

### Prerequisites

- Claude Code CLI installed
- Speckit installed and initialized in your project: `specify init`

### Install the Plugin

1. Clone or download this plugin:

```bash
cd ~/projects
git clone https://github.com/jeffkit/speckit-driver.git
```

2. Add as a local plugin in Claude Code:

```bash
# Create a local marketplace file
mkdir -p ~/.claude/marketplaces
cat > ~/.claude/marketplaces/local.json << 'EOF'
{
  "name": "Local Plugins",
  "plugins": [
    {
      "name": "speckit-driver",
      "version": "1.0.0",
      "path": "~/projects/skills/speckit-driver"
    }
  ]
}
EOF
```

3. In Claude Code, add the marketplace:

```
/plugin marketplace add ~/.claude/marketplaces/local.json
```

4. Install the plugin:

```
/plugin install speckit-driver
```

5. Restart Claude Code to activate the plugin

## Usage

### Starting a New Feature

Simply invoke the skill:

```
User: Use speckit to build a user authentication feature

Claude: I'll help you build this feature using the speckit workflow...
[Checks for constitution, guides through specification, planning, and implementation]
```

### The Main Agent Will:

1. **Check for constitution** - guides you through creation if needed
2. **Ask clarifying questions** - understands your feature thoroughly before starting
3. **Invoke sub-agents** - delegates work to specialists
4. **Review outputs** - validates quality before proceeding
5. **Stop when needed** - asks for your input only when truly necessary
6. **Continue automatically** - progresses workflow when path is clear
7. **Monitor implementation** - tracks progress and handles errors
8. **Recommend next steps** - suggests testing, commits, etc.

### Example Session

```
You: 用speckit开发一个任务管理CLI工具

Claude: 好的！我来帮你使用speckit流程构建任务管理CLI工具。首先让我检查项目宪法...

[没找到宪法]

我没看到项目宪法。在开始构建功能之前，让我们先建立指导所有开发的基本原则。

对于CLI工具，通常的原则包括：
- 易用性：命令应该直观且有良好文档
- 性能：操作应在1秒内完成
- 可靠性：数据永不损坏
- 可移植性：支持Linux、macOS和Windows

你的CLI工具最重要的原则是什么？

---

You: 这些都不错。另外加上：所有数据应该本地存储为JSON格式，工具应该离线工作。

Claude: 完美！让我创建宪法...

[调用speckit-constitution子代理]

✓ 宪法创建成功！你的项目现在有6条核心原则...

现在，让我们定义你的任务管理功能。它应该有什么能力？

---

You: 用户应该能够创建任务、列出它们、标记为完成、删除它们

Claude: 很好的开始！让我问几个问题以明确需求：

1. 任务属性 - 任务应该有：
   - 只有描述？
   - 还是也包括：优先级、截止日期、标签、状态？

2. 组织方式 - 任务应该：
   - 在一个扁平列表中？
   - 还是按项目/分类组织？

[...继续对话直到需求清晰...]

完美！我现在很清楚了。让我创建规范...

[调用speckit-specify子代理]

✓ 规范创建成功！准备好进行技术规划了吗？

---

You: 是的，继续

Claude: 正在创建技术计划...

[调用speckit-plan子代理]

我审核了技术计划。这是建议的方法：

**技术栈**：
- 语言：Node.js（跨平台兼容性）
- CLI框架：Commander.js
- 存储：~/.tasks/目录下的JSON文件

这看起来很稳固，符合你的宪法。我应该继续任务分解吗？

---

[继续整个流程直到实现完成...]

✓ 实现完成！所有32个任务成功执行。

建议的下一步：
1. 测试CLI：`node src/index.js --help`
2. 创建提交
...
```

## Components

### Sub-Agents

1. **speckit-constitution** (`agents/speckit-constitution.md`)
   - Creates/updates project constitutions
   - Manages principles and governance
   - Handles versioning and consistency

2. **speckit-specify** (`agents/speckit-specify.md`)
   - Converts feature descriptions to specifications
   - Handles clarifications and validation
   - Ensures spec quality

3. **speckit-clarify** (`agents/speckit-clarify.md`) ⭐ NEW
   - Identifies ambiguities in specifications
   - Asks targeted clarification questions (max 5)
   - Updates spec with resolved answers
   - Prevents downstream rework

4. **speckit-checklist** (`agents/speckit-checklist.md`) ⭐ NEW
   - Generates quality checklists ("unit tests for requirements")
   - Validates requirement completeness and clarity
   - Domain-specific checklists (UX, API, security, etc.)
   - Tests spec quality, not implementation

5. **speckit-plan** (`agents/speckit-plan.md`)
   - Generates technical implementation plans
   - Researches technology decisions
   - Creates design artifacts (data models, contracts, etc.)

6. **speckit-tasks** (`agents/speckit-tasks.md`)
   - Breaks down plans into actionable tasks
   - Organizes by user stories
   - Identifies parallelization opportunities

7. **speckit-analyze** (`agents/speckit-analyze.md`) ⭐ NEW
   - Cross-artifact consistency analysis (spec/plan/tasks)
   - Identifies inconsistencies and coverage gaps
   - Constitution compliance validation
   - Severity-ranked findings (CRITICAL/HIGH/MEDIUM/LOW)

8. **speckit-implement** (`agents/speckit-implement.md`)
   - Executes implementation phase by phase
   - Tracks progress and marks tasks complete
   - Handles errors and reports status

### Main Skill

**speckit-driver** (`skills/speckit-driver/SKILL.md`)
- Orchestrates the entire workflow
- Delegates to sub-agents
- Reviews outputs critically
- Makes continuation decisions
- Interacts with user appropriately

### Plugin Structure

This plugin follows Claude Code plugin conventions with the following directory layout:

```
speckit-driver/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── agents/                  # Sub-agent definitions (8 total)
│   ├── speckit-constitution.md
│   ├── speckit-specify.md
│   ├── speckit-clarify.md
│   ├── speckit-checklist.md
│   ├── speckit-plan.md
│   ├── speckit-tasks.md
│   ├── speckit-analyze.md
│   └── speckit-implement.md
├── skills/                  # Main orchestrator skill
│   └── speckit-driver/
│       └── SKILL.md
├── CHANGELOG.md
├── INSTALLATION.md
├── LICENSE
├── README.md
└── TASK_MARKING_PROTOCOL.md
```

**Plugin Manifest** (`.claude-plugin/plugin.json`):

The plugin.json file declares all components to Claude Code:

```json
{
  "name": "speckit-driver",
  "version": "1.1.1",
  "description": "Autonomous Spec-Driven Development orchestrator...",
  "agents": "./agents/",      // Points to sub-agents directory
  "skills": "./skills/"        // Points to skills directory
}
```

All sub-agents use YAML frontmatter to declare their configuration:

```yaml
---
name: speckit-constitution
description: Create or update the project constitution
tools: Read, Write, Edit, Bash, Grep, Glob
model: sonnet
---
```

The main skill (`speckit-driver`) coordinates all sub-agents through the Task tool, maintaining workflow state while delegating specialized tasks to the appropriate sub-agent.

## Key Features

### 1. Robust Task Marking System (NEW)

**Four-layer protection** ensures task completion is always tracked:

1. **Sub-agent mandatory workflow**: Tasks MUST be marked [X] immediately after completion
2. **Mandatory output format**: Every completion report must include "Marked: ✓" confirmation
3. **Main agent active monitoring**: Verifies each task marking in real-time
4. **Final audit**: Counts and validates all marks before declaring completion

**Why this matters**:
- Enables reliable resume after interruption
- Prevents duplicate work
- Accurate progress tracking
- Clean state for recovery

See [TASK_MARKING_PROTOCOL.md](TASK_MARKING_PROTOCOL.md) for complete details.

### 2. Intelligent Orchestration

The main agent doesn't just execute commands - it thinks about the workflow:

- Reviews sub-agent outputs for quality
- Makes judgment calls about when to proceed
- Flags concerns for user review
- Maintains context across phases

### 2. Smart User Interaction

Stops to ask user only when:
- Multiple reasonable approaches exist with different trade-offs
- Security or compliance concerns arise
- Scope is expanding beyond original intent
- Errors occur that can't be resolved automatically

Continues automatically when:
- Path forward is clear and unambiguous
- Sub-agent output looks correct
- No concerns or red flags
- Routine progression in workflow

### 3. Critical Review

Before proceeding to next phase, main agent reviews:
- Technology choices and their justification
- Architecture soundness
- Security considerations
- Alignment with project constitution
- Potential issues or concerns

### 4. Comprehensive Discovery

Before creating specifications:
- Asks clarifying questions
- Helps articulate vision clearly
- Discusses scope and boundaries
- Identifies edge cases
- Understands success criteria

### 5. Continuous Monitoring

During implementation:
- Monitors progress after each task/phase
- Handles errors gracefully
- Provides progress updates
- Recommends next steps upon completion

## Configuration

### Customizing Sub-Agents

Sub-agents can be customized by editing their markdown files in `agents/`:

- Adjust tools available
- Change model (sonnet/opus/haiku)
- Modify execution logic
- Add domain-specific guidance

### Customizing the Main Skill

Edit `skills/speckit-driver/SKILL.md` to:

- Adjust orchestration logic
- Change when to stop vs. continue
- Modify review criteria
- Add custom phases

## Comparison with Manual Speckit Usage

| Aspect | Manual Speckit | With Speckit Driver |
|--------|---------------|-------------------|
| Command execution | Manual for each phase | Automatic orchestration |
| Continuation | Constant "continue" prompts | Autonomous progression |
| Quality review | Manual review | Automatic critical review |
| User interaction | Frequent interruptions | Smart, minimal interruptions |
| Context maintenance | Loses context between commands | Maintains full context |
| Error handling | Manual intervention | Intelligent error handling |
| Progress tracking | Manual tracking | Automatic monitoring |

## Best Practices

1. **Let it run**: Trust the autonomous execution - it will stop when it needs your input
2. **Answer thoroughly**: When asked questions, provide complete context to minimize follow-ups
3. **Review critically**: When agent flags concerns, take time to review and decide
4. **Start simple**: Begin with smaller features to understand the workflow
5. **Iterate**: Use the workflow multiple times to build complex systems incrementally

## Troubleshooting

### Plugin not loading

- Verify plugin path in marketplace.json
- Restart Claude Code after installation
- Check ~/.claude/logs for errors

### Sub-agents not found

- Ensure all agent files are in `agents/` directory
- Check agent file names match exactly (e.g., `speckit-constitution.md`)
- Verify YAML frontmatter is correct

### Workflow stuck

- Check if speckit is properly initialized: `specify init`
- Verify `.specify/` directory exists with templates
- Check for error messages in agent outputs

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Credits

- Built on [speckit](https://github.com/github/spec-kit) by GitHub
- Designed for [Claude Code](https://claude.com/code)
- Created by [jeffkit](https://github.com/jeffkit)

## Support

- Issues: https://github.com/jeffkit/speckit-driver/issues
- Discussions: https://github.com/jeffkit/speckit-driver/discussions
- Speckit docs: https://github.com/github/spec-kit

## Version History

### 1.0.0 (Initial Release)

- Complete autonomous orchestration
- Five specialized sub-agents
- Intelligent workflow progression
- Critical review and validation
- Smart user interaction
- Comprehensive error handling
