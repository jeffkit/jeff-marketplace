# Speckit Driver Installation Guide

Complete guide for installing and configuring the Speckit Driver plugin for Claude Code.

## Prerequisites

Before installing the plugin, ensure you have:

1. **Claude Code** installed and working
   - Download from: https://claude.com/code
   - Verify: Run `claude --version` in terminal

2. **Speckit** installed (optional but recommended)
   - Install: `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git`
   - Verify: Run `specify --version`

3. **Git** installed
   - Verify: Run `git --version`

## Installation Methods

### Method 1: Install from GitHub (Recommended)

1. Clone the plugin repository:

```bash
cd ~/projects  # or your preferred directory
git clone https://github.com/jeffkit/speckit-driver.git
```

2. Create a local marketplace configuration:

```bash
# Create marketplace directory if it doesn't exist
mkdir -p ~/.claude/marketplaces

# Create marketplace configuration
cat > ~/.claude/marketplaces/local.json << 'EOF'
{
  "name": "Local Plugins",
  "plugins": [
    {
      "name": "speckit-driver",
      "version": "1.0.0",
      "path": "~/projects/speckit-driver"
    }
  ]
}
EOF
```

Note: Adjust the `path` to match where you cloned the repository.

3. In Claude Code, add the marketplace:

```
/plugin marketplace add ~/.claude/marketplaces/local.json
```

4. Install the plugin:

```
/plugin install speckit-driver
```

5. Restart Claude Code to activate the plugin.

### Method 2: Install from Local Directory

If you already have the plugin directory:

1. Ensure the plugin directory structure is correct:

```
speckit-driver/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── speckit-constitution.md
│   ├── speckit-specify.md
│   ├── speckit-plan.md
│   ├── speckit-tasks.md
│   └── speckit-implement.md
├── skills/
│   └── speckit-driver/
│       └── SKILL.md
└── README.md
```

2. Follow steps 2-5 from Method 1 above.

## Verification

After installation, verify the plugin is loaded:

1. In Claude Code, type:

```
/plugin list
```

You should see `speckit-driver` in the list of installed plugins.

2. Check if the skill is available. In a conversation, type a trigger phrase:

```
Use speckit to build a feature
```

If Claude responds with guidance about the speckit workflow, the plugin is working!

## Configuration

### For New Projects (First Time Setup)

When you first use speckit-driver in a new project:

1. The plugin will check for a project constitution
2. If none exists, it will guide you through creating one
3. This only happens once per project

### For Existing Speckit Projects

If you already have a speckit-initialized project with `.specify/` directory:

1. The plugin will use your existing constitution
2. Continue with your existing workflow
3. No additional setup needed

## Updating the Plugin

To update to a newer version:

1. Pull the latest changes:

```bash
cd ~/projects/speckit-driver
git pull origin main
```

2. In Claude Code, reinstall:

```
/plugin uninstall speckit-driver
/plugin install speckit-driver
```

3. Restart Claude Code.

## Uninstallation

To remove the plugin:

1. In Claude Code:

```
/plugin uninstall speckit-driver
```

2. Optionally, remove the marketplace configuration:

```bash
rm ~/.claude/marketplaces/local.json
```

3. Optionally, delete the plugin directory:

```bash
rm -rf ~/projects/speckit-driver
```

## Troubleshooting

### Plugin Not Loading

**Symptom**: Plugin doesn't appear in `/plugin list`

**Solutions**:
1. Check the plugin path in `~/.claude/marketplaces/local.json` is correct
2. Ensure path uses `~` for home directory or absolute path
3. Verify plugin directory structure matches expected format
4. Restart Claude Code after installation

### Skill Not Triggering

**Symptom**: Typing trigger phrases doesn't activate the skill

**Solutions**:
1. Verify plugin is installed: `/plugin list`
2. Check `skills/speckit-driver/SKILL.md` exists
3. Try explicit trigger phrases:
   - "用speckit开发"
   - "Use speckit to build"
   - "Help me with spec-driven development"
4. Restart Claude Code

### Sub-agents Not Found

**Symptom**: Error messages about missing sub-agents

**Solutions**:
1. Verify all agent files exist in `agents/` directory:
   - speckit-constitution.md
   - speckit-specify.md
   - speckit-plan.md
   - speckit-tasks.md
   - speckit-implement.md
2. Check file names are exactly as listed (case-sensitive)
3. Verify YAML frontmatter in each agent file is correct

### Speckit Commands Not Working

**Symptom**: Sub-agents fail when executing speckit commands

**Solutions**:
1. Install speckit if not already installed:
   ```bash
   uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
   ```
2. Initialize speckit in your project:
   ```bash
   cd your-project
   specify init
   ```
3. Verify `.specify/` directory exists with templates

### Permission Errors

**Symptom**: Cannot read/write files in `.specify/` directory

**Solutions**:
1. Check file permissions:
   ```bash
   ls -la .specify/
   ```
2. Ensure you have write permissions to project directory
3. On macOS, grant Claude Code file access in System Preferences

## Advanced Configuration

### Custom Sub-Agent Models

To use different models for sub-agents, edit the agent files:

```yaml
---
name: speckit-plan
model: opus  # Change from sonnet to opus for more powerful planning
---
```

Available models: `sonnet`, `opus`, `haiku`

### Custom Tool Access

To restrict or expand tools available to sub-agents:

```yaml
---
name: speckit-implement
tools: Read, Write, Edit, Bash  # Remove tools you don't want agent to use
---
```

### Adjusting Orchestration Logic

To customize how the main skill makes decisions, edit:

```
skills/speckit-driver/SKILL.md
```

Look for the "Decision Framework" section to modify when the orchestrator stops vs. continues.

## Getting Help

If you encounter issues not covered here:

1. Check the main [README.md](README.md) for usage examples
2. Review [GitHub Issues](https://github.com/jeffkit/speckit-driver/issues)
3. Create a new issue with:
   - Your Claude Code version
   - Plugin installation method
   - Error messages (if any)
   - Steps to reproduce the problem

## Next Steps

After successful installation:

1. Read the [README.md](README.md) for usage examples
2. Try building a simple feature to familiarize yourself with the workflow
3. Review the orchestration logic in `skills/speckit-driver/SKILL.md`
4. Customize sub-agents for your specific needs

Happy spec-driven development!
