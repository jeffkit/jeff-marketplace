# Jeff Marketplace

[中文文档](README_CN.md)

A collection of plugins for Jeff's workflow, designed to enhance Claude Code with personal assistance and autonomous development capabilities.


## Installation with Agent Studio

[Agent Studio](https://github.com/okguitar/agentstudio)

![Agent Studio Installation](docs/images/agentstudio-en.png)

## Installation with Claude Code CLI

### Quick Install

1. **Start Claude Code CLI**:
   ```bash
   claude
   ```

2. **Add this marketplace**:
   ```bash
   /plugin marketplace add https://github.com/jeffkit/jeff-marketplace.git
   ```

3. **Install plugins**:
   ```bash
   # Install the Assistant plugin for personal productivity
   /plugin install assistant@jeff-choices

   # Install the Speckit Driver plugin for autonomous development
   /plugin install speckit-driver@jeff-choices

   # Install the Nano-PPT plugin for AI-powered presentation creation
   /plugin install nano-ppt@jeff-choices

   # Browse available plugins and install interactively
   /plugin

   ```

### Usage Examples

After installation, you can use the plugins directly in your Claude conversations:

```bash
# Assistant plugin usage
"Help me record to complete the project report, high priority, due this Friday"

"Show me my TODO items"

"Write a journal entry about today's learning"

# Speckit Driver plugin usage
"Use speckit to develop a user login feature"

"Build an API service using speckit"

# Nano-PPT plugin usage
"Create a presentation about quarterly business results"

"Make a PowerPoint for the project proposal"

"Generate slides for the team meeting"
```

## Plugins

### 1. Assistant

**Version:** 2.2.0
**Description:** Personal assistant for managing TODOs and journal entries, supporting task tracking, activity logging, and smart querying through natural conversation. Enhanced with project-oriented features for better task organization.

#### Skills

- **assistant**: The core skill that transforms Claude into a personal assistant.
    - **Capabilities**:
        - **Enhanced TODO Management**: Track tasks with priority, category, status, due dates, project, assignee, tags, and description.
        - **Journal Management**: Record daily activities with mood and tags.
        - **Interactive Clarification**: Asks questions to ensure data accuracy.
        - **Smart Querying**: Filter and search tasks and journals by multiple dimensions.
        - **Project-Oriented**: Organize tasks by project, assign to people, and tag for better management.
    - **Triggers**: "记录一下" (Record this), "添加TODO" (Add TODO), "写个日志" (Write a journal), "查看我的任务" (Check my tasks).
    - **Data Storage**: All data is stored in `.assistant/` directory (automatically created).

#### Migration from v2.0.x

If you're upgrading from a previous version that stored data in the project root, use the migration script:

```bash
python3 assistant/skills/assistant/scripts/migrate_data.py
```

This will move your `todos.json` and `journals.json` files to `.assistant/` directory.

---

### 2. Speckit Driver

**Version:** 1.1.1  
**Description:** Autonomous Spec-Driven Development orchestrator that enables intelligent, continuous workflow execution with minimal user intervention.

#### Skills

- **speckit-driver**: The main orchestrator skill that manages the entire development workflow. It coordinates sub-agents to execute tasks from constitution to implementation.

#### Agents

This plugin utilizes a suite of specialized sub-agents:

- **speckit-constitution**: Creates and manages project principles and governance.
- **speckit-specify**: Converts feature descriptions into detailed specifications.
- **speckit-clarify**: Identifies ambiguities in specifications and asks targeted questions.
- **speckit-checklist**: Generates quality checklists and "unit tests for requirements".
- **speckit-plan**: Generates technical implementation plans and researches technology decisions.
- **speckit-tasks**: Breaks down plans into actionable tasks and user stories.
- **speckit-analyze**: Performs cross-artifact consistency analysis (spec/plan/tasks) to ensure alignment.
- **speckit-implement**: Executes the implementation phase, monitoring progress and handling errors.

---

### 3. Nano-PPT

**Version:** 1.0.0
**Description:** AI-powered presentation creator that generates professional PowerPoint slides using Google's Gemini AI model for image generation.

#### Prerequisites

Before using this plugin, you need to set up the following:

- **Google GenAI API Key**: Set the `GEMINI_API_KEY` environment variable
- **Python Dependencies**: Install required packages with `pip install -r nano-ppt/requirements.txt`

```bash
# Install dependencies
cd nano-ppt
pip install -r requirements.txt

# Set your API key
export GEMINI_API_KEY="your-google-ai-api-key"
```

#### Skills

- **nano-ppt**: The main orchestrator skill that manages the 4-phase presentation creation workflow.
    - **Capabilities**:
        - **Requirements Gathering**: Interactive Q&A session to understand presentation needs
        - **Structured Workflow**: 4-phase process (Requirements → Brief Outline → Detailed Outline → Generation)
        - **Visual Consistency**: Uses reference images to maintain style across slides
        - **User Approval Gates**: Requires user approval before each phase transition
        - **Sequential Generation**: Creates slides in order to ensure coherence
    - **Triggers**: "Create a presentation", "Make a PowerPoint", "Generate slides", "创建PPT", "制作演示文稿"
    - **Output**: Generated slides are saved to `./ppt-output/[presentation-name]/` directory

#### Agents

This plugin utilizes a suite of specialized sub-agents:

- **nanoppt-requirements**: Conducts conversational interviews to gather presentation requirements.
- **nanoppt-brief-outline**: Creates high-level slide structure with titles, main ideas, and transitions.
- **nanoppt-detailed-outline**: Expands to production-ready specifications with complete content and visual requirements.
- **nanoppt-slide-generator**: Generates individual slides as images using Google Gemini AI.

#### Workflow Phases

1. **Requirements Gathering**: Interactive Q&A to understand presentation goals, audience, and style preferences
2. **Brief Outline**: High-level slide structure with narrative flow and key messages
3. **Detailed Outline**: Complete content specifications including text, visual elements, and styling requirements
4. **Slide Generation**: Sequential image generation using Google Gemini with visual consistency across slides
