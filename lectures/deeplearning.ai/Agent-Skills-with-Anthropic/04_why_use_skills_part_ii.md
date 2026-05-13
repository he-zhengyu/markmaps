---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Agent Skills: The Open Standard

## What Are Skills?
- 🔑 **Open standard** for AI agents
  - Originally created at Anthropic
  - Now a formal specification
- **Cross-platform support**
  - Claude AI / Claude Desktop
  - Claude Code
  - Codex
  - Gemini CLI
  - Open Code
  - Agent SDK & API
- 💡 Similar in spirit to **Model Context Protocol (MCP)**

## Anatomy of a Skill
- **File system based**
  - A folder containing the skill's assets
- **`SKILL.md`** — the entry point
  - 🔑 Defines name and description
  - References other resources
- **Supporting resources**
  - Additional markdown documents
  - Executable scripts
  - Icons, images, brand assets
- **Example: PDF skill**
  - Convert PDFs to images
  - Extract info from form fields
  - Fill forms with annotations
  - 📌 Code is referenced from `SKILL.md`, not inlined

## Why Skills Matter
### Evolution of Agent Design
- **Old approach** — single-purpose agents
  - Coding, research, finance, marketing
  - Each with bespoke tools and context
- **New approach** — simple scaffolding
  - ✅ Easier to evaluate, understand, scale
  - Underlying tools: `bash` + filesystem
  - ⚠️ Lacks domain expertise on its own
- 💡 **Skills fill the expertise gap**

### What Skills Provide
- **Procedural knowledge**
  - Loaded on demand
- **User/company-specific context**
  - How *your* team does the work
- **Repeatable workflows**
  - 📌 Predictability in a non-deterministic system
  - Articulate steps and instructions
- **New capabilities**
  - Generate presentations, Excel, PDF reports
  - Execute scripts when needed

## Core Properties
### Portability
- ✅ Same format works everywhere
- Create once, share, scale across environments
- Open standard → growing ecosystem

### Composability
- Combine **custom skills** with **built-in skills**
  - *e.g.* marketing campaign analysis + PowerPoint generation
- Chain multiple skills into complex workflows
- 💡 Predictable outputs from non-deterministic models

### Domain Expertise
- Claude knows *general* data analysis, legal review, etc.
- Skills teach Claude **your specific way**
- Examples
  - Weekly marketing campaign reviews
  - Branded newsletter design
  - Company-specific financial analysis

## Progressive Disclosure
- 🔑 **Definition** — load only what's needed, when needed
- ⚠️ **Why it matters**
  - Context window is a **public good**
  - 📊 More tokens → faster fill-up
  - Risk of context degradation / wrong answers

### Three-Stage Loading
- **Stage 1 — Metadata only**
  - Skill *name* + *description* loaded
  - Lets Claude know what exists and when to trigger
- **Stage 2 — `SKILL.md` body**
  - Loaded once the skill is triggered
- **Stage 3 — On-demand resources**
  - Additional files read as required
  - 📌 Scripts execute *outside* the context window
  - Avoids polluting with unnecessary tokens

### Enabled By
- `bash` tool
- Filesystem access
- Lets Claude intentionally curate context

## Key Takeaways
- 🔑 Skills are an **open standard** — portable across Claude Code, Codex, Gemini CLI, Open Code, and more
- 💡 Skills = **procedural knowledge + domain expertise + repeatable workflows**, layered onto a simple agent scaffold
- ✅ **Composable** — mix custom and built-in skills to build predictable, complex pipelines
- 📌 **Progressive Disclosure** is the core design principle: only metadata enters context first, deeper resources load on demand
- ⚠️ Treat the **context window as a public good** — every token added risks degradation
- 💡 Skills shine where Claude knows the *general* task but not *your* specific way of doing it