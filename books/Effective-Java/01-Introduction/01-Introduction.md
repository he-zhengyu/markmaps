---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Effective Java — Ch. 1: Introduction

## Purpose & Scope
- Helps make **effective use** of Java and its core libraries
- Fundamental packages covered: `java.lang`, `java.util`, `java.io`
- Subpackages: `java.util.concurrent`, `java.util.function`
- Other libraries discussed occasionally

## Book Structure
- **90 items**, each conveying one rule
- Rules = practices held beneficial by the best, most experienced programmers
- Grouped into **11 chapters**, each one broad aspect of software design
- 💡 Not meant to be read cover to cover — each item stands on its own
- Heavily **cross-referenced** — plot your own course

## Key Features by Release
- Most items use platform features added since last edition
- **Lambdas** → Items 42–44, *Java 8*
- **Streams** → Items 45–48, *Java 8*
- **Optionals** → Item 55, *Java 8*
- **Default methods in interfaces** → Item 21, *Java 8*
- **try-with-resources** → Item 9, *Java 7*
- **@SafeVarargs** → Item 32, *Java 7*
- **Modules** → Item 15, *Java 9*

## Code Examples
- Most items illustrated with program examples
- Illustrate many design patterns & idioms
- Cross-referenced to the standard reference work [Gamma95]
- **Antipatterns**: bad practices labeled `// Never do this!`
  - ⚠️ Item explains why it's bad and suggests an alternative
- Examples favor *readability over completeness*
- 📌 May need extra `import` declarations to compile
- Expanded, runnable versions at [joshbloch.com/effectivejava](http://joshbloch.com/effectivejava)

## Intended Audience
- ❌ Not for beginners — assumes comfort with Java
- Beginners → try Peter Sestoft's *Java Precisely* [Sestoft16]
- 💡 Still offers food for thought for advanced programmers

## Fundamental Principles
- 🔑 **Clarity and simplicity** are paramount
- 💡 User of a component should never be surprised by its behavior
- Components as small as possible — *but no smaller*
  - 🔑 **Component** = any reusable software element (method → framework)
- ✅ **Reuse** code rather than copy it
- ✅ Keep **dependencies** between components to a minimum
- ✅ Detect errors ASAP — ideally at **compile time**

## On Following the Rules
- 💡 Rules characterize best practices in the great majority of cases
- ⚠️ Don't follow slavishly — violate only occasionally, with good reason
- 📌 Learn the rules first, then learn when to break them

## Not About Performance
- Focus: programs that are **clear, correct, usable, robust, flexible, maintainable**
- 💡 Get those right → performance usually follows (Item 67)
- A few items give numbers, prefixed *"On my machine"* — approximate at best
- Author's machine: 3.5GHz quad-core Intel Core i7-4770K, 16GB RAM, OpenJDK (Azul Zulu 9), Windows 7 SP1
  - *AI-added: hardware noted for context; absolute figures are not meaningful today*

## Release Names vs. Nicknames
- Book uses nicknames over official names for convenience
- JDK 1.0.x → **Java 1.0**
- JDK 1.1.x → **Java 1.1**
- SE v1.2 → **Java 2**
- SE v1.3 → **Java 3**
- SE v1.4 → **Java 4**
- SE v5.0 → **Java 5**
- SE 6 → **Java 6**
- SE 7 → **Java 7**
- SE 8 → **Java 8**
- SE 9 → **Java 9**

## Terminology
### From The Java Language Specification [JLS]
- Four kinds of **types**: interfaces (incl. annotations), classes (incl. enums), arrays, primitives
- 🔑 First three = **reference types**
- Class instances & arrays are **objects**; primitives are not
- 🔑 A class's **members**: fields, methods, member classes, member interfaces
- 🔑 A method's **signature** = name + formal parameter types
  - ⚠️ Signature does *not* include return type

### Terms Used Differently
- **Inheritance** used as synonym for *subclassing*
- For interfaces: a class **implements** / one interface **extends** another (not "inherits")
- Uses traditional **package-private** instead of technically correct *package access* [JLS 6.6.1]

### Terms Not in the JLS
- 🔑 **Exported API (API)**: classes, interfaces, constructors, members, serialized forms used to access a class/interface/package
  - Term *API* preferred over *interface* to avoid confusion with the language construct
- 🔑 **User** of an API: a programmer whose program uses it
- 🔑 **Client** of an API: a class whose implementation uses it
- 🔑 **API elements**: classes, interfaces, constructors, members, serialized forms
- **Exported API** = API elements accessible outside the defining package
  - Elements the author commits to support
  - Same elements **Javadoc** documents by default
  - ≈ public + protected members and constructors of every public class/interface

### Modules (Java 9)
- 🔑 Module system added to the platform in **Java 9**
- If a library uses it, its exported API = union of exported APIs of all packages exported by the module declaration

## Key Takeaways
- 📌 The book is a reference of **90 cross-referenced rules**, not a linear read
- 🔑 Core values: **clarity, simplicity, reuse, minimal dependencies, early error detection**
- 💡 Rules are guidelines — master them, then know when to break them
- ✅ Prioritize correct, maintainable code; performance usually follows
- 📌 Precise vocabulary (component, API, signature, exported API) underpins the whole book
- ⚠️ Assumes existing Java fluency — not an introductory text