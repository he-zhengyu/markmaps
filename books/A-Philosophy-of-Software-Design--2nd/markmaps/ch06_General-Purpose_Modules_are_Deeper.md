---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Ch. 6: General-Purpose Modules are Deeper

## Core Thesis
- 💡 **Over-specialization** may be the #1 cause of software complexity
- General-purpose code is simpler, cleaner, easier to understand
- Applies at multiple levels
  - Module/class design → general-purpose APIs are **deeper**
  - Detailed code → eliminate special cases
- Specialization can't be fully eliminated → separate it from general code

## 6.1 Make classes somewhat general-purpose
- The design decision: general vs. special-purpose
  - ✅ General: broad mechanism, unanticipated future uses, *investment mindset* (Ch. 3)
  - ❌ Risk: future is unpredictable; unused facilities; may fit today's problem poorly
  - ✅ Special: build only what's needed today, refactor later, fits *incremental development*
- Author's finding from student projects
  - General-purpose classes almost always better
  - 💡 General interfaces are **simpler and deeper**, with *less* implementation code
  - Less work even when used in a special-purpose way
  - Reuse is a bonus — but generality wins even without reuse
- 🔑 **Somewhat general-purpose**: functionality reflects current needs, but the *interface* does not
  - Interface general enough for multiple uses
  - Easy to use for today's needs, not tied to them
  - ⚠️ "Somewhat" matters: don't build something so general it's hard to use today

## 6.2 Example: storing text for an editor
- Project: GUI text editor
  - Display file; point, click, type to edit
  - Multiple simultaneous views of one file
  - Multi-level undo/redo
- Special-purpose text-class API (student approach)
  - Methods mirrored UI features
    - `void backspace(Cursor cursor)`
    - `void delete(Cursor cursor)`
    - `void deleteSelection(Selection selection)`
  - Problems
    - ❌ Many **shallow methods**, each for one UI operation
    - ❌ Many methods invoked in only one place
    - ❌ High cognitive load for UI *and* text-class developers
    - ❌ **Information leakage**: UI abstractions (selection, backspace) in text class
    - ❌ Every new UI feature → new text-class method
    - ❌ UI and text classes tied together, can't develop independently

## 6.3 A more general-purpose API
- Define API only in terms of **basic text features**
  - `void insert(Position position, String newText)`
  - `void delete(Position start, Position end)`
  - Generic `Position` type instead of UI-specific `Cursor`
  - Position manipulation: `Position changePosition(Position position, int numChars)`
- Implementing UI features on top
  - Delete key: `text.delete(cursor, text.changePosition(cursor, 1))`
  - Backspace: `text.delete(text.changePosition(cursor, -1), cursor)`
- Trade-off assessment
  - UI code slightly longer, but **more obvious**
  - Old code: developer must read backspace docs/code to verify behavior
  - ✅ Less code overall: few general methods replace many special ones
- Reusability payoff
  - Same class works for e.g. a find-and-replace application
  - Only needs `Position findNext(Position start, String string)`

## 6.4 Generality leads to better information hiding
- Cleaner separation of text and UI classes
  - Text class unaware of UI specifics (e.g. backspace handling)
  - New UI features need no new text-class support
  - Fewer, simpler, reusable methods → lower cognitive load
- 🔑 **False abstraction**: `backspace` purported to hide info the UI actually needs
  - UI developers read its code anyway to confirm behavior
  - Hiding needed details just creates obscurity
- 💡 Core design question: **who needs to know what, and when**
  - When details matter, make them explicit and obvious

## 6.5 Questions to ask yourself
- **What is the simplest interface covering all current needs?**
  - Fewer methods without losing capability → more general-purpose
  - Example: 3 delete methods → 1 general `delete`
  - ⚠️ Only if each method's API stays simple — lots of extra arguments ≠ simpler
- **In how many situations will this method be used?**
  - ⚠️ Red flag: a method designed for one use (like `backspace`)
  - Try replacing several special methods with one general one
- **Is this API easy to use for my current needs?**
  - Detects when generality goes *too far*
  - ⚠️ Red flag: lots of extra code needed to use the class
  - Example: single-character insert/delete → loops everywhere, inefficient
  - Better: built-in support for **ranges of characters**

## 6.6 Push specialization upwards (and downwards!)
- Specialization is inevitable (app features are specialized)
- 📌 Cleanly separate specialized code from general-purpose code
- Push **upwards**
  - Top-level classes are necessarily specialized for features
  - Don't let it percolate into lower-level classes
  - Editor example: UI details pushed up into UI code; text class stays general
- Push **downwards**
  - Example: **device drivers**
  - OS defines general interface: "read a block", "write a block"
  - Each driver implements it using device-specific commands
  - OS core written with no knowledge of device specifics
  - ✅ New devices added with no changes to the OS

## 6.7 Example: editor undo mechanism
- Requirement: multi-level undo/redo of text, selection, cursor, and view
- Flawed approach: entire undo mechanism inside text class
  - Text class kept the undo list; UI called extra methods to log its changes
  - Text class called back to UI for non-text undo entries
  - ❌ Selection/cursor undo handlers unrelated to text
  - ❌ Information leakage + extra pass-through methods
  - ❌ New undoable entity → changes to text class
  - ❌ General undo core unrelated to general text facilities
- Better design: extract general core into a `History` class
  - `History.Action` interface: `undo()` / `redo()` per operation
  - `History` manages the action list; knows nothing about action contents
  - `addFence()` groups related actions; undo walks back to next fence
- Functionality divided into three independent categories
  - General mechanism: manage/group actions, invoke undo/redo (`History`)
  - Specific actions: `UndoableInsert`, `UndoableDelete`, `UndoableSelection`, `UndoableCursor`
  - Grouping policy: high-level UI code places fences
- 💡 Key decision: separating general from special parts — the rest "fell out naturally"
- 📌 Nuance: separation applies *per mechanism*
  - Text class = general text mechanism + special-purpose undo code for text
  - That undo code belongs with text functions, not in `History`

## 6.8 Eliminate special cases in code
- Special cases → code riddled with `if` statements, hard to understand, bug-prone
- 💡 Design the **normal case** so edge conditions are handled automatically
- Example: text selection
  - ❌ Student approach: state variable for "selection exists" → checks everywhere
  - ✅ Fix: selection **always exists**; "none" = **empty selection** (start == end)
  - Copy of empty selection inserts 0 bytes — no special check needed
  - Delete: concatenate text before + after selection; empty case regenerates the line
- Related: exceptions create many special cases (Ch. 10)

## Key Takeaways
- 💡 Unnecessary specialization is a major contributor to complexity
- Make interfaces **somewhat general-purpose**: functionality for today, interface for many uses
- General APIs are deeper, hide information better, and need less code
- Push specialization up (into feature code) or down (into drivers/adapters)
- Eliminate special cases by making the normal case handle edges automatically
- Result: deeper classes, better information hiding, simpler and more obvious code