---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 16: In Public Classes, Use Accessor Methods, Not Public Fields

## The Problem: Degenerate Classes
- 🔑 **Degenerate class**: groups instance fields, serves no other purpose
- Example: `class Point { public double x; public double y; }`
- ⚠️ Should **not** be public
- Direct field access forfeits **encapsulation** (Item 15)
- ❌ Can't change representation without changing the API
- ❌ Can't enforce invariants
- ❌ Can't take auxiliary action when a field is accessed

## The Object-Oriented Fix
- Replace public fields with **private fields**
- Add public **accessors** (getters)
- For mutable classes, add **mutators** (setters)
- Example: `getX()`, `getY()`, `setX()`, `setY()`
- 💡 Preserves flexibility to change internal representation

## When the Hard-Line Rule Applies
### Public classes (accessible outside package)
- ✅ Must provide accessor methods
- 📌 Exposing fields loses all hope of changing representation
- Client code can be distributed far and wide
### Package-private or private nested classes
- ✅ Exposing fields is acceptable
- *Condition*: fields adequately describe the class's abstraction
- 💡 Less visual clutter than the accessor approach
- Client coupling confined to the package
- Private nested class: change scope restricted to enclosing class

## Cautionary Tales in the JDK
- `Point` and `Dimension` in `java.awt` expose fields directly
- ⚠️ Treat as warnings, not examples to emulate
- 📌 Exposed `Dimension` internals caused a lasting performance problem (Item 67)

## The Immutable-Field Exception
- Less harmful for a public class to expose **immutable** fields
- ❌ Still can't change representation without changing API
- ❌ Still can't take auxiliary action on read
- ✅ Can enforce invariants
- Example: `public final class Time` with `public final int hour, minute`
  - Constructor validates `0 ≤ hour < 24`, `0 ≤ minute < 60`
  - Guarantees each instance is a valid time
- ⚠️ Still considered *questionable*

## Key Takeaways
- 📌 Public classes should **never** expose mutable fields
- ⚠️ Exposing immutable fields is less harmful but still questionable
- ✅ Package-private and private nested classes *may* expose fields (mutable or immutable)
- 💡 Accessor methods preserve the freedom to evolve a public API