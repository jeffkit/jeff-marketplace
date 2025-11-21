# Changelog

All notable changes to the Speckit Driver plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2024-11-20

### Added

#### Task Marking Protection System (CRITICAL QUALITY IMPROVEMENT)

- **Four-layer protection** to ensure task completion tracking integrity
  - Layer 1: Sub-agent mandatory workflow (mark BEFORE next task)
  - Layer 2: Mandatory output format (must include "Marked: ✓")
  - Layer 3: Main agent active monitoring (verify each task)
  - Layer 4: Final audit (count and validate before completion)

- **New documentation**: TASK_MARKING_PROTOCOL.md
  - Complete protocol specification
  - Failure mode analysis
  - Recovery scenarios
  - Testing guidelines
  - Best practices for sub-agent and main agent

### Changed

- **speckit-implement sub-agent**: Enhanced with mandatory task marking workflow
  - Added critical rule: Mark [X] IMMEDIATELY after task completion
  - Added verification step after marking
  - Added structured output format requiring "Marked: ✓" confirmation
  - Added periodic status table with marking column

- **Main orchestrator skill**: Enhanced Phase 4 with active monitoring
  - Added per-task marking verification
  - Added periodic audit (every 5-10 tasks)
  - Added final audit before completion with bash grep counting
  - Added intervention protocol for missing marks

- **README**: Added task marking system as first key feature
  - Highlights importance for resume/recovery
  - Links to detailed protocol document

### Fixed

- **Task marking omission issue**: Previously tasks could be completed without [X] marks
  - Now enforced at 4 different levels
  - Sub-agent cannot proceed without marking
  - Main agent actively verifies and intervenes
  - Final state always audited

### Technical Improvements

- Robust progress tracking enables reliable workflow resume
- Prevents duplicate work on interruption and restart
- Accurate state representation in tasks.md
- Clean audit trail in conversation logs

## [1.1.0] - 2024-11-20

### Added

#### New Sub-Agents (Quality Gates)

- **speckit-clarify** sub-agent for specification ambiguity resolution
  - Systematic scan using structured taxonomy
  - Up to 5 targeted clarification questions
  - Direct spec updates with resolved answers
  - Prevents downstream rework by catching issues early

- **speckit-checklist** sub-agent for requirements quality validation
  - Generates "unit tests for requirements"
  - Domain-specific checklists (UX, API, security, performance, accessibility)
  - Validates requirement completeness, clarity, consistency
  - 20-30 quality-focused items per checklist
  - Tests spec quality, not implementation

- **speckit-analyze** sub-agent for cross-artifact consistency
  - Read-only analysis of spec.md, plan.md, tasks.md
  - Identifies inconsistencies, duplications, ambiguities
  - Constitution compliance validation
  - Coverage gap detection
  - Severity-ranked findings (CRITICAL/HIGH/MEDIUM/LOW)
  - Blocks implementation if CRITICAL issues found

#### Enhanced Workflow

- **Phase 1.5 - Clarification**: Optional but recommended phase between specify and plan
- **Phase 1.6 - Quality Checklist**: Optional phase for requirement validation
- **Phase 3.5 - Cross-Artifact Analysis**: Highly recommended quality gate before implementation

#### Updated Documentation

- README updated with 3 new sub-agents and enhanced workflow
- Main orchestrator skill updated to v1.1.0 with integration logic
- New workflow includes 8 phases (was 5) with 3 quality gates

### Changed

- Main skill version bumped to 1.1.0
- Workflow description now includes quality gates
- Sub-agent count increased from 5 to 8

### Technical Improvements

- Enhanced spec-driven workflow with systematic quality validation
- Earlier detection of issues (clarify phase vs. during implementation)
- Requirement quality validation before technical decisions
- Cross-artifact consistency ensures alignment before coding

## [1.0.0] - 2024-11-20

### Added

#### Core Infrastructure
- Initial release of Speckit Driver plugin for Claude Code
- Plugin manifest (`.claude-plugin/plugin.json`) with metadata
- Complete directory structure for Claude Code plugin

#### Sub-Agents
- **speckit-constitution** sub-agent for creating/updating project constitutions
  - Placeholder replacement and validation
  - Semantic versioning support
  - Consistency propagation across templates
  - Sync impact reporting
- **speckit-specify** sub-agent for creating feature specifications
  - Natural language to spec conversion
  - Branch naming and management
  - Quality validation with checklist generation
  - Interactive clarification workflow
  - Maximum 3 clarification limit with informed defaults
- **speckit-plan** sub-agent for technical implementation planning
  - Technology stack research and selection
  - Architecture design and patterns
  - Data model generation
  - API contract generation
  - Constitution compliance validation
  - Research documentation
- **speckit-tasks** sub-agent for task breakdown
  - User story-based task organization
  - Dependency analysis and ordering
  - Parallel execution opportunity identification
  - Strict checklist format enforcement
  - MVP scope recommendation
- **speckit-implement** sub-agent for implementation execution
  - Phase-by-phase task execution
  - Progress tracking with task marking
  - Checklist validation before implementation
  - Error handling and recovery
  - Ignore file generation for detected technologies

#### Main Orchestrator Skill
- **speckit-driver** skill for autonomous workflow orchestration
  - Five-phase workflow management (constitution → specify → plan → tasks → implement)
  - Intelligent sub-agent delegation via Task tool
  - Critical review and validation of sub-agent outputs
  - Smart user interaction (stops only when necessary)
  - Decision framework for continuation vs. user consultation
  - Progress monitoring and error handling
  - Context maintenance across workflow phases
  - Comprehensive example interactions and workflows

#### Documentation
- Comprehensive README with:
  - Problem statement and solution overview
  - Architecture and workflow diagrams
  - Complete usage examples
  - Component descriptions
  - Comparison with manual speckit usage
  - Best practices and troubleshooting
- Detailed INSTALLATION guide covering:
  - Prerequisites and setup
  - Multiple installation methods
  - Verification steps
  - Configuration options
  - Troubleshooting common issues
  - Advanced customization
- MIT License
- This CHANGELOG

#### Features
- **Autonomous Orchestration**: Main agent acts as project manager, delegating to specialized sub-agents
- **Continuous Workflow**: Executes complete workflows without constant user prompting
- **Critical Review**: Reviews sub-agent outputs before proceeding to next phase
- **Smart Pausing**: Stops for user input only when truly necessary
- **Informed Decision-Making**: Uses decision framework to determine when to continue vs. ask
- **Comprehensive Discovery**: Engages in thorough requirement gathering before specification
- **Constitution Validation**: Ensures all technical decisions align with project principles
- **Quality Assurance**: Validates specifications, plans, and tasks before implementation
- **Progress Tracking**: Marks tasks as complete and provides continuous updates
- **Error Recovery**: Handles errors gracefully with clear diagnostics and options

#### Integration
- Full integration with speckit slash commands from GitHub's spec-kit
- Compatible with existing speckit projects
- Works with speckit scripts (create-new-feature.sh, setup-plan.sh, etc.)
- Respects speckit templates and directory structure

### Technical Details

#### Sub-Agent Configuration
- All sub-agents use Sonnet model by default
- Configurable tool access per sub-agent
- YAML frontmatter for agent metadata
- Comprehensive system prompts for each agent

#### Main Skill Configuration
- Trigger phrases in multiple languages (English and Chinese)
- Detailed orchestration logic
- Example interactions for each workflow phase
- Error handling examples
- Decision framework documentation

#### File Structure
```
speckit-driver/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── agents/
│   ├── speckit-constitution.md
│   ├── speckit-specify.md
│   ├── speckit-plan.md
│   ├── speckit-tasks.md
│   └── speckit-implement.md
├── skills/
│   └── speckit-driver/
│       └── SKILL.md          # Main orchestrator skill
├── .gitignore
├── CHANGELOG.md
├── INSTALLATION.md
├── LICENSE
└── README.md
```

### Known Limitations

1. Sub-agents cannot directly call slash commands (by design - use speckit scripts instead)
2. Requires speckit to be initialized in project (`.specify/` directory must exist)
3. Main skill invocations require Task tool (sub-agents are not directly callable by users)
4. First-time constitution creation requires user interaction (cannot be fully automated)

### Compatibility

- Claude Code: Latest version
- Speckit: Compatible with spec-kit from GitHub
- Platform: macOS, Linux (Windows support via WSL)
- Git: Required for branch management

### Notes

This is the initial release, establishing the foundation for autonomous spec-driven development in Claude Code. Future releases will add enhancements based on user feedback and evolving speckit capabilities.

## [Unreleased]

### Planned Features for Future Releases

- Resume capability for paused workflows
- Workflow templates for common project types
- Custom phase injection points
- Integration with CI/CD systems
- Multi-feature parallel development support
- Analytics and metrics tracking
- Interactive workflow visualization
- Workflow dry-run mode
- Custom sub-agent creation wizard

---

## Version History Summary

- **1.0.0** (2024-11-20) - Initial release with complete autonomous orchestration

[1.0.0]: https://github.com/jeffkit/speckit-driver/releases/tag/v1.0.0
[Unreleased]: https://github.com/jeffkit/speckit-driver/compare/v1.0.0...HEAD
