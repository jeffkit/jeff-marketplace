# Speckit Driver Usage Examples

Real-world examples demonstrating how to use the Speckit Driver plugin for various scenarios.

## Table of Contents

- [Example 1: Building a CLI Tool from Scratch](#example-1-building-a-cli-tool-from-scratch)
- [Example 2: Adding a Feature to Existing Project](#example-2-adding-a-feature-to-existing-project)
- [Example 3: Web Application Feature](#example-3-web-application-feature)
- [Example 4: Handling Clarifications](#example-4-handling-clarifications)
- [Example 5: Reviewing Technical Plans](#example-5-reviewing-technical-plans)

---

## Example 1: Building a CLI Tool from Scratch

### Scenario
You want to build a new command-line tool for managing your development environment configurations.

### Conversation

```
You: Use speckit to build a CLI tool for managing dev environment configs

Claude: I'll help you build this CLI tool using the speckit workflow. Let me start by checking if we have a project constitution...

[Checks for .specify/memory/constitution.md - not found]

I don't see an existing project constitution. Let's establish the foundational principles first.

For a CLI tool, here are some typical important principles:

1. **Usability**: Commands should be intuitive with comprehensive help
2. **Performance**: Operations should complete in under 1 second
3. **Reliability**: Configuration data should never be corrupted
4. **Portability**: Should work on Linux, macOS, and Windows
5. **Security**: Sensitive data (API keys, tokens) must be encrypted

What are the most important principles for your configuration management CLI? Any specific requirements or constraints?

---

You: Those all look good. Add one more: the tool should store configs in a standard location (~/.devconfig/) and support version control integration.

Claude: Perfect! Let me create the constitution with these 6 principles...

[Invokes speckit-constitution sub-agent]

✓ Constitution created successfully at .specify/memory/constitution.md

**Your Project Principles**:
1. Usability - Intuitive commands with comprehensive help
2. Performance - Sub-second operation completion
3. Reliability - Data integrity guarantees
4. Portability - Cross-platform support (Linux, macOS, Windows)
5. Security - Encrypted storage for sensitive data
6. Standard Storage - Configs in ~/.devconfig/ with git integration

Now, let's define your configuration management feature in detail. What specific capabilities should the tool have?

---

You: Users should be able to:
- Set config values (name=value)
- Get config values
- List all configs
- Delete configs
- Import/export configs to JSON
- Support different environments (dev, staging, prod)

Claude: Great! Let me ask a few clarifying questions to ensure we build exactly what you need:

**1. Configuration Organization**
   - Should configs be flat (all in one namespace)?
   - Or hierarchical (e.g., database.host, api.key)?
   - Or grouped by environment?

**2. Sensitive Data Handling**
   - How should the tool identify what needs encryption?
   - Auto-detect by key name (containing "password", "token", "key")?
   - Or explicit marking when setting values?

**3. Environment Switching**
   - Should there be an "active environment" concept?
   - Or always specify environment per command?

**4. Import/Export Scope**
   - Export all environments or just one?
   - Should export include encrypted values (with warning)?

---

You:
1. Hierarchical with dot notation (database.host)
2. Auto-detect by key name patterns
3. Active environment with ability to override per command
4. Export one environment at a time, encrypted values as [ENCRYPTED] placeholder

Claude: Perfect! I now have a clear picture. Let me create the specification...

[Invokes speckit-specify sub-agent]

[Sub-agent creates spec, validates, generates checklist]

✓ Specification created successfully!

**Feature**: Dev Environment Configuration Manager
**Branch**: 1-devconfig-manager
**Spec File**: specs/1-devconfig-manager/spec.md

**User Stories Created**:
- US1 (P1): Set and get configuration values with dot notation
- US2 (P1): List configurations with filtering
- US3 (P1): Delete configuration values
- US4 (P2): Environment management (create, switch, list)
- US5 (P2): Import/export configurations as JSON
- US6 (P3): Automatic encryption for sensitive values

**Validation Results**: ✓ All quality checks passed
- No implementation details in spec
- All requirements testable
- Success criteria measurable
- Edge cases identified

Should I proceed to technical planning?

---

You: Yes

Claude: Creating technical plan...

[Invokes speckit-plan sub-agent]

[Sub-agent researches, generates plan, creates design artifacts]

I've reviewed the technical plan. Here's the proposed approach:

**Technology Stack**:
- Language: **Node.js** (excellent cross-platform support, mature crypto libraries)
- CLI Framework: **Commander.js** (popular, well-maintained, intuitive API)
- Storage: **JSON files** in ~/.devconfig/ directory
- Encryption: **Node crypto module** with AES-256-GCM
- Config Format: **Hierarchical JSON** with environment separation

**Architecture**:
```
src/
├── commands/         # CLI command handlers
├── services/
│   ├── config-service.js    # Config CRUD operations
│   ├── crypto-service.js    # Encryption/decryption
│   └── env-service.js       # Environment management
├── storage/
│   └── json-store.js        # File I/O operations
└── models/
    └── config.js            # Config validation
```

**Key Design Decisions**:

1. **Storage Structure**:
   ```
   ~/.devconfig/
   ├── environments.json        # Active env + env list
   ├── dev/
   │   └── config.json         # Dev configs
   ├── staging/
   │   └── config.json
   └── prod/
       └── config.json
   ```

2. **Encryption Strategy**:
   - Master key stored in OS keychain (macOS/Linux) or credential manager (Windows)
   - Per-environment encryption salt
   - Auto-detect patterns: `*password*`, `*token*`, `*key*`, `*secret*`

3. **Git Integration**:
   - Auto-init git repo in ~/.devconfig/
   - Auto-commit on changes
   - .gitignore for master key

**Constitution Compliance**: ✓ All principles satisfied
- Usability: Intuitive commands (devconfig set, get, list, etc.)
- Performance: In-memory operations, file I/O < 100ms
- Reliability: Atomic writes, backup before modifications
- Portability: Cross-platform paths, platform-specific keychain
- Security: AES-256-GCM encryption for sensitive data
- Standard Storage: ~/.devconfig/ with git auto-init

**Generated Artifacts**:
- specs/1-devconfig-manager/research.md (Technology decisions)
- specs/1-devconfig-manager/data-model.md (Config entity structure)
- specs/1-devconfig-manager/quickstart.md (Setup and usage examples)

This plan looks solid. Ready to proceed to task breakdown?

---

You: Yes, go ahead

Claude: Generating task breakdown...

[Invokes speckit-tasks sub-agent]

✓ Task breakdown complete!

**Summary**:
- **Total Tasks**: 52 tasks across 8 phases
- **Estimated Duration**: ~4-6 hours for full implementation

**Phase Breakdown**:

1. **Phase 1 - Setup** (8 tasks)
   - Initialize Node.js project
   - Install dependencies
   - Set up project structure
   - Configure linting and formatting

2. **Phase 2 - Foundation** (6 tasks)
   - Implement JSON storage layer
   - Create config model with validation
   - Set up error handling
   - Create utility functions

3. **Phase 3 - US1: Set/Get Configs** (9 tasks)
   - Implement config service (CRUD)
   - Create CLI commands (set, get)
   - Add dot notation parsing
   - Handle nested config paths

4. **Phase 4 - US2: List Configs** (5 tasks)
   - Implement list functionality
   - Add filtering by pattern
   - Format output (table, JSON, tree)

5. **Phase 5 - US3: Delete Configs** (4 tasks)
   - Implement delete functionality
   - Add confirmation prompts
   - Handle nested deletions

6. **Phase 6 - US4: Environments** (8 tasks)
   - Environment service implementation
   - Create env commands (create, switch, list, delete)
   - Active environment tracking
   - Environment validation

7. **Phase 7 - US5: Import/Export** (6 tasks)
   - Export to JSON
   - Import from JSON
   - Handle [ENCRYPTED] placeholders
   - Validation and error handling

8. **Phase 8 - US6: Auto-Encryption** (4 tasks)
   - Crypto service implementation
   - Key management (OS keychain integration)
   - Pattern-based detection
   - Encrypt/decrypt hooks

9. **Phase 9 - Polish** (2 tasks)
   - Comprehensive help documentation
   - Example configurations

**Parallelization Opportunities**: 18 tasks can run in parallel

**MVP Scope** (Phases 1-3): 23 tasks
- Gives you core set/get functionality
- Can test and validate before building advanced features

Ready to start implementation?

---

You: Yes, implement it

Claude: Starting implementation...

[Invokes speckit-implement sub-agent]

[Sub-agent checks checklists - none exist yet, proceeds]

Implementation in progress:

✓ **Phase 1 - Setup** (8/8 tasks complete)
  - Created Node.js project with package.json
  - Installed dependencies: commander, inquirer, chalk
  - Set up directory structure
  - Configured ESLint and Prettier
  - Created .gitignore

✓ **Phase 2 - Foundation** (6/6 tasks complete)
  - Implemented JSON storage layer with atomic writes
  - Created config model with validation
  - Added comprehensive error classes
  - Implemented path utilities for cross-platform support

✓ **Phase 3 - US1: Set/Get Configs** (9/9 tasks complete)
  - Implemented ConfigService with CRUD operations
  - Created 'set' command with dot notation support
  - Created 'get' command with nested path resolution
  - Added validation and error handling
  - Tested with various config structures

✓ **Phase 4 - US2: List Configs** (5/5 tasks complete)
  - Implemented list functionality with filtering
  - Added multiple output formats (table, JSON, tree)
  - Colored output using chalk
  - Pattern matching support

✓ **Phase 5 - US3: Delete Configs** (4/4 tasks complete)
  - Implemented delete with confirmation
  - Recursive deletion for nested paths
  - Undo support (backup before delete)

✓ **Phase 6 - US4: Environments** (8/8 tasks complete)
  - Environment service with create/switch/list/delete
  - Active environment tracking in environments.json
  - Environment-specific config storage
  - Validation and existence checks

✓ **Phase 7 - US5: Import/Export** (6/6 tasks complete)
  - Export to JSON with [ENCRYPTED] placeholders
  - Import from JSON with validation
  - Merge strategies (overwrite, merge)
  - Format validation and error handling

✓ **Phase 8 - US6: Auto-Encryption** (4/4 tasks complete)
  - Crypto service with AES-256-GCM
  - OS keychain integration (macOS/Linux/Windows)
  - Pattern-based auto-detection
  - Transparent encrypt/decrypt on set/get

✓ **Phase 9 - Polish** (2/2 tasks complete)
  - Comprehensive help system
  - Example configurations and documentation
  - CLI improvements and UX polish

✅ **Implementation Complete!** All 52 tasks executed successfully.

**What Was Built**:

```bash
devconfig/
├── src/
│   ├── commands/           # All CLI commands implemented
│   ├── services/           # Config, Crypto, Environment services
│   ├── storage/            # JSON storage with atomic writes
│   ├── models/             # Config validation
│   └── utils/              # Cross-platform utilities
├── tests/                  # (Ready for testing)
├── examples/               # Example configs
└── package.json
```

**Next Steps I Recommend**:

1. **Test the CLI**:
   ```bash
   # Link for global usage
   npm link

   # Test basic commands
   devconfig set database.host localhost
   devconfig get database.host
   devconfig list

   # Test environments
   devconfig env create staging
   devconfig env switch staging
   devconfig set api.url https://staging.api.com

   # Test encryption (try setting something with "password" in the name)
   devconfig set database.password mysecret
   devconfig get database.password

   # Test export
   devconfig export --output dev-config.json
   ```

2. **Review the code**:
   - Check src/services/crypto-service.js for encryption implementation
   - Review src/commands/ for CLI UX
   - Validate error handling

3. **Add tests** (optional):
   - Unit tests for services
   - Integration tests for CLI commands
   - End-to-end workflow tests

4. **Create a commit**:
   ```bash
   git add .
   git commit -m "feat: implement dev environment configuration manager

   - Complete CLI tool with set/get/list/delete commands
   - Environment management (dev/staging/prod)
   - Auto-encryption for sensitive values
   - Import/export functionality
   - Cross-platform support"
   ```

5. **Package for distribution** (optional):
   - Publish to npm
   - Create GitHub release
   - Write user documentation

Would you like me to help with any of these next steps?
```

---

## Example 2: Adding a Feature to Existing Project

### Scenario
You have an existing web application and want to add a notification system.

### Conversation

```
You: I want to use speckit to add a real-time notification feature to my Express.js app

Claude: I'll help you add a notification system using speckit. Let me check your project setup...

[Checks for constitution]

✓ Found existing constitution in .specify/memory/constitution.md

Your project has these principles:
1. Security First - All data encrypted, auth required
2. Performance - API response < 200ms
3. Scalability - Support 10k concurrent users
4. Code Quality - 80% test coverage minimum
5. Documentation - All APIs documented

Great! Now let's define your notification feature. Tell me more about what you need:

1. What types of notifications? (System alerts, user messages, etc.)
2. How should they be delivered? (Real-time, batch, email, push?)
3. Who can send/receive notifications?
4. Any persistence requirements?

---

You:
- Types: User messages, system alerts, activity updates
- Real-time delivery using WebSockets
- All authenticated users can receive, admins can send system alerts
- Store in database for history, mark as read/unread

Claude: Perfect! A few more questions to ensure we design this right:

1. **Scale expectations**: You mentioned 10k concurrent users in your constitution. Should notifications broadcast to all users or targeted delivery?

2. **Read receipts**: Besides mark as read, do you need delivery confirmation or read timestamps?

3. **Notification priority/urgency**: Should some notifications be highlighted or require acknowledgment?

4. **Integration**: Should this integrate with your existing auth system? What about user preferences (mute, frequency)?

---

You:
1. Targeted delivery - each notification has specific recipients
2. Just read/unread timestamps, no delivery confirmation
3. Yes, support priority levels: low, normal, high, urgent
4. Use existing JWT auth, add user preferences table for notification settings

Claude: Excellent! I have a clear picture. Creating specification...

[Invokes speckit-specify sub-agent]

✓ Specification complete!

**Feature**: Real-Time Notification System
**Branch**: 3-notification-system
**User Stories**:
- US1: Send targeted notifications with priority levels
- US2: Real-time delivery via WebSockets
- US3: Notification history and read/unread tracking
- US4: User notification preferences

Proceeding to technical planning...

[Invokes speckit-plan sub-agent]

**Technical Plan Review**:

**Proposed Stack**:
- WebSocket: Socket.io (easy integration with Express)
- Database: PostgreSQL (you're already using it)
- Queue: Redis for notification buffering
- Real-time: Socket.io rooms for targeted delivery

**New Tables**:
```sql
notifications (id, user_id, type, priority, message, metadata, read_at, created_at)
notification_preferences (user_id, enabled, priority_filter, quiet_hours)
```

**Architecture**:
```
src/
├── notifications/
│   ├── notification.controller.js
│   ├── notification.service.js
│   ├── notification.model.js
│   ├── websocket.handler.js
│   └── notification.queue.js
```

**Concerns I want to validate with you**:

1. **Redis Dependency**: The plan adds Redis for notification queuing. This ensures reliability but adds infrastructure. Alternatives:
   - In-memory queue (simpler, but lose buffered notifications on restart)
   - Database-backed queue (no new dependency, but slower)

   Recommendation: Redis is worth it for your 10k user scale. Agree?

2. **WebSocket Reconnection**: Plan includes automatic reconnection on client side. Should include exponential backoff?

3. **Notification Retention**: How long should we keep old notifications? Default plan: 90 days, then archive.

---

You:
1. Yes, add Redis - we'll need it for scaling anyway
2. Yes, exponential backoff with max retry limit
3. 90 days is fine

Claude: Perfect! Proceeding to task breakdown...

[Rest of workflow continues...]
```

---

## Example 3: Web Application Feature

### Scenario
Building a user dashboard with analytics.

```
You: Use speckit-driver to build a user analytics dashboard

Claude: I'll help you build an analytics dashboard. First, let me check if we have a project constitution...

[Workflow continues with constitution check, specification creation, planning, tasks, and implementation]
```

---

## Example 4: Handling Clarifications

### Scenario
The specify agent needs clarification on ambiguous requirements.

```
You: Use speckit to build a search feature

Claude: Let me help you build a search feature. Creating specification...

[Invokes speckit-specify sub-agent]

[Sub-agent finds 3 things that need clarification]

I've drafted the initial specification, but there are a few important decisions that will significantly impact the implementation. Let me ask about them:

## Question 1: Search Scope

**Context**: "Users should be able to search"

**What we need to know**: What exactly should be searchable?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | Content only (posts, articles) | Simpler implementation, focused UX |
| B | Content + Users | More complex, needs different result types |
| C | Everything (content, users, tags, comments) | Most flexible, but complex relevance ranking |
| Custom | Provide your own list | Specify exactly what's searchable |

**Your choice**: _______

## Question 2: Search Performance

**Context**: Results should be "fast"

**What we need to know**: What's the acceptable response time?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | < 100ms (instant) | Requires search index (Elasticsearch, etc.) |
| B | < 500ms (fast) | Can use database with good indexes |
| C | < 2s (acceptable) | Simple database queries sufficient |
| Custom | Specify your target | Tell us your performance requirement |

**Your choice**: _______

## Question 3: Search Features

**Context**: Basic text search is specified

**What we need to know**: What advanced features do you need?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | Basic text matching only | Simple, quick implementation |
| B | Text + Filters (date, category, author) | Moderate complexity, better UX |
| C | Full-text search with fuzzy matching, autocomplete | Complex, requires search engine |
| Custom | List your requirements | Specify exact features needed |

**Your choice**: _______

Please respond with your choices (e.g., "Q1: B, Q2: A, Q3: C") or "Custom" with your specific requirements.

---

You: Q1: B, Q2: A, Q3: C

Claude: Perfect! Let me update the specification with your choices...

[Updates spec, removes clarification markers]

✓ Specification updated with:
- Search scope: Content + Users
- Performance target: < 100ms (will use Elasticsearch)
- Features: Full-text search with fuzzy matching and autocomplete

Proceeding to technical planning with these requirements...

[Workflow continues...]
```

---

## Example 5: Reviewing Technical Plans

### Scenario
The orchestrator flags concerns about the technical plan.

```
Claude: I've reviewed the technical plan, and I have some concerns I'd like to discuss with you:

**Proposed Approach**:
The plan suggests using MongoDB for the new feature, but I notice:

1. **Your existing project uses PostgreSQL** for all other data
2. **Your constitution principle #3** says "Prefer proven, mainstream technologies"
3. **Adding MongoDB** means:
   - New database server to maintain
   - Additional deployment complexity
   - Team needs MongoDB expertise
   - Dual database management in codebase

**My Recommendation**:
Use PostgreSQL with JSONB columns for flexible schema, because:
- Stays within existing infrastructure
- PostgreSQL JSONB performance is excellent
- Simpler deployment and operations
- Team already knows PostgreSQL
- Still get schema flexibility where needed

**Alternative Option**:
If MongoDB-specific features are truly needed (e.g., geospatial queries, aggregation pipelines), we can justify it, but I'd need to understand why PostgreSQL + PostGIS won't work.

**What would you like to do?**

---

You: You're right, let's stick with PostgreSQL. I don't really need MongoDB-specific features.

Claude: Great decision! Let me update the plan to use PostgreSQL with JSONB...

[Updates plan]

✓ Plan updated - using PostgreSQL with JSONB columns

This aligns better with your constitution and keeps infrastructure simple.

Proceeding to task breakdown...

[Workflow continues...]
```

---

## Tips for Effective Use

Based on these examples:

1. **Be Specific Early**: The more detail you provide upfront, the fewer clarifications needed
2. **Trust the Process**: Let the orchestrator guide you through each phase
3. **Engage in Discovery**: Answer clarifying questions thoroughly
4. **Review Critical Decisions**: When orchestrator flags concerns, take time to review
5. **Iterate**: Start with MVP scope, then add features incrementally

## Next Steps

- Try these patterns in your own projects
- Experiment with different feature types
- Customize the orchestration logic for your workflow
- Share your experiences and examples!
