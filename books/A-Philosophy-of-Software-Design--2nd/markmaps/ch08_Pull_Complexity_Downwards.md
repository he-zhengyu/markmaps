---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# 8: Pull Complexity Downwards

## Core Principle
- 🔑 When facing **unavoidable complexity**: handle it *inside* the module, not push to users
- 💡 More important for a module to have a **simple interface** than a simple implementation
- 📌 Most modules have **more users than developers** → better for developers to suffer than users
- Module developer's duty: make life as easy as possible for users, even at extra cost to yourself
- ⚠️ Tempting opposite behavior: solve easy problems, punt hard ones upward
  - Throw an exception → *every caller* must handle it
  - Export config parameters → *every sysadmin in every installation* must learn them
  - ❌ Eases your life short-term, but **amplifies complexity**: many people deal with a problem instead of one

## 8.1 Example: editor text class
- Context: GUI text editor's file text class (from Chapters 6 & 7)
  - Reads file into memory, queries/modifies in-memory copy, writes back to disk
- **Line-oriented interface** (many students' choice)
  - ✅ Simple implementation for the class
  - ❌ Complexity pushed up: UI operations rarely involve whole lines
    - Keystrokes insert individual characters within a line
    - Copy/delete selection modifies parts of several lines
    - Higher-level software forced to split/join lines
- **Character-oriented interface** (Section 6.3)
  - ✅ Pulls complexity downward
  - UI inserts/deletes arbitrary text ranges without splitting/merging
  - Implementation gets more complex (internal line splitting/merging)
  - 💡 Encapsulating split/merge complexity in the text class **reduces overall system complexity**

## 8.2 Example: configuration parameters
- 🔑 Config parameters = moving complexity **upwards** instead of down
  - Class exports parameters controlling behavior (cache size, retry count) rather than deciding internally
  - Very popular today; some systems have **hundreds**
- Arguments *for*
  - ✅ Users can tune system to their requirements and workloads
  - Low-level code may not know best policy; users know their domains
    - e.g., user marks time-critical requests with higher priority
  - Can yield better performance across broader variety of domains
- Arguments *against*
  - ❌ Easy excuse to avoid important issues and pass them to someone else
  - Often difficult/impossible for users or admins to determine right values
  - Right values often computable automatically with a little extra work
  - ⚠️ Config parameters easily become **out of date**
- Case: network protocol retry interval
  - Naive: expose retry interval as a config parameter
  - Better: protocol measures response time of successful requests, uses a multiple as retry interval
    - ✅ Pulls complexity down; users spared from guessing
    - ✅ Dynamic: auto-adjusts as operating conditions change
- Guidance
  - 📌 Avoid configuration parameters as much as possible
  - Ask first: *"Can users determine a better value than we can here?"*
  - If exporting one, provide **reasonable defaults** — users override only in exceptional cases
  - 💡 Each module should solve a problem **completely**; config parameters = incomplete solution → added system complexity

## 8.3 Taking it too far
- ⚠️ Pulling complexity down can be **overdone**
  - Extreme absurdity: pull the entire application into a single class
- When pulling down makes sense — all three:
  - (a) Complexity is **closely related** to the class's existing functionality
  - (b) Pulling down **simplifies other parts** of the application
  - (c) Pulling down **simplifies the class's interface**
- 📌 The goal is always to **minimize overall system complexity**
- Counterexample: backspace method in text class (Chapter 6)
  - Seemed like pulling complexity down
  - ❌ Barely simplifies higher-level code
  - ❌ UI knowledge unrelated to text class's core functions
  - Result: **information leakage**, not simplification

## 8.4 Conclusion
- 💡 Take a little extra suffering upon yourself to reduce the suffering of your users

## Key Takeaways
- Simple **interface** trumps simple **implementation** — encapsulate unavoidable complexity where it arises
- Pushing problems upward (exceptions, config params) multiplies who must deal with them
- Prefer computing sensible values automatically over exposing configuration knobs; give defaults when knobs are unavoidable
- Pull complexity down only when it's related to the class, simplifies the rest of the app, and simplifies the interface
- Ultimate measure: **overall system complexity**, not local convenience