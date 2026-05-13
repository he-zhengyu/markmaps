---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Agent Skills with Claude

## What Are Skills
- 🔑 **Skill** — folder of instructions for an agent
- Package three things
  - Repeated **workflows**
  - **Specialized knowledge**
  - New **capabilities**
- 💡 If you retype the same prompt across chats → make it a skill
- Course: [Agent Skills with Anthropic](https://learn.deeplearning.ai/courses/agent-skills-with-anthropic/information)

## The Problem Skills Solve
- Scenario: **weekly marketing campaign analysis**
  - CSV input: date, campaign, impressions, clicks, conversions
  - Long prompt with input format, quality checks, metrics, output format
- Pain points without a skill
  - ⚠️ Re-paste the same prompt every week
  - ⚠️ Must bring external docs (e.g. budget rules) each time
  - ⚠️ Everything dumped into the **context window**
  - ⚠️ Hard to share with teammates
- ✅ Skill packages this once, reusable forever

## Walkthrough: Marketing Campaign Analysis
### Step 1 — Quality & Funnel
- Attach campaign CSV
- Prompt asks for
  - Data quality check
  - Funnel analysis vs benchmarks
  - Specified output format
- Output
  - Total records, missing data, **anomalies**
  - Funnel vs benchmark CTR / CVR
  - Interpretation of what's working

### Step 2 — Efficiency Metrics
- 📊 Metrics requested
  - **ROAS** (return on ad spend)
  - **CPA** (cost per acquisition)
  - **Net profit**
- Reveals portfolio performance & total profit

### Step 3 — Budget Reallocation
- Upload separate **budget reallocation rules** file
- Specific to this team's framework
  - Increase, maintain, or decrease budget
- Output: pass/fail per rule + proposed reallocation
- ⚠️ Requires niche, in-house knowledge — perfect skill candidate

## Anatomy of a Skill
### `SKILL.md` File
- 📌 Must be named **`SKILL.md`** in Markdown
- Contains the underlying instructions
  - Input requirements
  - Data quality check
  - Funnel analysis + historical benchmarks
  - Efficiency analysis
  - Output format
  - Conditional reference to other files

### YAML Frontmatter
- Required at top of `SKILL.md`
- Required fields
  - 🔑 **`name`** — used for referencing & UI
  - 🔑 **`description`** — tells the model *when* to use the skill
- 💡 Description quality drives correct skill activation

### Supporting Files
- Skill can reference any file in the **same parent folder**
- Example: `references/budget_reallocation_rules.md`
- Loaded **only when needed** → context-efficient
- ✅ Keeps unrelated chats clean

### Folder Structure
- `analyzing-marketing-campaign/`
  - `SKILL.md` *(top level)*
  - `references/`
    - `budget_reallocation_rules.md`
- Naming rules
  - ✅ lowercase letters
  - ✅ dashes between words
  - ❌ reserved words like `Claude` or `Anthropic`
- 📌 `references/` is the standard folder name for external files

## Using a Skill in Claude.ai
- Zip the skill folder
- **Settings → Capabilities → Skills → Add**
- Drag & drop the `.zip`
- Name + description appear once uploaded
- In a new chat
  - Attach CSV, ask normal question
  - Claude auto-detects skill via name & description
  - Reads `SKILL.md`, then loads referenced files only as needed
  - Executes analysis without re-prompting
- Inspect the **code execution panel** to see what's running

## Built-in Skills
- Spreadsheet creation ships **built-in**
- Demo: generate Excel report with
  - Executive summary
  - Funnel analysis
  - Efficiency analysis
  - Color coding
- 💡 Custom skills + built-in skills compose naturally
- Output: download or open in Google Drive

## Portability — Open Standard
- Skills are an **open standard**
- Work across environments
  - Claude.ai
  - Claude Code
  - Codex
  - Gemini CLI
  - Other agentic tools
- ✅ Write once, run across the AI ecosystem

## Key Takeaways
- 🔑 A **skill** = folder with `SKILL.md` + optional reference files
- 📌 `name` and `description` in YAML frontmatter are **required** — description determines activation
- 💡 Skills keep the **context window lean** by loading reference files only when needed
- ✅ Turn any repeated prompt into a portable, shareable asset
- ⚠️ Avoid reserved words (`Claude`, `Anthropic`) and use `lowercase-with-dashes` names
- 📌 Use the standard `references/` subfolder for supporting docs
- 💡 Custom skills compose with **built-in skills** (e.g. spreadsheet creation) for end-to-end workflows
- ✅ Open standard → same skill runs in Claude.ai, Claude Code, Codex, Gemini CLI, and beyond