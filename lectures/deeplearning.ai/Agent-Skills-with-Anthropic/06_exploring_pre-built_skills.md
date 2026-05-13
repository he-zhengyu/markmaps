---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Pre-built Skills & Skill-Creator Workflow

## Anthropic Skills Repository
- 📌 Lives at [github.com/anthropic/skills](https://github.com/anthropic/skills)
- All skills are **production-ready**
- Two categories of skills

### Document Skills
- 🔑 **Built-in & always available** in Claude AI
- Cannot be toggled on/off
- Includes:
  - `PowerPoint` skill
  - `Word` skill
  - `Excel` skill
  - `PDF` skill

### Example Skills
- Toggleable in Claude settings
- ⚠️ **Off by default** (with one exception)
- ✅ `skill-creator` is **on by default**

## PowerPoint Skill (Anatomy)
- Standard structure
  - `SKILL.md` file
  - Supporting files & folders
- **YAML frontmatter** with name + description
- `SKILL.md` contents
  - Overview of use cases
    - Create, edit, analyze `.pptx` files
  - Reading instructions
  - Underlying scripts for specific tasks
- 💡 Scripts are **only loaded when needed**
- Design guidance baked in
  - Colors & typography
  - Design principles & requirements
  - Color palette selection when unspecified

## Skill-Creator Skill
- 🔑 A **meta-skill** — a skill that creates skills
- Eliminates manual file/folder scaffolding
- `SKILL.md` structure
  - Name + description
  - Best practices for skill authoring
  - **Explicit step-by-step process**
- 📌 Explicit steps → predictable workflow
- Workflow steps
  - Start with **concrete examples**
  - Plan reusable skill contents
  - Pattern-match from existing examples
  - Initialize via Python scripts

### Underlying Python Scripts
- `init_skill`
  - Fills template with YAML frontmatter
  - Replaces placeholders & TODOs
- `package_skill`
  - Zips skill in correct structure
  - Imports needed modules
- `validate_skill`
  - ✅ Confirms `SKILL.md` exists
  - ✅ Validates YAML frontmatter
  - ✅ Checks folder/file correctness

## End-to-End Workflow Demo
- 💡 Goal: combine **prompting + skills + MCP** into one pipeline
- Three building blocks
  - Modify existing skill → use BigQuery
  - Create new brand-guidelines skill
  - Combine with built-in PowerPoint skill

### Step 1 — MCP + BigQuery Setup
- Using **Claude Desktop** with local MCP server
- Configured in `Settings → Developer`
  - Command + arguments
  - Environment variables
  - Credentials path
- Config file specifies servers + startup commands
- ⚠️ BigQuery is just an example — any data store works
- Verification prompts
  - "List the tables in BigQuery"
  - "Show me the schema of the table"

### Step 2 — Update Marketing Skill
- Replace **CSV upload → BigQuery query**
- Pass schema inline in conversation
- 📌 Preserve budget reallocation rules unchanged
- Skill-creator behavior
  - Analyzes existing skill structure
  - Applies best practices
  - Rewrites `SKILL.md` with BigQuery references
  - Specifies MCP server + tool name
- Best practices applied automatically
  - ⚠️ Avoid ambiguous date ranges
  - Ask user to clarify range
  - Provide example queries with explicit dates
- 📌 **Copy the skill** to persist across conversations

### Step 3 — Create Brand Guidelines Skill
- Upload assets
  - Brand guidelines document
  - Logo files
- Guidelines include
  - Color palette
  - Supporting colors
  - Typography
- 💡 Skills shine when encoding **company-specific** preferences
- Skill-creator process
  - Analyzes other skills for complementary patterns
  - Runs `init_skill` Python script
  - Populates `assets/` folder with logos, colors, fonts
  - Generates `SKILL.md` with name + description
- 📌 Copy skill to save for future chats

### Step 4 — Generate Presentation
- Combines **3 skills** in one chat
  - Marketing analysis skill (custom)
  - Brand guidelines skill (custom)
  - PowerPoint skill (built-in)
- Execution flow
  - Read relevant skill files
  - Query BigQuery for target week
  - Generate slide HTML/CSS using brand styling
  - Hand off to PowerPoint skill for `.pptx` creation
- 💡 Model **backtracks & self-corrects** when issues arise
- Output deliverables
  - Efficiency analysis slide
  - Funnel analysis slide
  - Executive summary slide
- Distribution options
  - Download `.pptx` directly
  - Open in Google Drive / Google Slides
  - Continue iterating via prompts

## Key Takeaways
- 🔑 **Document skills** (PPT, Word, Excel, PDF) are built-in; **example skills** are opt-in
- 💡 `skill-creator` is a meta-skill that scaffolds new skills following best practices
- 📌 Even with skill-creator, **clear prompts and context still matter**
- ✅ Combine **MCP servers + custom skills + built-in skills** for end-to-end workflows
- 📌 Always **copy generated skills** to persist them across conversations
- ⚠️ Avoid ambiguous inputs (e.g., date ranges) — bake clarification into the skill
- 💡 Skills are where you encode **company-specific** logic: brands, data sources, rules