---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 34: Use Enums Instead of int Constants

## The Problem: int Enum Pattern

### What It Is
- 🔑 **Enumerated type**: fixed set of legal constant values (seasons, planets, card suits)
- Pre-enum pattern: group of named `int` constants, e.g. `APPLE_FUJI = 0`
- Severely deficient!

### Shortcomings
- ❌ **No type safety**: compiler allows passing apple where orange expected
- ❌ Nonsense operations compile: `(APPLE_FUJI - ORANGE_TEMPLE) / APPLE_PIPPIN`
- ❌ **No namespaces**: prefixes needed to avoid clashes (`ELEMENT_MERCURY` vs `PLANET_MERCURY`)
- ❌ **Brittle**: values are constant variables, compiled into clients
  - Changing a value requires recompiling clients
  - Stale clients still run — with incorrect behavior
- ❌ **No printable strings**: printing/debugging shows only a number
- ❌ No reliable way to iterate over constants or get group size

### String Enum Pattern Variant
- Even less desirable than int variant
- ⚠️ Invites hard-coded string constants in client code
- Typos escape compile-time detection → runtime bugs
- Performance cost of string comparisons

## The Solution: Enum Types

### What Java Enums Are
- Simplest form: `public enum Apple { FUJI, PIPPIN, GRANNY_SMITH }`
- Unlike C/C++/C# enums (essentially int values) — **full-fledged classes**
- 💡 Export one instance per constant via `public static final` field
- Effectively final: no accessible constructors
- 🔑 **Instance-controlled**: generalization of singletons (single-element enums)

### Benefits Over int Constants
- ✅ **Compile-time type safety**: wrong-type pass/assign/`==` comparison → compile errors
- ✅ Each type has its **own namespace**: identically named constants coexist
- ✅ Add/reorder constants without recompiling clients (fields insulate constant values)
- ✅ Printable strings via `toString`
- ✅ Can add arbitrary methods, fields, and interfaces
- ✅ High-quality `Object` method implementations
- ✅ Implement `Comparable` and `Serializable`
- ✅ Serialized form withstands most enum changes

## Enums with Data and Behavior

### The Planet Example
- Each constant holds mass and radius → computes surface gravity → `surfaceWeight(mass)`
- Constructor parameters follow each constant: `MERCURY(3.302e+23, 2.439e6)`
- Recipe for rich enums:
  - Declare instance fields; constructor stores the data
  - 📌 Enums are immutable — all fields should be **final** (Item 17)
  - Prefer private fields + public accessors (Item 16)
  - Derived values (surface gravity) can be precomputed as optimization

### Built-in Conveniences
- Static `values()` method: array of constants in declaration order
- Default `toString` returns declared name — easy `println`/`printf`
- `valueOf(String)` translates name → constant (auto-generated)

### Removing a Constant (Pluto, 2006)
- Clients not referring to removed element: keep working fine
- Clients referring to it:
  - Recompile → helpful compile error at the offending line
  - No recompile → helpful runtime exception at that line
- 💡 Best behavior you could hope for — far better than int pattern

### API Design Guidance
- Hide constant behaviors used only internally: private/package-private methods (Item 15)
- Generally useful enum → top-level class (e.g. `java.math.RoundingMode`)
- Enum tied to one class → member class of that class (Item 24)
- Top-level reuse increases API consistency

## Constant-Specific Behavior

### Switching on Own Value — Questionable
- `Operation` enum with `switch(this)` in `apply` method
- ❌ Needs unreachable `throw` to compile
- ⚠️ **Fragile**: new constant without new case → compiles but fails at runtime

### Constant-Specific Method Implementations
- 🔑 Declare **abstract method** in enum; override in each constant's class body
- New constant → `apply` sits right beside declaration, hard to forget
- ✅ Compiler enforces: abstract methods must be overridden in all constants

### Combining with Constant-Specific Data
- `Operation` with symbol field: `PLUS("+") { ... }`
- Override `toString` to return the symbol → easy expression printing

### The fromString Idiom
- 📌 If you override `toString`, consider a `fromString` method
- Build `Map<String, Operation>` from `Stream.of(values())` in static field initialization
- Returns `Optional<Operation>` → forces client to confront invalid strings (Item 55)
- ⚠️ Constants **cannot** add themselves to map from constructors
  - Enum constructors can't access static fields (except constant variables)
  - Static fields not yet initialized when constructors run
  - Constants can't access one another from constructors

## Sharing Code Among Constants

### The PayrollDay Problem
- Pay = base pay + overtime; weekdays vs weekends differ
- Switch with multiple case labels: concise but dangerous
- ⚠️ Add vacation day, forget case → silently paid as ordinary weekday
- Constant-specific methods alternative: duplicated computation or helper-method boilerplate
- Concrete default `overtimePay` + weekend overrides: silently inherits weekday behavior

### The Strategy Enum Pattern
- 💡 Goal: be **forced to choose** a strategy for each new constant
- Move overtime computation into private nested enum (`PayType`)
- Pass strategy instance to `PayrollDay` constructor
- `PayrollDay` delegates pay calculation to the strategy enum
- ✅ Safer and more flexible, though less concise than switch

## When Switches on Enums Are Good
- ✅ **Augmenting** enum types with constant-specific behavior
- Example: static `inverse(Operation)` when enum isn't under your control
- Also for your own enums when a method doesn't belong in the type itself

## When to Use Enums
- 📌 Any set of constants **known at compile time**
- Natural enumerated types: planets, days of week, chess pieces
- Also: menu choices, operation codes, command line flags
- Set need not stay fixed forever — designed for binary compatible evolution
- 📊 Performance comparable to int constants
- ⚠️ Minor space/time cost to load and initialize — rarely noticeable

## Key Takeaways
- Enums are more **readable, safer, more powerful** than int constants
- Many enums need no explicit constructors or members
- Associate data with constants via fields + constructor when beneficial
- Prefer **constant-specific methods** over switching on own value
- Use the **strategy enum pattern** when some, but not all, constants share behavior