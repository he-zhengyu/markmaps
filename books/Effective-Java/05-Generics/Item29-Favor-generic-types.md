---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 29: Favor Generic Types

## Motivation
- Using JDK generics is easy; **writing your own** is harder but worth learning
- Starting point: Object-based `Stack` from Item 7
- Non-generic version forces clients to **cast popped objects**
- ⚠️ Those casts **might fail at runtime**
- Generifying after the fact **doesn't harm existing clients**

## Generification Steps
### Step 1: Add Type Parameters
- Add one or more type parameters to class declaration
- Element type conventionally named **`E`** (Item 68)
- Declaration becomes `public class Stack<E>`

### Step 2: Replace Object with E
- Swap all uses of `Object` for the type parameter
- Compile and fix resulting errors/warnings
- ❌ First attempt fails: `elements = new E[DEFAULT_INITIAL_CAPACITY]`
- Error: **generic array creation**
- 🔑 Can't create arrays of **non-reifiable types** like `E` (Item 28)
- 📌 Arises whenever a generic type is **backed by an array**

## Two Solutions to Generic Array Creation
### Solution 1: Cast Object[] to E[]
- Create `Object[]`, cast to generic array type: `(E[]) new Object[...]`
- Compiler emits **unchecked cast warning** instead of error
- Legal but not (in general) typesafe — *you* must prove safety
- Safety proof for Stack
  - `elements` is **private**, never returned or passed out
  - Only `push(E)` stores elements → all are of type `E`
  - ✅ Unchecked cast can do no harm
- Suppress warning in **narrowest scope** (Item 27) — here, the whole constructor
- `@SuppressWarnings("unchecked")` on constructor → compiles cleanly, no client casts

### Solution 2: Keep Object[] Field
- Change field type from `E[]` to `Object[]`
- New error: `Object` found where `E` required in `pop`
- Fix by casting element read: `(E) elements[--size]` → unchecked warning
- Compiler can't check cast at runtime since `E` is non-reifiable
- Prove safety, then suppress on the **assignment only**, not entire `pop` method

### Comparing the Techniques
- ✅ First: more **readable** — array declared as `E[]`, clearly holds only `E`
- ✅ First: more **concise** — one cast at creation vs. cast on every read
- 📌 First is preferable and **more common in practice**
- ⚠️ First causes **heap pollution** (Item 32): runtime type `Object[]` ≠ compile-time `E[]`
- Heap pollution is **harmless here**, but queasy programmers pick the second

## Using the Generic Stack
- Demo: print command-line args reversed and uppercased
- `Stack<String> stack = new Stack<>()`
- No explicit cast to call `toUpperCase()` on popped elements
- ✅ Auto-generated cast **guaranteed to succeed**

## Arrays Inside Generic Types
- Seems to contradict Item 28 (prefer lists to arrays) — but doesn't
- Lists aren't native to Java: `ArrayList` must be built **atop arrays**
- `HashMap` uses arrays for **performance**

## Type Parameter Restrictions
### Unrestricted (the majority)
- Any object reference type works: `Stack<Object>`, `Stack<int[]>`, `Stack<List<String>>`
- ❌ No primitive types: `Stack<int>`, `Stack<double>` → compile-time error
- 🔑 Fundamental limitation of Java generics
- Workaround: **boxed primitives** (Item 61)

### Bounded Type Parameters
- Example: `class DelayQueue<E extends Delayed> implements BlockingQueue<E>`
- Requires actual type `E` to be a **subtype of `Delayed`**
- ✅ Enables `Delayed` methods on elements without casts or `ClassCastException` risk
- 📌 Every type is a subtype of itself [JLS, 4.10] → `DelayQueue<Delayed>` is legal

## Key Takeaways
- 💡 Generic types are **safer and easier to use** than types requiring client casts
- Design new types to be usable **without casts** — usually means making them generic
- **Generify existing types** that should be generic
- ✅ Helps new users **without breaking existing clients** (Item 26)