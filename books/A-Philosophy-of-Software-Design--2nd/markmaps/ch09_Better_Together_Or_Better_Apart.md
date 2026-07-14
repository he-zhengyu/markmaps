---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Ch 9: Better Together Or Better Apart?

## The Fundamental Question
- 🔑 Given two pieces of functionality: implement together or apart?
- Applies at all levels: functions, methods, classes, services
- Goal: reduce **overall system complexity**, improve modularity
- ⚠️ More small components ≠ simpler system
### Costs of subdivision
- More components → harder to track and find them
- More interfaces → every new interface adds complexity
- Extra management code (e.g. managing multiple objects)
- **Separation**: related code farther apart
  - ✅ Good if components truly independent — focus on one at a time
  - ❌ Bad if dependent — flipping back and forth, hidden dependencies → bugs
- **Duplication**: code may repeat across subdivided components
### Signs that two pieces of code are related
- They **share information** (e.g. both depend on a document syntax)
- They are **used together** — only compelling if *bidirectional*
  - ❌ Counter-example: block cache needs hash table, but hash tables have many other uses → keep separate
- They **overlap conceptually** under a higher-level category
  - e.g. substring search + case conversion → *string manipulation*
- Hard to understand one without looking at the other

## 9.1 Bring together if information is shared
- HTTP server example (from Section 5.4)
- Two methods: one read request from socket, one parsed the string
- Both needed deep knowledge of HTTP request format
  - Reader had to parse headers just to find the request's end
- 💡 Combining read + parse in one place → shorter, simpler code

## 9.2 Bring together if it will simplify the interface
- Combined module can offer a simpler interface than the originals
- Common when each original module solved only *part* of a problem
- HTTP example: merging eliminated the pass-the-string interface
- Combining can make functions **automatic** — invisible to most users
  - Java I/O: merge `FileInputStream` + `BufferedInputStream`, buffer by default
  - Most users never need to know buffering exists

## 9.3 Bring together to eliminate duplication
- ⚠️ Red Flag: **Repetition** — same code over and over means wrong abstractions
### Approach 1: factor into a method
- Replace repeated snippets with calls to one method
- ✅ Best when snippet is long and method signature is simple
- ❌ Little benefit for 1–2 line snippets
- ❌ Complex environment interaction → complex signature, reduced value
### Approach 2: refactor so snippet executes in one place
- Example: same cleanup before multiple error returns
- `goto` to cleanup code at end of method (Figures 9.1, 9.2)
- 💡 goto is usually bad, but useful for escaping nested code

## 9.4 Separate general-purpose and special-purpose code
- A general-purpose mechanism should provide *only* that mechanism
- No specializing code, no other general mechanisms bundled in
- Special-purpose code goes in a different module (tied to its purpose)
- GUI editor example (Chapter 6)
  - Text class: general text operations
  - UI module: UI-specific ops like *delete selection*
  - Eliminated information leakage and extra interfaces
- ⚠️ Red Flag: **Special-General Mixture**
  - Mechanism contains code specialized for one use
  - Creates information leakage; use-case changes force mechanism changes

## 9.5 Example: insertion cursor and selection
### The entities
- **Insertion cursor**: blinking line where typed text appears; always visible
- **Selection**: highlighted character range for copy/delete; may not exist
- Cursor always sits at one end of the selection
### Combined-object attempt
- One object: two file positions + booleans (which end is cursor, selection exists)
- ❌ No benefit: higher-level code still treated them as distinct entities
- ❌ More complex: cursor position stored indirectly via boolean + selection end
### The better design: separate
- 💡 Not closely enough related to combine
- Simpler usage *and* simpler implementation after separation
- New general `Position` class (line + character)
  - Selection = two Positions; cursor = one Position
  - Positions reused elsewhere in the project
- 💡 Shows value of lower-level but more general-purpose interfaces (Ch 6)

## 9.6 Example: separate class for logging
- Student project: `NetworkErrorLogger` class with methods like `logRpcOpenError`
- Errors logged via separate method instead of at detection point
### Why the separation failed
- ❌ Logging methods were **shallow**: one line of code, lots of documentation
- ❌ Each method invoked in only one place
- ❌ Highly dependent on invocation sites — readers flip back and forth
### Better approach
- ✅ Inline logging statements where errors are detected
- Easier to read; eliminates the logging-method interfaces

## 9.7 Splitting and joining methods
### Against length-based splitting
- Common rigid rule: "split any method over 20 lines!"
- ⚠️ Length alone is rarely a good reason to split
- Developers tend to break up methods **too much**
- Splitting adds interfaces and separates related pieces
- 📌 Only split if it makes the overall system simpler
### Long methods can be fine
- Five independent 20-line blocks in order → readable block by block
- Complex block interactions → even more important to keep together
- Hundreds of lines OK with simple signature and easy readability
- 💡 Such methods are **deep**: lots of functionality, simple interface
### Design goal: clean abstractions
- Each method: do one thing and do it completely
- Simple interface — little info needed to use correctly
- Deep: interface much simpler than implementation
- If these hold, length probably doesn't matter
### Two ways to split (Figure 9.3)
- **(b) Extract a subtask** into a child method — the best way
  - Parent keeps original interface; parent invokes child
  - Valid if child readable without parent, and vice versa
  - Child typically general-purpose, usable elsewhere
  - ⚠️ Flipping between parent and child → *Conjoined Methods* red flag
- **(c) Divide into two caller-visible methods**
  - Makes sense if original interface was overly complex, doing unrelated things
  - Each new interface should be simpler than the original
  - ✅ Ideally most callers invoke only one of the two
  - ✅ Good sign: new methods more general-purpose
  - ⚠️ Rarely makes sense — callers deal with multiple methods
  - ❌ (d) Risk: shallow methods with state passed back and forth
### When joining helps
- Replace two shallow methods with one **deeper** method
- Eliminate code duplication
- Eliminate dependencies or intermediate data structures
- Better encapsulation: knowledge isolated in one place
- Simpler interface (as in Section 9.2)
- ⚠️ Red Flag: **Conjoined Methods**
  - Can't understand one method without another's implementation
  - Also applies to physically separated code that must be read together

## 9.8 A different opinion: Clean Code
- Robert Martin: functions should be split based on **length alone**
  - Functions should be small — even 10 lines is too long
  - Blocks in if/else/while should be one line (a function call)
  - Indent level no more than one or two
### Ousterhout's counterargument
- ✅ Agrees shorter is generally easier to understand
- Below a few dozen lines, further shrinking barely helps readability
- 💡 Real question: does splitting reduce *overall system* complexity?
- More functions → more interfaces to document and learn
- Too-small functions lose independence → conjoined functions
- 📌 **Depth is more important than length**
  - First make functions deep, then short enough to read easily
  - Never sacrifice depth for length

## 9.9 Conclusion
- Split-or-join decisions should be based on **complexity**
- Pick the structure with:
  - Best information hiding
  - Fewest dependencies
  - Deepest interfaces

## Key Takeaways
- 💡 Combine code that is closely related; separate code that is not
- Subdivision has real costs: more interfaces, separation, duplication
- Bring together when: information is shared, interface simplifies, duplication dies
- Keep general-purpose mechanisms free of special-purpose code
- Method length is a weak signal — **depth over length**
- 📌 Optimize the complexity of the *whole system*, not individual pieces