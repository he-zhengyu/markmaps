---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 33: Consider Typesafe Heterogeneous Containers

## Motivation

### Normal Generic Usage
- Container itself is parameterized: `Set<E>`, `Map<K,V>`
- Single-element containers: `ThreadLocal<T>`, `AtomicReference<T>`
- Limits to a **fixed number of type parameters** per container
- Usually exactly what you want (Set → 1 param, Map → 2 params)

### When More Flexibility Is Needed
- E.g. a **database row** has arbitrarily many columns
- Goal: access all of them in a *typesafe* manner

### Core Idea
- 💡 **Parameterize the key, not the container**
- Present the parameterized key to insert/retrieve values
- Generic type system guarantees value type agrees with its key

## Type Tokens

### Class as Generic Key
- Class `Class` is generic: class literal type is `Class<T>`, not raw `Class`
- `String.class` → `Class<String>`; `Integer.class` → `Class<Integer>`
- 🔑 **Type token**: class literal passed among methods to convey both compile-time and runtime type info [Bracha04]

## The Favorites Class

### API
- Looks like a simple map, but the **key is parameterized**, not the map
- `public <T> void putFavorite(Class<T> type, T instance)`
- `public <T> T getFavorite(Class<T> type)`
- Client presents a `Class` object when setting and getting

### Client Example
- Store `String.class → "Java"`, `Integer.class → 0xcafebabe`, `Class.class → Favorites.class`
- Prints `Java cafebabe Favorites`
- 📌 Java's `printf` uses `%n` (platform line separator) where C uses `\n`

### Properties
- ✅ **Typesafe**: never returns an `Integer` when asked for a `String`
- ✅ **Heterogeneous**: unlike ordinary maps, all keys have different types
- Hence: *typesafe heterogeneous container*

### Implementation
    #### Backing Map
    - `private Map<Class<?>, Object> favorites = new HashMap<>()`
    - 💡 Wildcard is **nested**: the key type is a wildcard, not the map type
    - Every key can have a different parameterized type → source of heterogeneity
    - Value type is plain `Object`: map doesn't guarantee key–value type relationship
    - Java's type system can't express that invariant, but we know it holds

    #### putFavorite
    - Trivial: maps the `Class` object to the instance
    - Discards the "type linkage" between key and value
    - OK — `getFavorite` reestablishes the linkage

    #### getFavorite
    - Retrieves value: correct reference, but compile-time type `Object`
    - **Dynamically casts** to `T` via `Class.cast`
    - `cast` = dynamic analogue of Java's cast operator
    - Checks argument is an instance of the represented type; else throws `ClassCastException`
    - Won't throw here if client code compiled cleanly
    - `cast`'s return type is `Class`'s type parameter: `T cast(Object obj)`
    - ✅ Achieves type safety **without an unchecked cast** to `T`

## Two Limitations

### 1. Malicious Client Can Corrupt Type Safety
- ⚠️ Using a `Class` object in **raw form** bypasses safety
- But such client code generates an unchecked warning at compile time
- Same weakness as `HashSet`/`HashMap` — raw `HashSet` can put a `String` into `HashSet<Integer>` (Item 26)
- ✅ Fix: **runtime type safety** via dynamic cast in `putFavorite`: `favorites.put(type, type.cast(instance))`
- Analogous wrappers: `Collections.checkedSet`, `checkedList`, `checkedMap`, etc.
  - Generic static factories take `Class` object(s) plus a collection
  - Add **reification** to wrapped collections — e.g. throw `ClassCastException` if a `Coin` goes into `Collection<Stamp>`
  - Useful for tracking down wrongly typed inserts in apps mixing generic and raw types

### 2. Cannot Store Non-Reifiable Types (Item 28)
- ⚠️ Can store `String` or `String[]`, but **not** `List<String>`
- `List<String>.class` is a syntax error — no `Class` object exists for it
- `List<String>` and `List<Integer>` share the single object `List.class`
- Legal "type literals" returning the same reference would wreak havoc internally
- ❌ No entirely satisfactory workaround

## Bounded Type Tokens

### Concept
- Favorites' tokens are **unbounded**: any `Class` object accepted
- 🔑 **Bounded type token**: restricts representable types via a bounded type parameter (Item 30) or bounded wildcard (Item 31)

### Annotations API Example (Item 39)
- `AnnotatedElement` interface, implemented by reflective types (classes, methods, fields…)
- `<T extends Annotation> T getAnnotation(Class<T> annotationType)`
- Returns the element's annotation of that type, or `null`
- 💡 An annotated element is a typesafe heterogeneous container keyed by annotation types

### asSubclass for Safe Casting
- Problem: casting `Class<?>` to `Class<? extends Annotation>` is unchecked → compile-time warning (Item 27)
- `asSubclass` casts a `Class` object to a subclass of its argument's class, **safely and dynamically**
- Succeeds → returns the argument; fails → throws `ClassCastException`
- Enables reading an annotation whose type is unknown at compile time, with no error or warning
- Pattern: `Class.forName(name).asSubclass(Annotation.class)` passed to `getAnnotation`

## Key Takeaways
- Normal generics (collections APIs) fix the number of type parameters per container
- 💡 Escape the limit by putting the type parameter on the **key**, not the container
- Use `Class` objects as keys — a `Class` used this way is a **type token**
- Custom key types also work — e.g. `DatabaseRow` container with generic `Column<T>` keys
- ⚠️ Limits: raw-type abuse (mitigate with dynamic cast) and non-reifiable types (no full workaround)