# Jeff Marketplace

[English Documentation](README.md)

Jeff 工作流的插件集合，旨在通过个人助手和自主开发能力增强 Claude Code。

## 插件列表

### 1. Assistant (个人助手)

**版本:** 2.1.0
**描述:** 用于管理 TODO 和日志条目的个人助手，支持通过自然对话进行任务跟踪、活动记录和智能查询。

#### 技能 (Skills)

- **assistant**: 将 Claude 转变为个人助手的核心技能。
    - **功能**:
        - **TODO 管理**: 跟踪具有优先级、分类、状态和截止日期的任务。
        - **日志管理**: 记录带有心情和标签的日常活动。
        - **交互式澄清**: 提问以确保数据准确性。
        - **智能查询**: 筛选和搜索任务及日志。
    - **触发词**: "记录一下", "添加TODO", "写个日志", "查看我的任务"。
    - **数据存储**: 所有数据存储在 `.assistant/` 目录下（自动创建）。

#### 从 v2.0.x 版本迁移

如果你从之前在项目根目录存储数据的版本升级，请使用迁移脚本：

```bash
python3 assistant/skills/assistant/scripts/migrate_data.py
```

这将把你的 `todos.json` 和 `journals.json` 文件移动到 `.assistant/` 目录。

---

### 2. Speckit Driver (Speckit 驱动器)

**版本:** 1.1.1  
**描述:** 自主 Spec 驱动开发 (SDD) 编排器，能够以最少的用户干预实现智能、连续的工作流执行。

#### 技能 (Skills)

- **speckit-driver**: 主要的编排技能，管理整个开发工作流。它协调子 Agent 从宪法到实现执行各项任务。

#### 代理 (Agents)

该插件使用一套专门的子 Agent：

- **speckit-constitution**: 创建和管理项目原则与治理。
- **speckit-specify**: 将功能描述转换为详细的规范。
- **speckit-clarify**: 识别规范中的歧义并提出针对性问题。
- **speckit-checklist**: 生成质量检查清单和“需求单元测试”。
- **speckit-plan**: 生成技术实施计划并研究技术决策。
- **speckit-tasks**: 将计划分解为可执行的任务和用户故事。
- **speckit-analyze**: 执行跨工件一致性分析 (spec/plan/tasks) 以确保对齐。
- **speckit-implement**: 执行实施阶段，监控进度并处理错误。
