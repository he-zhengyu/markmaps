---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Pull Complexity Downwards (Ch. 8)

## The Core Principle
- The choice when facing **unavoidable complexity** in a module
  - Let *users* of the module deal with it?
  - Or handle it *internally* within the module?
- 💡 If complexity relates to the module's functionality, handle it **internally**
- 🔑 More important to have a **simple interface** than a **simple implementation**
- 📌 Most modules have more **users** than **developers** → better for developers to suffer than users
- The tempting opposite: solve easy problems, **punt the hard ones**
  - Unsure how to handle a condition → throw an *exception*, let caller cope
  - Unsure which policy to use → add *configuration parameters*, let admins decide
- ⚠️ These shortcuts **amplify complexity** — many people must deal with one problem
  - A thrown exception → *every caller* must handle it
  - A config parameter → *every admin in every installation* must learn it

## 8.1 Example: Editor Text Class
- **Context**: class managing a file's text for a GUI editor
  - Read file from disk into memory
  - Query & modify the in-memory copy
  - Write modified version back to disk
- ❌ The **line-oriented interface** (many students' choice)
  - Methods to read, insert, delete *whole lines*
  - Simple implementation, but pushes complexity *upward*
  - UI rarely works on whole lines: keystrokes insert single chars; selections span partial lines
  - Higher-level software forced to **split and join lines**
- ✅ The **character-oriented interface** (`Section 6.3`)
  - UI inserts/deletes arbitrary text ranges — no line splitting/merging
  - Implementation gets *more complex*: class splits/merges lines internally
  - 💡 Encapsulates splitting/merging inside the text class → lowers **overall** system complexity

## 8.2 Example: Configuration Parameters
- 🔑 Config parameters move complexity **upward**, not down
  - Class exports knobs (cache size, retry count) instead of deciding internally
  - 📊 Very popular today — some systems have *hundreds*
- The case **for** them
  - ✅ Let users tune the system for their workloads
  - Low-level code may not know the best policy; users know their domain
  - *e.g.* a user flags time-critical requests with higher priority
  - Can yield better performance across diverse domains
- The case **against** them
  - ⚠️ An easy excuse to dodge hard issues and pass them on
  - Users often *can't* determine the right values
  - Right value could often be computed automatically with a little extra work
  - 📊 **Retry-interval example** (lost-packet protocol)
    - Naive: expose retry interval as a config parameter
    - ✅ Better: measure successful response times, use a *multiple* as the interval
    - Adjusts dynamically as conditions change
    - ⚠️ Static config parameters easily go *out of date*
- **Guidance**
  - 📌 Avoid configuration parameters as much as possible
  - Ask: *"Will users determine a better value than we can here?"*
  - Provide **reasonable defaults** — values needed only in exceptional cases
  - 💡 Each module should solve its problem **completely**; config params = an incomplete solution

## 8.3 Taking It Too Far
- ⚠️ Use **discretion** — this idea is easily overdone
- Extreme: pull *all* application functionality into one class — nonsensical
- Pull complexity down only when **all** hold:
  - (a) The complexity is closely related to the class's existing functionality
  - (b) Pulling it down simplifies things *elsewhere* in the application
  - (c) Pulling it down simplifies the class's *interface*
- 📌 The goal is always to **minimize overall system complexity**
- ❌ Counter-example: text-class methods that mirror the UI (*e.g.* a backspace method)
  - Seems to pull complexity down, but...
  - Barely simplifies higher-level code
  - UI knowledge is unrelated to the text class's core functions
  - 💡 Result is mere **information leakage**

## 8.4 Conclusion
- 💡 Take a little extra suffering on *yourself* to reduce the suffering of your **users**

## Key Takeaways
- 🔑 A **simple interface** matters more than a simple implementation
- 📌 With more users than developers, the developer should absorb the complexity
- ✅ Pull complexity down when it's *related*, simplifies *elsewhere*, and simplifies the *interface*
- ⚠️ Configuration parameters usually push complexity *upward* — prefer computing values; default heavily
- 💡 Aim for modules that solve their problem **completely**
- ❌ Don't overreach: pulling in unrelated concerns causes **information leakage**