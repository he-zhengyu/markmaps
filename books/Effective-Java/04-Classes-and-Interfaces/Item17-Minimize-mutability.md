---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Minimize Mutability (Item 17)

## 🔑 What Is an Immutable Class
- A class whose instances **cannot be modified**
- All info fixed for the object's **lifetime** — no change observable
- 💡 Easier to design, implement, and use than mutable classes
- ✅ Less error-prone and more secure
- Platform examples: `String`, boxed primitives, `BigInteger`, `BigDecimal`

## Five Rules for Immutability
### 1. No mutators
- Don't provide methods that modify the object's state
### 2. Prevent extension
- Stops careless/malicious subclasses from faking state changes
- Usually via `final`; a more flexible alternative exists (see below)
### 3. Make all fields `final`
- Expresses intent, enforced by the system
- 📌 Required for safe publication across threads without synchronization
### 4. Make all fields `private`
- Blocks clients from accessing/mutating referenced objects
- ⚠️ Public final fields technically allowed but discouraged — locks in representation
### 5. Exclusive access to mutable components
- Never store a client-provided reference; never return one from an accessor
- 🔑 Make **defensive copies** in constructors, accessors, and `readObject`

## Example — `Complex`
- Provides accessors but **no mutators**
- Arithmetic ops return a *new* instance, never modify `this`
- 🔑 **Functional approach** — return result of a function on the operand
  - ```java
    public Complex plus(Complex c) {
      return new Complex(re + c.re, im + c.im);
    }
    ```
- Contrast: **procedural / imperative** — mutate operand state
- 💡 Method names are **prepositions** (`plus`) not verbs (`add`)
  - Emphasizes values don't change
  - ⚠️ `BigInteger`/`BigDecimal` broke this → many usage errors

## Advantages of Immutability
### Objects are simple
- Exactly **one state** — the state at creation
- Constructor-established invariants hold *forever*, with no extra effort
- ❌ Mutable objects have arbitrarily complex state spaces
### Inherently thread-safe
- 💡 Require **no synchronization**; can't be corrupted by concurrent access
- Easiest possible way to achieve thread safety
- Can be **shared freely** → encourage instance reuse
  - `public static final` constants for common values
    - ```java
      public static final Complex ZERO = new Complex(0, 0);
      public static final Complex ONE  = new Complex(1, 0);
      public static final Complex I    = new Complex(0, 1);
      ```
  - **Static factories** that cache frequent instances
    - ✅ Used by all boxed primitives and `BigInteger`
    - Reduces memory footprint and GC cost
    - 📌 Lets you add caching later without changing clients
### Never need defensive copies
- Copies stay forever equivalent to originals
- ❌ Don't provide `clone` or a copy constructor
- `String`'s copy constructor exists by mistake — rarely use it
### Can share internals
- `BigInteger`: sign (`int`) + magnitude (`int[]`)
- `negate` returns a new instance pointing to the *same* array
### Great building blocks
- Easier to maintain invariants when components can't change
- 📌 Ideal **map keys** and **set elements** — values can't shift
### Failure atomicity for free
- State never changes → no temporary inconsistency

## Disadvantages
### Separate object per distinct value
- ⚠️ Can be costly, especially for large objects
- `BigInteger.flipBit(0)` copies a million-bit instance — time & space proportional to size
- Contrast `java.util.BitSet.flip(0)` — mutable, **constant time**
### Multistep-operation cost
- New object discarded at every step magnifies the problem
- **Approach 1 — package-private mutable companion**
  - Predict common multistep ops, provide as primitives
  - `BigInteger` uses one internally to speed up modular exponentiation
  - 💡 Hard to use, but implementors did the work for you
- **Approach 2 — public mutable companion**
  - Use when client operations can't be predicted
  - `String` → `StringBuilder` (and obsolete `StringBuffer`)

## Design Alternatives
### Factories instead of `final` class
- Make all constructors `private`/package-private; add public static factories
  - ```java
    private Complex(double re, double im) { ... }
    public static Complex valueOf(double re, double im) {
      return new Complex(re, im);
    }
    ```
- ✅ Most flexible — allows multiple package-private implementation classes
- Effectively `final` to outside clients (can't extend without accessible constructor)
- 📌 Enables performance tuning via object caching in later releases
### Defend against untrusted subclasses
- ⚠️ `BigInteger`/`BigDecimal` aren't effectively final — methods may be overridden
- If security depends on immutability, verify the real class:
  - ```java
    public static BigInteger safeInstance(BigInteger val) {
      return val.getClass() == BigInteger.class ?
        val : new BigInteger(val.toByteArray());
    }
    ```

## Relaxing the Rules
- 🔑 True rule: **no method may produce an externally visible state change**
- Slightly weaker than "all fields final" — improves performance
- Nonfinal fields may **cache** results of expensive computations
  - Works *because* the object is immutable — recomputation yields the same result
  - Example of **lazy initialization** (Item 83)
  - Used by `PhoneNumber.hashCode` and `String`

## Serializability Caveat
- ⚠️ If `Serializable` with fields referring to mutable objects:
  - Provide explicit `readObject` or `readResolve`, **or**
  - Use `writeUnshared` / `readUnshared`
- Otherwise an attacker could create a mutable instance (see Item 88)

## Key Takeaways
- 📌 **Resist the urge to write a setter for every getter**
- Classes should be **immutable unless** there's a very good reason not to be
- ✅ Always make small value objects immutable — `PhoneNumber`, `Complex`
  - ⚠️ `java.util.Date` and `java.awt.Point` should have been immutable but aren't
- Seriously consider immutability for larger value objects — `String`, `BigInteger`
- Provide a public mutable companion **only** once proven necessary for performance
- If immutability is impractical, **limit mutability as much as possible**
  - **Reducing states makes objects easier to reason about** and less error-prone
  - 🔑 Declare every field **`private final`** unless there's a good reason otherwise
- Constructors must create fully initialized objects with all invariants established
  - ❌ No separate public init method; ❌ no "reinitialize" method
- `CountDownLatch` — mutable but with an intentionally tiny state space; use once