---
markmap:
  initialExpandLevel: -1
  maxWidth: 400
  colorFreezeLevel: 3
---

# A Philosophy of Software Design — Preface

## The Neglected Problem
- 80+ years of programming, little design discussion
- Well-explored adjacent topics
  - **Processes** — agile development
  - **Tools** — debuggers, version control, test coverage
  - **Techniques** — OOP, functional programming
  - **Patterns & algorithms**
- ⚠️ Core problem of **software design** remains untouched
- 📌 Parnas' 1971 paper *"On the Criteria to be used in Decomposing Systems into Modules"*
  - Field hasn't progressed much in 45 years

## Central Thesis
- 🔑 **Problem decomposition** — splitting a complex problem into independently solvable pieces
  - 💡 Most fundamental problem in computer science
  - Daily central task for programmers
- ⚠️ Not taught as a central topic in any university course
  - We teach `for` loops and OOP, *not* software design

## Why Quality Varies
- Huge variation in programmer productivity & skill
- Best programmers can't articulate their techniques
- Common assumption: design skill is **innate talent**
- 💡 Counter-evidence: excellence comes from *high-quality practice*
  - Reference: *Talent is Overrated* by Geoff Colvin
- Hypothesis: design skill separates great from average programmers

## Origin of the Book
- Born from **CS 190** at Stanford University
  - Set of software design principles
  - Projects to assimilate and practice them
- Taught like an English writing class
  - Iterative: draft → feedback → rewrite
  - Build software from scratch → code reviews → revise
- 💡 Principles are high-level, near philosophical
  - e.g. *"Define errors out of existence"*
  - Best learned by writing code, making mistakes, seeing fixes

## Author's Credibility
- ❌ No design classes or mentor when learning
- Ideas drawn from personal experience
- 📊 ~250,000 lines of code across many languages
- Built from scratch
  - 3 operating systems
  - File & storage systems
  - Debuggers, build systems, GUI toolkits
  - A scripting language
  - Interactive editors (text, drawings, slides, ICs)
- Read much code by others — good and bad
- Extracted **common threads**: mistakes to avoid, techniques to use
  - Every problem & technique personally experienced

## Caveats & Invitation
- ⚠️ Not the final word on software design
- An **opinion piece** — readers may disagree
  - If you disagree, understand *why*
- Goal: start a conversation, improve collective understanding
- Feedback channel
  - 📌 [software-design-book@googlegroups.com](mailto:software-design-book@googlegroups.com)
  - Google Group: **software-design-book**
  - Best contributions: compelling, simple examples
- 💡 Take suggestions *with a grain of salt*
  - Overarching goal = **reduce complexity**, above any single principle
  - If an idea doesn't reduce complexity, drop it

## Acknowledgments
- Reviewers offered comments on drafts
- Christos Kozyrakis coined **"deep"** / **"shallow"**
  - Replacing ambiguous *"thick"* / *"thin"*
- CS 190 students helped crystallize the ideas

## Key Takeaways
- 🔑 Software design's core is **problem decomposition**, yet it's rarely taught
- 💡 Great design skill comes from **practice**, not innate talent
- 📌 The single overriding goal is to **reduce complexity**
- Principles are guidelines — keep what reduces complexity, discard what doesn't
- ⚠️ The book is opinion grounded in firsthand experience, not final doctrine