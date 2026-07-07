---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 31: Use Bounded Wildcards to Increase API Flexibility

## The Problem: Invariance of Parameterized Types
- 🔑 **Invariant**: `List<Type1>` is neither subtype nor supertype of `List<Type2>`
- `List<String>` is *not* a subtype of `List<Object>`
  - Can put any object into `List<Object>`, only strings into `List<String>`
  - `List<String>` can't do everything `List<Object>` can → not a subtype
  - Follows the **Liskov substitution principle** (Item 10)
- 💡 Sometimes you need more flexibility than invariant typing provides

## Motivating Example: `Stack<E>` (Item 29)

### `pushAll` — Producer Case
  #### Deficient version (no wildcard)
  - `public void pushAll(Iterable<E> src)`
  - Works only if element type *exactly* matches stack's type
  - ❌ `Stack<Number>.pushAll(Iterable<Integer>)` fails to compile
    - Error: `Iterable<Integer>` cannot be converted to `Iterable<Number>`
    - Yet logically it should work — `Integer` is a subtype of `Number`
  #### Fixed with bounded wildcard
  - `public void pushAll(Iterable<? extends E> src)`
  - 🔑 Means "Iterable of *some subtype* of E"
  - ⚠️ Keyword `extends` slightly misleading: every type is a subtype of itself
  - ✅ Both `Stack` and client code compile cleanly → typesafe

### `popAll` — Consumer Case
  #### Deficient version (no wildcard)
  - `public void popAll(Collection<E> dst)`
  - Works only on exact type match
  - ❌ `Stack<Number>.popAll(Collection<Object>)` fails to compile
    - `Collection<Object>` is not a subtype of `Collection<Number>`
    - Yet storing a popped `Number` into an `Object` variable is fine
  #### Fixed with bounded wildcard
  - `public void popAll(Collection<? super E> dst)`
  - 🔑 Means "collection of *some supertype* of E" (E is a supertype of itself [JLS, 4.10])
  - ✅ Both `Stack` and client code compile cleanly

## The PECS Principle
- 📌 **PECS**: **p**roducer-**extends**, **c**onsumer-**super**
- T producer → `<? extends T>`
- T consumer → `<? super T>`
- Applied to Stack:
  - `pushAll`'s `src` *produces* E instances → `Iterable<? extends E>`
  - `popAll`'s `dst` *consumes* E instances → `Collection<? super E>`
- 💡 Use wildcards on **input parameters** that represent producers or consumers
- ⚠️ Parameter that is *both* producer and consumer → wildcards do no good; exact type needed
- Also called the **Get and Put Principle** by Naftalin & Wadler [Naftalin07, 2.4]

## Applying PECS to Earlier Declarations

### `Chooser` constructor (Item 28)
- Original: `public Chooser(Collection<T> choices)`
- `choices` only *produces* T values → `public Chooser(Collection<? extends T> choices)`
- ✅ Practical gain: pass `List<Integer>` to a `Chooser<Number>` constructor

### `union` method (Item 30)
- Original: `public static <E> Set<E> union(Set<E> s1, Set<E> s2)`
- Both `s1` and `s2` are E producers → `Set<? extends E>` for both
- ✅ Enables: `Set<Number> numbers = union(Set<Integer>, Set<Double>)`
- ⚠️ **Do not use bounded wildcards as return types**
  - Would force clients to use wildcard types in their code
  - 💡 If users must think about wildcards, the API is probably wrong
- Pre-Java 8 caveat:
  - Type inference couldn't use target type to infer E → convoluted error
  - Fix: **explicit type argument** [JLS, 15.12]
  - `Set<Number> numbers = Union.<Number>union(integers, doubles);`

### `max` method (Item 30)
- Original: `public static <T extends Comparable<T>> T max(List<T> list)`
- Revised: `public static <T extends Comparable<? super T>> T max(List<? extends T> list)`
- PECS applied **twice**:
  - `list` produces T instances → `List<? extends T>`
  - `Comparable<T>` *consumes* T instances (produces order integers) → `Comparable<? super T>`
- 📌 **Comparables are always consumers**: prefer `Comparable<? super T>` over `Comparable<T>`
- 📌 Same for comparators: prefer `Comparator<? super T>` over `Comparator<T>`
- Why the complexity pays off:
  - `List<ScheduledFuture<?>>` rejected by original, permitted by revised
  - `ScheduledFuture` doesn't implement `Comparable<ScheduledFuture>`
  - It extends `Delayed`, which extends `Comparable<Delayed>`
  - 💡 Wildcard needed for types that don't implement `Comparable` directly but extend one that does

## Type Parameters vs. Wildcards — Duality

### The rule for public APIs
- Many methods can be declared either way:
  - `public static <E> void swap(List<E> list, int i, int j)`
  - `public static void swap(List<?> list, int i, int j)`
- ✅ Second is better in a public API — simpler, no type parameter to worry about
- 📌 **If a type parameter appears only once in a declaration, replace it with a wildcard**
  - Unbounded type parameter → unbounded wildcard
  - Bounded type parameter → bounded wildcard

### The wildcard capture problem
- Straightforward implementation won't compile:
  - `list.set(i, list.set(j, list.get(i)));`
  - Error: `Object cannot be converted to CAP#1`
- ⚠️ Can't put any value except `null` into a `List<?>`
- Fix: **private generic helper method to capture the wildcard**
  - `private static <E> void swapHelper(List<E> list, int i, int j)`
  - Helper knows list is `List<E>` → safe to get out and put back E values
  - ✅ No unsafe cast or raw type needed
  - 💡 Exports the simple wildcard declaration; complex generic method stays internal
  - Helper's signature is exactly the one dismissed as too complex for the public method

## Key Takeaways
- Wildcard types in APIs are tricky but make them far more flexible
- 📌 For widely used libraries, proper wildcard use is **mandatory**
- 📌 Basic rule: **producer-extends, consumer-super (PECS)**
- 📌 All **comparables and comparators are consumers** → use `<? super T>`
- Never use bounded wildcards as return types
- Type parameter appearing once → replace with a wildcard (use a private helper for capture if needed)