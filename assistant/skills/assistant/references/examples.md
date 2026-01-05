# Usage Examples

Detailed usage examples showing how the assistant skill works in different scenarios.

## Table of Contents

1. [Basic TODO Management](#basic-todo-management)
2. [Enhanced TODO with Project Management](#enhanced-todo-with-project-management)
3. [Journal Management](#journal-management)
4. [Advanced Querying](#advanced-querying)
5. [Complete Workflow Examples](#complete-workflow-examples)

---

## Basic TODO Management

### Simple Task Recording (Backward Compatible)

**Scenario:** User wants to record a simple life task.

```
User: 帮我记录要买菜
Claude: 好的，这是生活类的待办事项吗？需要设置优先级或截止时间吗？
User: 就是普通的生活任务，优先级中等
Claude: [Executes: python3 scripts/todo_manager.py add "买菜" --category life --priority medium]

已记录：
- 任务：买菜
- 分类：生活
- 优先级：中等
- 状态：待办
```

### Quick Work Task

**Scenario:** Recording a work task with deadline.

```
User: 记录一下周五前要完成项目报告
Claude: 好的，这是工作任务吗？优先级如何？
User: 是的，高优先级
Claude: [Executes: python3 scripts/todo_manager.py add "完成项目报告" --category work --priority high --due-date 2025-11-22]

已记录：
- 任务：完成项目报告
- 分类：工作
- 优先级：高
- 截止日期：2025-11-22
- 状态：待办
```

### Listing Pending Tasks

**Scenario:** Check what needs to be done.

```
User: 看看我有什么待办事项
Claude: [Executes: python3 scripts/todo_manager.py list --status pending]

您有以下待办事项：
1. 买菜 (生活/中等)
2. 完成项目报告 (工作/高/截止：2025-11-22)
```

### Marking Task as Completed

**Scenario:** Finish a task.

```
User: 买菜完成了
Claude: [Searches for "买菜", finds ID 1]
       [Executes: python3 scripts/todo_manager.py update 1 --status completed]

已将"买菜"标记为已完成！
```

---

## Enhanced TODO with Project Management

### Recording Project Task with Full Details

**Scenario:** Developer needs to track a technical task.

```
User: 我们需要修复用户登录的bug
Claude: 好的，我来记录这个技术任务。请问：
- 这个任务属于哪个项目？
- 需要分配给谁处理？
- 优先级如何？有什么标签要添加吗？（比如backend, urgent, bug-fix）

User: jeff-marketplace项目，分配给alice，高优先级，添加backend和urgent标签
Claude: 有什么具体要求或详细说明吗？
User: 修复用户登录时的500错误，可能是session问题
Claude: [Executes: python3 scripts/todo_manager.py add "修复用户登录bug" \
         --category work --priority high \
         --project jeff-marketplace --assignee alice \
         --tags backend,urgent,bug-fix \
         --description "修复用户登录时的500错误，可能是session问题"]

已记录：
- 任务：修复用户登录bug
- 项目：jeff-marketplace
- 分配给：alice
- 分类：工作
- 优先级：高
- 标签：backend, urgent, bug-fix
- 描述：修复用户登录时的500错误，可能是session问题
- 状态：待办
```

### Viewing Project Tasks

**Scenario:** Check all tasks in a specific project.

```
User: 看看jeff-marketplace项目的所有任务
Claude: [Executes: python3 scripts/todo_manager.py list --project jeff-marketplace]

jeff-marketplace项目有以下任务：

待办 (2):
1. 修复用户登录bug (alice/高优先级/backend, urgent, bug-fix)
2. 实现邮箱验证功能 (jeff/中等优先级/backend, feature)

进行中 (1):
3. 优化数据库查询 (bob/高优先级/backend, performance)

已完成 (3):
4. 搭建项目框架 (jeff/完成于 2025-11-15)
5. 配置CI/CD (alice/完成于 2025-11-18)
...
```

### Filtering by Assignee

**Scenario:** Check what's assigned to a specific person.

```
User: 有哪些分配给alice的高优先级工作？
Claude: [Executes: python3 scripts/todo_manager.py list --assignee alice --priority high --category work]

alice负责的高优先级工作任务：
1. 修复用户登录bug (jeff-marketplace/backend, urgent, bug-fix)
2. 升级依赖包到最新版本 (internal-tools/maintenance, urgent)
```

### Updating Task Status and Details

**Scenario:** Mark task as in progress and add notes.

```
User: 把用户认证功能的开发标记为进行中
Claude: [Searches for "用户认证功能", finds ID 7]
       [Executes: python3 scripts/todo_manager.py update 7 --status in_progress]

已将"用户认证功能"标记为进行中！

需要更新其他信息吗？比如优先级、分配人员或标签？
```

---

## Journal Management

### Simple Daily Log

**Scenario:** Recording a simple life event.

```
User: 记录一下今天天气很好，去公园散步了
Claude: 好的，这是生活类的记录吗？心情如何？
User: 是的，心情很开心
Claude: [Executes: python3 scripts/journal_manager.py add "今天天气很好，去公园散步了" --category life --mood happy]

已记录日志：
- 内容：今天天气很好，去公园散步了
- 分类：生活
- 心情：开心
- 时间：2025-11-20 16:30
```

### Study Journal with Tags

**Scenario:** Recording learning progress.

```
User: 写个日志，今天学习了Python装饰器的原理，理解了闭包和高阶函数
Claude: 这是学习类的记录吗？心情如何？需要添加标签吗？
User: 是学习记录，心情motivated，添加python和decorators标签
Claude: [Executes: python3 scripts/journal_manager.py add "今天学习了Python装饰器的原理，理解了闭包和高阶函数" \
         --category study --mood motivated --tags python,decorators,learning]

已记录学习日志：
- 内容：今天学习了Python装饰器的原理，理解了闭包和高阶函数
- 分类：学习
- 心情：充满动力
- 标签：python, decorators, learning
- 时间：2025-11-20 20:30
```

### Work Achievement Log

**Scenario:** Recording work accomplishment.

```
User: 记录一下完成了用户认证模块的开发，所有测试通过
Claude: 这是工作成就吗？心情如何？
User: 是成就，很excited
Claude: [Executes: python3 scripts/journal_manager.py add "完成了用户认证模块的开发，所有测试通过" \
         --category achievement --mood excited --tags work,milestone,backend]

已记录成就：
- 内容：完成了用户认证模块的开发，所有测试通过
- 分类：成就
- 心情：兴奋
- 标签：work, milestone, backend
- 时间：2025-11-20 18:00
```

### Viewing Recent Journals

**Scenario:** Review last week's journals.

```
User: 看看本周的日志
Claude: [Executes: python3 scripts/journal_manager.py list --start-date 2025-11-18 --end-date 2025-11-24]

本周日志（2025-11-18 至 2025-11-24）：

2025-11-20 20:30 [学习/充满动力]
今天学习了Python装饰器的原理，理解了闭包和高阶函数
标签：python, decorators, learning

2025-11-20 18:00 [成就/兴奋]
完成了用户认证模块的开发，所有测试通过
标签：work, milestone, backend

2025-11-20 16:30 [生活/开心]
今天天气很好，去公园散步了

...共 5 条记录
```

---

## Advanced Querying

### Multi-criteria TODO Filtering

**Scenario:** Find specific subset of tasks.

```
User: 显示所有urgent标签的后端任务
Claude: [Executes: python3 scripts/todo_manager.py list --tags urgent,backend]

找到以下urgent标签的后端任务：
1. 修复用户登录bug (jeff-marketplace/alice/高优先级)
2. 升级依赖包 (internal-tools/alice/高优先级)
3. 数据库迁移脚本 (data-platform/bob/中等优先级)
```

### Complex Project Query

**Scenario:** Find high-priority backend tasks in a project.

```
User: jeff-marketplace项目里有哪些高优先级的后端任务？
Claude: [Executes: python3 scripts/todo_manager.py list --project jeff-marketplace --priority high --tags backend]

jeff-marketplace项目的高优先级后端任务：
1. 修复用户登录bug (alice/backend, urgent, bug-fix)
2. 优化数据库查询 (bob/backend, performance/进行中)
```

### Searching Across All Data

**Scenario:** Find all items related to a keyword.

```
User: 搜索所有跟"认证"相关的任务
Claude: [Executes: python3 scripts/todo_manager.py search "认证"]

找到 3 个相关任务：
1. 修复用户认证bug (jeff-marketplace/待办)
2. 实现邮箱认证功能 (jeff-marketplace/待办)
3. 添加双因素认证 (security-project/已完成)
```

### Mood-based Journal Query

**Scenario:** Review entries with specific mood.

```
User: 看看我什么时候心情最motivated
Claude: [Executes: python3 scripts/journal_manager.py list --mood motivated]

您心情充满动力的时候：

2025-11-20 20:30 [学习]
今天学习了Python装饰器的原理...

2025-11-18 14:00 [工作]
完成了重要的代码重构...

...共 8 条记录
```

---

## Complete Workflow Examples

### Full Project Task Lifecycle

```
# Day 1: Create task
User: 我们需要开发一个新的支付模块
Claude: [Collects details: project=payment-system, assignee=jeff, priority=high, tags=backend,payment,feature]
       [Creates TODO]

# Day 3: Start working
User: 开始做支付模块了
Claude: [Finds task, updates status to in_progress]

# Day 5: Reassign
User: 把支付模块转给alice负责
Claude: [Updates assignee to alice]

# Day 7: Priority change
User: 支付模块需要加急
Claude: [Updates priority to high, adds "urgent" tag]

# Day 10: Complete
User: 支付模块完成了
Claude: [Updates status to completed]
       需要记录这个成就到日志吗？
User: 好的
Claude: [Creates achievement journal entry]
```

### Weekly Review Workflow

```
User: 帮我总结一下本周的工作
Claude: [Executes multiple queries]

本周工作总结（2025-11-18 至 2025-11-24）：

✅ 已完成任务 (5):
- 用户认证模块 (jeff-marketplace)
- 数据库优化 (jeff-marketplace)
- CI/CD配置 (internal-tools)
- 文档更新 (documentation)
- Bug修复 #123 (bug-tracker)

🔄 进行中任务 (3):
- 支付模块开发 (payment-system/alice)
- API重构 (backend-api/bob)
- 性能监控 (monitoring/jeff)

📝 新增任务 (4):
- 邮箱验证功能 (jeff-marketplace)
- 用户反馈系统 (feedback-system)
- ...

📖 学习记录 (2):
- Python装饰器学习
- Docker最佳实践

🎉 成就记录 (3):
- 完成用户认证模块
- 通过代码审查
- ...
```

### Tag-based Organization

```
User: 显示所有urgent任务，按项目分组
Claude: [Executes: python3 scripts/todo_manager.py list --tags urgent]
       [Groups results by project]

紧急任务分组：

jeff-marketplace (2):
- 修复用户登录bug (alice/高优先级)
- 数据库迁移 (bob/中等优先级)

payment-system (1):
- 支付接口集成测试 (jeff/高优先级)

internal-tools (1):
- 依赖包升级 (alice/高优先级)

总计 4 个紧急任务
```

---

## Tips for Effective Use

### For Users

1. **Be specific about projects**: Always mention project names for work tasks
2. **Use tags consistently**: Establish a tagging convention (e.g., "backend", "urgent", "bug-fix")
3. **Regular reviews**: Use weekly queries to review progress
4. **Descriptive titles**: Make task titles clear and actionable
5. **Update promptly**: Mark tasks as in_progress or completed when status changes

### For Claude

1. **Always clarify**: Don't guess category, priority, or project
2. **Suggest tags**: Based on context, recommend relevant tags
3. **Group results**: When listing many items, group by project or category
4. **Highlight urgency**: Call out high-priority or overdue items
5. **Proactive reminders**: Suggest reviewing upcoming deadlines
6. **Natural language**: Present data conversationally, not as raw JSON
