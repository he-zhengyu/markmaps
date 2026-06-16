---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 6: Avoid Creating Unnecessary Objects

## Core Principle
- Reuse a single object instead of creating a new **functionally equivalent** one each time
- 💡 Reuse can be both *faster* and more *stylish*
- 🔑 An object can **always** be reused if it is **immutable** (Item 17)

## Reusing Immutable Objects
### The `String` Anti-Pattern
- ❌ `String s = new String("bikini");`
  - Creates a new `String` instance on **every** execution
  - The argument `"bikini"` is *itself* a `String`, identical to all objects the constructor makes
  - ⚠️ In a loop or hot method → **millions** of needless instances
- ✅ `String s = "bikini";`
  - Uses a single `String` instance
  - 📌 Guaranteed reuse across the same JVM for identical **string literals** (JLS 3.10.5)

### Prefer Static Factory Methods
- Use static factories (Item 1) over constructors on immutable classes that offer both
- ✅ `Boolean.valueOf(String)` over `Boolean(String)` constructor (deprecated in Java 9)
- 🔑 Constructor **must** create a new object; factory is *never required* to

### Reusing Mutable Objects
- Mutable objects can be reused too — *if you know they won't be modified*

## Caching Expensive Objects
- 💡 Some object creations are far more expensive than others; cache the expensive ones for reuse
- ⚠️ It's not always obvious when you're creating an expensive object

### Example: Roman Numeral Validation
- ❌ Slow version relies on `String.matches`
  - 🔑 `String.matches` internally builds a `Pattern`, uses it once, then discards it
  - Compiling a regex into a **finite state machine** is expensive
- ✅ Compile the `Pattern` once as a `static final` field and reuse it
  ```java
  private static final Pattern ROMAN = Pattern.compile(
      "^(?=.)M*(C[MD]|D?C{0,3})"
    + "(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})$");
  ```
- 📊 On the author's machine: **1.1 μs → 0.17 μs** (≈ 6.5× faster) on 8-char input
- ✅ Bonus: naming the field improves **clarity** over a raw regex

### Lazy Initialization Caveat
- ⚠️ Lazy-initializing `ROMAN` (Item 83) is **not recommended** here
- Complicates the implementation with no measurable gain (Item 67)

## Reusing Adapters (Views)
- 🔑 **Adapter / view**: an object delegating to a backing object, offering an alternative interface (Gamma95)
- Has no state beyond its backing object → no need for more than one instance per backing object
- 💡 Example: `Map.keySet()` may return the **same** `Set` view on each call
  - All returned `Set`s are functionally identical — all backed by the same `Map`
  - Multiple instances are harmless but unnecessary

## Autoboxing Pitfall
- 🔑 **Autoboxing**: automatic conversion between primitive and boxed types
- ⚠️ Blurs but doesn't erase the primitive/boxed distinction → subtle semantics + performance costs (Item 61)
- ❌ The one-character bug:
  ```java
  Long sum = 0L;           // should be 'long'
  for (long i = 0; i <= Integer.MAX_VALUE; i++)
      sum += i;            // boxes ~2^31 times
  ```
  - Declaring `sum` as `Long` constructs ~**2³¹** unnecessary `Long` instances
- 📊 Fixing `Long` → `long`: **6.3 s → 0.59 s**
- 📌 Lesson: prefer **primitives** to boxed primitives; watch for unintentional autoboxing

## When NOT to Avoid Object Creation
- ⚠️ Don't read this item as "object creation is expensive and should be avoided"
- ✅ Creating/reclaiming small objects with cheap constructors is **inexpensive**, especially on modern JVMs
- ✅ Creating objects to enhance *clarity, simplicity, or power* is generally good

### Object Pools Are Usually Bad
- ❌ Maintaining your own object pool is bad unless objects are *extremely heavyweight*
- ✅ Justified case: a **database connection** (high setup cost)
- ⚠️ Otherwise pools clutter code, increase memory footprint, and harm performance
- 💡 Modern garbage collectors easily outperform pools on lightweight objects

## Counterpoint: Defensive Copying (Item 50)
- This item: *"Don't create a new object when you should reuse an existing one"*
- Item 50: *"Don't reuse an existing object when you should create a new one"*
- 📌 The penalties are **asymmetric**:
  - ❌ Failing to defensively copy → insidious **bugs and security holes**
  - ⚠️ Creating objects needlessly → merely affects *style and performance*

## Key Takeaways
- 🔑 Reuse immutable objects freely; reuse mutable ones only when they won't change
- ✅ Prefer static factory methods over `new` on immutable classes
- 📌 Cache **expensive** objects (compiled `Pattern`s, etc.) as `static final` fields
- 📌 Prefer **primitives** over boxed primitives to avoid hidden autoboxing
- ⚠️ Don't build object pools for lightweight objects — trust the JVM's garbage collector
- 💡 The goal is avoiding *needless* creation, not avoiding object creation altogether
- 📌 When in doubt, defensive copying (Item 50) outweighs the cost of an extra object