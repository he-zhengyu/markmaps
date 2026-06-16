---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 8: Avoid Finalizers and Cleaners

## Core Thesis
- 📌 **Finalizers**: unpredictable, dangerous, generally unnecessary
- ⚠️ Cause erratic behavior, poor performance, portability problems
- As of **Java 9**, finalizers are *deprecated* (still used by Java libraries)
- 🔑 **Cleaners** = Java 9 replacement for finalizers
  - Less dangerous than finalizers
  - ❌ Still unpredictable, slow, generally unnecessary
- ✅ **Rule of thumb**: avoid both

## Not C++ Destructors
- 💡 Don't think of them as Java's analogue to **C++ destructors**
- C++: destructors are the normal way to reclaim object resources (counterpart to constructors)
- Java: the **garbage collector** reclaims storage when an object becomes unreachable — no programmer effort needed
- For nonmemory resources, Java uses `try-with-resources` or `try-finally` (Item 9)

## Problems with Finalizers & Cleaners
### No Guarantee of Prompt Execution
- ⚠️ No guarantee they run promptly [JLS, 12.6]
- Arbitrarily long delay between unreachability and execution
- 📌 Never do anything **time-critical** in a finalizer or cleaner
- ❌ Grave error to rely on them to **close files** — file descriptors are limited; program may fail when it can't open more files
- Promptness depends on the **GC algorithm**, which varies widely across implementations
  - 💡 May run perfectly on your test JVM, fail on a customer's JVM
- 📊 **Real case**: GUI app died with `OutOfMemoryError` — thousands of graphics objects stuck on the finalizer queue
  - Finalizer thread ran at lower priority than another thread
  - Spec makes no guarantee which thread runs finalizers
- Cleaners are slightly better — authors control their own cleaner threads — but still no guarantee of prompt cleaning

### No Guarantee They Run At All
- ⚠️ Program may terminate without running them on unreachable objects
- ❌ Never depend on them to update **persistent state**
- 💡 e.g. releasing a persistent DB lock via a finalizer can halt a distributed system

### Don't Trust System.gc / runFinalization
- `System.gc` and `System.runFinalization` may increase odds, but **don't guarantee** execution
- ❌ `System.runFinalizersOnExit` and `Runtime.runFinalizersOnExit` — fatally flawed, deprecated for decades [ThreadStop]

### Uncaught Exceptions Are Ignored
- ⚠️ An uncaught exception during finalization is **ignored**; finalization of that object terminates [JLS, 12.6]
- Can leave other objects in a **corrupt state** → arbitrary nondeterministic behavior
- ❌ No stack trace, not even a warning printed
- ✅ Cleaners avoid this — the library controls the cleaner thread

### Severe Performance Penalty
- 📊 Create + `try-with-resources` close + GC reclaim ≈ **12 ns**
- 📊 With a finalizer ≈ **550 ns** → ~**50× slower**
- Primarily because finalizers **inhibit efficient GC**
- 📊 Cleaners cleaning *all* instances ≈ **500 ns** (comparable to finalizers)
- 📊 Cleaner as a **safety net** only ≈ **66 ns** → ~**5× cost** for unused insurance

### Finalizer Attacks (Security)
- 🔑 **Finalizer attack**: malicious subclass's finalizer runs on a partially constructed object
- Trigger: exception thrown from a constructor or from `readObject` / `readResolve` (Chapter 12)
- ⚠️ Finalizer records a reference in a static field → object escapes GC
- Then attacker invokes arbitrary methods on an object that should never have existed
- 💡 Throwing from a constructor *should* prevent existence — but finalizers defeat this
- ✅ **Defenses**
  - `final` classes are immune (no malicious subclass possible)
  - For nonfinal classes: write a `final finalize` method that does nothing

## What to Do Instead
- ✅ Implement **`AutoCloseable`**
- ✅ Require clients to call `close`, typically via `try-with-resources` (Item 9)
- 📌 Track closed state
  - `close` records in a field that the object is invalid
  - Other methods check the field, throw `IllegalStateException` if used after close

## Legitimate Uses
### Safety Net
- Backup if a resource owner neglects to call `close`
- 💡 Better to free a resource *late than never*
- ⚠️ Weigh whether the protection is worth the cost
- Library examples: `FileInputStream`, `FileOutputStream`, `ThreadPoolExecutor`, `java.sql.Connection`

### Objects with Native Peers
- 🔑 **Native peer**: a non-Java object a Java object delegates to via native methods
- GC doesn't know about it and can't reclaim it
- ✅ Cleaner/finalizer OK *if* performance is acceptable **and** the peer holds no critical resources
- ❌ Otherwise provide a `close` method

## Example: Room Class (Cleaner as Safety Net)
- Implements `AutoCloseable`; cleaner is an internal implementation detail
- ✅ Unlike finalizers, cleaners **don't pollute the public API**
- 🔑 Static nested `State` class holds the resources to clean (e.g. `numJunkPiles`, or a `long` pointer to a native peer)
  - `State implements Runnable`; its `run` is invoked **at most once**
- `run` is triggered by either:
  - Usually: `close()` → `Cleanable.clean()`
  - Fallback: GC eligibility → cleaner calls `State.run()`
- ⚠️ **Critical**: `State` must **not** refer to its `Room` instance
  - A back-reference creates a circularity that blocks GC eligibility
  - 📌 Therefore `State` must be a **static** nested class (nonstatic ones hold an enclosing reference — Item 24)
  - ⚠️ Avoid lambdas too — they easily capture enclosing objects
- 💡 Behavior demonstration
  - `Adult` (try-with-resources): prints `Goodbye`, then `Cleaning room`
  - `Teenager` (never closes): often prints only `Peace out` — *never* `Cleaning room`
  - 📌 Spec: cleaner behavior during `System.exit` (and normal exit) is implementation-specific — no guarantees

## Key Takeaways
- 📌 **Don't use cleaners** (or finalizers pre-Java 9) **except** as a safety net or to terminate noncritical native resources
- ⚠️ Even then, beware the **indeterminacy** and **performance** consequences
- ✅ For resources needing termination, use `AutoCloseable` + `close` + `try-with-resources`
- 💡 Finalizers are slow (~50×), insecure (finalizer attacks), and may never run — the GC already handles memory