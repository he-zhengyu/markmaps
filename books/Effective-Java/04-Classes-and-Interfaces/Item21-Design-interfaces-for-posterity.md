---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 21: Design Interfaces for Posterity

## The Pre-Java 8 Constraint
- Impossible to add methods to an interface without breaking implementations
- New method → existing implementations lack it → **compile-time error**
- Implementors wrote code with the tacit understanding that interfaces would *never* acquire new methods

## Default Methods (Java 8)
- 🔑 **default method** `[JLS 9.4]`: an interface method carrying a default implementation
- Used by all implementing classes that do **not** override it
- Intent: allow adding methods to *existing* interfaces
- Many added to core collection interfaces, mainly to facilitate **lambdas** (Chapter 6)
- Library defaults are high-quality, general-purpose, and usually work fine
- ⚠️ But adding new methods to existing interfaces is fraught with risk

## Why Adding Methods Is Risky
- ⚠️ Defaults are *“injected”* into existing implementations without the implementor's knowledge or consent
- 💡 Not always possible to write a default that maintains **every** implementation's invariants
- 💡 Existing implementations may compile without error or warning yet **fail at runtime**
- Not isolated: a handful of Java 8 collection methods and existing implementations are known to be affected

## Case Study: `removeIf`
### What `removeIf` Does
- Added to the `Collection` interface in Java 8
- Removes all elements for which a **predicate** returns `true`
- Default impl: traverse via the collection's `iterator`, test each element, call `iterator.remove()` on matches

### The Default Implementation
- ```java
  default boolean removeIf(Predicate<? super E> filter) {
      Objects.requireNonNull(filter);
      boolean result = false;
      for (Iterator<E> it = iterator(); it.hasNext(); ) {
          if (filter.test(it.next())) {
              it.remove();
              result = true;
          }
      }
      return result;
  }
  ```
- 💡 The best general-purpose implementation possible — yet it still fails on some real-world collections

### Failure: Apache `SynchronizedCollection`
- A **wrapper class** (Item 18); every method synchronizes on a locking object before delegating
- Adds the ability to use a client-supplied lock object
- Still actively maintained, but does **not** override `removeIf`
- ❌ Inherits the default, which cannot keep the class's core promise: synchronize around each invocation
- Default knows nothing about synchronization and has no access to the lock field
- ⚠️ Concurrent modification → `ConcurrentModificationException` or other unspecified behavior

### The JDK's Fix
- JDK maintainers **overrode** the default `removeIf` (and similar methods) in `Collections.synchronizedCollection` to synchronize before invoking it
- ⚠️ Non-platform implementations couldn't change in lockstep with the interface — some still have not

## When to Use Default Methods
- ⚠️ Avoid using defaults to add methods to existing interfaces unless the need is **critical**
- If critical, think long and hard about whether an existing implementation could break
- ✅ Extremely useful at **interface creation time** — provide standard implementations to ease the task of implementing the interface (Item 20)

## What Default Methods Cannot Do
- ❌ Not designed to **remove** methods from interfaces
- ❌ Not designed to **change signatures** of existing methods
- Either change breaks existing clients

## Test Interfaces Before Release
- 📌 Test each new interface before you release it
- Have multiple programmers implement it in different ways — aim for at least **three diverse implementations**
- Write multiple client programs that exercise each interface on various tasks
- 💡 This surfaces flaws while they are still easy to correct
- ⚠️ Fixing flaws *after* release may be possible, but you cannot count on it

## Key Takeaways
- 📌 Even with default methods, design interfaces with the **utmost care**
- Default methods make adding to existing interfaces possible, but the risk is great
- 💡 A minor flaw can irritate users forever; a severe deficiency can **doom the entire API**
- ✅ Treat default methods as a tool for interface *creation*, not as a safe way to evolve published interfaces