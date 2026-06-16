---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

<!-- # Item 4: Enforce Noninstantiability with a Private Constructor -->

## Utility Classes — When You Want Them
- A class that is just a grouping of **static methods** and **static fields**
- ⚠️ Bad reputation: abused to avoid thinking in terms of objects
- 💡 But they have valid uses
- Group related methods on **primitive values or arrays**
  - e.g. `java.lang.Math`, `java.util.Arrays`
- Group static methods, including **factories** (Item 1), for objects implementing some interface
  - e.g. `java.util.Collections`
  - 📌 As of **Java 8**, such methods can also go in the interface (if it's yours to modify)
- Group methods on a **final class**
  - 🔑 You can't put them in a subclass

## The Problem
- 🔑 Utility classes were **not designed to be instantiated** — an instance would be nonsensical
- ⚠️ With no explicit constructors, the compiler supplies a **public, parameterless default constructor**
- To a user, this constructor is indistinguishable from any other
- 📌 Unintentionally instantiable classes appear in published APIs

## Wrong Approach: Making the Class `abstract`
- ❌ The class can be subclassed and the subclass instantiated
- ❌ Misleads the user into thinking the class was designed for **inheritance** (Item 19)

## The Solution: Private Constructor Idiom
- 🔑 A default constructor is generated **only** if the class contains no explicit constructors
- ✅ Add a `private` constructor to make the class noninstantiable

```java
// Noninstantiable utility class
public class UtilityClass {
    // Suppress default constructor for noninstantiability
    private UtilityClass() {
        throw new AssertionError();
    }
    ... // Remainder omitted
}
```

- `private` → constructor inaccessible **outside** the class
- The `AssertionError` isn't strictly required
  - 💡 Insurance if the constructor is accidentally invoked **from within** the class
  - Guarantees the class is never instantiated under any circumstances
- ⚠️ Mildly counterintuitive: the constructor exists expressly so it *cannot* be invoked
- 📌 Include a **comment** explaining the intent

## Side Effect: Prevents Subclassing
- All constructors must invoke a superclass constructor, explicitly or implicitly
- ✅ A subclass would have **no accessible superclass constructor** to invoke

## Key Takeaways
- 🔑 Utility classes (static-only) should never be instantiated
- ⚠️ Without an explicit constructor, the compiler adds a public default one
- ❌ Using `abstract` does **not** enforce noninstantiability and invites misuse
- ✅ A single **private constructor that throws `AssertionError`** is the correct idiom
- 💡 The idiom also blocks subclassing as a free side effect
- 📌 Always document *why* the private constructor exists