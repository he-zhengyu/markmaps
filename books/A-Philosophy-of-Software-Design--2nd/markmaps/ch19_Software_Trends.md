---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Ch.19 Software Trends — Evaluating Trends Through the Lens of Complexity

## 19.1 Object-oriented programming and inheritance

### OOP mechanisms
- One of the most important ideas of the last 30–40 years
- Introduced **classes**, **inheritance**, **private methods**, **instance variables**
- ✅ Private methods/variables enforce **information hiding**: no external dependencies possible
- ⚠️ Mechanisms assist clean design but don't *guarantee* it
  - Shallow classes, complex interfaces, or exposed internal state → still high complexity

### Interface inheritance
- 🔑 Parent defines method **signatures only**; each subclass implements them differently
- Example: one I/O interface → disk-file subclass + network-socket subclass
- ✅ Leverage against complexity: **reuse one interface for multiple purposes**
- 💡 Knowledge transfers: learning disk-file I/O also solves socket communication
- 💡 **Depth view**: more implementations → deeper interface
- Interface must capture **essential features** of all implementations, omit differing details — the heart of **abstraction**

### Implementation inheritance
- 🔑 Parent defines signatures **plus default implementations**; subclasses inherit or override
- ✅ Avoids duplicating method code across subclasses → reduces **change amplification** (Ch. 2)
- ⚠️ Creates **parent–child dependencies**
  - Shared instance variables → **information leakage** across the hierarchy
  - Changing parent may require examining **all subclasses**
  - Overriding subclass may need to study parent's implementation
  - Worst case: full knowledge of entire class hierarchy needed for any change
- 📌 Heavy implementation inheritance → high complexity

### Using implementation inheritance safely
- Use with **caution**; first consider **composition** instead
  - Small **helper classes** implement shared functionality; classes build on them
- If unavoidable: **separate parent state from subclass state**
  - Parent-managed instance variables; subclasses read-only or via parent methods
  - 💡 Applies **information hiding within the class hierarchy**

## 19.2 Agile development

### What it is
- Emerged late 1990s; formally defined by practitioners in **2001**
- Goal: make development **lightweight, flexible, incremental**
- Mostly about **process** (teams, schedules, unit testing, customer interaction), not design

### Alignment with the book
- ✅ **Incremental and iterative** development: each iteration adds/evaluates a few features with design, test, customer input
- 💡 Matches Ch. 1: a complex system can't be fully visualized up front
- Good design emerges via increments that **add abstractions and refactor existing ones** based on experience

### Risk: tactical programming
- ⚠️ Focuses developers on **features, not abstractions**
- ⚠️ Encourages deferring design to ship working software fast
- Example stance: start with minimal special-purpose mechanism, generalize later
- Argues against the **investment mindset** → rapid complexity accumulation

### The fix
- 📌 **Increments should be abstractions, not features**
- Fine to defer an abstraction until a feature needs it
- Once needed: invest in clean design, make it **somewhat general-purpose** (Ch. 6)

## 19.3 Unit tests

### Historical shift
- Formerly: developers rarely wrote tests; separate QA team if any
- Agile tenet: testing integrated with development; **developers test their own code** — now widespread

### Two kinds of tests
- **Unit tests**
  - Small, focused: validate a small section of code in one method
  - Run in isolation, no production environment needed
  - Paired with **coverage tools** to test every line
  - Developers must update tests when writing/modifying code
- **System tests** (integration tests)
  - Verify parts of the application **work together**
  - Run whole app under production-like conditions
  - More likely written by separate QA team

### Role in design
- 💡 Tests **facilitate refactoring**
- Without tests: structural changes are dangerous
  - Bugs surface only after deployment, where fixing is expensive
  - Developers avoid refactoring → complexity accumulates, design mistakes persist
- With good tests: confidence to make **structural improvements** → better design
- ✅ Unit tests especially valuable: higher coverage than system tests → more bugs found

### Tcl byte-code compiler example
- Replaced Tcl's interpreter with byte-code compiler — huge change to nearly the entire core engine
- Excellent existing unit test suite ran against new engine
- 📊 Only **one bug** appeared after the alpha release

## 19.4 Test-driven development

### The approach
- 🔑 Write unit tests **before** code, based on expected behavior
- All tests fail initially; write just enough code to pass each test; done when all pass

### Why the author objects
- ⚠️ Focuses on **getting features working**, not finding the best design
- **Tactical programming pure and simple**
- Too incremental: tempting to hack in the next feature to pass the next test
- No obvious time to design → easy to end up with a mess
- 📌 Units of development should be **abstractions, not features**
- Once an abstraction is needed, **design it all at once** — not piecemeal — for pieces that fit together

### ✅ The exception: bug fixes
- Write a failing unit test that reproduces the bug **first**, then fix
- Best proof the bug is truly fixed
- Fixing first risks a test that never actually triggers the bug

## 19.5 Design patterns

### What they are
- 🔑 Commonly used approach for a class of problem (e.g., **iterator**, **observer**)
- Popularized by *Design Patterns* (Gamma, Helm, Johnson, Vlissides — "Gang of Four")
- Widely used in object-oriented development

### Value
- ✅ Alternative to designing from scratch
- Arose because they solve common problems with **generally agreed clean solutions**
- If a pattern fits well, a better custom approach is unlikely

### Risk: over-application
- ⚠️ Not every problem fits an existing pattern
- Don't force a problem into a pattern when a **custom approach is cleaner**
- Patterns only improve a system **if they fit**
- 💡 "Patterns are good" ≠ "more patterns are better"

## 19.6 Getters and setters

### The pattern
- Popular in the **Java** community
- Paired with an instance variable: `getFoo` returns value, `setFoo` modifies it

### Arguments for
- Allow extra behavior on access: update related values, notify listeners, enforce constraints
- Features can be added later **without changing the interface**

### Why to avoid
- ⚠️ Better not to **expose instance variables at all**
- Exposure makes implementation externally visible → violates **information hiding**
- Increases interface complexity
- **Shallow methods** (often one line): clutter without functionality
- 📌 Avoid getters/setters — and any exposure of implementation data — as much as possible

### Meta-lesson
- ⚠️ Risk of any established pattern: developers assume it's good and **overuse** it
- Led to getter/setter overusage in Java

## 19.7 Conclusion
- 📌 Challenge every new development paradigm from the standpoint of **complexity**
- Ask: does it really minimize complexity in **large software systems**?
- ⚠️ Many proposals sound good on the surface but make complexity **worse**

## Key Takeaways
- 💡 **Complexity is the universal yardstick** for judging any software trend
- Interface inheritance = abstraction and depth ✅; implementation inheritance = dependencies ⚠️ — prefer **composition**
- Incremental development works, but increments must be **abstractions, not features**
- Unit tests enable refactoring — the key to continual design improvement
- TDD is tactical programming; write tests first **only for bug fixes**
- Design patterns and getters/setters: good when they fit, harmful when applied by reflex