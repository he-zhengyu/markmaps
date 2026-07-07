---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 30: Favor Generic Methods

## Why Generic Methods
- Methods can be generic, just like classes
- 📌 Static utility methods on parameterized types are usually generic
- Example: all "algorithm" methods in `Collections` (`binarySearch`, `sort`)
- Writing generic methods ≈ writing generic types

## Motivating Example: `union` of Two Sets
### Deficient Raw-Type Version
- ❌ `public static Set union(Set s1, Set s2)` — uses raw types (Item 26)
- Compiles but emits **two unchecked warnings**
  - `unchecked call to HashSet(Collection<? extends E>)`
  - `unchecked call to addAll(Collection<? extends E>)`
### Typesafe Generic Version
- Fix: declare a **type parameter** `<E>` for element type of all three sets
- 🔑 **Type parameter list** goes between method's modifiers and return type
- `public static <E> Set<E> union(Set<E> s1, Set<E> s2)`
- Naming conventions same as generic types (Items 29, 68)
- ✅ Compiles with no warnings; typesafe and easy to use
- Client code needs **no casts**, no errors or warnings
- Output order implementation-dependent: `[Moe, Tom, Harry, Larry, Curly, Dick]`
### Limitation
- ⚠️ All three sets (params + return) must have exactly the same type
- 💡 More flexible with **bounded wildcard types** (Item 31)

## Generic Singleton Factory Pattern
### Motivation
- Need: an **immutable object** applicable to many types
- Generics implemented by **erasure** (Item 28) → single object works for all parameterizations
- 🔑 **Generic singleton factory**: static factory doles out the object per requested type
- Used for function objects (Item 42): `Collections.reverseOrder`
- Occasionally for collections: `Collections.emptySet`
### Example: Identity Function Dispenser
- Libraries already provide `Function.identity` — don't write your own (Item 59); shown for instruction
- Wasteful to create a new identity object per request — it's **stateless**
- If generics were reified → one identity function per type; erasure → one singleton suffices
- `private static UnaryOperator<Object> IDENTITY_FN = (t) -> t;`
- Factory casts to `UnaryOperator<T>` → generates unchecked cast warning
- 💡 Identity function returns argument unmodified → typesafe for any `T`
- ✅ Confidently suppress with `@SuppressWarnings("unchecked")` → compiles cleanly
- Same singleton usable as `UnaryOperator<String>` and `UnaryOperator<Number>` without casts

## Recursive Type Bounds
### Concept
- 🔑 Type parameter bounded by an expression involving **itself**
- Permissible, though relatively rare
- Most common use: with `Comparable` interface (Item 14)
### `Comparable<T>` Interface
- `public interface Comparable<T> { int compareTo(T o); }`
- `T` = type to which elements can be compared
- In practice, types compare only to their own type
  - `String implements Comparable<String>`
  - `Integer implements Comparable<Integer>`
### Expressing Mutual Comparability
- Many methods sort, search, or compute min/max on `Comparable` collections
- Requires elements be **mutually comparable**
- `public static <E extends Comparable<E>> E max(Collection<E> c)`
- 💡 Read as: "any type `E` that can be compared to itself"
### `max` Implementation Notes
- Computes maximum by elements' **natural order**; compiles warning-free
- Throws `IllegalArgumentException` on empty collection
- ✅ Better alternative: return `Optional<E>` (Item 55)
### Complexity in Practice
- Recursive bounds can get much more complex, but rarely do
- Master three idioms to handle most cases
  - This idiom (`E extends Comparable<E>`)
  - Wildcard variant (Item 31)
  - Simulated self-type idiom (Item 2)

## Key Takeaways
- 📌 Generic methods are **safer and easier to use** than methods requiring client-side casts
- Ensure methods can be used **without casts** — often means making them generic
- **Generify existing methods** whose use requires casts
- 💡 Generifying helps new users **without breaking existing clients** (Item 26)