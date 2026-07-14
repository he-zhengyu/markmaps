---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Ch. 15: Write The Comments First

## 15.1 Delayed comments are bad comments
- Common excuses for delaying documentation
  - "Code is still changing" — fear of rewriting comments
  - Documentation viewed as *drudge work*, so it's postponed
- ⚠️ Consequence 1: comments never get written at all
  - Easy to keep delaying; code "will be more stable soon"
  - Backlog grows huge → task even less attractive
  - Never a convenient time to stop and fill in comments
  - Rationalized: fix bugs / build features instead → more undocumented code
- ⚠️ Consequence 2: late comments are low quality
  - You've mentally **checked out**; eager to move on
  - Quick pass, just enough comments "to look respectable"
  - Memories of design decisions have gone **fuzzy**
  - Written while staring at code → comments merely *repeat the code*
  - Non-obvious design ideas forgotten → most important content missing

## 15.2 Write the comments first
- The comments-first workflow (for a new class)
  - Write the **class interface comment** first
  - Write interface comments + signatures for key **public methods** (bodies empty)
  - **Iterate** on these comments until structure feels right
  - Declare + comment key **instance variables**
  - Fill in **method bodies**, adding implementation comments as needed
  - New methods/variables discovered mid-coding
    - New method → interface comment *before* the body
    - New variable → comment written with the declaration
- 💡 Code done ⇒ comments done — never a comment backlog
- Benefit 1: **better comments**
  - Design issues fresh in mind → easy to record
  - Interface comment before body → focus on **abstraction**, not implementation
  - Comments noticed and fixed during coding/testing → improve over development

## 15.3 Comments are a design tool
- Benefit 2 (most important): **improves system design**
  - 💡 Comments are the *only* way to fully capture abstractions
  - Writing them early lets you review/tune abstractions before coding
  - 🔑 Writing a good comment forces you to identify the **essence** of a thing
  - Skipping this early step = "just hacking code"
- 💡 Comments as a **canary in the coal mine of complexity**
  - Long comment needed ⇒ red flag: poor abstraction
  - Ties to Ch. 4: classes should be **deep** — simple interface, powerful function
  - Interface comment = best gauge of interface complexity
    - ✅ Short, simple, complete comment → simple interface
    - ❌ Only describable by a long, complicated comment → complex interface
  - Depth test: compare interface comment vs. implementation
    - Comment must cover all major implementation features ⇒ method is **shallow**
  - Same for variables: long comment ⇒ wrong **variable decomposition**
- 📌 Red Flag: **Hard to Describe**
  - A method/variable comment should be *simple yet complete*
  - Difficulty writing it ⇒ likely design problem in the thing described
- ⚠️ Caveat: only valid if comments are complete and clear
  - Incomplete or cryptic comments don't measure depth

## 15.4 Early comments are fun comments
- Benefit 3: comment-writing becomes **enjoyable**
- Early design phase = most enjoyable part of programming
  - Fleshing out abstractions and class structure
  - Comments record and *test* design-decision quality
- Goal: design expressible **completely and clearly in fewest words**
  - Simpler comments → better feeling about design
  - Finding simple comments is a source of **pride**
- 💡 If programming *strategically* (great design > code that merely works), commenting is fun — it's how you identify the best designs

## 15.5 Are early comments expensive?
- Revisiting the delay argument: "avoid reworking comments as code evolves"
- Back-of-the-envelope calculation
  - 📊 Typing code + comments ≈ ≤10% of total development time
  - 📊 Even if half of lines are comments → commenting ≈ ~5% of dev time
  - Delaying saves only a fraction of that ≈ negligible
- Hidden savings of comments-first
  - Abstractions **more stable** before coding begins → saves coding time
  - ❌ Code-first: abstractions evolve mid-coding → more code revisions
- 💡 All factors considered, comments-first may be *faster overall*

## 15.6 Conclusion
- Invitation: try comments-first; stick with it long enough to adjust
- Then evaluate its effect on
  - Quality of your comments
  - Quality of your design
  - Enjoyment of software development
- Author asks readers to report whether their experience matches his

## Key Takeaways
- 📌 Write comments **at the start**, as part of design — not after coding
- Delayed comments → often never written, and repeat code instead of capturing design
- Three benefits: better comments, better design, more fun
- 💡 Comments are the only full record of **abstractions** — the core of good design
- 🔑 Hard-to-describe = red flag; long comments signal shallow methods or bad decomposition
- 📊 Commenting is ~5% of dev time — delaying saves almost nothing; comments-first may even be faster