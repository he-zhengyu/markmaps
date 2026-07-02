---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 22: Use Interfaces Only to Define Types

## The Core Principle
- 🔑 An interface is a **type** used to refer to instances of an implementing class
- 💡 Implementing an interface should say *what a client can do* with instances
- ⚠️ Defining an interface for any other purpose is inappropriate

## The Constant Interface Antipattern
### What It Is
- 🔑 An interface with **no methods**, only `static final` constant fields
- 💡 Classes implement it to use constants *unqualified* (without a class-name prefix)
- ❌ Example: `PhysicalConstants` exporting `AVOGADROS_NUMBER`, `BOLTZMANN_CONSTANT`, `ELECTRON_MASS`
  ```java
  // Constant interface antipattern - do not use!
  public interface PhysicalConstants {
      static final double AVOGADROS_NUMBER   = 6.022_140_857e23;
      static final double BOLTZMANN_CONSTANT = 1.380_648_52e-23;
      static final double ELECTRON_MASS      = 9.109_383_56e-31;
  }
  ```
### Why It's a Poor Use of Interfaces
- ⚠️ Internal constant use is an **implementation detail** — it leaks into the exported API
- ⚠️ Of no consequence to users; may even confuse them
- 📌 Represents a binding **commitment**: must keep implementing it for *binary compatibility*, even if constants are no longer needed
- ⚠️ A nonfinal class pollutes *all subclasses'* namespaces with its constants
### Existing Examples in Java
- 📌 `java.io.ObjectStreamConstants` and others exist in the platform libraries
- ❌ Regard these as **anomalies**; do not emulate them

## Proper Ways to Export Constants
### Add to a Related Class or Interface
- ✅ Use when constants are strongly tied to an existing class/interface
- 📊 Boxed primitives like `Integer` and `Double` export `MIN_VALUE` and `MAX_VALUE`
### Use an Enum Type
- ✅ Use when constants are best viewed as members of an *enumerated type* (Item 34)
### Use a Noninstantiable Utility Class
- ✅ The general-purpose fallback (Item 4)
- 🔑 Private constructor prevents instantiation
  ```java
  // Constant utility class
  package com.effectivejava.science;
  public class PhysicalConstants {
      private PhysicalConstants() { } // Prevents instantiation
      public static final double AVOGADROS_NUMBER = 6.022_140_857e23;
      public static final double BOLTZMANN_CONST  = 1.380_648_52e-23;
      public static final double ELECTRON_MASS    = 9.109_383_56e-31;
  }
  ```

## Avoiding Qualification: Static Import
- 💡 Utility classes normally require qualifying: `PhysicalConstants.AVOGADROS_NUMBER`
- ✅ For heavy use, the **static import** facility removes the need to qualify
  ```java
  import static com.effectivejava.science.PhysicalConstants.*;
  public class Test {
      double atoms(double mols) {
          return AVOGADROS_NUMBER * mols;
      }
  }
  ```
- 📌 Justified only when use of the constants is heavy

## Aside: Underscores in Numeric Literals
- 🔑 Legal since *Java 7*; **no effect** on the literal's value
- 💡 Improve readability when used with discretion
- 📌 Consider adding them to literals with **five or more** consecutive digits
- 📊 For base-ten literals, group digits in **threes** (powers of one thousand)

## Key Takeaways
- 📌 Interfaces should be used **only to define types**, never merely to export constants
- ❌ The constant interface pattern leaks implementation details and creates lasting commitments
- ✅ Export constants via a related class/interface, an `enum`, or a noninstantiable utility class
- 💡 Use static import to avoid qualification only when constant use is heavy