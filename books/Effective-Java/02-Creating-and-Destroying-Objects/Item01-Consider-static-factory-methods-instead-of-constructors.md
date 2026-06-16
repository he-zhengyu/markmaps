---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 1: Static Factory Methods vs Constructors

## Core Idea
- 🔑 **Static factory method**: a `static` method that returns an instance of the class
- Can be provided *instead of*, or *in addition to*, public constructors
- ⚠️ Not the Factory Method pattern from *Design Patterns* [Gamma95] — no direct equivalent
- Example from `Boolean`:
  ```java
  public static Boolean valueOf(boolean b) {
      return b ? Boolean.TRUE : Boolean.FALSE;
  }
  ```
- 💡 Has both advantages and disadvantages — weigh them deliberately

## Advantages

### 1. They have names
- ✅ A well-chosen name makes the API easier to use and code easier to read
- ⚠️ Constructors can't describe the returned object when params aren't self-explanatory
- Example: `BigInteger(int, int, Random)` → better as `BigInteger.probablePrime`
- 📌 A class can have only **one** constructor per signature
  - ❌ Faking it by reordering parameter types confuses users
  - ✅ Factories with distinct names sidestep this restriction

### 2. Not required to create a new object each call
- Lets **immutable classes** (Item 17) reuse preconstructed or cached instances
- `Boolean.valueOf(boolean)` never creates an object
- Similar to the **Flyweight pattern** [Gamma95]
- 💡 Big performance win when equivalent objects are requested often or costly to build
- 🔑 **Instance-controlled** classes: control which instances exist at any time
  - Guarantee a class is a singleton (Item 3) or noninstantiable (Item 4)
  - Immutable value class: `a.equals(b)` *iff* `a == b`
  - Enum types (Item 34) provide this guarantee

### 3. Can return any subtype of the return type
- Great flexibility in choosing the returned object's class
- ✅ Return objects without making their classes public → **compact API**
- Suits **interface-based frameworks** (Item 20)
- `java.util.Collections`: ~45 implementations exported via factories in one noninstantiable class
  - Smaller API in bulk *and* conceptual weight
  - Client refers to object by interface, not implementation (Item 64)
- Companion-class convention (interface `Type` → `Types`) now mostly obsolete
  - As of **Java 8**, interfaces may have static methods
  - ⚠️ Java 8 requires interface static members to be public; **Java 9** adds private static methods, but static fields/member classes stay public

### 4. Returned class can vary by input parameters
- Any subtype of the declared return type is permissible; can change release to release
- 📊 `EnumSet` example (OpenJDK):
  - ≤ 64 elements → `RegularEnumSet` (backed by a single `long`)
  - ≥ 65 elements → `JumboEnumSet` (backed by a `long` array)
- 💡 Implementation classes are invisible to clients — free to add or remove them

### 5. Returned class need not exist when the method is written
- 🔑 Basis of **service provider frameworks** (e.g. **JDBC**)
- 🔑 Providers implement a service; the system exposes implementations, decoupling clients from them
- Three essential components:
  - **Service interface** — represents an implementation
  - **Provider registration API** — providers register implementations
  - **Service access API** — clients obtain instances (the flexible static factory itself)
- Optional fourth: **service provider interface** — a factory object producing service instances
  - Without it, implementations are instantiated reflectively (Item 65)
- JDBC mapping:
  - `Connection` → service interface
  - `DriverManager.registerDriver` → provider registration API
  - `DriverManager.getConnection` → service access API
  - `Driver` → service provider interface
- Variants: richer return type = **Bridge pattern**; DI frameworks (Item 5) are powerful providers
- 📌 Since **Java 6**: use built-in `java.util.ServiceLoader` rather than rolling your own (Item 59)

## Limitations

### Classes without public/protected constructors can't be subclassed
- ❌ Impossible to subclass Collections Framework convenience implementations
- ✅ Arguably a blessing: encourages composition over inheritance (Item 18); required for immutable types (Item 17)

### Hard for programmers to find
- ⚠️ Don't stand out in API docs the way constructors do
- ✅ Mitigate via clear class/interface documentation and common naming conventions

## Naming Conventions
- `from` — type-conversion, single param → `Date.from(instant)`
- `of` — aggregation, multiple params → `EnumSet.of(JACK, QUEEN, KING)`
- `valueOf` — verbose alternative to `from`/`of` → `BigInteger.valueOf(Integer.MAX_VALUE)`
- `instance` / `getInstance` — returns described instance, *not* necessarily same value → `StackWalker.getInstance(options)`
- `create` / `newInstance` — guarantees a **new** instance each call → `Array.newInstance(classObject, arrayLen)`
- `getType` — like `getInstance` but factory in a different class → `Files.getFileStore(path)`
- `newType` — like `newInstance` but factory in a different class → `Files.newBufferedReader(path)`
- `type` — concise alternative to `getType`/`newType` → `Collections.list(legacyLitany)`

## Key Takeaways
- 📌 Static factories and public constructors each have their place — understand their relative merits
- 💡 Five advantages: names, instance reuse/control, subtype returns, input-dependent class, deferred class existence
- ⚠️ Two costs: no subclassing without accessible constructors, and low discoverability
- ✅ Static factories are *often* preferable — **avoid the reflex** to reach for a public constructor first