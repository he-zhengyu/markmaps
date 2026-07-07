---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 26: Don't Use Raw Types

## Terminology

### Generic Types
- 🔑 **Generic class/interface**: declaration with one or more **type parameters** [JLS, 8.1.2, 9.1.2]
- Example: `List<E>` — `E` is the element type; called `List` for short
- Generic classes + interfaces = **generic types**

### Parameterized Types
- 🔑 Class/interface name + angle-bracketed **actual type parameters** [JLS, 4.4, 4.5]
- Example: `List<String>` — "list of string"
- `String` is the *actual* type parameter for formal parameter `E`

### Raw Types
- 🔑 Generic type name used **without type parameters** [JLS, 4.8]
- Example: raw type of `List<E>` is `List`
- Behaves as if all generic type info were **erased**
- Exists primarily for **compatibility with pre-generics code**

## The Danger of Raw Types

### The Stamp Collection Example
- Raw declaration: `private final Collection stamps` ❌
- Comment "Contains only Stamp instances" — compiler can't read comments
- Erroneous `stamps.add(new Coin(...))` **compiles** with only a vague "unchecked call" warning
- Error surfaces only at retrieval: `(Stamp) i.next()` throws `ClassCastException`

### Why Late Errors Hurt
- 💡 Errors should be caught **as soon as possible, ideally at compile time**
- Runtime failure occurs long after, in code **distant** from the actual bug
- Must search the codebase for the offending insertion — compiler can't help

### The Generic Fix
- ✅ `private final Collection<Stamp> stamps` — typesafe
- Declaration carries the type info, not the comment
- Erroneous insertion → **compile-time error**: `Coin cannot be converted to Stamp`
- Compiler inserts **invisible casts** on retrieval, guaranteed not to fail
- ⚠️ Guarantee holds only if code compiles without emitting or suppressing warnings (Item 27)
- Realistic scenario: `BigInteger` slipped into a `BigDecimal` collection

## Why Raw Types Still Exist
- Never use them — you lose all **safety and expressiveness** benefits of generics
- Kept for **compatibility**: generics arrived near Java's second decade
- Enormous pre-generics codebase had to remain legal and interoperate
- 🔑 **Migration compatibility** drove raw-type support and **erasure**-based generics (Item 28)

## Raw Type `List` vs `List<Object>`

### Semantic Difference
- `List` has **opted out** of the generic type system
- `List<Object>` explicitly tells the compiler it can hold objects of **any type**

### Subtyping Rules
- `List<String>` **is** a subtype of raw `List`
- `List<String>` is **not** a subtype of `List<Object>` (Item 28)
- 💡 You lose type safety with raw `List`, but not with `List<Object>`

### The `unsafeAdd` Demonstration
- `unsafeAdd(List list, Object o)` with raw type: compiles with **unchecked warning**
- Runtime: `strings.get(0)` casts `Integer` to `String` → `ClassCastException`
- ⚠️ Compiler-generated cast is normally safe — ignored warning = paid the price
- Changing parameter to `List<Object>` → compile error: `List<String> cannot be converted to List<Object>` ✅

## Unbounded Wildcard Types `<?>`

### When Element Type Is Unknown
- Temptation: raw types for methods where element type "doesn't matter" ❌
- Example: `numElementsInCommon(Set s1, Set s2)` — works but dangerous

### The Safe Alternative
- ✅ `Set<?>` — "set of some type" — the most general parameterized `Set` type
- `numElementsInCommon(Set<?> s1, Set<?> s2)` — typesafe and flexible

### Wildcard vs Raw: What `?` Buys You
- 📌 Wildcard is **safe**; raw type is **not**
- Raw type: any element can be inserted, corrupting the **type invariant**
- `Collection<?>`: cannot insert any element except `null` — compile-time error
- Error mentions fresh capture variable `CAP#1` — cryptic but the compiler did its job
- Cannot assume anything about the type of retrieved objects
- If too restrictive → use **generic methods** (Item 30) or **bounded wildcards** (Item 31)

## Exceptions: Legitimate Raw Type Uses

### Class Literals
- Must use raw types: parameterized types not permitted [JLS, 15.8.2]
- ✅ Legal: `List.class`, `String[].class`, `int.class`
- ❌ Illegal: `List<String>.class`, `List<?>.class`

### `instanceof` Operator
- Generic type info is **erased at runtime**
- `instanceof` illegal on parameterized types except unbounded wildcards
- Wildcards add no behavior here — angle brackets are just noise
- Preferred idiom: `if (o instanceof Set)` then cast to `Set<?>`
- 📌 Cast to wildcard `Set<?>`, not raw `Set` — a **checked cast**, no warning

## Key Takeaways
- Raw types cause runtime exceptions — **don't use them**
- They exist only for **legacy compatibility** with pre-generics code
- `Set<Object>`: parameterized, holds any type — ✅ safe
- `Set<?>`: wildcard, holds some unknown type — ✅ safe
- `Set`: raw, opts out of generics — ❌ unsafe
- Only exceptions: **class literals** and **`instanceof`**