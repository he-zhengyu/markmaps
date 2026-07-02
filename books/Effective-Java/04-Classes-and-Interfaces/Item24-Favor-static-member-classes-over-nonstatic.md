---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 24: Favor Static Member Classes over Nonstatic

## What Is a Nested Class
- 🔑 A class defined within another class
- 📌 Should exist *only* to serve its enclosing class
- ⚠️ If useful in another context → make it a **top-level class**

## Four Kinds of Nested Classes
- **Static member classes**
- **Nonstatic member classes**
- **Anonymous classes**
- **Local classes**
- 🔑 All but the first are called **inner classes**

## Static Member Class
### Nature
- 💡 Simplest kind of nested class
- Behaves like an ordinary class declared inside another
- Has access to all enclosing members, even `private`
- Obeys same accessibility rules as other static members (e.g. `private` → enclosing-only)
- Syntactically: identical to nonstatic, but with the `static` modifier
### Common Uses
- ✅ **Public helper class** tied to its outer class
  - Example: an `Operation` enum inside `Calculator`
  - Clients refer via `Calculator.Operation.PLUS`, `Calculator.Operation.MINUS`
- ✅ **Private static member class** to represent components of the enclosing object
  - Example: `Map` `Entry` for each key-value pair
  - 💡 Entry methods (`getKey`, `getValue`, `setValue`) don't need the map → static is best

## Nonstatic Member Class
### Behavior
- 🔑 Each instance is implicitly associated with an **enclosing instance**
- Can invoke enclosing methods / get reference via qualified `this`
- 📌 Cannot create an instance without an enclosing instance
- Association fixed at creation, cannot be modified later
- Usually established automatically by calling the constructor from an enclosing instance method
- Rarely: `enclosingInstance.new MemberClass(args)`
- ⚠️ Association costs **space** in the instance and **time** at construction
### Common Use
- ✅ Define an **Adapter** — view outer instance as an instance of an unrelated class
  - `Map` collection views: `keySet`, `entrySet`, `values`
  - `Set` / `List` iterators (e.g. `MyIterator implements Iterator<E>`)
### The Static Modifier Rule
- 📌 If no access to enclosing instance is needed → **always add** `static`
- ⚠️ Omitting it gives each instance a hidden reference to the enclosing instance
- ⚠️ Wastes time and space
- ⚠️ Can retain the enclosing instance, blocking **garbage collection** (Item 7)
- ⚠️ Resulting **memory leak** can be catastrophic and hard to detect (reference is invisible)
- ⚠️ Choice is doubly important for `public`/`protected` members of an exported class
  - Such a member class is an exported API element
  - Cannot switch nonstatic → static later without breaking backward compatibility

## Anonymous Class
### Characteristics
- 🔑 Has no name; not a member of the enclosing class
- Declared and instantiated simultaneously at the point of use
- Permitted anywhere an expression is legal
- Has an enclosing instance only in a nonstatic context
- No static members except constant variables (`final` primitive/string constants)
### Limitations
- ❌ Can't instantiate except where declared
- ❌ Can't do `instanceof` or anything needing the class name
- ❌ Can't implement multiple interfaces, or extend a class *and* implement an interface
- ❌ Clients can only invoke members inherited from the supertype
- ⚠️ Must stay short (~10 lines or fewer) or readability suffers
### Uses
- Formerly preferred for small **function/process objects**
- 💡 Now superseded by **lambdas** (Item 42)
- Still used in **static factory methods** (e.g. `intArrayAsList`, Item 20)

## Local Class
- 🔑 Least frequently used of the four kinds
- Declarable practically anywhere a local variable can be, with the same scoping rules
- Like member classes: has a name, can be used repeatedly
- Like anonymous classes: enclosing instance only in nonstatic context; no static members
- ⚠️ Keep short to preserve readability

## Decision Guide (Recap)
- Visible outside one method, or too long for a method → **member class**
  - Needs reference to enclosing instance → **nonstatic**
  - Otherwise → **static**
- Fits inside a method:
  - Instantiated from one place + preexisting type fits → **anonymous class**
  - Otherwise → **local class**

## Key Takeaways
- 🔑 Each of the four nested-class kinds has its place; choose by need
- 📌 Default to a **static** member class; add `static` whenever no enclosing reference is needed
- ⚠️ A missing `static` causes hidden references, wasted resources, and catastrophic memory leaks
- 💡 Prefer **lambdas** over anonymous classes for small function objects
- ⚠️ Get the static/nonstatic choice right for exported API members — it can't change without breaking compatibility