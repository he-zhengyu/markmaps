---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

<!-- # Item 3 — Enforce Singleton via Private Constructor or Enum -->

## What Is a Singleton
- 🔑 A class **instantiated exactly once** *[Gamma95]*
- Typical use cases
  - A **stateless object** acting like a function (*Item 24*)
  - A **system component** that is intrinsically unique
- ⚠️ Makes clients **hard to test**
  - Can't substitute a mock implementation
  - Unless the singleton **implements an interface** to serve as its type

## Common Implementation Foundation
- Both standard approaches share the same mechanism
  - 📌 Keep the **constructor private**
  - 📌 Export a **public static member** for access to the sole instance

## Approach 1 — Public Final Field
- Member is a `public static final` field
```java
public class Elvis {
    public static final Elvis INSTANCE = new Elvis();
    private Elvis() { ... }
    public void leaveTheBuilding() { ... }
}
```
- How it works
  - Private constructor runs **once**, to set `Elvis.INSTANCE`
  - No public/protected constructor → a *"monoelvistic"* universe
  - 💡 Exactly one instance once the class is initialized — no client can change this
- ⚠️ Reflection caveat
  - Privileged client can invoke the private constructor reflectively (*Item 65*)
  - Via `AccessibleObject.setAccessible`
  - ✅ Defense: make the constructor **throw on a second instantiation**
- Advantages
  - ✅ **API clarity**: the `final` field signals the class is a singleton
  - ✅ **Simpler**

## Approach 2 — Static Factory Method
- Public member is a static factory
```java
public class Elvis {
    private static final Elvis INSTANCE = new Elvis();
    private Elvis() { ... }
    public static Elvis getInstance() { return INSTANCE; }
    public void leaveTheBuilding() { ... }
}
```
- All calls to `getInstance` return the **same reference** (same reflection caveat applies)
- Advantages
  - ✅ **Flexibility**: can stop being a singleton without changing the API
    - e.g. return a separate instance per invoking thread
  - ✅ Can write a **generic singleton factory** (*Item 30*)
  - ✅ A **method reference** works as a supplier
    - `Elvis::instance` is a `Supplier<Elvis>`
- 📌 Verdict: unless an advantage applies, the **public field approach is preferable**

## Serialization Concern (Approaches 1 & 2)
- ⚠️ Adding `implements Serializable` is **not sufficient**
- To preserve the singleton guarantee
  - Declare all instance fields `transient`
  - Provide a `readResolve` method (*Item 89*)
```java
private Object readResolve() {
    // Return the one true Elvis and let the GC
    // take care of the Elvis impersonator.
    return INSTANCE;
}
```
- ❌ Otherwise each deserialization creates a new instance — *spurious Elvis sightings*

## Approach 3 — Enum Singleton *(preferred)*
- Declare a **single-element enum**
```java
public enum Elvis {
    INSTANCE;
    public void leaveTheBuilding() { ... }
}
```
- Why it wins
  - ✅ More **concise**
  - ✅ **Serialization machinery for free**
  - ✅ 💡 **Ironclad guarantee** against multiple instantiation
    - Holds even against sophisticated serialization or reflection attacks
- 📌 Often the **best way** to implement a singleton, despite feeling unnatural
- ⚠️ Limitation
  - Can't be used if the singleton must **extend a superclass** other than `Enum`
  - (It *can* still **implement interfaces**)

## Key Takeaways
- A singleton guarantees **exactly one instance** via a private constructor + public static accessor
- Three implementations: **public final field**, **static factory**, **single-element enum**
- Between field and factory, prefer the **field** unless you need factory flexibility, a generic factory, or a supplier reference
- Both field/factory require **`transient` fields + `readResolve`** to stay singletons when serialized
- 📌 A **single-element enum** is usually the best choice — concise, serialization-safe, and attack-proof
- ⚠️ Singletons can complicate testing unless they implement an interface