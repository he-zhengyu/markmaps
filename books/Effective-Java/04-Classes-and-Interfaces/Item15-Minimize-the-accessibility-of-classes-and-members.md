---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 15: Minimize the Accessibility of Classes and Members

## Information Hiding (Encapsulation)
- 🔑 Hiding a component's internal data & implementation details from other components
- 💡 Well-designed component cleanly separates its **API** from its **implementation**
- Components communicate only through APIs, oblivious to each other's internals
- 📌 A fundamental tenet of software design `[Parnas72]`
### Why It Matters
- 💡 Core benefit: **decouples** the components of a system
- ✅ Develop, test, optimize, use, understand & modify components in isolation
- ✅ Speeds development — components built in **parallel**
- ✅ Eases maintenance — easier to understand, debug, replace safely
- ✅ Enables effective **performance tuning** after profiling (Item 67)
- ✅ Increases software **reuse** — loosely coupled components useful elsewhere
- ✅ Decreases **risk** in large systems — components may succeed even if system fails

## Java's Access Control Mechanism
- 🔑 Specifies accessibility of classes, interfaces & members `[JLS, 6.6]`
- Determined by **declaration location** + **access modifier** (`private`, `protected`, `public`)
- 📌 **Rule of thumb:** make each class or member *as inaccessible as possible*
- Use lowest access level consistent with proper functioning

## Top-Level Classes & Interfaces
- Only two access levels: **package-private** & **public**
- `public` modifier → public; otherwise → package-private
### Prefer Package-Private
- ✅ If it can be package-private, it should be
- 💡 Becomes part of implementation, not exported API → free to modify/replace/remove
- ⚠️ Making it `public` obligates you to support it *forever* for compatibility
### Reducing Further
- If used by only one class, make it a `private static` nested class (Item 24)
- ⚠️ Far more important to demote a *gratuitously public* class than a package-private one

## Members: Four Access Levels
- *(increasing accessibility)*
### `private`
- 🔑 Accessible only from the top-level class where declared
### `package-private`
- 🔑 Accessible from any class in the same package
- Technically "default access" — no modifier specified
- ⚠️ Exception: interface members are `public` by default
### `protected`
- 🔑 Accessible from subclasses + classes in the same package `[JLS, 6.6.2]`
### `public`
- 🔑 Accessible from anywhere

## Guidelines for Members
### Default to private
- **📌 After designing the public API**, reflex should be to make everything else `private`
- Relax to package-private only if another class in the package truly needs it
- 💡 Doing this often signals a design that needs better decomposition
- ⚠️ `private`/package-private fields can still **leak** into the API via `Serializable` (Items 86, 87)
### protected Is Expensive
- ⚠️ Jump from package-private → `protected` is a *huge* increase in accessibility
- A `protected` member is part of the exported API — supported forever
- 💡 Represents a public commitment to an implementation detail (Item 19)
- The need for protected members should be relatively rare
### Override Constraint
- 📌 Overriding method **cannot** be more restrictive than superclass method `[JLS, 8.4.8.3]`
- 💡 Ensures the **Liskov substitution principle** — subclass usable wherever superclass is
- Violation → compiler error
- Special case: interface methods implemented in a class must be `public`

## Testing & Accessibility
- ✅ Acceptable: relax a `private` member to package-private to test it
- ❌ Not acceptable: raise accessibility any higher to facilitate testing
- 💡 Unnecessary anyway — run tests as part of the package under test for package-private access

## Public Fields Are Dangerous
### Instance Fields
- 📌 Instance fields of public classes should rarely be `public` (Item 16)
- ⚠️ Nonfinal / mutable-reference field → lose ability to enforce **invariants**
- ⚠️ Lose ability to act on modification → not generally thread-safe
- ⚠️ Even `final` + immutable → lose flexibility to change internal representation
### Static Fields & Constants
- ✅ Exception: expose constants via `public static final` fields (integral to the abstraction)
- Naming convention: capitals with underscores (Item 68)
- 📌 Must hold **primitives** or references to **immutable** objects (Item 17)
- ⚠️ Reference to a mutable object has all the disadvantages of a nonfinal field

## The Mutable Array Pitfall
- 🔑 A nonzero-length array is *always* mutable
- ❌ Wrong to have a `public static final` array field or accessor returning one
- ⚠️ Frequent source of **security holes** — clients can modify contents
- ⚠️ Some IDEs auto-generate accessors returning private array references
### Two Fixes
- ✅ Private array + public immutable `List`
  - ```java
    private static final Thing[] PRIVATE_VALUES = { ... };
    public static final List<Thing> VALUES =
      Collections.unmodifiableList(Arrays.asList(PRIVATE_VALUES));
    ```
- ✅ Private array + method returning a `.clone()` copy
  - ```java
    private static final Thing[] PRIVATE_VALUES = { ... };
    public static final Thing[] values() {
      return PRIVATE_VALUES.clone();
    }
    ```
- 💡 Choose by what the client will do: which return type is more convenient / performant?

## Module System (Java 9+)
- 🔑 A **module** groups packages, as a package groups classes
- Exports packages via `export` declarations in `module-info.java`
- 💡 Public/protected members of *unexported* packages are inaccessible outside the module
- Gives two implicit, intramodular access levels (analogues of public/protected)
- 💡 Lets you share classes within a module without exposing them to the world
### Caveats
- ⚠️ Module access levels are largely **advisory**
- On the *class path* (not module path), packages revert to non-modular behavior `[Reinhold, 1.2]`
- Strictly enforced only within the **JDK** itself
- ⚠️ Requires modularizing packages, explicit dependencies, source-tree rearrangement `[Reinhold, 3]`
- 📌 Best to avoid modules unless you have a compelling need

## Key Takeaways
- 📌 Reduce accessibility of program elements as much as possible (within reason)
- 💡 Design a minimal public API; prevent stray classes/interfaces/members from joining it
- ⚠️ Public classes should have **no public fields** — except `public static final` constants
- 📌 Objects referenced by `public static final` fields **must be immutable**
- 🔑 Information hiding decouples components → faster development, easier maintenance, reuse & lower risk