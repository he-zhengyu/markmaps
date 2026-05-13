---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Agent Skills with Anthropic

## Course Overview
- **Partnership** between DeepLearning.AI & Anthropic
- **Instructor**: Elie Schoppik (returning)
- **Contributor**: Hawraa Salami (DeepLearning.AI)
- 🔗 [Course link](https://learn.deeplearning.ai/courses/agent-skills-with-anthropic/information)

## What Are Skills?
- 🔑 **Folders of instructions** that extend agent capabilities
- Provide **specialized knowledge** for tasks
- 💡 Give Claude Code & other agents **new abilities**
- 📌 Now an **open standard**
  - Standardized format
  - Works with any skills-compatible agent
  - ✅ Build once, deploy across multiple agent products

## Skill Structure
- **`SKILL.md`** *(required markdown file)*
  - `name`
  - `description`
  - Main instructions
- **Referenced files** *(optional)*
  - Scripts
  - Additional markdown files
  - Assets (templates, images)

## Progressive Disclosure
- 🔑 **How skills load into context**
- **Always in context window**
  - Skill `name`
  - Skill `description`
- **Loaded on demand**
  - Main instructions — when user request matches description
  - Reference & asset files — only if needed
- 💡 Keeps context window efficient

## Required Agent Tools
- 📌 **Filesystem access** — read & write files
- 📌 **Bash tool** — execute code
- ✅ Together enable running any command a skill requires

## Combining with Other Capabilities
- **MCP (Model Context Protocol)**
  - Fetch data from external sources
  - Skill knows what to do with that data
- **Sub-agents**
  - Delegate tasks with **isolated context**
  - Sub-agents can themselves use skills
- 💡 Enables **powerful agentic workflows**

## When to Use a Skill
- 📌 You **repeatedly** ask the agent for the same workflow
- ❌ Re-explaining the workflow every time
- ✅ Package once as a skill → agent **automatically knows what to do**

## Course Roadmap
### Lesson Path
- **Claude.ai**
  - Build a marketing campaign skill
  - Combine with pre-built **Excel** & **PowerPoint** skills
- **Claude API**
  - Skill for content creation
  - Skill for data analysis
- **Claude Code**
  - Skill for code review
  - Skill for testing
- **Claude Agent SDK**
  - Build a **research agent**
  - Skill to combine research results

## Key Takeaways
- 🔑 **Skills = folders of instructions** packaged as `SKILL.md` + optional assets
- 💡 **Progressive disclosure** keeps context lean — only `name` + `description` always loaded
- 📌 Skills are an **open standard** — portable across any skills-compatible agent
- ✅ Best used for **repeated workflows** you'd otherwise re-explain each time
- 💡 Pair skills with **MCP** (data) and **sub-agents** (isolated context) for compound workflows
- ⚠️ Agent must have **filesystem + bash** tools for skills to be useful