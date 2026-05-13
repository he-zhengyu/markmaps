---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Skills in the Agent Ecosystem

## Ecosystem Overview
- Core components work **together**
  - **MCP** → external context & data
  - **Subagents** → isolated threads & parallelization
  - **Skills** → repeatable workflows
  - **Tools** → low-level capabilities
- 💡 Each solves a different problem — combine intentionally
- Goal: powerful **agentic workflows**

## Skills vs. MCP
- **MCP (Model Context Protocol)**
  - Connects agents to *external systems & data*
  - Examples
    - External databases
    - Google Drive
    - Third-party APIs
  - Brings in **underlying tooling**
- **Skills**
  - Set of *instructions* on how to use those tools
  - Build **repeatable workflows**
  - Produce the kind of data you want
- 🔑 Analogy
  - MCP = the **toolbox** delivered to the agent
  - Skills = the **recipe** for using those tools

## Skills vs. Tools
- 🔑 **Tools** — low-level capabilities
  - Analogy: *hammer, saw, nails*
  - Access systems & perform actions
  - Power skill execution under the hood
    - Generate skills
    - Read skills
    - Produce a filesystem
    - Execute code
  - Sources
    - Built-in to agentic ecosystems
    - Custom-written
    - Loaded via MCP
  - 📌 Definitions **always live in context window**
- 🔑 **Skills** — specialized knowledge
  - Analogy: *how to build a bookshelf*
  - Bundle files, scripts, instructions
  - 📌 **Progressively loaded** only when needed
- 💡 Skills can invoke scripts *like a tool on demand*
  - Avoid bloating every conversation

## Subagents
- **Definition**
  - Spawned by a **main agent**
  - Report back to the parent
  - Created via Claude Code, Agent SDK, or custom
- **Value**
  - Isolated context window
  - Fine-grained permissions
  - ✅ Parallel task execution
- **Access control**
  - Limited tool permissions
  - Specify which **skills** each subagent can use
- **Pattern**
  - Main agent = *orchestrator*
  - Subagent = *specialist* (e.g. **Code Reviewer**)
    - Uses skills defining team/company review process

## Putting It Together
- Example: **Customer Insight Analyzer**
  - Main agent
    - Loads tools via **MCP servers**
    - Pulls in data & resources
  - Subagents (parallel, isolated)
    - Analyze customer interviews
    - Process customer surveys
  - Skills used inside subagents
    - Categorize feedback
    - Summarize findings
    - Analyze interviews & surveys
  - 💡 Predictable, repeatable, portable analysis

## The Stack — Atomic to Composite
- **Prompts**
  - Most atomic unit of conversation
  - ⚠️ Don't scale across teams & companies
- **Skills**
  - Bundle prompts + code + assets
- **Subagents**
  - Delegate tasks, consume skills
- **Tools (via MCP)**
  - Underlying capabilities skills rely on

## Design Principles
- **Context window is a public good**
  - 📌 Be intentional about what loads when
  - Subagents → minimize main context
  - MCP → load needed external data
  - Skills → load **progressively**
- **Persistence**
  - Subagents → persist across parent/sub sessions
  - Skills → persist across user ↔ AI conversations
- **When to use what**
  - ✅ **Skills** → procedural, predictable workflows
  - ✅ **Subagents** → full agentic logic for specialized tasks *only when necessary*

## Key Takeaways
- 💡 **MCP brings tools in, skills tell the agent what to do with them**
- 🔑 Tools are *low-level*; skills are *high-level workflows* built on top
- 📌 Tool definitions stay in context — skills load **progressively**
- ✅ Use **subagents** for isolation, parallelism, and scoped permissions
- ⚠️ Don't rely on raw prompts alone — they don't scale across teams
- 💡 Treat the **context window as a public good** — load intentionally via MCP, skills, and subagents