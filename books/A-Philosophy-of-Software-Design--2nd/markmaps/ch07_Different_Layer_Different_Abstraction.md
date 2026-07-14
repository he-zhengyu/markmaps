---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Ch. 7: Different Layer, Different Abstraction

## Core Principle
- Systems are composed in **layers**; higher layers use lower layers
- 💡 Each layer should provide a **different abstraction** from adjacent layers
- Abstractions should change with each method call across layers
- ⚠️ Adjacent layers with similar abstractions → red flag for class decomposition
- Examples of well-layered systems
  - **File system**
    - Top: file = variable-length byte array, read/write byte ranges
    - Middle: in-memory cache of fixed-size disk blocks
    - Bottom: device drivers moving blocks between disk and memory
  - **Network transport (TCP)**
    - Top: reliable byte stream between machines
    - Bottom: best-effort bounded packets (may be lost / out of order)

## 7.1 Pass-through Methods
- 🔑 **Pass-through method**: does little except invoke another method with similar/identical signature
- Example: student GUI text editor
  - `TextDocument` delegated to `TextArea` and `TextDocumentListener`
  - 📊 13 of 15 public methods were pass-throughs
- Why they're harmful
  - ❌ Make classes **shallower**: more interface complexity, no new functionality
  - ❌ Create **dependencies**: signature change in `TextArea.insertString` forces matching change in `TextDocument`
  - ❌ Signal confusion over **division of responsibility** between classes
- 📌 Interface to functionality should live in the class that implements it
- Diagnostic question: *"Exactly which features and abstractions is each class responsible for?"*
- Refactoring solutions (Figure 7.1)
  - Expose the lower-level class **directly to callers**
  - **Redistribute functionality** between the classes
  - **Merge the classes** if they can't be disentangled
- Student's fix: collapsed 3 intertwined classes into 2 with distinct responsibilities

## 7.2 When Is Interface Duplication OK?
- 💡 Same signature is fine if each method contributes **significant, distinct functionality**
- ✅ **Dispatcher**
  - Uses arguments to select which of several methods to invoke
  - Same signature as callees, but adds value: *choosing* the handler
  - Example: web server matching URL rules → file contents vs. PHP/JavaScript handler
- ✅ **Multiple implementations of one interface**
  - Example: OS disk drivers — different disks, same interface
  - 💡 Reduces cognitive load: learn one interface, use them all
  - Such methods are in the **same layer** and don't invoke each other

## 7.3 Decorators
- 🔑 **Decorator (wrapper)**: extends an existing object with a similar/identical API, delegating to it
- Examples
  - Java I/O: `BufferedInputStream` adds buffering over `InputStream`
  - Windowing: `ScrollableWindow` adds scrollbars to `Window`
- Motivation: separate special-purpose extensions from a generic core
- Problems
  - ❌ Tend to be **shallow**: lots of boilerplate, little new functionality
  - ❌ Often full of pass-through methods
  - ⚠️ Easy to overuse → explosion of shallow classes (e.g., Java I/O)
- Alternatives to consider first
  - Add functionality **directly to the underlying class**
    - Fits if general-purpose, logically related, or used by most users
    - Example: nearly everyone wraps `InputStream` in `BufferedInputStream` → should be combined
  - Merge specialized functionality **with the use case**
  - Merge into an **existing decorator** → one deeper decorator vs. many shallow
  - Implement as a **stand-alone class** without wrapping
    - Example: scrollbars implemented separately from the window
- ✅ Legitimate (rare) use: adapting an unmodifiable external class to a different required interface

## 7.4 Interface versus Implementation
- 📌 A class's interface should normally differ from its internal representation
- ⚠️ If interface and implementation share abstractions → class probably isn't deep
- Text editor case study
  - Internal storage: **lines of text**, stored separately
  - ❌ **Line-oriented API** (`getLine`/`putLine`)
    - Callers forced to split/join lines for mid-line inserts and multi-line deletes
    - Nontrivial code, duplicated and scattered across the UI layer
  - ✅ **Character-oriented API** (`insert` string at position, `delete` range)
    - Encapsulates line split/join complexity inside the text class
    - Makes the class **deeper**, simplifies higher-level code
  - 💡 The interface–implementation difference *is* the valuable functionality

## 7.5 Pass-through Variables
- 🔑 **Pass-through variable**: passed down through a long chain of methods that don't use it
- Example: `cert` (certificate info) passed from `main` through `m1`, `m2` to `m3`, which opens a socket
- Problems
  - ❌ Intermediate methods must be aware of variables they never use
  - ❌ Adding a new variable later may force changes to many interfaces and methods
- Techniques for elimination (Figure 7.2)
  - **Shared object** between topmost and bottommost methods
    - ⚠️ But the shared object may itself become a pass-through variable
  - **Global variable**
    - Avoids passing, but ❌ prevents multiple independent instances per process
    - ⚠️ Multiple instances are often needed in testing
  - **Context object** — 📌 the author's preferred solution
    - Stores *all* application-global state (config options, shared subsystems, performance counters)
    - One context per system instance → multiple instances can coexist in one process
    - Reference stored as instance variable in major objects
    - Passed explicitly only in **constructors**
    - ✅ Benefits
      - New variables: only context constructor/destructor change
      - Global state identifiable and managed in one place
      - Testing: modify context fields to change configuration
    - ⚠️ Drawbacks
      - Retains most disadvantages of global variables (unclear provenance/usage)
      - Without discipline → grab-bag of data with nonobvious dependencies
      - Thread-safety issues; best mitigated by keeping context variables **immutable**
    - Author: not ideal, but no better solution found

## 7.6 Conclusion
- Every design element (interface, argument, function, class, definition) **adds complexity**
- 💡 An element must eliminate more complexity than it introduces to be a net gain
- Example: a class earns its keep by encapsulating functionality from its users
- "Different layer, different abstraction" applies this idea
  - Same abstraction across layers (pass-throughs, decorators) → likely insufficient benefit
  - Pass-through arguments burden many methods without adding functionality

## Key Takeaways
- 📌 Each layer must offer a **distinct abstraction**; similarity across layers is a red flag
- Pass-through methods/variables add interface complexity without functionality — refactor responsibilities
- Duplicate signatures are fine only when each method adds distinct value (dispatchers, multiple implementations)
- Prefer deepening classes over multiplying shallow decorators
- Interface ≠ implementation: the gap between them is where a class delivers value
- Use a context object (with discipline, immutable fields) for system-global state