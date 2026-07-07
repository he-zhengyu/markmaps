---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 25: Limit Source Files to a Single Top-Level Class

## The Core Problem
- Java compiler *permits* multiple top-level classes per source file
- ❌ **No benefits**, significant risks
- ⚠️ Enables **multiple definitions** of the same class
- 💡 Which definition wins depends on **compiler argument order**

## Demonstration Example
### Setup
- `Main` class references `Utensil.NAME + Dessert.NAME`
- `Utensil.java` defines both `Utensil` ("pan") and `Dessert` ("cake")
- Duplicate `Dessert.java` also defines both: `Utensil` ("pot"), `Dessert` ("pie")
### Outcomes by Compile Command
- `javac Main.java Dessert.java` → ✅ compilation **fails** (duplicate definitions detected)
  - Compiler resolves `Utensil` via `Utensil.java` first, then hits `Dessert.java` duplicates
- `javac Main.java` or `javac Main.java Utensil.java` → prints **pancake**
- `javac Dessert.java Main.java` → prints **potpie**
### Diagnosis
- ⚠️ Program behavior depends on **source file ordering** — clearly unacceptable

## Solutions
### Split into Separate Source Files
- Simplest fix: one top-level class per file
### Static Member Classes (Item 24)
- Preferred when classes are **subservient** to another class
- ✅ Enhances readability
- ✅ Allows reduced accessibility via `private` (Item 15)
- Example: `Utensil` and `Dessert` as `private static class` inside `Test`

## Key Takeaways
- 📌 **Never put multiple top-level classes or interfaces in one source file**
- Guarantees no multiple class definitions at compile time
- 💡 Class files and program behavior become **independent of compilation order**
- Use static member classes as the alternative for helper classes