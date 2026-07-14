---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Chapter 14: Choosing Names

## Why Names Matter
- Names are a **form of documentation**
- Good names → easier understanding, fewer errors
- Poor names → ambiguity, misunderstandings, bugs
- 💡 **Complexity is incremental**: one mediocre name matters little, thousands matter a lot

## 14.1 Example: Bad Names Cause Bugs
### The Sprite Bug
- Distributed OS built with grad students (late 1980s–early 1990s)
- Symptom: file data blocks randomly turned to zeroes
- Rare, hard to reproduce; took **6 months** to fix
### Root Cause
- Variable `block` used for **two purposes**
  - Physical block number on disk
  - Logical block number within a file
- Logical block used where physical block was needed → unrelated disk block zeroed
- Readers reflexively assumed `block` = physical block; name created a mental block
### Fixes That Would Have Prevented It
- Distinct names: `fileBlock` vs `diskBlock`
- ✅ Even better: **distinct types** so they can't be interchanged
### Lesson
- ⚠️ Don't settle for names that are just "reasonably close"
- 📌 Take extra time for **precise, unambiguous, intuitive** names — it pays for itself

## 14.2 Create an Image
- Goal: name creates an **image in the reader's mind**
- Conveys what the entity **is** — and what it **is not**
- 💡 Test: "Seen in isolation, how closely can someone guess what it refers to?"
- ⚠️ Names become unwieldy beyond 2–3 words
- 🔑 **Names are a form of abstraction**: highlight what's most important, omit the rest

## 14.3 Names Should Be Precise
### Red Flag: Vague Name
- ⚠️ A name broad enough to mean many things conveys little and invites misuse
### Examples of Imprecise Names
- `getCount()` → count of what? Better: `numActiveIndexlets`
- `x`, `y` for character position in file → better: `charIndex`, `lineIndex`
- `blinkStatus` (boolean) → "status" says nothing about true/false
  - Better: `cursorVisible`
  - 📌 Boolean names should be **predicates**
- `VOTED_FOR_SENTINEL_VALUE` → says it's special, not what it means
  - Better: `NOT_YET_VOTED`
- `result` in a method with no return value
  - ❌ Misleadingly implies a return value
  - ❌ Says nothing about content → better: `mergedLine`, `totalChars`
  - ✅ Acceptable when it actually holds the return value
- Linux kernel: `struct socket` vs `struct sock`
  - Too similar to distinguish
  - Better: `struct sock_base` and `struct inet_sock`
### Exceptions: Generic Names OK
- ✅ `i`, `j` as loop variables **if the loop spans only a few lines**
- If the whole usage range is visible, meaning is obvious from code
- Longer loops need more descriptive names
### Names Can Be Too Specific
- `delete(Range selection)` — implies UI-selected text only
- Method works on any range → use generic `range`
### Red Flag: Hard to Pick Name
- ⚠️ Difficulty finding a precise, intuitive name hints at unclean design
- 💡 Consider refactoring: one variable representing several things → split it
- Choosing names can **improve your design** by exposing weaknesses

## 14.4 Use Names Consistently
- Pick one name per common purpose; use it everywhere
- Example: file system always uses `fileBlock` for block index within a file
- 💡 Like reusing a class: knowledge transfers instantly across contexts
### Three Requirements of Consistency
- Always use the common name for the given purpose
- Never use the common name for anything else
- Purpose narrow enough that all uses have the **same behavior**
  - ⚠️ Violated in the Sprite `block` bug
### Multiple Similar Variables
- Add distinguishing prefixes: `srcFileBlock`, `dstFileBlock`
### Loops
- `i` always outermost, `j` for nested → readers make instant safe assumptions

## 14.5 Avoid Extra Words
- Every word must carry useful information; clutter causes line wraps
- ❌ Generic nouns add nothing: `fileObject` → `file`
- ❌ Type info in names: `filePtr`
  - Extreme case: **Hungarian Notation** at Microsoft, e.g. `arru8NumberList`
  - Modern IDEs show declarations/types → type prefixes unnecessary
- ❌ Repeating the class name in instance variables
  - `fileBlock` inside class `File` → just `block` (unless multiple block types)

## 14.6 A Different Opinion: Go Style Guide
### Go's Position
- Names should be very short, often single characters
- Andrew Gerrand: long names obscure what the code does [Go talk](https://talks.golang.org/2014/names.slide#1)
- Example: `RuneCount` with `i`, `n`, `b` vs `index`, `count`, `buffer`
- Go culture reuses short names: `ch` = character or channel; `d` = data/difference/distance
### Ousterhout's Response
- Longer version no harder to read; `count` clearer than `n`
- ✅ Short names OK **if used consistently system-wide** for one meaning
- ⚠️ Ambiguous short names risk confusion — like the `block` bug
- 💡 **Readability is determined by readers, not writers**
  - Complaints of cryptic code → use longer names
### Point of Agreement
- 📌 Gerrand: the greater the distance between declaration and use, the longer the name should be
- The `i`/`j` loop rule is an instance of this

## 14.7 Conclusion
- Good names make code **obvious**: first guess about behavior is correct
- **Investment mindset** (Chapter 3): small upfront cost, easier future work, fewer bugs
- Naming skill is itself an investment
  - Frustrating and slow at first
  - With experience, good names come almost for free

## Key Takeaways
- 💡 Names are documentation and abstraction — they shape how readers think
- Two properties of good names: **precision** and **consistency**
- ⚠️ Vague names and hard-to-name entities are red flags for design problems
- Avoid words that add no information (type prefixes, generic nouns, class-name repeats)
- Short names work only with strict system-wide consistency; readers judge readability
- Investing in naming pays off: fewer bugs, easier maintenance, faster over time