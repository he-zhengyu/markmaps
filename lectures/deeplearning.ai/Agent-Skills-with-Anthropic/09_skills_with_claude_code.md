---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Skills & Sub-Agents in Claude Code

## Project Setup
### Application Context
- **CLI to-do app** built with Claude Code
- Commands: `add`, `done`, `list`, (later) `edit`, `clear`
- Tech stack
  - Python + **Typer** (CLI framework)
  - **dataclasses** for models
  - **Rich** for terminal display
  - **JSON file** for persistence
  - **uv** for dependency management

### `CLAUDE.md` File
- 🔑 Project-level context file always in scope
- Created via `/init` or manually
- Contains
  - Project purpose & tech stack
  - Architecture conventions
  - Folder/file layout
- 💡 Use for **global** instructions every conversation needs

### Architecture Pattern
- Entry point + per-command Python files
- `models.py` — dataclasses (`Priority`, `Task`)
- `storage.py` — persistence & (de)serialization
- `display.py` — Rich terminal formatting
- `constants.py` + `tests/`

## Project Skills
### Skill Location & Loading
- Stored in `.claude/skills/`
- 📌 Project-level vs. user-level (`~`) skills
- ⚠️ Restart Claude Code after creating a new skill
- View with `/skills` command
- Token cost shown per skill

### Skill 1 — `adding-cli-command`
#### Purpose
- Predictable workflow for new Typer commands
- Encodes **coding style** and library conventions

#### Workflow Encoded
- Place new file in `commands/` directory
- Register in `commands/__init__.py`
- Use modern `Annotated` type hints
- Call `display.success()` / `display.info()` for output
- Define flags with shorthand, longhand, help text
- Confirm before destructive actions (e.g. hard delete)

#### Why Not Put in `CLAUDE.md`?
- 💡 Conventions only needed for **command creation**
- Load on demand → keeps context window lean
- Generic naming (`CLI app`) → portable across projects

### Skill 2 — `generating-cli-tests`
#### Purpose
- Generate **pytest** tests for Typer commands
- Triggered by *"write tests"* / *"add test coverage"*

#### Patterns Encoded
- **Fixtures** for temp storage & sample data
- **Arrange → Act → Assert** structure
- Per-command test scenarios (read, add, edit…)
- Edge cases checklist
  - ⚠️ Invalid input
  - ⚠️ State / confirmation flows
  - ⚠️ Not-found cases
- Test runner commands (verbose, single-file)

### Skill 3 — `reviewing-cli-command`
#### Purpose
- Validate that generated commands meet conventions
- Acts as an **evaluation layer** over other skills

#### Review Checklist
- ✅ Correct file location & decorator
- ✅ Registered in `__init__.py`
- ✅ `Annotated` type hints used
- ✅ Proper flags & help text
- ✅ Error handling & exit codes
- Provides positive/negative examples
- Output: summary + suggested fixes

## Sub-Agents
### Why Sub-Agents?
- 💡 Offload work to keep main context lean
- Each sub-agent has **own context window**
- Returns only the result to parent agent
- Useful when iterating many test runs

### Creating Sub-Agents
- Use `/agents` command
- Project vs. user scope
- Manual configuration shows full structure
- Configure
  - **Name** (unique ID)
  - **Description** (when to dispatch)
  - **Tools** (least privilege)
  - **Model** (inherit from parent)
  - **Color** (visual marker)
  - **Skills** field — list by name

### ⚠️ Skills & Sub-Agents
- 🔑 Sub-agents do **not** inherit parent's skills
- Must explicitly list skills per sub-agent
- Entire `SKILL.md` is **pre-loaded** on dispatch
- ❌ No progressive disclosure of bundled files inside sub-agent

### Sub-Agent A — `code-reviewer`
- Uses skill: `reviewing-cli-command`
- Tools: `Bash`, `Glob`, `Grep`, `Read`
- Color: purple
- Generic prompt → reusable across projects

### Sub-Agent B — `test-generator-runner`
- Uses skill: `generating-cli-tests`
- Tools: `Bash`, `Glob`, `Grep`, `Read`, `Edit`, `Write`
- Color: yellow
- Triggered on *"test"* / *"run tests"*

## Putting It Together
### Workflow — Adding `edit` Command
- Main agent uses `adding-cli-command` skill
  - Reads existing files for convention
  - Creates `edit.py`
  - Registers in `__init__.py`
- Dispatch `code-reviewer` sub-agent
  - Returns warnings + suggested fixes
- Dispatch `test-generator-runner` sub-agent
  - Generates tests for `edit.py`
  - Runs `uv run` in verbose mode
- Main agent applies fixes from sub-agent output

### Workflow — Fixing Non-Compliant `clear.py`
- Scenario: teammate added command without skills
- `code-reviewer` finds 6 critical + 4 warnings
  - ❌ Wrong console output method
  - ❌ Bad flag format
  - ❌ Incorrect exit codes
  - ❌ Missing registration
- Main agent applies fixes
- `test-generator-runner` adds & runs tests
- ✅ All tests pass; conventions enforced

## Key Takeaways
- 💡 **Skills encode predictable workflows** — load only when needed instead of bloating `CLAUDE.md`
- 🔑 `CLAUDE.md` = always-on project context; **skills** = on-demand conventions
- 📌 Sub-agents isolate context — main agent stays focused on development while reviewers/testers run in parallel windows
- ⚠️ Sub-agents do **not** inherit skills — list them explicitly in the agent config
- ⚠️ Restart Claude Code after creating a skill, or it won't appear in `/skills`
- ✅ Pair a *generator* skill with a *reviewer* skill to get an automatic evaluation loop
- 💡 Keep sub-agent prompts **generic** and push specifics into skills for maximum reuse
- 📌 Give sub-agents **least-privilege tools** — only what the task requires