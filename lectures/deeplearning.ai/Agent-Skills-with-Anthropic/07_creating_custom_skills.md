---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Agent Skills: Structure & Best Practices

## Skill Anatomy
### Required: `SKILL.md`
- **YAML Frontmatter**
  - 🔑 `name` — required
  - 🔑 `description` — required
- **Body** — instructions & content
- **External references** — loaded only when needed
### Optional Fields
- `license`
- `compatibility`
- Arbitrary key-value metadata
- ⚠️ Spec is *actively evolving* — some skills won't follow it exactly

## Naming & Description
### Why It Matters
- 💡 How Claude **detects** when to invoke the skill
- 💡 How Claude **understands** what the skill does
### `name` Rules
- Lowercase letters, numbers, hyphens only
- Character limit applies
- 📌 Prefer **verb + -ing** form (e.g. `generating-practice-questions`)
### `description` Rules
- State **what** it does
- State **when** to use it
- Lean into **trigger keywords** that should activate it

## Writing the Skill Body
### Structure Principles
- Step-by-step instructions for predictable workflows
- Specify **edge cases** explicitly
- 📌 If a step is skippable, explain *why*
- ⚠️ Keep under **~500 lines** — offload the rest to references
- Use **forward slashes** in paths (cross-platform)
### Degree of Freedom
- **Low freedom** — best practices, deterministic workflows
- **High freedom** — creative output (colors, fonts, styles)
- 💡 Match the freedom to the task type
### Composition Strategy
- ✅ Many small, sequential, well-named skills
- ❌ One giant skill that does everything
- 📌 Systems handle **100+ skills** if named clearly

## Optional Directories
### `scripts/`
- Executable code
- Must include **error handling**
- Must include **clear documentation**
### `references/`
- Supplementary docs / reference files
- 📌 Instruct skill to read entire file if long
### `assets/`
- Output **templates**
- Images, logos, schemas, data files
### Progressive Disclosure
- 💡 Load files **only when needed** → saves tokens & context
- ⚠️ Folder names are *standard but not universal* yet

## Example 1: Generating Practice Questions
### Description
- Educational practice questions from lecture notes
- Audience: teachers / instructors testing understanding
### Skill Sections
- **Supported input formats**
  - Specifies libraries to use
  - Specifies text-extraction approach
- **Question structure** *(strict order)*
  - True/False
  - → ... →
  - Realistic applications
  - Each type has sub-guidelines
- **Output format**
  - Depends on user request
  - 📌 Templates live in `assets/` — *not* inline
    - Markdown template
    - LaTeX template
- **Domain examples** → linked from `references/`

## Example 2: Analyzing Time Series Data
### Goal
- Characterize a CSV before forecasting
### Deterministic Workflow
- 📌 Same exact order, every run
- Input format spec
  - Required columns
  - Required data types
- Run scripts in sequence
- Optional: generate plots
- Report `summary.txt` + relevant plots
- Use `interpretation.md` for guidance
### Python Scripts
- `visualize.py`
  - Time series plot, histogram
  - Rolling stats, box plots
  - Autocorrelation, decomposition
- `diagnose.py`
  - Data quality
  - Distribution
  - Stationarity tests
  - Seasonality, trend, autocorrelation
  - Transform recommendation
### Output Contract
- Predictable file tree
- Specific folders for plots, text, summary
### Dependencies
- ⚠️ List Python libraries explicitly
- Ensure they're installed before scripts run

## Evaluating Skills
### Static Review with `skill-creator`
- Run your skill *through* the skill-creator skill
- Checks frontmatter, conciseness, duplication, structure
- 📊 Practice questions skill: **9/10** — improve conciseness
- 📊 Time series skill: **higher** — strong on duplication & frontmatter
### Using Claude Code
- Claude Code has **no built-in skills** by default
- Install via **marketplace**
  - `anthropic/skills` repo
  - `document-skills` collection (Excel, PPT, Word, PDF)
  - `example-skills` collection (incl. skill-creator)
- Install at **project scope** → restart → `/skills`
- 💡 Dispatch **subagents in parallel**, one per skill, for fast review
### Behavioral Testing (Skill Unit Tests)
- 📌 Treat skills like software — write a test harness
- **Practice questions tests**
  - Queries: save to `.md`, `.tex`, `.pdf`
  - Verify correct PDF library used
  - Verify learning objectives extracted
  - Verify question types & guidelines
  - Verify correct templates from `assets/`
  - ✅ LaTeX must compile
- **Time series tests**
  - Assume Python scripts already unit-tested
  - Verify **workflow step order**
  - Verify optional plot step when requested
  - Verify summary + interpretation returned
  - Verify output folder structure
- 📌 Always gather **human feedback**
- 📌 Test across **every model** you'll deploy on

## Key Takeaways
- 🔑 **Name + description** are mission-critical — they decide *if* and *when* a skill triggers
- 💡 **Progressive disclosure**: keep `SKILL.md` lean, offload to `scripts/`, `references/`, `assets/` loaded only when needed
- 📌 Prefer many **small, composable, sequential** skills over one monolith — systems handle 100+
- ⚠️ Cap `SKILL.md` at **~500 lines**; use forward slashes for cross-platform safety
- ✅ Match **degree of freedom** to the task: deterministic for workflows, loose for creative work
- 💡 Evaluate skills two ways: **static** (run through `skill-creator`) and **behavioral** (unit-test-style harness with human feedback across models)