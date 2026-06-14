---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Different Layer, Different Abstraction

## Core Principle
- 🔑 Systems are composed in **layers**; higher layers use facilities of lower layers
- 💡 Each layer should provide a **different abstraction** from layers above and below
- As an operation moves through layers, the abstraction changes with each method call
- ⚠️ Adjacent layers with **similar abstractions** = red flag for poor class decomposition
- 📌 An operation's abstraction should shift at each `method` call
### Examples of distinct layers
- **File system**
  - Top: file as variable-length **byte array** (read/write byte ranges)
  - Middle: in-memory **cache** of fixed-size disk blocks
  - Bottom: **device drivers** moving blocks between storage and memory
- **TCP transport protocol**
  - Top: reliable **byte stream** between machines
  - Bottom: best-effort **packets** of bounded size (may be lost or reordered)

## 7.1 Pass-through Methods
- 🔑 A **pass-through method** does little except invoke another method with a similar/identical signature
- 📌 Signals there is **no clean division of responsibility** between classes
### Case study: GUI text editor
- `TextDocument` class was almost entirely pass-throughs (e.g. `getCursorOffset`, `insertString`)
- 📊 **13 of 15** public methods were pass-through methods
- Only `willInsertString` had any logic — and just a null check
### Why they're harmful
- ❌ Make classes **shallow** — add interface complexity, no new functionality
- ❌ Create **dependencies**: a signature change in `TextArea` forces a change in `TextDocument`
- ❌ Indicate **overlapping responsibility** between classes
- 💡 The interface to a feature should live in the class that *implements* it
### How to refactor (Figure 7.1)
- ✅ (b) Expose lower-level class **directly** to callers; strip the feature from the upper class
- ✅ (c) **Redistribute** functionality between the classes
- ✅ (d) If inseparable, **merge** the classes
- Case study fix: collapsed `TextDocument`, `TextArea`, `TextDocumentListener` from three classes into two

## 7.2 When Is Interface Duplication OK?
- 💡 Same signature is fine **if each method adds significant, distinct functionality**
- ⚠️ Pass-through methods are bad precisely because they add *none*
### Dispatcher
- 🔑 A **dispatcher** uses its arguments to select which of several methods to invoke
- Often shares the callees' signature, but adds real value: the **selection** itself
- Example: Web server inspects incoming **URL**, routes to file-return vs. PHP/JavaScript handler
### Multiple implementations of one interface
- Example: **disk drivers** — different hardware, same interface
- ✅ Reduces **cognitive load**: learn one, the rest feel familiar
- 📌 Usually in the same layer; they **don't invoke each other**

## 7.3 Decorators
- 🔑 **Decorator** ("wrapper"): extends an existing object, exposing a similar/identical API that calls the underlying object
- Motivation: separate **special-purpose extensions** from a generic core
- Examples
  - `BufferedInputStream` wraps `InputStream` to add buffering (reads larger blocks)
  - `ScrollableWindow` decorates `Window` by adding scrollbars
### The problem
- ❌ Decorators tend to be **shallow** — lots of boilerplate, little new functionality
- ❌ Often full of pass-through methods
- ⚠️ Easy to overuse → **explosion of shallow classes** (e.g. Java I/O)
### Alternatives to consider first
- Add the feature **directly to the underlying class** (if general-purpose or commonly used together — e.g. buffering *is* a natural part of I/O)
- **Merge** the feature with its specific use case
- Fold it into an **existing decorator** → one deeper class instead of many shallow ones
- Implement as a **stand-alone class**, not wrapping the base (e.g. scrollbars separate from the window)
- 📌 Wrappers occasionally justified: adapting an **unmodifiable external class** to a required interface — but such cases are rare

## 7.4 Interface versus Implementation
- 💡 A class's **interface should differ from its implementation**
- ⚠️ If internal representation ≈ interface abstraction, the class probably isn't **deep**
### Text editor example (from Ch. 6)
- ❌ Line-oriented API (`getLine`, `putLine`) mirrored line-based storage → **shallow & awkward**
- Callers had to split/join lines for mid-line typing or cross-line deletes — duplicated, scattered code
- ✅ Character-oriented API: `insert` arbitrary string at any position, `delete` between two positions
- 💡 Internally still stored as lines, but complexity of splitting/joining is **encapsulated** → deeper class, simpler callers

## 7.5 Pass-through Variables
- 🔑 A **pass-through variable** is passed down a long chain of methods that don't use it
- Example: `cert` (certificate info) flows from `main` through `m1`, `m2` to `m3`, used only by `m3`
### Why harmful
- ❌ Forces every intermediate method to **know about** a variable it has no use for
- ❌ Adding a new variable later means editing **many interfaces and methods**
### Solutions (Figure 7.2)
- **(b) Shared object** between top and bottom methods — but that object may itself become a pass-through variable
- **(c) Global variable** — ⚠️ blocks multiple independent instances in one process (hurts testing)
- ✅ **(d) Context object** — author's preferred solution
  - 🔑 A **context** stores all application global state (config, shared subsystems, performance counters)
  - One context **per system instance** → multiple instances coexist in one process
  - Reference saved in major objects; passed via **constructors** only, so it isn't a pervasive argument
  - ✅ New global var → add to context; only constructor/destructor affected
  - ✅ Centralizes and clarifies global state; convenient for **testing**
  - ⚠️ Caveats: shares most downsides of globals; can become a **grab-bag**; thread-safety risks → prefer **immutable** variables
  - 💡 Imperfect, but author hasn't found anything better

## 7.6 Conclusion
- 📌 Every design element (interface, argument, function, class, definition) **adds complexity** — developers must learn it
- 💡 An element earns its place only if it **eliminates more complexity than it introduces**
- The "different layer, different abstraction" rule applies this idea: duplicated abstractions across layers (pass-through methods, decorators) rarely pay for their added infrastructure

## Key Takeaways
- 💡 Each layer should offer a **genuinely different abstraction**; sameness across adjacent layers is a red flag
- ❌ **Pass-through methods** add interface complexity and dependencies without functionality — refactor toward clear responsibility
- ✅ Duplicate signatures are fine **only** when each adds distinct value (dispatchers, interface implementations)
- ⚠️ **Decorators** breed shallow classes; prefer direct integration, merging, or stand-alone designs
- 🔑 Keep a class's **interface distinct from its implementation** to make it deep
- ✅ Replace **pass-through variables** with a **context object**, the least-bad way to manage system-wide state
- 📌 Every abstraction must **pay for the complexity** it introduces