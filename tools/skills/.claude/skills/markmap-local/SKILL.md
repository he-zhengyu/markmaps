---
name: markmap-local
description: Generate interactive markmap mind maps from any content — learning notes, book chapters, lecture transcripts, video subtitles (.srt/.vtt), outlines, documents, PDFs, or structured/unstructured text. Use this skill when the user explicitly asks for markmap.
---

# Markmap Skill

Generate Markdown mind maps from any source content using the [markmap](https://markmap.js.org/) format. Output is standard Markdown that the user can paste into the markmap online editor, VSCode extension, or Obsidian.

---

## How Markmap Works

Markmap parses **standard Markdown** and maps its hierarchy into an interactive mind map:

- `# Heading 1` → root node (center of the map)
- `## Heading 2` → Level 1 branches
- `### Heading 3` → Level 2 branches
- Heading 4–6 can also be used if appropriate
- `- list items` → child nodes under the nearest heading
  - Nested list items → deeper child nodes
  - If stepwise, use numbered list
- Inline Markdown is preserved: **bold**, *italic*, `code`, ~~strikethrough~~, ==highlight==, [links](url), and inline math `$...$`
- Code blocks and tables render inside nodes
- HTML comments `<!-- markmap: fold -->` control initial fold state

---

## PDF Helper: bookmarks.py

`bookmarks.py` extracts the bookmark tree from any PDF with accurate page numbers. The cached YAML file (`<pdf-stem>_bookmarks.yaml`, saved next to the PDF) avoids re-running the script on every request.

### Chapter markmap workflow (use this for any "markmap chapter N" request)

> **PDF page numbers**: Always use the PDF's physical page number (e.g., "294 of 453" shown in the viewer), NOT the printed book page number (e.g., "265"). The `bookmarks.py` script returns PDF page numbers directly — use them as-is.

```
1. Derive cache path:  <same dir as pdf>/<pdf-stem>_bookmarks.yaml
2. If cache does not exist:
     python3 /path/to/bookmarks.py <pdf> --format yaml -o <cache-path>
3. Read the cache JSON.
4. Find the entry whose title matches the target chapter (e.g. "19" or "Chapter 19").
5. Find the immediately following top-level chapter entry → its .page is the end boundary.
6. Page range = chapter.page  to  next_chapter.page - 1  (these are PDF page numbers)
7. Read PDF content: Read tool with pages: "start-end", in ≤20-page chunks if needed.
8. Generate detailed markmap from the content (section titles + explanations + examples).
```

**Do NOT** use the bookmark titles as the chapter markmap — they are only headings, not content.

### Whole-book markmap workflow

When the user wants a markmap of the **entire book**:

```
1. Derive cache path as above; create it if missing.
2. Run:  python3 bookmarks.py <pdf> --format markdown
3. The bookmark tree IS the markmap — output it directly, no content reading needed.
```

---

## Step-by-Step Process

### 1. Read the source material

- **PDF + chapter request:** follow the chapter markmap workflow above to determine the exact page range, then read those pages with the `Read` tool (`pages: "X-Y"`, ≤20 pages per call)
- **PDF + whole-book request:** follow the whole-book markmap workflow above
- **Other files** (.srt, .vtt, .md, etc.): read the relevant portions directly
- If the source has an existing tree-like structure (outline, TOC, nested headings), use it as the skeleton and enrich with content
- Identify the input type — this determines your extraction strategy

### 2. Extract the logical skeleton

The core principle: **extract intellectual structure, not surface text**.

- For book chapters / articles: follow the argument spine — thesis → sections → evidence
- For lecture / video transcripts and subtitles: group by topic, not chronology; merge revisited topics
- For structured notes / outlines / markdown: respect existing hierarchy, clean up redundancy
- For raw text / brainstorms: impose structure by clustering related ideas

### 3. Write the Markdown

Structure the Markdown so markmap renders a clear, readable map:

```markdown
# Root Topic

## Branch 1
- Key point
  - Supporting detail
  - Supporting detail
- Key point

## Branch 2
- Key point
  - Sub-point
    - Detail
```

**Markdown rules for markmap:**

- The single `# H1` becomes the root (center) node — use exactly one
- `## H2` headings become the main branches radiating out
- `### H3` and deeper headings create sub-branches
- List items (`-`) create child nodes under their parent heading or list item
- Keep node text concise — aim for under 50 characters per node, but never sacrifice clarity for brevity
- Use **bold** for key terms, `code` for technical identifiers, and *italic* for emphasis
- Recommended depth: 3–5 levels. Go deeper only when the material genuinely requires it
- Use `<!-- markmap: fold -->` after a heading or list item to collapse that branch by default (useful for large maps)

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

### 4. Present the output

Always write the Markdown to a `.md` file using the Write tool. Save it next to the source file (or in the current working directory if no source file). Tell the user the file path.

**Do NOT generate HTML.** No `npm install`, no script execution, no HTML output — just the `.md` file.

---

## Emoji and Visual Markers

Emoji render natively in markmap nodes and are useful for visual scanning. Use them sparingly — only where they aid comprehension.

| Marker | Meaning | Example |
|--------|---------|---------|
| ✅ / ❌ | Yes / No, Supported / Unsupported, Pro / Con | `- ✅ Idempotent` / `- ❌ Not thread-safe` |
| ⚠️ | Warning / caveat / gotcha | `- ⚠️ Rate limits apply in prod` |
| 💡 | Key insight / tip | `- 💡 Caching is the bottleneck here` |
| 🔑 | Key term / definition | `- 🔑 Idempotency: safe to retry` |
| 📌 | Must remember / pinned note | `- 📌 Deploy before migrating the DB` |
| 🚀 | Highlight / cutting-edge / best option | `- 🚀 Preferred approach for high throughput` |
| 💥 | Failure mode / breaking change | `- 💥 OOM crash under high load` |

Aim for roughly 10–20% of nodes having emoji. More than that creates visual noise.

---

## Quality Checklist

Before generating the final output, verify:

- [ ] Exactly one `# H1` root node
- [ ] Branches are balanced — no single branch with 15 children while others have 2
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
  - 🚀 Recommended for web apps
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
- 💥 Token leakage via open redirect
```

### Example: Book Chapter Summary

```markdown
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
- 🚀 Train System 2 for high-stakes decisions
- 💥 System 1 errors: bias, anchoring, framing
```
