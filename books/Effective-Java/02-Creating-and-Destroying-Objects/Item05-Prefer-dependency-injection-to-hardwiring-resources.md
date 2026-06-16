---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 5: Prefer Dependency Injection to Hardwiring Resources

## The Problem: Hardwired Resources
- Many classes depend on one or more **underlying resources**
  - 🔑 Example: a `SpellChecker` depends on a `Lexicon` *dictionary*
- Common but flawed implementations
  - **Static utility class** (Item 4)
    - `private static final Lexicon dictionary`
    - noninstantiable, `static` methods
    - ❌ inflexible & untestable
  - **Singleton** (Item 3)
    - `private final Lexicon dictionary` + `static INSTANCE`
    - ❌ inflexible & untestable

## Why These Approaches Fail
- 💡 Both assume **one dictionary suffices for all time** — wishful thinking
- Reality demands multiple resources
  - each language has its own dictionary
  - special dictionaries for special vocabularies
  - a separate dictionary desirable for **testing**
- Attempted workaround: nonfinal field + setter method
  - ⚠️ awkward, error-prone
  - ⚠️ unworkable in a **concurrent** setting
- 📌 Static utilities & singletons are inappropriate for classes whose behavior is *parameterized by an underlying resource*

## The Solution: Dependency Injection
- 🔑 **Dependency injection**: pass the resource into the constructor when creating a new instance
  - the dictionary is *injected* into the spell checker at creation time
- Implementation
  - `public SpellChecker(Lexicon dictionary)`
  - guard with `Objects.requireNonNull(dictionary)`
  - keep the field `private final`
- ✅ Supports **multiple instances**, each using the client's desired resource
- 💡 So simple that many use it for years without knowing its name

## Properties & Reach
- Works with an **arbitrary number of resources** and arbitrary dependency graphs
- Preserves **immutability** (Item 17)
  - multiple clients can share dependent objects (if they want the same resources)
- Applicable to constructors, **static factories** (Item 1), and **builders** (Item 2)

## Variant: Pass a Resource Factory
- 🔑 A **factory** is an object called repeatedly to create instances of a type
  - embodies the **Factory Method** pattern [Gamma95]
- `Supplier<T>` (Java 8) is perfect for representing factories
- 📌 Constrain the type with a **bounded wildcard** (Item 31) to accept any subtype
  - `Mosaic create(Supplier<? extends Tile> tileFactory)`

## Managing Clutter at Scale
- ⚠️ DI can clutter large projects with **thousands of dependencies**
- Use a **DI framework** to eliminate the clutter
  - **Dagger**, **Guice**, **Spring**
- 💡 APIs designed for *manual* DI adapt trivially to these frameworks

## Key Takeaways
- ❌ Don't use a singleton or static utility class for a class that depends on underlying resources whose behavior affects it
- ❌ Don't have the class create those resources directly
- ✅ Instead, **pass the resources (or factories for them)** into the constructor, static factory, or builder
- 💡 This practice — **dependency injection** — greatly enhances *flexibility*, *reusability*, and *testability*