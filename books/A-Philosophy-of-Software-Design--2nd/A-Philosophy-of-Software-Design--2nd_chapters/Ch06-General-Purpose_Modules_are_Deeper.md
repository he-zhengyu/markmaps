---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Ch. 6: General-Purpose Modules are Deeper

## Core Principle
- 💡 **Over-specialization** may be the single greatest cause of complexity
- 💡 General-purpose code is *simpler, cleaner, easier to understand*
- Applies at many design levels
  - **APIs**: general-purpose → deeper APIs, more information hiding
  - **Detailed code**: eliminate special cases so common-case code handles edges
  - ✅ Eliminating special cases can also improve efficiency

## 6.1 Make classes somewhat general-purpose
- The recurring design choice: **general-purpose** vs **special-purpose**
- ### Case for general-purpose
  - Mechanism addresses a broad range of problems, not just today's
  - May find unanticipated future uses → saves time
  - Fits the *investment mindset* (Ch. 3)
- ### Case for special-purpose
  - ⚠️ Hard to predict a system's future needs
  - ⚠️ Too-general solution may not solve today's problem well
  - Build only what you need; refactor to general later
  - Fits *incremental development*
- ### The verdict
  - 💡 Author switched views after teaching: general-purpose almost always better
  - 📌 General-purpose interfaces are **simpler and deeper**, less implementation code
  - Even for single-use, it's *less work* to build general-purpose
- ### 🔑 "Somewhat general-purpose" — the sweet spot
  - **Functionality** reflects *current* needs
  - **Interface** is general enough for *multiple* uses
  - ⚠️ "Somewhat" matters — don't over-generalize so much that it's hard to use today

## 6.2 Example: storing text for an editor
- GUI text editor project
  - Display file; point, click, type to edit
  - Support multiple simultaneous views
  - Support multi-level undo/redo
- ### The specialized text-class API
  - Tailored methods mirroring UI features
  - `void backspace(Cursor cursor)`
  - `void delete(Cursor cursor)`
  - `void deleteSelection(Selection selection)`
  - Used UI-specific types: `Cursor`, `Selection`
- ### Why it failed
  - ❌ Many **shallow methods**, each for one UI operation
  - ❌ Methods like `delete` invoked in only one place
  - ⚠️ High cognitive load on both UI and text developers
  - ⚠️ **Information leakage**: UI abstractions reflected in text class
  - ❌ Each new UI op forced a new text-class method → classes tied together

## 6.3 A more general-purpose API
- 🔑 Define API only in terms of **basic text features**
- ### Generic modification methods
  - `void insert(Position position, String newText)`
  - `void delete(Position start, Position end)` — deletes `[start, end)`
  - Uses neutral type `Position`, not UI-bound `Cursor`
- ### Position helper
  - `Position changePosition(Position position, int numChars)`
  - Positive `numChars` → later; negative → earlier
  - Auto-skips to next/previous line
- ### UI ops built on top
  - delete key: `text.delete(cursor, text.changePosition(cursor, 1))`
  - backspace: `text.delete(text.changePosition(cursor, -1), cursor)`
- ### Benefits
  - ✅ Slightly longer UI code, but **more obvious** about which chars are deleted
  - ✅ Less code overall: few general methods replace many special ones
  - ✅ Reusable — e.g., search-and-replace tool needs only `findNext(...)`

## 6.4 Generality leads to better information hiding
- ✅ Cleaner separation between text and UI classes
- Text class need not know UI specifics (e.g., backspace behavior)
- New UI features added without new text-class methods
- ✅ Lower cognitive load — few simple, reusable methods
- ### 🔑 False abstraction
  - Old `backspace` *pretended* to hide which chars are deleted
  - But UI developers **need** that info → they will need to read its code anyway
  - 💡 Hiding details the caller needs just creates **obscurity**
  - 📌 When details matter, make them explicit and obvious

## 6.5 Questions to ask yourself
- 💡 Easier to *recognize* a clean general-purpose design than to *create* one
- ### What is the simplest interface covering all current needs?
  - Fewer methods, same capability → likely more general-purpose
  - One general `delete` replaced `backspace` + `delete` + `deleteSelection`
  - ⚠️ Don't trade method count for many extra arguments
- ### In how many situations will this method be used?
  - 🔑 A method for one specific use (like `backspace`) is a **red flag**
  - Try replacing several special methods with one general method
- ### Is this API easy to use for current needs?
  - Detects over-generalizing
  - ⚠️ Lots of extra calling code = wrong functionality
  - Example: single-character `insert`/`delete` is simple & general but...
    - ❌ Forces loops in higher-level code
    - ❌ Inefficient for large operations
  - ✅ Better: built-in support for *range* operations

## 6.6 Push specialization upwards (and downwards!)
- 📌 Some specialization is inevitable (app features)
- 🔑 Specialized code must be **cleanly separated** from general-purpose code
- ### Push upwards
  - Top-level classes are specialized for their features
  - Specialization shouldn't percolate down into lower-level classes
  - Editor example: UI specifics pushed *up*, text class stays general
- ### Push downwards
  - Example: OS **device drivers**
  - OS defines a general interface ("read a block", "write a block")
  - Each `device driver` implements it using device-specific features
  - ✅ Core OS written without knowledge of specific devices
  - ✅ New devices added with no changes to the OS core

## 6.7 Example: editor undo mechanism
- Requirement: multi-level undo/redo for text, selection, cursor, *and* view
- ### The flawed approach
  - Entire undo mechanism inside the **text class**
  - Text class held the undo list, called back to UI for non-text entries
  - ❌ Special-purpose handlers unrelated to text functionality
  - ⚠️ Information leakage + extra cross-module methods
  - ❌ New undoable entity → changes to the text class
- ### The fix: extract a general-purpose `History` class
  - `interface Action { void redo(); void undo(); }`
  - `addAction(Action)`, `addFence()`, `undo()`, `redo()`
  - 🔑 `History` knows nothing about action contents
  - ### `History.Action` objects (special-purpose)
    - Each understands one undoable operation
    - Text class: `UndoableInsert`, `UndoableDelete`
    - UI code: `UndoableSelection`, `UndoableCursor`
  - ### 🔑 Fences
    - Markers grouping related actions
    - One user undo can restore text + reselect + reposition cursor
    - Grouping policy set by higher-level code via `addFence`
- ### Three separated categories
  - General mechanism for managing/grouping/invoking actions → `History`
  - Specifics of particular actions → various action classes
  - Policy for grouping actions → high-level UI code
  - 💡 Each implemented without understanding the others
- ### 📌 Nuance
  - Separate general vs special code *within a mechanism*
  - But special code for one mechanism may live with general code for another
  - Text class holds general text mechanism *plus* its own undo (text-specific) code

## 6.8 Eliminate special cases in code
- 🔑 Special cases breed `if` statements → hard to understand, bug-prone
- 💡 Best fix: design the **normal case** to handle edge conditions automatically
- ### The selection example
  - Students used a state flag for "selection exists?"
  - ❌ Led to numerous "no selection" checks
- ### The fix: selection always exists
  - Represent "no selection" as an **empty selection** (start == end)
  - ✅ Copying empty selection → inserts 0 bytes, no special check
  - ✅ Deleting empty selection → concatenation regenerates original line
- See Ch. 10 on exceptions and reducing where they're handled

## 6.9 Conclusion
- 📌 Unnecessary specialization is a significant contributor to complexity
  - In special-purpose classes/methods
  - In special cases within code
- Can't be eliminated, but good design reduces and separates it
- ✅ Result: **deeper classes**, better information hiding, simpler/more obvious code

## Key Takeaways
- 💡 Over-specialization is arguably the **single greatest cause** of complexity
- 🔑 Aim for **somewhat general-purpose**: functionality for today, interface for many uses
- 📌 General-purpose interfaces are **simpler, deeper, and need less code**
- ⚠️ Beware **false abstractions** that hide details the caller actually needs
- 🔑 Ask: *simplest interface covering current needs? how many uses? still easy to use?*
- ✅ Separate specialization by **pushing it up** (UI) or **down** (device drivers)
- ✅ Extract a general-purpose core (e.g., `History`) and push specifics into subclasses
- 💡 Eliminate special cases by making the **common-case code handle edges** (empty selection)