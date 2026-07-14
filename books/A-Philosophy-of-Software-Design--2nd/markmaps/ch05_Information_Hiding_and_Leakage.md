---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Ch5: Information Hiding (and Leakage)

## 5.1 Information Hiding

### Core Idea
- 🔑 Each module encapsulates a few pieces of **knowledge** (design decisions)
- Knowledge lives in the **implementation**, not the interface
- First described by **David Parnas** ("On the Criteria to be Used in Decomposing Systems into Modules", *CACM*, Dec 1972)
- 💡 Key technique for creating **deep modules** (follows Ch4)

### Examples of Hidden Information
- How to store/access info in a **B-tree**
- Mapping logical file blocks → physical disk blocks
- Implementing the **TCP** protocol
- Thread scheduling on multi-core processors
- Parsing **JSON** documents
- Ranges from low-level (page size) to abstract assumptions (most files are small)

### Two Ways It Reduces Complexity
- **Simplifies the interface**
  - Presents a simpler, more abstract view
  - Reduces cognitive load (e.g., B-tree user ignores fanout/balancing)
- **Easier system evolution**
  - No outside dependencies on hidden info
  - Change affects only one module (e.g., TCP congestion control change)

### ⚠️ Not the Same as `private` Declarations
- `private` helps, but getters/setters can still expose the info
- Then variables are as exposed as if they were public

### Partial Information Hiding
- Best: info totally invisible to users
- Still valuable: info accessed via separate methods, hidden in common cases
- Fewer dependencies than universally visible info

## 5.2 Information Leakage

### Definition
- 🔑 A design decision reflected in **multiple modules**
- Creates dependency: change requires modifying all involved modules
- Info in an interface = leaked by definition → simpler interfaces correlate with better hiding

### Back-Door Leakage
- Leakage without appearing in any interface
- Example: two classes both know a **file format** (one reads, one writes)
- ⚠️ More pernicious than interface leakage — it isn't obvious

### How to Respond
- 📌 One of the most important **red flags** in software design
- Cultivate high sensitivity to leakage
- Ask: "How can knowledge affect only a **single class**?"
- ✅ Merge small, closely-tied classes
- ✅ Extract a new class encapsulating just that info
  - ⚠️ Only works with a simple abstracting interface — else back-door leakage just becomes interface leakage

## 5.3 Temporal Decomposition

### Definition
- 🔑 Structure mirrors the **time order** of operations
- Example: read file → modify → write, split into three classes
- Read & write classes both know file format → leakage

### Why It's a Trap
- Execution order is on your mind while coding
- But design decisions manifest at **several different times** in an app's life

### The Fix
- Combine read/write mechanisms into one class used in both phases
- Order matters, but shouldn't drive module structure (unless stages use totally different info)
- 💡 Focus on the **knowledge needed** for tasks, not the order tasks occur

## 5.4 Example: HTTP Server

### Context
- Students in a software design course implemented HTTP classes
- Task: make it easy for servers to receive requests and send responses

### HTTP Basics
- Browser ↔ server communication over the network
- Requests and responses are **textual**
- POST request structure:
  - Initial line: request type, URL + parameters (`photo_id=246`), protocol version
  - Headers (e.g., `Content-Length`), terminated by empty line
  - Optional body with more parameters (`comment`, `priority`)

## 5.5 Example: Too Many Classes

### The Mistake
- Most common error: many **shallow classes** → leakage between them
- One team: class 1 reads request into string, class 2 parses it
- ⚠️ Temporal decomposition: "first read, then parse"

### Why It Leaked
- Can't read a request without parsing it
- `Content-Length` header must be parsed to know total request length
- Both classes understood most of HTTP request structure; parsing code **duplicated**
- Extra caller complexity: two methods, two classes, fixed order

### The Fix
- ✅ Merge into one class: reading + parsing
- Isolates request-format knowledge; simpler interface (one method)

### 💡 General Theme: Slightly Larger Classes Can Help
- Bring together all code for one capability (e.g., HTTP parsing)
- Raise the interface level: one method for the whole computation vs. three step methods
- Combined class is **deeper**
- ⚠️ Don't take it too far (one class for the whole app); Ch9 covers when to split

## 5.6 Example: HTTP Parameter Handling

### Background
- Parameters appear in the first line or the body
- Values use **URL encoding** (`+` = space, `%21` = `!`)
- Server wants values **unencoded**

### What Students Did Well
- ✅ Hid the header-line vs. body distinction; merged parameters
- ✅ Hid URL encoding: parser decodes before returning ("What a cute baby!")
- Both cases → simpler APIs

### The Shallow Mistake: `getParams()`
- `public Map<String, String> getParams()` returns the internal Map
- ❌ Exposes internal representation → representation change forces caller changes
- ❌ More caller work: getParams, then a Map lookup
- ❌ Callers must not modify the returned Map (affects internal state)
- 📌 Avoid exposing internal data structures

### The Better Interface
- `public String getParameter(String name)` — deeper, hides representation
- `public int getIntParameter(String name)` — hides string→int conversion
- Extensible: `getDoubleParameter`, etc.
- Throw exceptions for missing/unconvertible parameters

## 5.7 Example: Defaults in HTTP Responses

### The Mistake: Inadequate Defaults
- One team required callers to specify the **HTTP protocol version**
- But version must match the request, already passed as an argument
- ❌ Caller unlikely to know the version; specifying it leaks info
- ✅ Library should also default the **Date header**

### Principles
- 💡 Interfaces should make the **common case as simple as possible**
- Defaults = **partial information hiding**: normally invisible; overridable via special method
- 📌 Classes should "do the right thing" without being asked
- Java I/O counterexample: buffering should be automatic, not requested
- 💡 "The best features are the ones you get without even knowing they exist"

### ⚠️ Red Flag: Overexposure
- Common-case API forcing users to learn rarely-used features increases cognitive load

## 5.8 Information Hiding Within a Class

- Hiding applies inside classes too, not just external APIs
- Design **private methods** to each encapsulate some info/capability
- Minimize places each **instance variable** is used
- Fewer usage sites → fewer internal dependencies → less complexity

## 5.9 Taking It Too Far

- ⚠️ Only hide info that is **not needed outside** the module
- Example: performance config parameters needed by different users → must be exposed for tuning
- Goal: **minimize** info needed externally
  - ✅ Auto-adjusting configuration beats exposed parameters
- 📌 But recognize genuinely needed info and expose it

## 5.10 Conclusion

- Information hiding and deep modules are closely related
- More hidden info → more functionality + smaller interface → **deeper**
- Little hidden info → little functionality or complex interface → **shallow**
- Don't let runtime operation order shape modules (avoids temporal decomposition)
- Design each module around **one or a few pieces of knowledge**

## Key Takeaways

- 🔑 Hide design decisions inside modules; keep them out of interfaces
- 💡 Hiding cuts complexity twice: simpler interfaces + localized change
- ⚠️ Information leakage — especially back-door leakage — is a top red flag
- ⚠️ Temporal decomposition (structure = execution order) is a common leakage cause
- Organize modules around **knowledge**, not the order of operations
- Slightly larger, deeper classes often beat many shallow ones
- Never expose internal data structures; prefer targeted accessors
- Defaults make the common case simple — "do the right thing" automatically
- Expose only what's genuinely needed outside; hide everything else