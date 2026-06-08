---
name: markmap
description: Generate interactive markmap mind maps from any content — learning notes, book chapters, lecture transcripts, video subtitles (.srt/.vtt), outlines, documents, PDFs, or structured/unstructured text. Use this skill whenever the user wants to create a mind map, markmap, mindmap, or visual knowledge tree, or says things like "markmap this", "turn this into a mind map", "visualize this as a mindmap", "create a markmap", "convert to markmap". Also trigger when the user uploads a document (PDF, markdown, text, subtitles) and asks to visualize, outline, or map its structure. Trigger for any request involving hierarchical visualization of content, knowledge mapping, study aids, revision maps, concept maps, or topic overviews — even if the user doesn't explicitly say "markmap". If the user uploads learning materials and wants a visual summary or overview, use this skill. Do NOT use for Lark MindNote (飞书思维笔记) — use the lark-mindnote skill instead. Do NOT use for Mermaid diagrams.
---

# Markmap Skill

Generate interactive, zoomable mind map HTML files from any source content using [markmap](https://markmap.js.org/). Markmap converts standard Markdown into beautiful, interactive SVG mind maps that users can zoom, pan, and collapse/expand.

---

## How Markmap Works

Markmap parses **standard Markdown** and maps its hierarchy into an interactive mind map:

- `# Heading 1` → root node (center of the map)
- `## Heading 2` → Level 1 branches
- `### Heading 3` → Level 2 branches
- `- list items` → child nodes under the nearest heading
  - Nested list items → deeper child nodes
- Inline Markdown is preserved: **bold**, *italic*, `code`, ~~strikethrough~~, ==highlight==, [links](url), and inline math `$...$`
- Code blocks and tables render inside nodes
- HTML comments `<!-- markmap: fold -->` control initial fold state

The output is a **self-contained HTML file** that loads markmap from CDN and renders an interactive SVG. No server needed — just open in a browser.

---

## Output Strategy

There are two ways to produce the markmap, depending on what the user needs:

### 1. HTML File (Default)

Generate a `.md` file with the structured content, then use the bundled script to produce a standalone `.html` file. This is ideal when the user wants a file to open, share, or bookmark.

### 2. Markdown Only

If the user explicitly asks for "just the markdown" or wants to paste it into the [markmap online editor](https://markmap.js.org/repl), VSCode extension, or Obsidian, output the raw Markdown in a code block and skip HTML generation.

**Default to HTML file output** unless the user says otherwise.

---

## Step-by-Step Process

### 1. Read the source material

- If an uploaded file is provided, read it fully first (use the file-reading skill for PDF, .srt, .vtt, etc.)
- Identify the input type — this determines your extraction strategy (see the reference file `references/input-strategies.md` for detailed guidance on each input type)

### 2. Extract the logical skeleton

Read `references/input-strategies.md` for type-specific instructions. The core principle across all types: **extract intellectual structure, not surface text**.

- For book chapters / articles: follow the argument spine — thesis → sections → evidence
- For lecture / video transcripts and subtitles: group by topic, not chronology; merge revisited topics
- For structured notes / outlines / markdown: respect existing hierarchy, clean up redundancy
- For raw text / brainstorms: impose structure by clustering related ideas

### 3. Write the Markdown

Structure the Markdown so markmap renders a clear, readable map:

<<<
# Root Topic

## Branch 1
### Branch a
- Key point
  - Supporting detail
  - Supporting detail
- Key point

### Branch b
- Key point
  - Supporting detail
  - Supporting detail
- Key point

## Branch 2
- Key point
  - Sub-point
    - Detail
>>>

**Markdown rules for markmap:**

- The single `# H1` becomes the root (center) node — use exactly one
- `## H2` headings become the main branches radiating out
- `### H3` and deeper headings create sub-branches
- List items (`-`) create child nodes under their parent heading or list item
- Keep node text concise — aim for under 50 characters per node, but never sacrifice clarity for brevity
- Use **bold** for key terms, `code` for technical identifiers, and *italic* for emphasis
- Recommended depth: 3–5 levels. Go deeper only when the material genuinely requires it
- Use `<!-- markmap: fold -->` after a heading or list item to collapse that branch by default (useful for large maps)
- Use `<!-- markmap: foldAll -->` to collapse a node and all its descendants

**Frontmatter options** (optional, placed at the top of the .md file):

```yaml
---
markmap:
  initialExpandLevel: 3
  maxWidth: 300
  colorFreezeLevel: 2
---
```

- `initialExpandLevel`: how many levels to expand on load (-1 = all, default)
- `maxWidth`: max pixel width per node (0 = no limit)
- `colorFreezeLevel`: freeze branch colors at this depth (0 = no freeze)
- `color`: custom color array, e.g. `['#2196F3', '#4CAF50', '#FF9800']`

### 4. Generate the HTML file

**First, ensure dependencies are installed** (only needed once per session):

```bash
cd /home/claude && npm list markmap-lib markmap-render 2>/dev/null || npm install markmap-lib markmap-render 2>&1
```

Then run the bundled generation script. Replace `<SKILL_DIR>` with the actual path to this skill's directory:

```bash
node <SKILL_DIR>/scripts/generate_markmap.mjs <input.md> <output.html>
```

If the script is not available or fails, fall back to markmap-cli:

```bash
npm install -g markmap-cli 2>/dev/null; npx markmap-cli <input.md> --no-open -o <output.html>
```

### 5. Present the output

Copy the HTML file to `/mnt/user-data/outputs/` and present it to the user with `present_files`. Also save the `.md` source file alongside it so the user can edit and regenerate later.

---

## Emoji and Visual Markers

Emoji render natively in markmap nodes and are useful for visual scanning. Use them sparingly — only where they aid comprehension.

| Marker | Meaning | Example |
|--------|---------|---------|
| ⚠️ | Warning / caveat | `- ⚠️ Rate limits apply` |
| ✅ / ❌ | Pro / Con | `- ✅ Fast iteration` |
| 💡 | Key insight | `- 💡 Caching is the bottleneck` |
| 🔑 | Definition / key term | `- 🔑 Idempotency: safe to retry` |
| 📌 | Important to remember | `- 📌 Deadline: March 30` |

Aim for roughly 10–20% of nodes having emoji. More than that creates visual noise.

---

## Quality Checklist

Before generating the final output, verify:

- [ ] Exactly one `# H1` root node
- [ ] Node text is concise (under 50 chars where possible)
- [ ] Depth stays within 3–5 levels for most branches
- [ ] No orphaned nodes or empty branches
- [ ] Markdown formatting (bold, code, links) is used where it adds value
- [ ] For large maps (30+ nodes), some branches use `<!-- markmap: fold -->` to keep the initial view manageable

---

## Examples

### Example: Technical Concept Overview

```markdown
# OAuth 2.0

## Grant Types
- Authorization Code
  - **Most secure** for server apps
  - Uses redirect URI + auth code exchange
  - ✅ Recommended for web apps
- Client Credentials
  - Machine-to-machine only
  - No user involvement
- Implicit *(deprecated)*
  - ⚠️ Tokens exposed in URL fragment
  - Replaced by Auth Code + PKCE
- Device Code
  - For input-limited devices (TV, CLI)

## Key Concepts
- 🔑 **Access Token**: short-lived credential
- 🔑 **Refresh Token**: used to get new access tokens
- **Scopes**: limit what the token can do
- **PKCE**: prevents auth code interception
  - Required for public clients

## Security
- ⚠️ Always use HTTPS
- ⚠️ Validate `state` parameter
- Store tokens securely
  - ❌ Never in localStorage
  - ✅ HttpOnly cookies or server session
```

### Example: Book Chapter Summary

<<<
# Thinking, Fast and Slow — Ch. 1

## Two Systems
- **System 1**: Fast, intuitive, automatic
  - Pattern recognition
  - Emotional reactions
  - 💡 Operates with little effort
- **System 2**: Slow, deliberate, analytical
  - Complex calculations
  - Conscious reasoning
  - ⚠️ Lazy — avoids engagement when possible

## Key Experiments
- Gorilla experiment
  - Selective attention blindness
  - System 1 filters what we see
- Müller-Lyer illusion
  - System 1 can't be "turned off"
  - Even knowing the trick doesn't help

## Implications
- 📌 Most decisions are System 1
- Overconfidence comes from System 1 fluency
- System 2 needed for: statistics, logic, planning
>>>
