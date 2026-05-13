---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Research Agent with Claude Agent SDK

## Overview
- **Goal**: Build a research agent that creates learning guides
- **Use case**: Open source tool research from docs, GitHub, web
- **Tech stack**
  - `claude-agent-sdk`
  - `python-dotenv`
  - `asyncio`
  - **Notion MCP server**
- 💡 Same internal harness as **Claude Code**

## Architecture

### Main Agent (Orchestrator)
- Dispatches subagents in **parallel**
- Synthesizes results from multiple sources
- Follows **Skill** instructions when provided
- 📌 Be explicit about behavior with/without skills

### Subagents
- **Documentation Researcher**
  - Tools: `WebSearch`, `WebFetch`
  - Locates official documentation
  - Returns findings in structured format
- **Repository Analyzer**
  - Tools: `WebSearch`, `Bash`, `Read`, `Glob`, `Grep`
  - Clones repos via `git`
  - Reads files & extracts data
- **Web Researcher**
  - Tools: `WebSearch`, `WebFetch`
  - Finds articles, videos, community content
  - Accepts extraction instructions from main agent

## The Skill: `learning-a-tool`

### Purpose
- 🔑 Guides the **main orchestrator only** (not subagents)
- Creates **predictable workflow** for dispatching subagents
- Defines what to research and how to synthesize

### Workflow Phases
- **Research Phase** *(parallel)*
  - Spec for docs subagent
  - Spec for repo analyzer
  - Spec for web researcher
- **Organization Phase**
  - 💡 Uses **progressive disclosure** → loads another `.md` file
  - Progressive levels:
    - Overview & motivation
    - Installation
    - Core concepts
    - Practical patterns
    - Where to go next
- **Output Phase**
  - Strict structure & format
  - Deliverables: overview, resources, learning path, code examples

## Building the Agent

### Setup
- `uv init` → initialize project
- Install dependencies
- Create `agent.py`
- Boilerplate
  - `asyncio` for async runtime
  - `dotenv` for env vars
  - `display_message` helper for nice output

### Configuring `ClaudeAgentOptions`
- **`system_prompt`**
  - Loaded from `main_agent_prompt.md`
- **`allowed_tools`** *(must list every tool subagents need)*
  - ⚠️ Read-only (`Read`, `Grep`, `Glob`) allowed by default
  - Must add explicitly:
    - `Write`
    - `Bash`
    - `WebSearch`
    - `WebFetch`
    - `Task` — 📌 required to dispatch subagents
    - `Skill` — 📌 required to use skills
    - `mcp__notion__*` — wildcard for all Notion tools
- **`mcp_servers`**
  - Key: `notion`
  - Command runs Notion MCP server
  - Reads `NOTION_TOKEN` from `.env`
- **`agents`** dictionary
  - Maps name → `AgentDefinition`
  - Fields: `description`, `prompt`, `tools`
- **`setting_sources`**
  - `user` → `~/.claude/skills/`
  - `project` → `./.claude/skills/`

### Skills Configuration
- Folder structure: `.claude/skills/<name>/SKILL.md`
- ⚠️ Folder must be `skills` (plural)
- ⚠️ File must be named `SKILL.md`
- Skills auto-discovered via `setting_sources`

## Demo: Researching MinerU

### Why MinerU?
- Open library for **PDF extraction**
- 💡 Chosen because Claude lacks deep training data on it
- Forces real external research

### Flow Observed
- User asks for **plan first** (like Claude Code plan mode)
- Skill `learning-a-tool` invoked with args
- Plan shows: parallel research → structure → output
- User approves → execution begins
- **Parallel dispatch**
  - Docs researcher → official docs
  - Repo analyzer → GitHub clone via Bash
  - Web researcher → tutorials, YouTube
- Synthesis into folder structure
  - `README.md` with learning path & time estimates
  - `resources.md` with links, papers, articles
  - Code examples: hello-world, core concepts, practical patterns

### Notion Integration
- Existing **resources** subpage in Notion
- Agent reads `resources.md`
- Converts to **rich Notion blocks**
- Writes via Notion MCP tools in batches

## Security Considerations
- ⚠️ `Write` and `Bash` execute **without user permission**
- ⚠️ No confirmation prompts like Claude Code has
- Next steps to harden:
  - ✅ Build permission/confirmation UI
  - ✅ Add **interrupts** for agents and subagents
  - ✅ Scope tool access more tightly per subagent

## Key Takeaways
- 🔑 The **Agent SDK** lets you build Claude Code-style agents programmatically
- 📌 Every tool used by main agent **or** subagents must be in `allowed_tools` — otherwise subagents are blocked
- 📌 The `Task` tool is required for subagent dispatch; the `Skill` tool is required for skills
- 💡 Skills shine as **orchestration patterns** — guiding the main agent on *how* to coordinate, not what subagents do internally
- 💡 **Progressive disclosure** keeps the main `SKILL.md` lean by deferring detail to linked markdown files
- ✅ Parallel subagent dispatch dramatically speeds up multi-source research
- ⚠️ Default config grants `Write` and `Bash` without prompts — add a permission layer before production
- 📌 MCP servers (e.g. Notion) extend agents into external systems with minimal config