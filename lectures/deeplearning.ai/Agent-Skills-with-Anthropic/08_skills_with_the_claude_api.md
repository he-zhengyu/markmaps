---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Skills with the Claude API

## Context & Setup

### Lesson Goal
- Test two **custom skills** built previously
  - Generating practice questions
  - Time series analysis
- Move from **Claude AI / Desktop** → **Claude Messages API**

### Key Differences vs Claude AI
- ⚠️ Skills in **Claude AI / Desktop** are **not shared** with the API or Claude Code
- 📌 Skill format itself is **unchanged** across environments
- Only the *integration mechanics* differ

### Required Capabilities for Skills
- 🔑 **Code execution** — run bash, edit files
- 🔑 **File system access** — read/write artifacts
- 🔑 **Document creation** — docs, slides, PDFs, reports
- In Claude AI/Desktop → enabled by default under *Settings → Capabilities → Code execution and file creation*
- In API → must be **wired up manually**

## Code Execution Tool

### Purpose
- Gives Claude a **sandboxed container** to run code
- Executes **bash / shell** commands
- Enables creating, viewing, editing files
- Mission-critical for skills to actually *do* anything

### Sandbox Properties
- ✅ Safe & isolated environment
- ⚠️ Limited **RAM, disk, CPU**
- ⚠️ **No internet connection** (API-only limitation)
- ✅ Pre-installed libraries available out of the box
- ❌ Not every coding environment supported

### Contrast with Claude AI/Desktop
- Claude AI/Desktop sandbox **does** have internet
  - Can download/install packages
- API sandbox does **not**

## Files API

### Role
- Storage layer for files used in/produced by the container
- Pairs naturally with the Code Execution Tool

### Typical Workflow
- **Upload** input file → get `file_id`
- File is made available inside the container
- Skill/code reads, processes, writes new files
- **Download** generated files via `file_id`

### Example Scenario
- 💡 User asks Claude to summarize input → save summary to `.txt`
  - Upload input
  - Container runs skill
  - Download generated summary

## How Skills Plug In

- Skills live in a **skills directory** inside the container
- Claude reads `SKILL.md` first (progressive disclosure)
- Pulls in supporting files (templates, scripts) only when needed
- 📌 **Requirement:** to use skills via the API, you **must** also enable the Code Execution Tool

## API Request Anatomy

### Required Beta Headers
- `skills` beta
- `code-execution` beta
- `files-api` beta (when sending/receiving files)

### Key Parameters
- `container` — keyword arg holding the **list of skills**
  - Custom skills (by skill ID + version)
  - Built-in skills (e.g. `docx`)
- `tools` — must include code execution tool
- `messages` — user prompt + file references

### Skill Management Endpoints
- `skills.upload` — upload a skill directory
- `skills.list(source="custom")` — list only your custom skills
- Versioning
  - Reference a specific timestamp/version
  - Or use the **latest** version
- Deletion (programmatic)
  - 1️⃣ List all **versions** of the skill
  - 2️⃣ Delete every version
  - 3️⃣ Delete the underlying skill

## Walkthrough 1 — Practice Questions Skill

### Inputs
- Custom skill: *generating practice questions*
- Lecture notes folder
- Source file: `notes04.tex` (LaTeX)

### Steps
- Load env vars + helper for finding files in a directory
- **Upload skill directory** via `files_from_dir` → get skill ID
- Confirm via `.list(source="custom")`
- **Upload `notes04.tex`** via Files API → get file object
- Build message with **Sonnet** + container (skill) + tools (code execution)
- Send request

### What Claude Does (observed)
- Detects the right skill
- Reads **only** `SKILL.md` first (progressive disclosure)
- Reads YAML frontmatter + LaTeX content
- Reads `assets/markdown_template.md` when format is needed
- Generates questions in the skill's required structure
- Writes output file via code execution
- Copies file to **output directory**
- Returns a `file_id`

### Output Structure (from the skill)
- True/false questions
- Explanatory questions
- Coding questions
- Use case applications

### Downloading the Result
- Extract `file_id` from response
- Download with Files API + beta headers
- Save locally as `notes04.md`
- Preview as rendered markdown

### Evaluation Notes
- ✅ Output matched skill spec
- 💡 Add **unit tests** to harden this
- Iterate by modifying the skill, re-uploading

## Walkthrough 2 — Time Series + `docx`

### Inputs
- Custom skill: *analyzing time series*
- Built-in skill: **`docx`**
- Data file: retail sales **CSV**

### Why Combine Skills
- Custom skill → analysis & visualizations
- `docx` skill → produce a polished **Word document** with results + plots

### Request Construction
- Upload custom skill → skill ID
- Note: `.list()` without `source="custom"` also reveals **built-in skills**
- Upload CSV via Files API
- `container` includes:
  - Custom skill (ID + version)
  - Anthropic built-in `docx` skill
- Same beta headers: skills, code execution, files API

### Execution Trace
- Reads **both** `SKILL.md` files (custom + `docx`)
- Inspects CSV — first ~20 lines for columns/types
- Runs **diagnostics** script from skill
- Runs **visualize** script from skill
- Reads `summary.txt` produced by analysis
- Uses `docx` skill (progressive disclosure — only the markdown→docx path)
- Generates Word document with:
  - Overview
  - Statistics
  - Plots / visualizations
  - Statistical analysis
- Copies `.docx` to output dir → returns `file_id`

### Download & Inspect
- Find `file_id`, download as `.docx`
- 📌 Confirms skill + built-in skill composed correctly
- Re-evaluate; modify skill if needed

## Mental Model

- 💡 Skills are **portable**; the *runtime* differs
- Claude AI/Desktop = batteries-included runtime
- API = **bring-your-own runtime**
  - Code Execution Tool = the *computer*
  - Files API = the *disk* / transport
  - Skills = the *playbooks* Claude follows
- 🔑 **Progressive disclosure** keeps token use lean — only `SKILL.md` is read until more is needed

## Key Takeaways
- 📌 To use skills via the **Messages API**, you **must** enable both the **Code Execution Tool** and the **Files API**
- ⚠️ Skills created in Claude AI / Desktop do **not** transfer to the API or Claude Code — re-upload them
- 🔑 Workflow pattern: **upload skill → upload input file → call API with `container` + tools → download result via `file_id`**
- 💡 Combine **custom skills** with **built-in skills** (e.g. `docx`) in a single `container` for richer outputs
- ⚠️ API sandbox has **no internet** and limited resources — unlike Claude AI/Desktop
- ✅ Always send the three beta headers: **skills**, **code-execution**, **files-api**
- 📌 Deleting a skill requires deleting **all versions first**, then the skill itself
- 💡 **Progressive disclosure** — Claude reads `SKILL.md` first and pulls deeper assets only on demand