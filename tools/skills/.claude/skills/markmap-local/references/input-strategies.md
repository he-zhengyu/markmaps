# Input Strategies Reference

How to extract structure from different source material types for markmap generation.

---

## Table of Contents

1. [Book Chapters / Articles](#book-chapters--articles)
2. [Lecture / Video Transcripts](#lecture--video-transcripts)
3. [Subtitles (.srt / .vtt)](#subtitles-srt--vtt)
4. [Structured Notes / Outlines / Markdown](#structured-notes--outlines--markdown)
5. [PDFs](#pdfs)
6. [Raw Text / Brainstorms / Freeform](#raw-text--brainstorms--freeform)
7. [Code / Technical Documentation](#code--technical-documentation)
8. [Meeting Notes](#meeting-notes)
9. [Research Papers](#research-papers)

---

## Book Chapters / Articles

Book chapters have explicit or implicit structure — lean on it.

1. **Find the argument spine**: What is the chapter's main thesis? This becomes the root or a prominent H2 branch.
2. **Map sections to branches**: Each major section or heading → H2 node. Subsections → H3 or list items.
3. **Extract key concepts, not sentences**: A 3-paragraph argument about "why caching fails at scale" becomes a single node like `Caching failures at scale` with child nodes for each reason.
4. **Preserve examples as leaf nodes**: Important examples or data points go one level below the claim they support. Label concisely (e.g., `Example: Netflix 2015 outage`).
5. **Capture definitions**: If the chapter introduces terms, give each a node with the definition as a child.
6. **Don't reproduce paragraphs**: Compress ruthlessly. A page of prose might yield 3–5 nodes.

---

## Lecture / Video Transcripts

Transcripts are messy — filler, repetition, tangents, non-linear flow. Extract the *intellectual structure*, not a timeline.

1. **Read the full transcript first** before building any hierarchy. Speakers revisit topics; you need the full picture.
2. **Identify topic segments**: Where does the speaker shift topics? Each becomes an H2 branch. Ignore chronological order — merge segments about the same topic.
3. **Strip verbal noise**: Ignore filler ("so basically what I'm saying is..."), self-corrections, off-topic tangents (unless they contain a useful insight).
4. **Reconstruct logical structure**: A lecturer might explain concept A, give example B, then state principle C. In the map, C is the parent — A and B are children — even though C was said last.
5. **Preserve memorable phrases**: If the speaker coins a term or uses a vivid phrase, keep it as node text.
6. **Estimate topic weight**: Longer segments → more child nodes. Brief mentions → single node.

---

## Subtitles (.srt / .vtt)

Subtitles are just transcripts with timestamps. Same strategy as transcripts, plus:

1. **Strip timestamp lines and formatting tags** (`<i>`, `<b>`, position markers) during preprocessing.
2. **Merge subtitle fragments into sentences**: Subtitles split sentences across multiple entries. Rejoin them before analyzing.
3. **Use timestamps as bookmarks** (optional): For large videos, you can note approximate timestamps in leaf nodes, e.g., `📌 ~12:30 — Demo of the technique`. This helps users jump back to the relevant section.
4. **Handle multilingual subtitles**: If the subtitles are bilingual, pick the primary language for the map and note translations only for key terms.

**SRT preprocessing** — strip cue numbers and timestamps:
```
Remove lines matching: /^\d+$/
Remove lines matching: /^\d{2}:\d{2}:\d{2}[,.]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[,.]\d{3}/
Remove empty lines
Join remaining lines into paragraphs
```

**VTT preprocessing** — also strip the `WEBVTT` header and any `NOTE` blocks.

---

## Structured Notes / Outlines / Markdown

Simplest case — the hierarchy often maps directly.

1. Convert headings to tree levels (`#` → root, `##` → H2, `###` → H3).
2. Bullet points become list-item nodes.
3. Collapse deeply nested lists if they exceed 5 levels — promote or merge.
4. Merge near-duplicate points.
5. If the original uses numbered lists for sequences, preserve the numbering in node text (e.g., `1. Install dependencies`).
6. Convert tables into branches: table title → parent node, each row → child with key columns as text.

---

## PDFs

PDFs vary wildly. Identify the type first:

- **Text-heavy PDF** (textbook, report): Extract text, treat as book chapter / article.
- **Slide deck PDF**: Each slide → an H2 branch. Slide title → branch label. Bullet points → children.
- **Scanned / image PDF**: OCR first, then treat as text. Note that OCR quality affects output.
- **Form PDF**: Probably not a good candidate for markmap — tell the user.

For all PDFs, use the pdf-reading skill or file-reading skill to extract content before applying the appropriate strategy above.

---

## Raw Text / Brainstorms / Freeform

Unstructured text needs you to *impose* structure.

1. **Read everything first** — understand the themes.
2. **Cluster related ideas**: Group sentences or fragments by topic. Each cluster → an H2 branch.
3. **Find a root theme**: What ties everything together? That's your H1.
4. **Order branches logically**: Chronological, by importance, by category — pick what fits.
5. **Don't force depth**: If the content is naturally flat (a list of 10 unrelated ideas), a wide shallow map is fine.

---

## Code / Technical Documentation

Technical content has natural hierarchies: modules, classes, functions, parameters.

1. **API documentation**: Module → H2, Class/Function → H3, Parameters/Returns → list items. Use `code` formatting for identifiers.
2. **Architecture docs**: System → H2 for each component, dependencies and data flows as children.
3. **README files**: Follow the existing heading structure. Add key details from code examples as leaf nodes.
4. **Error handling / troubleshooting guides**: Group by error category → specific errors → solutions.

---

## Meeting Notes

Meeting notes are semi-structured — agenda items, decisions, action items.

1. **Meeting topic** → root node.
2. **Agenda items** → H2 branches.
3. **Discussion points** under each agenda item → list items.
4. **Decisions** → highlighted with ✅ or 📌.
5. **Action items** → branch with owner names and deadlines as children.
6. **Open questions** → branch with ❓ markers.

---

## Research Papers

Academic papers have a standard structure — leverage it.

1. **Paper title** → root node.
2. **Standard sections**: Abstract (summarized as 2–3 nodes), Introduction (problem statement + motivation), Methods, Results, Discussion, Conclusion → each an H2 branch.
3. **Key findings** → highlighted with 💡 or 📌.
4. **Figures / tables** → referenced as leaf nodes (e.g., `Fig. 3: Accuracy vs. training size`).
5. **Citations** → only include if central to the argument (e.g., `Based on Smith et al. 2023`).
6. **Limitations** → ⚠️ markers.
