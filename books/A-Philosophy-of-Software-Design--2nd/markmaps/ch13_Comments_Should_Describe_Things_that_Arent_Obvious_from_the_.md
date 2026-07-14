---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Ch 13: Comments Should Describe Things that Aren't Obvious from the Code

## Core Premise
- 🔑 Code can't capture all info in the developer's mind
- Comments record that info for future developers
- 📌 Guiding principle: describe what **isn't obvious from the code**
- Things not obvious from code
  - Low-level details (e.g. are range indices inclusive/exclusive?)
  - **Why** code is needed or implemented a certain way
  - Rules followed (e.g. "always invoke a before b")
- 💡 Most important reason: **abstractions**
  - Code is too detailed to reveal the abstraction
  - Comments give a simpler, higher-level view
  - Users should understand a module from declarations + comments alone
- Good comments explain at a **different level of detail** than code
  - More detailed (precision) or less detailed (intuition)

## 13.1 Pick conventions
- Decide what to comment and the format
- Follow document compilation tools if available
  - `Javadoc` (Java), `Doxygen` (C++), `godoc` (Go)
  - ✅ Imperfect conventions, but tool benefits outweigh
- No existing conventions? Borrow from a similar language/project
- Two purposes of conventions
  - Consistency → easier to read and understand
  - Ensure you actually write comments
- Four comment categories
  - **Interface**: precedes a class/function declaration; describes the abstraction, behavior, args, return, side effects, exceptions, caller requirements
  - **Data structure member**: next to a field declaration
  - **Implementation comment**: inside code; how it works internally
  - **Cross-module comment**: dependencies crossing module boundaries
- 📌 First two categories matter most
  - Every class, class variable, and method should have one
  - ✅ Easier to comment everything than debate each case
  - Implementation comments often unnecessary
  - Cross-module comments rare but important when needed

## 13.2 Don't repeat the code
- ❌ Most common failure: comment info deducible from adjacent code
  - Example: line-by-line comments like `# Get pointer copy`
  - ⚠️ Comments at the same level of detail as the code are rarely useful
- Self-test 💡: could someone who's never seen the code write this comment just by looking at the code?
  - If yes → the comment adds nothing
- ⚠️ Red Flag: **Comment Repeats Code**
  - Includes using the same words as the entity's name
  - e.g. "Obtain a normalized resource name" for `getNormalizedResourceNames`
  - Only new word in one example was "to"!
- What's *missing* is the useful part
  - What is a "normalized resource name"? Units of padding? One side or both?
- ✅ First step: use **different words** than the name
  - Add info about the entity's *meaning*, not restate its name
  - Better `textHorizontalPadding` comment: blank space on left and right of each line, **in pixels**

## 13.3 Lower-level comments add precision
- 🔑 Precision: clarify the exact meaning of the code
- Most useful for variable declarations (instance vars, args, return values)
- Details comments should fill in
  - Units for the variable
  - Boundary conditions inclusive or exclusive?
  - Meaning of a permitted `null` value
  - Who frees/closes an owned resource?
  - Invariants (e.g. "list always has ≥1 entry")
- 📌 "The code" = the declaration next to the comment, not the whole app
- ⚠️ Most common problem: comments too vague
  - `// Current offset in resp Buffer` — what does "current" mean?
  - `lineWidths` TreeMap — keys? values? pixels or characters?
- Fixes shown
  - Precise: "position of first object not yet returned to client"
  - Rename `lineWidths` → `numLinesWithLength`; document entry format *and* what a missing entry means
- 💡 Think **nouns, not verbs**
  - Describe what the variable *represents*, not how it's manipulated
  - `receivedValidHeartbeat`: "True means a heartbeat received since election timer reset" — toggling behavior becomes easy to infer

## 13.4 Higher-level comments enhance intuition
- 🔑 Intuition: omit details; convey overall intent and structure
- Common for in-method comments and interface comments
- Bad example (RPC loop comment)
  - ❌ Partially repeats code ("if there is a LOADING readRPC")
  - ❌ Doesn't explain the overall purpose
- Better: "Try to append the current key hash onto an existing RPC to the desired server that hasn't been sent yet"
  - Reader can then explain nearly every statement in the loop
  - 💡 Provides a basis to *judge* the code's correctness
- Harder to write than lower-level comments
  - Ask: What is this code trying to do?
  - The simplest statement that explains everything?
  - The most important thing about this code?
- 💡 Essence of abstraction: step back from details, express one or a few simple ideas as a conceptual framework
- "How we get here" comments
  - Explain *why* the code executes, not just what it does
  - Very useful for methods invoked only in unusual situations

## 13.5 Interface documentation
- 📌 Most important role of comments: **define abstractions**
  - Code is too low-level; only comments can describe abstractions
- Separate interface comments from implementation comments
  - Interface: what users need to know to use the class/method
  - Implementation: how it works internally
  - 💡 If interface comments must describe implementation → the class is **shallow** (design clue)
- Class interface comment
  - High-level description of the abstraction (e.g. `Http` server class)
  - What each instance represents
  - Limitations (e.g. single-threaded, no concurrent access)
- Method interface comment contents
  - Behavior as perceived by callers (higher-level abstraction)
  - Each argument and return value — precise, with constraints and dependencies
  - Side effects (consequences affecting future behavior, not part of result)
  - Exceptions that can emanate
  - Preconditions (e.g. list must be sorted for binary search); minimize but document
  - Example: `Buffer::copy` Doxygen comment — caller never reads the body
- `IndexLookup` case study
  - Distributed storage: tables, indexes, range queries via `getNext()`
  - What users need to know (answers in 13.9)
  - Original comment's problems
    - ❌ First paragraph mostly implementation (RPC names, private config params)
    - ❌ States the obvious ("include IndexLookup.h", "providing all necessary information")
  - ✅ Shorter revision: what the class is for, what an instance represents, how methods work together
    - Usage examples helpful for deep classes with nonobvious patterns
    - Omits server crashes — invisible to users (auto-recovery)
- ⚠️ Red Flag: **Implementation Documentation Contaminates Interface**
- `isReady()` example
  - ❌ Original: DCFT/rule-based implementation talk, cryptic `RESULT_READY`
  - ✅ Revision: precise meaning of "ready"; must be invoked for progress; exact blocking semantics of return value

## 13.6 Implementation comments: what and why, not how
- Most methods are short → no implementation comments needed
- Goal: help readers understand **what** the code does, not how
  - Once "what" is known, "how" is usually easy
- Longer methods: comment before each major block
  - e.g. `// Phase 1: Scan active RPCs to see if any have completed.`
  - Helps readers navigate to the parts that matter
- Loops: comment describing what each iteration does
  - Abstract level, no extraction/increment details
  - Only for longer or complex loops
- Also explain **why**
  - Document tricky, non-obvious aspects
  - Bug fixes: reference the bug tracker instead of repeating details
    - e.g. "Fixes RAM-436, device driver crashes in Linux 2.4.x"
    - 💡 Avoids duplication in comments
- Local variables
  - Most need no comment if well-named and used within a few lines
  - Comment variables used over a large span of code
  - 📌 Focus on what the variable represents, not how it's manipulated

## 13.7 Cross-module design decisions
- Real systems have decisions affecting multiple classes
  - e.g. network protocol affects sender and receiver
  - ⚠️ Complex, subtle, account for many bugs → documentation crucial
- Biggest challenge: **where to put it** so developers naturally find it
- Case 1: obvious central place exists
  - RAMCloud `Status` enum: comment at end of the enum lists all 7 places to update when adding a value
  - Placed where new values are added — most likely to be seen
- Case 2: no obvious central place
  - RAMCloud zombie servers: code spread across modules, mutually dependent
  - ❌ Duplicating docs everywhere: awkward, hard to keep current
  - ❌ Docs in one dependent location: unlikely to be found
- Experimental approach: central `designNotes` file
  - Clearly labeled sections per topic (e.g. "Zombies")
  - Code sites carry a short pointer: `// See "Zombies" in designNotes.`
  - ✅ Single copy, easy to find when needed
  - ⚠️ Not near dependent code → may drift out of date

## 13.8 Conclusion
- Goal: make system structure and behavior obvious so readers can find info and modify with confidence
- Comments fill in what can't easily be deduced from code
- 📌 "Obvious" is from the perspective of a **first-time reader**, not the author
- Put yourself in the reader's mindset; ask what they need to know
- 💡 If a reviewer says something isn't obvious — don't argue; it isn't
  - Understand the confusion; fix with better comments or better code

## 13.9 Answers to questions from Section 13.5
- Message format to servers → ❌ No: implementation detail, hide in class
- Comparison function (int/float/string?) → ✅ Yes: users need this
- Server-side index data structure → ❌ No: encapsulated on servers; even `IndexLookup` shouldn't know
- Concurrent requests to servers → Possibly: document high-level performance techniques since users may care
- Server crash handling → ❌ No: auto-recovery makes crashes invisible; document only if crashes surfaced to applications

## Key Takeaways
- 📌 Comments must add what code cannot express — never restate it
- Comment at a **different level** than the code: lower for precision, higher for intuition
- Comments are the only way to document **abstractions**; keep interface and implementation docs separate
- Interface docs contaminated by implementation details signal a shallow class
- Implementation comments: explain *what* and *why*, not *how*
- Centralize cross-module documentation where developers will find it
- "Obvious" is judged by the first-time reader — if a reviewer is confused, fix it