---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Ch.4 Modules Should Be Deep

## 4.1 Modular design
- 💡 Core technique: developers face only a **small fraction** of complexity at a time
- 🔑 **Modular design**: decompose system into relatively independent **modules**
  - Forms: classes, subsystems, services
  - Also methods/functions — anything with interface + implementation
- Ideal: modules completely independent → system complexity = worst module
  - ⚠️ Not achievable: modules must call each other
- 🔑 **Dependencies**: if one module changes, others may need to change
  - Example: method signature ↔ all its invocations
  - Can be subtle, e.g. method requires another to be called first
  - 📌 Goal: **minimize dependencies** between modules
- Each module has two parts
  - 🔑 **Interface**: what others must know to use the module — *what*, not *how*
  - 🔑 **Implementation**: code carrying out the interface's promises
  - Developer must know: own module's interface + implementation, others' interfaces only
  - Example: balanced tree — complex balancing hidden; simple insert/remove/fetch interface
- ✅ Best modules: interface **much simpler** than implementation
  - Minimizes complexity imposed on rest of system
  - Implementation changes don't ripple if interface unchanged

## 4.2 What's in an interface?
- **Formal** parts
  - Specified explicitly in code; checkable by the language
  - Method: signature — parameter names/types, return type, exceptions
  - Class: signatures of all public methods + public variables
- **Informal** parts
  - Not enforceable by the language; described only in comments
  - High-level behavior (e.g. "deletes the file named by an argument")
  - Usage constraints (e.g. call order between methods)
  - 📌 Rule: anything a developer must know to use a module is part of its interface
  - ⚠️ Usually **larger and more complex** than the formal parts
  - Footnote: formal specification languages exist, but English descriptions are likely more intuitive
- 💡 A clearly specified interface eliminates "unknown unknowns" (cf. §2.2)

## 4.3 Abstractions
- 🔑 **Abstraction**: simplified view of an entity that **omits unimportant details**
  - Makes complex things easier to think about and manipulate
  - Each module's interface *is* its abstraction
- The word "unimportant" is crucial
  - More unimportant details omitted → better abstraction
- Two ways abstractions go wrong
  - ❌ Includes unimportant details → unnecessary complexity, higher cognitive load
  - ❌ Omits **important** details → obscurity
    - 🔑 **False abstraction**: looks simple but isn't
- 💡 Key to design: understand what's important; minimize what *must* be important
- Example: file system
  - Omitted: block allocation on storage device
  - Must be visible: rules for flushing cached data to disk (databases need crash guarantees)
- Everyday abstractions: microwave buttons, car controls hide complex machinery

## 4.4 Deep modules
- 🔑 **Deep module**: powerful functionality behind a simple interface
  - Rectangle visualization (Fig. 4.1): area = functionality, top edge = interface complexity
- 💡 Depth = cost vs. benefit
  - Benefit = functionality; cost = interface (complexity imposed on system)
  - ⚠️ More or larger interfaces are *not* necessarily better
- Example: **Unix file I/O**
  - Only five basic system calls: `open`, `read`, `write`, `lseek`, `close`
  - `open` returns integer **file descriptor**; sequential access is default; `lseek` for random access
  - Implementation: hundreds of thousands of lines hiding
    - On-disk file representation for efficient access
    - Directory storage & hierarchical path lookup
    - Permission enforcement
    - Interrupt handlers vs. background code
    - Scheduling for concurrent access
    - In-memory caching to reduce disk reads
    - Supporting diverse storage devices
  - 📌 Implementations evolved radically; the five calls never changed
- Example: **garbage collector** (Go, Java)
  - No interface at all — works invisibly
  - 💡 Adding GC *shrinks* the system's interface (removes object freeing)

## 4.5 Shallow modules
- 🔑 **Shallow module**: interface complex relative to functionality provided
- Example: linked list class
  - Insert/delete take only a few lines; little hidden
  - Interface complexity ≈ implementation complexity
  - Sometimes unavoidable, but little leverage against complexity
- Extreme example: `addNullValueForAttribute(String attribute)`
  - One line: `data.put(attribute, null);`
  - ❌ No abstraction — all functionality visible through interface
  - ❌ Proper documentation would be longer than the code
  - ❌ Calling it takes more keystrokes than direct manipulation
  - Adds a new interface to learn with no compensating benefit
- ⚠️ **Red Flag: Shallow Module** — benefit (hidden internals) negated by cost of learning the interface; small modules tend to be shallow

## 4.6 Classitis
- ⚠️ Conventional wisdom: classes should be **small**, not deep
  - "Any method longer than N lines should be split" (N as low as 10)
  - Produces many shallow classes/methods → more system complexity
- 🔑 **Classitis**: "classes are good, so more classes are better"
  - Minimize functionality per class; want more? add more classes
  - Classes individually simple, but interfaces accumulate → tremendous system-level complexity
  - Verbose style from per-class boilerplate

## 4.7 Examples: Java and Unix I/O
- ❌ Java class library: visible classitis (culture, not language requirement)
  - Reading serialized objects required three objects
    - `FileInputStream` — rudimentary I/O only
    - `BufferedInputStream` — adds buffering
    - `ObjectInputStream` — adds serialized-object reading
  - First two never used after opening
  - ⚠️ Forgetting `BufferedInputStream` → silently slow, unbuffered I/O
- 💡 Principle: **make the common case as simple as possible**
  - Nearly everyone wants buffering → should be the default
  - Disabling it should be a cleanly separated mechanism most never see
- ✅ Unix contrast: sequential I/O is the common case → made the default
  - Random access still easy via `lseek`, invisible if unneeded
  - 💡 Effective interface complexity = complexity of the **commonly used** features

## Key Takeaways
- 📌 Separate interface from implementation to hide complexity from the rest of the system
- 📌 Users need only understand the interface's abstraction
- 📌 The most important issue in module design: make modules **deep** — simple interfaces for common cases, significant functionality
- 💡 Depth maximizes the amount of complexity concealed
- ⚠️ Beware shallow modules and classitis: many small classes add net complexity