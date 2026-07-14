---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Ch. 18: Code Should be Obvious

## 18.1 Things that make code more obvious

### What "obvious" means
- 🔑 **Obvious code**: read quickly, first guesses about behavior are correct
- Reader gathers needed information with little time or effort
- Nonobvious code → wasted effort, misunderstanding, bugs
- 💡 Obvious code needs fewer comments
- Obscurity is one of the two main causes of **complexity** (§2.3)

### Obviousness is judged by the reader
- 📌 "Obvious" is in the *mind of the reader*, not the author
- Easier to spot nonobviousness in others' code than your own
- ✅ Best test: **code reviews** — if a reader says it's not obvious, it's not
- Understanding why code confused readers teaches you to write better

### Techniques from earlier chapters
- **Good names** (Ch. 14): precise names clarify behavior, reduce docs
  - Vague names force readers to deduce meaning from code — slow, error-prone
- **Consistency** (Ch. 17): similar things done in similar ways
  - Readers recognize familiar patterns and draw *safe* conclusions instantly

### Judicious use of white space
- Formatting affects how easily structure is grasped
- Parameter docs: blank space between `@param` blocks reveals structure
  - Squeezed docs hide where one parameter ends and the next begins
- Blank lines separate major blocks within a method
  - 💡 Works best when each block starts with a comment — blank lines make comments visible
- White space *within* a statement clarifies its structure
  - `for (int pass = 1; pass >= 0 && !empty; pass--)` vs. the squeezed version

### Comments
- When nonobvious code is unavoidable, comments supply the missing information
- 📌 Put yourself in the reader's position: what will confuse them, and what clears it up?

## 18.2 Things that make code less obvious

### ⚠️ Red Flag: Nonobvious Code
- If meaning/behavior can't be understood with a quick reading → red flag
- Signals important information isn't immediately clear to the reader

### Event-driven programming
- 🔑 App responds to external events (network packet, mouse press) via registered handlers
- ⚠️ Hard to follow the **flow of control**
  - Handlers invoked indirectly via function pointers/interfaces, never directly
  - Which handler runs depends on runtime registration
  - Hard to reason about or convince yourself the code works
- ✅ Compensate: interface comment on each handler stating *when* it is invoked
  - e.g. `Transport::RpcNotifier::failed()` — "invoked in the dispatch thread… on transport-level error"

### Generic containers
- e.g. `Pair` in Java, `std::pair` in C++ — tempting for returning multiple values
- ❌ Generic names obscure meaning: `result.getKey()` / `result.getValue()` say nothing
- ✅ Define a specialized class/struct instead
  - Meaningful element names + room for documentation in the declaration
- 💡 General rule: design software for **ease of reading, not ease of writing**
  - A few extra minutes for the writer saves confusion for all readers

### Different types for declaration and allocation
- e.g. declared `List<Message>`, allocated `new ArrayList<Message>()`
- Legal, but misleads readers who see only the declaration
- Actual type affects usage (performance, thread-safety differ across `List` subclasses)
- ✅ Match the declaration with the allocation

### Code that violates reader expectations
- e.g. `main` returns but app keeps running — `RaftClient` constructor spawned threads
- Readers assume apps exit when `main` returns
- ✅ Document in the constructor's interface comment **and** a short comment at end of `main`
- 📌 Code is most obvious when it conforms to conventions readers expect; deviations must be documented

## 18.3 Conclusion

### Obviousness as information
- 💡 Nonobvious code = the reader lacks important information
  - RaftClient: reader doesn't know the constructor creates threads
  - Pair: reader doesn't know `getKey()` returns the current term

### Three ways to ensure readers have the information
- **Reduce** information needed — abstraction, eliminating special cases (best way)
- **Leverage** what readers already know — follow conventions, conform to expectations
- **Present** the information in the code — good names, strategic comments

## Key Takeaways
- Obviousness is defined by the *reader*; code reviews are the true test
- Good names, consistency, white space, and comments make code obvious
- ⚠️ Avoid: generic containers, mismatched declaration/allocation types, violated expectations; document unavoidable obscurity (e.g. event-driven code)
- Design for **ease of reading, not ease of writing**
- Make code obvious by reducing needed information, exploiting reader conventions, or presenting the information directly