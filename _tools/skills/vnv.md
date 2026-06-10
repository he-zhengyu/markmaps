Here's a comprehensive overview of both concepts:

---

## Subagents in Claude Code

Subagents are separate agent instances that your main agent can spawn to handle focused subtasks. Think of them as specialist workers you can dispatch while your main session stays focused.

**Why use them?**

Your main Claude session gets cluttered fast during complex work. Subagents solve this by spinning up separate AI instances — each with its own system prompt, tool permissions, and even a different model. A "code-reviewer" agent reads diffs. An "explorer" agent searches a massive repo. They work in isolation, then hand back a summary.

**How to create one** — a subagent is just a Markdown file with YAML frontmatter:

```markdown
---
name: code-reviewer
description: Reviews code for style and bugs. Use when changes need review.
tools: Read, Grep, Glob
model: sonnet
---

You are a careful code reviewer. Focus on correctness, style, and potential bugs.
```

Store them in different locations depending on scope. Project subagents go in `.claude/agents/` (ideal for project-specific agents). User-scoped subagents go in `~/.claude/agents/` and are available across all your projects. When multiple subagents share the same name, the higher-priority location wins.

**Tool permissions:**

By default, subagents inherit all tools from the main conversation, including MCP tools. To restrict tools, use either the `tools` field (allowlist) or the `disallowedTools` field (denylist). If both are set, `disallowedTools` is applied first, then `tools` is resolved against the remaining pool.

| Scope | Location | Use case |
|---|---|---|
| Project | `.claude/agents/` | Codebase-specific agents |
| User | `~/.claude/agents/` | Personal agents across all projects |
| Plugin | Loaded via plugin | Shared across teams |

**Managing subagents:**

Run `/agents` to view all available subagents (built-in, user, project, and plugin), create new ones with guided setup, edit existing configurations, and see which subagents are active when duplicates exist.

---

## Plugins in Claude Code

Plugins allow you to extend Claude Code with custom functionality that can be shared across projects. You can programmatically load plugins from local directories to add custom slash commands, agents, skills, hooks, and MCP servers to your agent sessions.

Think of a plugin as a **bundle** — it packages multiple extensions together so a team can install one thing and get everything.

**What a plugin can contain:**

| Component | Purpose |
|---|---|
| `skills/` | Model-invoked capabilities (also callable via `/skill-name`) |
| `agents/` | Subagent definitions |
| `hooks/` | Lifecycle event scripts |
| MCP servers | External tool connections |
| `commands/` | Legacy slash commands (still supported) |

**Plugin directory structure:**

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json      ← required manifest
├── skills/
│   └── my-skill/
│       └── SKILL.md
└── agents/
    └── reviewer.md
```

**Installing from the marketplace:**

You can install plugins with: `claude plugin marketplace add <github-repo>` and `claude plugin install <plugin-name>`.

**Skills from plugins are namespaced** — when invoked as slash commands, the format is `plugin-name:skill-name`, avoiding conflicts between plugins.

---

## How Everything Fits Together

Use subagents when you need parallel execution or want to isolate heavy computational work (best for preventing context pollution, specialized deep dives). Use plugins to package and share complete configurations across teams or projects (best for team standardization, distributing opinionated setups). Use MCP to integrate external systems and expose their capabilities as native commands.

In short: **MCP** connects external tools → **Subagents** isolate and parallelize work → **Plugins** bundle everything for sharing.