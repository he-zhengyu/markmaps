---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 32: Combine Generics and Varargs Judiciously

## The Core Problem: A Leaky Abstraction
### Why Varargs and Generics Clash
- Both added in **Java 5**, yet interact poorly
- Varargs purpose: pass a variable number of arguments
- ⚠️ **Leaky abstraction**: invoking a varargs method creates an **array**, which should be hidden but is visible
- Result: confusing compiler warnings with generic/parameterized varargs

### Non-Reifiable Types & Warnings
- 🔑 **Non-reifiable type**: runtime representation has *less* information than compile-time (Item 28)
- Nearly all generic and parameterized types are non-reifiable
- Compiler warns on **declaration** if varargs parameter is non-reifiable
- Compiler warns on **invocation** if inferred varargs type is non-reifiable
- Warning form: `[unchecked] Possible heap pollution from parameterized vararg type List<String>`

### Heap Pollution
- 🔑 Occurs when a variable of parameterized type refers to an object **not of that type** [JLS, 4.12.2]
- Can cause compiler-generated casts to fail
- ⚠️ Violates the fundamental guarantee of the generic type system

## How Type Safety Breaks
### The `dangerous` Method
- ```java
  static void dangerous(List<String>... stringLists) {
      List<Integer> intList = List.of(42);
      Object[] objects = stringLists;
      objects[0] = intList;             // Heap pollution
      String s = stringLists[0].get(0); // ClassCastException
  }
  ```
- No visible casts, yet throws `ClassCastException`
- Failure caused by an **invisible compiler-generated cast**
- 📌 It is **unsafe to store** a value in a generic varargs array parameter

### Why Is This Even Legal?
- Explicit generic array creation is an **error**; generic varargs declaration is only a **warning**
- Reason: such methods are **very useful in practice**, so designers accepted the inconsistency
- Typesafe library examples:
  - `Arrays.asList(T... a)`
  - `Collections.addAll(Collection<? super T> c, T... elements)`
  - `EnumSet.of(E first, E... rest)`

### Leaking the Array Also Breaks Safety
#### The `toArray` Trap
- ```java
  // UNSAFE - exposes its generic parameter array!
  static <T> T[] toArray(T... args) { return args; }
  ```
- ⚠️ Unsafe even though it **never stores** into the array
- Array's type set by compile-time argument types — compiler may lack info to determine it accurately
- Returning the array **propagates heap pollution up the call stack**

#### The `pickTwo` Chain Failure
- `pickTwo(T a, T b, T c)` returns `toArray(...)` of two random arguments
- Compiler allocates `Object[]` for the varargs array — most specific type guaranteed to hold any arguments
- So `pickTwo` **always returns `Object[]`**
- Client: `String[] attributes = pickTwo("Good", "Fast", "Cheap");`
- Compiles cleanly, but throws `ClassCastException` at runtime
- Hidden cast to `String[]` fails: `Object[]` is not a subtype of `String[]`
- 💡 Disconcerting: failure is **two levels removed** from the polluting method, with no array modification at all

#### Two Safe Exceptions for Passing the Array
- ✅ Pass to another varargs method correctly annotated with `@SafeVarargs`
- ✅ Pass to a non-varargs method that merely **computes a function of the contents**

## The @SafeVarargs Annotation
### Purpose and History
- Before Java 7: authors couldn't silence call-site warnings
  - Users tolerated warnings or added `@SuppressWarnings("unchecked")` at **every call site** (Item 27)
  - ❌ Tedious, harmed readability, hid warnings flagging real issues
- **Java 7**: `@SafeVarargs` lets the author suppress client warnings automatically
- 🔑 Constitutes the author's **promise that the method is typesafe**; compiler stops warning in exchange

### When a Generic Varargs Method Is Safe
- ⚠️ Never annotate with `@SafeVarargs` unless the method actually **is** safe
- Safe if the array is used **only to transmit arguments** from caller to method
- The two conditions — if either is violated, fix it:
  - ✅ Doesn't **store** anything in the varargs parameter array
  - ✅ Doesn't make the array (or a clone) **visible to untrusted code**

### Safe Example: `flatten`
- ```java
  @SafeVarargs
  static <T> List<T> flatten(List<? extends T>... lists) {
      List<T> result = new ArrayList<>();
      for (List<? extends T> list : lists)
          result.addAll(list);
      return result;
  }
  ```
- No warnings on declaration or at call sites

### The Rule
- 📌 Use `@SafeVarargs` on **every** method with a generic/parameterized varargs parameter
- Implies: never write unsafe methods like `dangerous` or `toArray`
- Whenever the compiler warns of heap pollution in your method, verify safety

### Where the Annotation Is Legal
- Only on methods that **can't be overridden** — overriding methods can't be guaranteed safe
- Java 8: static methods and final instance methods
- Java 9: also **private instance methods**

## Alternative: Replace Varargs with List
### The List-Parameter Version of `flatten`
- Varargs is *an array in disguise* — replace it with a `List` parameter (Item 28)
- ```java
  static <T> List<T> flatten(List<List<? extends T>> lists) { ... }
  ```
- Only the parameter declaration changes
- Client uses `List.of` for variable arity: `flatten(List.of(friends, romans, countrymen))`
- Relies on `List.of` itself being `@SafeVarargs`-annotated

### Trade-offs
- ✅ Compiler **proves** type safety — no author vouching, no risk of misjudging safety
- ❌ Client code slightly more verbose
- ❌ May be a bit slower

### Rescuing the Impossible Cases
- Works even where a safe varargs method **cannot** be written (e.g., `toArray`)
- `List` analogue of `toArray` is `List.of` — already provided by the Java libraries
- `pickTwo` rewritten to return `List<T>` via `List.of(a, b)` etc.
- Client: `List<String> attributes = pickTwo("Good", "Fast", "Cheap");`
- ✅ Typesafe because it uses **only generics, no arrays**

## Key Takeaways
- Varargs is a leaky abstraction over arrays; arrays and generics have **different type rules**, so they mix badly
- Generic varargs parameters are **legal but not typesafe**
- A generic varargs method is safe only if it neither stores into nor exposes its parameter array
- If you write one: **ensure it's typesafe, then annotate with `@SafeVarargs`** so it's pleasant to use
- 💡 Or sidestep arrays entirely: replace the varargs parameter with a `List` and let the compiler prove safety