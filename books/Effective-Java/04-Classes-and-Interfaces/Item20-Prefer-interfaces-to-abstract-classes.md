---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Prefer Interfaces to Abstract Classes

## Two Mechanisms for Types
- Java defines **multi-implementation types** via `interface` and abstract class
- Since **Java 8**, both can supply instance method implementations via *default methods*
- 🔑 **Default method**: an instance method implementation provided directly on an interface
- ⚠️ Abstract class requires implementers to be a **subclass**
  - Java permits only **single inheritance** → severely constrains abstract classes as types
- ✅ Any class obeying the contract may implement an interface, regardless of hierarchy position

## Why Interfaces Win

### Easy Retrofitting
- Add the missing methods + an `implements` clause to an existing class
- 💡 Real cases: existing classes retrofitted to `Comparable`, `Iterable`, `AutoCloseable`
- ❌ Existing classes **can't** generally be retrofitted to extend a new abstract class
  - ⚠️ A shared abstract class must sit high in the hierarchy → forces it onto all descendants, even where inappropriate

### Ideal for Mixins
- 🔑 **Mixin**: a type a class implements *alongside* its primary type to declare optional behavior
- *Comparable* is a mixin: instances are ordered relative to mutually comparable objects
- ❌ Abstract classes can't define mixins — no room for a second parent in the hierarchy

### Nonhierarchical Type Frameworks
- 💡 Some concepts don't fit a rigid hierarchy
- Example: separate `Singer` and `Songwriter` interfaces
  - A single class may implement **both**
  - Can extend both into `SingerSongwriter` with added methods
- ⚠️ Abstract-class alternative breeds a **combinatorial explosion**
  - 📊 *n* attributes → up to **2ⁿ** classes to support every combination
  - Leads to bloated classes with near-duplicate methods

### Powerful Enhancement via Wrappers
- Interfaces enable safe enhancement through the **wrapper class idiom** (Item 18)
- ❌ Abstract classes leave only *inheritance* → resulting classes are less powerful and more fragile

## Default Methods
- Provide implementation assistance when a method has an obvious form in terms of other methods
  - Example: the `removeIf` method
- 📌 Document them for inheritance with the `@implSpec` Javadoc tag (Item 19)
- ⚠️ **Limits on default methods**
  - ❌ Cannot provide defaults for `Object` methods like `equals`, `hashCode`
  - ❌ No instance fields or nonpublic static members (private static methods excepted)
  - ❌ Cannot add defaults to an interface you don't control

## Skeletal Implementation

### Concept
- 💡 Combine the merits of interfaces and abstract classes
- Interface defines the type (+ optional default methods); abstract class implements the rest atop the primitives
- 🔑 This is the **Template Method pattern** [Gamma95]
- Extending it removes most of the work of implementing an interface

### Naming & Examples
- Convention: `AbstractInterface` (e.g. would-be `Skeletal*` names lost out)
- Collections Framework provides `AbstractCollection`, `AbstractSet`, `AbstractList`, `AbstractMap`
- Example: `intArrayAsList` builds a full `List` atop `AbstractList`
  - An **Adapter** [Gamma95]: views an `int[]` as `List<Integer>`
  - ⚠️ Boxing/unboxing makes its performance poor
  - Implemented as an **anonymous class** (Item 24)

### Benefits & Flexibility
- ✅ Implementation assistance of abstract classes **without** their type-definition constraints
- Extending the skeletal class is the obvious choice but strictly **optional**
  - A class can implement the interface directly and still gain its default methods
- 🔑 **Simulated multiple inheritance**: forward interface calls to a private inner class extending the skeletal impl
  - Related to the wrapper idiom (Item 18); gains of multiple inheritance without the pitfalls

## Writing a Skeletal Implementation

### The Process
- First, pick the **primitive** methods → these become the **abstract** methods
- Add default methods on the interface for everything implementable atop the primitives
  - ❌ Not for `Object` methods (`equals`, `hashCode`)
- If primitives + defaults cover the interface → **done**, no skeletal class needed
- Otherwise write a class implementing the remaining methods, with any nonpublic fields/methods needed

### Map.Entry Example
- Primitives: `getKey`, `getValue`, optionally `setValue` → in `AbstractMapEntry`
- 📌 `equals`, `hashCode`, `toString` placed in the **class**, since defaults can't override `Object` methods
- `setValue` throws `UnsupportedOperationException` unless overridden by modifiable maps

### Documentation
- 📌 Follow all design/documentation guidelines of Item 19 — skeletal impls are designed for inheritance
- 💡 Good documentation is **essential**, whether default methods or a separate abstract class

## Simple Implementation
- 🔑 A **simple implementation** is like skeletal but **not abstract** — the simplest working implementation
- Example: `AbstractMap.SimpleEntry`
- Use it as-is or subclass it as circumstances warrant

## Key Takeaways
- 📌 An interface is generally the **best way** to define a type permitting multiple implementations
- ✅ For a nontrivial exported interface, **strongly consider** providing a skeletal implementation
- ✅ Deliver the skeletal impl via **default methods** where possible, so all implementors benefit
- ⚠️ Interface restrictions usually force the skeletal implementation to take the form of an **abstract class**