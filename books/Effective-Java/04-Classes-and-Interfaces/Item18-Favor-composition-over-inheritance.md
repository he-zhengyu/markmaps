---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 18: Favor Composition over Inheritance

## Scope & Safe Uses of Inheritance
- 🔑 **Inheritance** here means *implementation inheritance* (one class `extends` another)
- ❌ Does **not** apply to *interface inheritance* (`implements` an interface, or interface extending interface)
- ✅ Safe **within a package** — sub/superclass controlled by same programmers
- ✅ Safe when extending classes **designed and documented for extension** (Item 19)
- ⚠️ Dangerous: inheriting from ordinary concrete classes **across package boundaries**

## Why Inheritance Is Problematic
### Violates Encapsulation
- 💡 Unlike method invocation, **inheritance breaks encapsulation** [Snyder86]
- Subclass depends on the **implementation details** of its superclass
- Superclass implementation may change release to release
- ⚠️ Subclass can **break though its own code is untouched**
- 📌 Subclass must evolve in tandem with its superclass

### Fragility from Overriding — `InstrumentedHashSet`
- Goal: count attempted insertions via a `HashSet` variant
- Overrides both element-adding methods: `add` and `addAll`
- 📊 After `addAll(List.of("Snap","Crackle","Pop"))`, `getAddCount()` returns **6, not 3**
- 💡 Cause: `HashSet.addAll` is internally built on `add` → each element **double-counted**
- ⚠️ The "self-use" of `add` by `addAll` is an **undocumented implementation detail**, subject to change

### Attempted Fixes All Fail
- ❌ Drop the `addAll` override → still depends on fragile undocumented self-use
- ❌ Reimplement `addAll` to loop calling `add`
  - Difficult, time-consuming, error-prone, may hurt performance
  - Sometimes impossible — needs **private fields** inaccessible to subclass

### Fragility from New Superclass Methods
- Superclass can **gain new methods** in later releases
- 💡 A new element-adding method bypasses subclass invariant checks
- ⚠️ Real example: security holes fixed when **`Hashtable` and `Vector`** joined the Collections Framework

### Even Adding (Not Overriding) Methods Is Risky
- New superclass method, same signature **+ different return type** → ❌ subclass won't compile [JLS 8.4.8.3]
- Same signature **+ same return type** → you're now overriding it (earlier problems return)
- ⚠️ Your method unlikely to honor a contract written **after** you wrote it

## The Solution: Composition & Forwarding
### Mechanism
- 🔑 **Composition**: new class holds a *private field* referencing an instance of the existing class
- 🔑 **Forwarding methods**: each method invokes the corresponding method on the contained instance
- 💡 Result is **rock solid** — no dependence on the existing class's internals; new methods on it have no impact

### Implementation in Two Pieces
- **Wrapper class** `InstrumentedSet<E> extends ForwardingSet<E>` — holds the instrumentation logic
- **Reusable forwarding class** `ForwardingSet<E> implements Set<E>` — wraps a private `Set` and forwards every method

### Why It Is Superior
- Enabled by the **`Set` interface** capturing `HashSet`'s functionality
- ✅ Flexible: a single `Set`-argument constructor instruments **any `Set` implementation**
- ✅ Works with any preexisting constructor (`TreeSet`, `HashSet`, …)
- ✅ Can temporarily instrument an already-used set instance
- 💡 Inheritance approach works for **one concrete class** and needs a constructor per superclass constructor

### Patterns & Terminology
- 🔑 **Wrapper class** — each instance contains ("wraps") another instance
- 🔑 **Decorator pattern** [Gamma95] — decorates the set by adding instrumentation
- 🔑 **Delegation** — loose name for composition + forwarding; *technically* delegation only if wrapper passes itself to the wrapped object [Lieberman86]

### Disadvantages (Few)
- ⚠️ Unsuited to **callback frameworks** — the **SELF problem** [Lieberman86]: wrapped object passes `this`, callbacks elude the wrapper
- 📌 Performance / memory overhead of forwarding — negligible in practice
- Tedious to write forwarding methods — but written **once per interface**; e.g. **Guava** provides them [Guava]

## When Inheritance *Is* Appropriate
### The "is-a" Test
- ✅ Use inheritance only for a genuine **subtype** relationship
- 📌 Ask: *Is every B really an A?* — if not, **B should not extend A**
- If no: B should hold a **private instance of A** and expose a different API

### Java Platform Violations
- ❌ `Stack` extends `Vector` — a stack is **not** a vector
- ❌ `Properties` extends `Hashtable` — a property list is **not** a hash table
- Composition would have been preferable in both

### Consequences of Misuse
- ⚠️ Needlessly exposes implementation details; API forever tied to original implementation
- Clients access internals directly → confusing semantics
- 💡 `p.getProperty(key)` (uses defaults) ≠ inherited `p.get(key)` (ignores defaults)
- ⚠️ Most serious: clients can **corrupt invariants** — non-string keys broke `Properties` `load`/`store`, too late to fix

### Final Question Before Choosing Inheritance
- Does the class you'd extend have **API flaws**?
- ⚠️ Inheritance **propagates** superclass API flaws
- ✅ Composition lets you design a new API that **hides** them

## Key Takeaways
- Inheritance is powerful but **violates encapsulation**, causing fragility across package boundaries
- Use inheritance only when a **genuine subtype ("is-a") relationship** truly exists
- Prefer **composition and forwarding (wrapper classes)**, especially when a suitable interface exists
- Wrapper classes are both **more robust and more powerful** than subclasses