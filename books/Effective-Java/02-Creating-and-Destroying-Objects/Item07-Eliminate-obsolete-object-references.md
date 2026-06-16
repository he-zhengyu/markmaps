---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 7: Eliminate Obsolete Object References

## The Illusion of Automatic Memory Management
- Garbage-collected languages (**Java**) reclaim objects automatically
- 💡 Feels like *magic* coming from manual-memory languages (**C/C++**)
- ⚠️ Misleading impression: "no need to think about memory"
- 🔑 Truth: GC reduces—but does not eliminate—memory responsibility

## The Leaking `Stack` Example
### The Implementation
- Backing store: `Object[] elements`, tracked by `size`
- `push()` → `ensureCapacity()`, then `elements[size++] = e`
- `pop()` → returns `elements[--size]`
- `ensureCapacity()` roughly doubles array: `Arrays.copyOf(elements, 2 * size + 1)`
- Passes every test, yet harbors a hidden flaw
### The Hidden Memory Leak
- 🔑 **Memory leak** here = *unintentional object retention*
- When stack grows then shrinks, popped objects are **not** collected
- Cause: stack keeps **obsolete references** to them
- 🔑 **Obsolete reference**: one that will never be dereferenced again
- 📌 Everything outside the *active portion* (`index < size`) is obsolete
### Why It's So Insidious
- ⚠️ A retained reference also retains everything **it** references—transitively
- 💡 A few stray references can block *many* objects from collection
- 📊 Symptoms: ↑ GC activity, ↑ memory footprint
- Extreme cases: disk paging, even `OutOfMemoryError` (rare)

## The Fix: Null Out Obsolete References
- Corrected `pop()` sets `elements[size] = null` after reading the result
- ✅ Added benefit: accidental later use fails fast with `NullPointerException`
- 💡 Detect programming errors as quickly as possible

## Don't Overcompensate
- ❌ Nulling out *every* reference once finished with it
- ⚠️ Clutters the program; neither necessary nor desirable
- 📌 Nulling references should be the **exception, not the norm**
- ✅ Best practice: let the variable **fall out of scope**
- Achieved naturally by declaring each variable in the narrowest scope (*Item 57*)

## When Should You Null a Reference?
- 🔑 Rule: be alert whenever a class **manages its own memory**
- Why `Stack` is vulnerable: it owns its storage pool (the array cells)
- GC sees all references in `elements` as equally valid
- Only the programmer knows the inactive portion is unimportant
- 📌 Whenever an element is freed, null out the references it held

## Other Common Sources of Leaks
### Caches
- ⚠️ Easy to forget an entry and leave it long after it's irrelevant
- ✅ Key-tied lifetime → use `WeakHashMap` (entries auto-removed)
  - 📌 Works only when lifetime depends on external refs to the *key*, not the value
- Ill-defined lifetime → periodically purge stale entries
  - Background thread (e.g. `ScheduledThreadPoolExecutor`)
  - As a side effect of insertion via `LinkedHashMap.removeEldestEntry`
- Sophisticated needs → use `java.lang.ref` directly
### Listeners & Callbacks
- ⚠️ Clients register but never deregister → callbacks accumulate
- ✅ Store only **weak references**, e.g. as keys in a `WeakHashMap`

## Detection
- ⚠️ Leaks rarely surface as obvious failures—may linger for **years**
- Found via careful **code inspection**
- Or with a **heap profiler** debugging tool
- 💡 Best of all: anticipate and prevent them before they occur

## Key Takeaways
- 🔑 Garbage collection does **not** free you from thinking about retention
- 📌 Null out a reference once it becomes obsolete—but only when warranted
- 💡 Prefer scoping variables narrowly over manual nulling
- ⚠️ Classes that **manage their own memory** are prime leak suspects
- 📌 Watch caches, listeners, and callbacks; reach for `WeakHashMap` when fitting
- ✅ Anticipate leaks early—they hide silently until inspection or profiling reveals them