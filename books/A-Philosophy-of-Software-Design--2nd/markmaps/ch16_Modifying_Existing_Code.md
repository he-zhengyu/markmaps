---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Ch.16 Modifying Existing Code

## Context: Software Evolves
- Development is **iterative and incremental**
- Design constantly evolving through evolutionary stages
- 💡 Mature system's design shaped more by **evolution** than initial conception
- Goal: keep complexity from **creeping in** as system evolves

## 16.1 Stay Strategic
### Tactical vs. Strategic (recap Ch.3)
- 🔑 **Tactical**: get it working fast, tolerate complexity
- 🔑 **Strategic**: great system design is the top goal
- ⚠️ "Working" isn't a high enough standard
### Typical Tactical Mindset in Changes
- "What is the **smallest possible change** that works?"
- Justified by discomfort with unfamiliar code / fear of new bugs
- ❌ Each minimal change adds special cases & dependencies
- ⚠️ Design gets a bit worse each step; problems accumulate
### Strategic Ideal for Modifications
- 📌 After each change, system looks **as if designed that way from the start**
- Resist the quick fix; ask if current design is still best
- Refactor to the **best possible design** if not
- ✅ Result: design *improves* with every modification
### Investment Mindset
- Extra refactoring time → cleaner system → faster future development
- Even without required refactoring, fix design imperfections you find
- 💡 "If you're not making the design better, you're probably making it worse"
### Real-World Compromises
- Tight deadline: 2-hour hack vs. 3-month refactoring
- Refactoring may break compatibility for other teams
- ✅ Ask: "Is this the **best I can do** given my constraints?"
- Seek middle ground: almost-as-clean fix in a couple of days
- Get time allocated to revisit after the deadline
- 📌 Organizations should budget a fraction of effort for **cleanup & refactoring**

## 16.2 Keep Comments Near the Code
### The Stale-Comment Problem
- Code changes easily invalidate comments
- ⚠️ Stale comments frustrate readers → distrust of *all* comments
### Core Rule: Proximity
- 💡 The farther a comment from its code, the less likely it gets updated
- Interface comment belongs **next to the method body** in the code file
### Header Files (C/C++)
- ❌ Interface comments in `.h` files are far from the code
- Developers won't see them while editing the body
- Users shouldn't read code or headers anyway
  - Use docs from tools like `Doxygen` / `Javadoc`
  - IDEs display method docs as you type
- ✅ Put docs where **developers working on the code** see them
### Implementation Comments
- ❌ Don't pile all comments at the top of a method
- ✅ Push each comment to the **narrowest scope** covering its code
- Per-phase comments just above each phase's first line
- Top-of-method overview of overall strategy is OK
  - e.g. `// Phase 1 / Phase 2 / Phase 3` outline
- 📌 Farther from code → comment should be more **abstract**

## 16.3 Comments Belong in Code, Not Commit Log
- ❌ Common mistake: detail only in the commit message
- Developers rarely think to scan the repository log
- Finding the right log message is tedious
- ✅ Test: will developers need this info later? → put it **in the code**
- Example: subtle bug that motivated a change
  - ⚠️ Undocumented → someone may undo it and re-create the bug
- Copy in commit message is fine, but code comes first
- 💡 Place docs where developers are **most likely to see them**

## 16.4 Avoid Duplication
### Document Each Decision Once
- ⚠️ Duplicated docs are hard to find & update consistently
- Find the **most obvious single place**
- e.g. tricky variable behavior → comment at its **declaration**
### When No Obvious Place Exists
- Use a `designNotes` file (Section 13.7)
- Or pick the best spot + short cross-references elsewhere
  - "See the comment in xyz for an explanation"
- ✅ Broken reference is **self-evident**; stale duplicate copy is not
### Don't Redocument Other Modules
- ❌ No comments before a call explaining the called method
- Readers should use the method's **interface comments**
- Tools show interface docs on hover/selection
### Reference External Docs
- ❌ Don't restate the HTTP protocol in your code — link a URL
- Features in user manual: `// Implements the Foo command; see the user manual`
- 💡 Readers must *find* all needed docs — you needn't *write* them all

## 16.5 Check the Diffs
- ✅ Before committing, scan **all changes** in the diff
- Verify each change is reflected in documentation
- Bonus catches: leftover **debugging code**, unfixed **TODO items**

## 16.6 Higher-Level Comments Are Easier to Maintain
- 💡 Abstract comments don't track code details
- Minor code changes don't invalidate them; only **behavior changes** do
- Some comments still must be detailed & precise (Ch.13)
- 📌 Most useful comments (non-repetitive) are also easiest to maintain

## Key Takeaways
- 📌 Treat every modification as a **design opportunity**, not just a patch
- After a change, the system should look **designed that way from the start**
- If you're not improving the design, you're probably degrading it
- Keep comments **close to their code**; farther away → more abstract
- Durable knowledge goes in the **code**, not the commit log
- Document each decision **exactly once**; cross-reference, don't copy
- Scan diffs pre-commit to sync docs and catch debris
- Higher-level comments survive change best