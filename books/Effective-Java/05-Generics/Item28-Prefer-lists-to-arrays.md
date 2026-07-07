---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 28: Prefer Lists to Arrays

## Two Fundamental Differences: Arrays vs Generics

### Difference 1: Covariant vs Invariant
- 🔑 **Covariant**: if `Sub` subtypes `Super`, then `Sub[]` subtypes `Super[]`
- 🔑 **Invariant**: `List<Type1>` is neither subtype nor supertype of `List<Type2>`
- 💡 Arguably *arrays* are the deficient ones, not generics
- ❌ Array version compiles, **fails at runtime**
  - `Object[] objectArray = new Long[1];`
  - `objectArray[0] = "I don't fit in";` → `ArrayStoreException`
- ✅ List version **fails at compile time**
  - `List<Object> ol = new ArrayList<Long>();` → incompatible types
- 📌 Either way a String can't go in a Long container — but compile-time detection is preferable

### Difference 2: Reified vs Erased
- 🔑 **Reified**: arrays know and enforce element type at *runtime*
  - Putting `String` into `Long[]` → `ArrayStoreException`
- 🔑 **Erasure**: generics enforce types only at *compile time*, discard element type at runtime
- 💡 Erasure enabled smooth interop with pre-generics legacy code (Java 5 transition, Item 26)

## Consequence: Arrays and Generics Don't Mix

### Generic Array Creation Is Illegal
- Illegal forms: `new List<E>[]`, `new List<String>[]`, `new E[]`
- All produce *generic array creation* errors at compile time
- Reason: it isn't **typesafe** — compiler-generated casts could fail with `ClassCastException`, violating the generic type system's fundamental guarantee

### Proof: Why It Must Be Illegal
- Pretend `List<String>[] stringLists = new List<String>[1];` were legal (1)
- `List<Integer> intList = List.of(42);` (2)
- `Object[] objects = stringLists;` — legal, arrays are **covariant** (3)
- `objects[0] = intList;` — succeeds due to **erasure**: runtime types are just `List` / `List[]`, no `ArrayStoreException` (4)
- `String s = stringLists[0].get(0);` — auto-cast to `String` hits an `Integer` → `ClassCastException` (5)
- 📌 To prevent this, line 1 must be a compile-time error

### Non-Reifiable Types
- 🔑 **Non-reifiable type**: runtime representation holds *less* information than compile-time representation
- Examples: `E`, `List<E>`, `List<String>`
- Only reifiable parameterized types: **unbounded wildcards** like `List<?>`, `Map<?,?>` (Item 26)
- Arrays of unbounded wildcard types are legal, though rarely useful

### Practical Annoyances
- Generic collections generally can't return arrays of their element type (partial fix: Item 33)
- ⚠️ Confusing warnings with **varargs** + generics (Item 53)
  - Each varargs call creates an array; non-reifiable element type → warning
  - Fix: `SafeVarargs` annotation (Item 32)

## Case Study: The Chooser Class

### Version 1: No Generics
- `private final Object[] choiceArray;` filled via `choices.toArray()`
- `choose()` returns random element as `Object`
- ❌ Client must cast return value on every call; wrong cast fails at runtime

### Version 2: Generic with `T[]` — Won't Compile
- `choiceArray = choices.toArray();` → error: `Object[]` cannot be converted to `T[]`

### Version 3: Unchecked Cast
- `choiceArray = (T[]) choices.toArray();`
- ⚠️ Error becomes *unchecked cast* warning — compiler can't vouch for runtime safety since `T` is erased
- Program works, but compiler can't prove it
- 💡 Better to eliminate the warning's cause than suppress it (Item 27)

### Version 4: List-Based — Typesafe ✅
- `private final List<T> choiceList = new ArrayList<>(choices);`
- `choose()` uses `choiceList.get(rnd.nextInt(choiceList.size()))`
- Trade-off: slightly more verbose, perhaps slightly slower
- ✅ Guaranteed no `ClassCastException` at runtime

## Key Takeaways
- 📌 Arrays are **covariant and reified**; generics are **invariant and erased**
- Arrays give runtime type safety but not compile-time safety; generics the reverse
- As a rule, arrays and generics don't mix well
- 💡 On compile-time errors/warnings from mixing them, first impulse: **replace arrays with lists**
- Sacrifice a little conciseness/performance for **type safety and interoperability**