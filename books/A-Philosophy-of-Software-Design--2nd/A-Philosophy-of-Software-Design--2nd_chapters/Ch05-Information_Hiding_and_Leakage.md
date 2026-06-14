---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Ch 5: Information Hiding (and Leakage)

## 5.1 Information hiding

### Core idea
- 🔑 Each module encapsulates a few pieces of knowledge (design decisions)
- Knowledge embedded in implementation, **not visible in interface**
- First described by David Parnas (*"On the Criteria to be Used in Decomposing Systems into Modules"*, CACM, Dec 1972)

### What can be hidden
- How to store/access a **B-tree** efficiently
- Mapping logical file blocks → physical disk blocks
- Implementing the **TCP** protocol
- Scheduling threads on a multi-core processor
- Parsing **JSON** documents
- Spans data structures, algorithms, low-level details (page size), and abstract assumptions (most files are small)

### Why it reduces complexity
- ✅ **Simplifies the interface** — more abstract view, less cognitive load
  - B-tree users needn't know fanout or balancing
- ✅ **Easier evolution** — no outside dependencies on hidden info
  - TCP congestion-control change → only the implementation changes

### Clarifications
- ⚠️ `private` declarations ≠ information hiding
  - Getters/setters can expose variables as if they were public
- 💡 **Partial hiding** still has value
  - Rarely-used info in separate methods → fewer dependencies
- 📌 Hiding more information → simpler interface → **deeper module**

## 5.2 Information leakage

### Definition
- 🔑 A design decision reflected in **multiple modules**
- Creates dependency: changing the decision means changing every involved module

### Two forms
- Leakage through the **interface** (by definition leaked)
  - 💡 Simpler interfaces correlate with better hiding
- ⚠️ **Back-door leakage** — not in any interface
  - e.g. two classes both know a file format (reader + writer)
  - More pernicious because it isn't obvious

### Responding to leakage
- 📌 One of the most important **red flags** in design — cultivate sensitivity to it
- Ask: *"How can this knowledge affect only a single class?"*
- ✅ Merge small, closely-tied classes into one
- ✅ Pull info into a new class that encapsulates it
  - ⚠️ Only works with a simple abstracting interface — else you just swap back-door for interface leakage

## 5.3 Temporal decomposition

### Definition
- 🔑 Structure of system mirrors the **time order** of operations

### Example
- Read file → modify → write, split into 3 classes
- Reader and writer both know the file format → leakage
- ✅ Fix: one class for the core read/write mechanisms, used in both phases

### Why it's a trap
- ⚠️ Execution order is on your mind while coding
- Most design decisions manifest at **several different times**
- Order matters and will appear somewhere — just not in module structure
- 📌 *Focus on the knowledge needed for each task, not the order tasks occur*

## 5.4 Example: HTTP server

### Context
- Student projects from a software design course: implement classes for servers to receive HTTP requests and send responses

### HTTP basics
- Browser sends textual **request** over the network; server returns a **response** (usually a Web page)
- Request structure (Figure 5.1, POST form submission)
  - Initial line: type (`POST`), URL (`/comments/create`) + optional params (`photo_id=246`), protocol version
  - Headers: name + value (e.g. `Content-Length`), ended by an empty line
  - Optional body: additional params (`comment`, `priority`)

## 5.5 Example: too many classes

### The most common mistake
- ⚠️ Many **shallow classes** → leakage between them
- Two classes for receiving requests: one reads string from network, one parses
  - Temporal decomposition: *"first read, then parse"*
  - ❌ Can't read without parsing: `Content-Length` header determines body length
  - ❌ Both classes knew HTTP structure; parsing code duplicated
  - ❌ Callers had to invoke two methods, in order

### The fix
- ✅ Merge reading + parsing into one class
  - All knowledge of request format isolated in one place
  - Simpler interface: one method to invoke

### General theme
- 💡 *Information hiding can often be improved by making a class slightly larger*
  - Bring together all code for one capability
  - Raise the interface level (one method for the whole computation)
  - Result: a **deeper** class
- ⚠️ Don't take it too far (one class for the whole app) — Ch. 9 covers when to split

## 5.6 Example: HTTP parameter handling

### What students did well
- ✅ Hid header-line vs body location of parameters — merged them
- ✅ Hid **URL encoding** (`+` = space, `%21` = `!`)
  - Parser returns decoded values: "What a cute baby!" not "What+a+cute+baby%21"
- 💡 Both choices yielded simpler APIs

### What went wrong: shallow getParams
- ❌ `public Map<String, String> getParams()` returns the internal `Map`
  - Exposes internal representation → any change breaks all callers
  - Extra work: call `getParams`, then look up in the `Map`
  - ⚠️ Callers must know not to modify the returned `Map`
- 📌 Representations of key data structures often change (e.g. for performance) — avoid exposing them

### Better interface
- ✅ `getParameter(String name)` → value as string, representation hidden
- ✅ `getIntParameter(String name)` → also hides string-to-int conversion
- Extensible: `getDoubleParameter`, etc.; exceptions on missing/unconvertible params

## 5.7 Example: defaults in HTTP responses

### The mistake: inadequate defaults
- ❌ Requiring callers to specify HTTP protocol version explicitly
  - Version must match the request, which is already passed in
  - Caller-specified values likely cause leakage between library and caller
- ✅ Library should also default the `Date` header

### Principles
- 💡 Interfaces should make the **common case as simple as possible**
- Defaults = **partial information hiding**: normal callers unaware; rare overrides via special method
- 📌 Classes should *"do the right thing"* without being asked
  - Counterexample: Java I/O buffering should be automatic, never requested
  - *The best features are the ones you get without even knowing they exist*
- ⚠️ Red Flag: **Overexposure** — common-case API forcing users to learn rarely-used features raises cognitive load

## 5.8 Information hiding within a class

- Applies at other levels, not just external APIs
- ✅ Design private methods to each encapsulate one capability, hidden from the rest of the class
- ✅ Minimize the places each instance variable is used
  - Fewer usage sites → fewer internal dependencies → less complexity

## 5.9 Taking it too far

- ⚠️ Only hide information **not needed outside** the module
- If outside code needs it (e.g. tunable performance config), it **must** be exposed
- Goal: *minimize* externally-needed information
  - ✅ Self-adjusting configuration beats exposed parameters
- 📌 Recognize what truly must be exposed, and expose it

## 5.10 Conclusion

- Information hiding and **deep modules** are closely related
  - More hidden info → more functionality + smaller interface → deeper
  - Little hidden info → little functionality or complex interface → shallow
- ❌ Don't let runtime operation order shape decomposition (temporal decomposition → leakage, shallow modules)
- ✅ Identify the pieces of knowledge needed; each module encapsulates one or a few

## Key Takeaways

- 🔑 **Information hiding**: encapsulate design decisions inside modules, invisible to interfaces — the key route to deep modules
- ⚠️ **Information leakage** (same knowledge in multiple modules) is a top red flag; back-door leakage is worse than interface leakage
- ⚠️ Avoid **temporal decomposition** — structure around knowledge, not execution order
- 💡 Slightly larger classes can improve hiding: unify a capability, raise the interface level
- 💡 Never expose internal representations (e.g. return values, not internal `Map`s)
- 💡 Good **defaults** make the common case simple; classes should "do the right thing" automatically
- ⚠️ Don't hide what's genuinely needed outside — but minimize that need