---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Ch.4 Modules Should Be Deep

## 4.1 Modular design

### Core idea
- 🔑 **Modular design**: decompose system into relatively independent modules
- Goal: developers face only a **small fraction of complexity** at a time
- Modules take many forms: **classes, subsystems, services**
- Ideal world: each module fully independent → system complexity = worst module's complexity
- ⚠️ Ideal unachievable: modules must call each other → **dependencies**

### Dependencies
- If one module changes, others may need to change to match
- Example: method arguments create dependency with all callers
- Can be subtle: e.g., method requires another method invoked first
- 📌 Goal of modular design: **minimize dependencies** between modules

### Interface vs. implementation
- 🔑 **Interface**: everything a developer in another module must know to use this one
  - Describes *what* the module does, not *how*
- 🔑 **Implementation**: code carrying out the promises made by the interface
- Developer must understand: own module's interface + implementation, plus **interfaces only** of invoked modules
- Example: balanced tree module
  - Complex balancing code hidden
  - Simple interface: insert / remove / fetch with key & value

### What counts as a module
- Any unit of code with an interface and an implementation
- Classes, methods, functions, subsystems, services
- Higher-level interfaces may be kernel calls or HTTP requests

### Best modules
- Interface **much simpler** than implementation
- ✅ Simple interface minimizes complexity imposed on rest of system
- ✅ Changes not affecting the interface don't affect other modules

## 4.2 What's in an interface?

### Formal parts
- Specified explicitly in code; language can check correctness
- Method: **signature** — parameter names/types, return type, exceptions
- Class: signatures of all public methods + public variables

### Informal parts
- Not enforceable by the programming language
- High-level behavior (e.g., "deletes the file named by an argument")
- Usage constraints (e.g., call order between methods)
- 📌 Rule: any info a developer needs to use a module is part of its interface
- Only describable via **comments**; language can't verify completeness
- ⚠️ Informal aspects usually **larger and more complex** than formal ones
- Footnote: formal specification languages exist (research), but English descriptions are likely more intuitive

### Benefit of clear interfaces
- 💡 Shows exactly what developers need to know → eliminates **"unknown unknowns"** (Section 2.2)

## 4.3 Abstractions

### Definition
- 🔑 **Abstraction**: simplified view of an entity, omitting unimportant details
- Makes complex things easier to think about and manipulate
- Each module's interface *is* its abstraction

### The word "unimportant" is crucial
- The more unimportant details omitted, the better
- Two failure modes:
  - ❌ Includes unimportant details → more complicated than necessary, higher cognitive load
  - ❌ Omits **important** details → **obscurity**; a **false abstraction** (looks simple, isn't)
- 💡 Key skill: understand what's important; design to **minimize what is important**

### Examples
- File system
  - Omits block allocation details — unimportant to users
  - ⚠️ Caching / delayed writes matter to databases → flush rules must be in the interface
- Everyday life
  - Microwave oven: complex electronics behind a few buttons
  - Cars: drive without understanding motors, ABS, cruise control

## 4.4 Deep modules

### Concept
- 🔑 **Deep module**: powerful functionality behind a simple interface
- Rectangle visualization (Figure 4.1)
  - Area = functionality; top edge = interface complexity
- 💡 Cost vs. benefit: benefit = functionality; cost = interface complexity
- ⚠️ More or larger interfaces are **not** necessarily better

### Example: Unix file I/O
- Only five basic system calls with simple signatures
  - `open`, `read`, `write`, `lseek`, `close`
- Implementation: hundreds of thousands of lines handling
  - On-disk file representation for efficient access
  - Directory storage & hierarchical path lookup
  - Permission enforcement
  - Interrupt handlers vs. background code coordination
  - Scheduling policies for concurrent access
  - Caching to reduce disk accesses
  - Supporting diverse storage devices (disks, flash)
- 📌 Implementations evolved radically; the five calls never changed

### Example: garbage collector (Go, Java)
- **No interface at all** — works invisibly
- 💡 Adding GC *shrinks* system's interface (eliminates freeing objects)
- Complex implementation, fully hidden

## 4.5 Shallow modules

### Concept
- 🔑 **Shallow module**: interface relatively complex vs. functionality provided
- Example: linked list class
  - Manipulation takes few lines; abstraction hides little
  - Interface complexity ≈ implementation complexity
  - Sometimes unavoidable and useful, but little leverage against complexity

### Extreme example
- `addNullValueForAttribute(String attribute) { data.put(attribute, null); }`
  - ❌ No abstraction: all functionality visible in interface
  - Caller must still know about the `data` variable
  - Proper documentation would be longer than the code
  - More keystrokes to call than to do it directly
  - Adds interface complexity with no compensating benefit

### 🚩 Red Flag: Shallow Module
- Benefit (hidden internals) negated by cost of learning the interface
- ⚠️ Small modules tend to be shallow

## 4.6 Classitis

- Conventional wisdom: classes should be **small**, not deep
- Common teaching: split large classes; "methods > N lines must be divided" (N as low as 10)
- 🔑 **Classitis**: syndrome from the view "classes are good, so more classes are better"
- Consequences
  - ❌ Individually simple classes, but **greater overall system complexity**
  - Many small classes → many interfaces → complexity accumulates system-wide
  - Verbose programming style from per-class boilerplate

## 4.7 Examples: Java and Unix I/O

### Java class library (classitis)
- Language doesn't require small classes; the **culture** does
- Reading serialized objects from a file needed **three objects**
  - `FileInputStream` → rudimentary I/O only
  - `BufferedInputStream` → adds buffering
  - `ObjectInputStream` → reads/writes serialized objects
  - First two never used after opening
- ⚠️ Buffering must be requested explicitly — forgetting it silently makes I/O slow
- 💡 Interfaces should make the **common case as simple as possible**
  - Almost everyone wants buffering → provide by default
  - Disabling should be cleanly separated so most developers never see it
- AI-added: Java 7+ eases this somewhat (e.g., `Files.newBufferedReader`), but the design lesson stands

### Unix system calls (contrast)
- ✅ Common case made simple: **sequential I/O is the default**
- Random access easy via `lseek`, invisible to sequential-only users
- 💡 Effective interface complexity = complexity of the **commonly used features**

## Key Takeaways
- 📌 Separate interface from implementation to **hide complexity** from the rest of the system
- 📌 Make modules **deep**: simple interfaces for common cases, significant functionality behind them
- 💡 Depth = benefit (functionality) ÷ cost (interface complexity)
- ⚠️ Beware classitis: many small shallow classes increase system-level complexity
- ✅ Design for the common case; keep rare options out of sight