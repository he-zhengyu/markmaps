---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 10: Obey the `equals` Contract

## When *Not* to Override `equals`
- 💡 Easiest way to avoid problems: don't override → each instance equal only to itself
- **Instances inherently unique**
  - Classes representing active entities, not values (e.g. `Thread`)
  - `Object.equals` already behaves correctly
- **No need for "logical equality" test**
  - e.g. `java.util.regex.Pattern` — designers saw no client need
- **Superclass already overrode `equals`** appropriately
  - `Set` ← `AbstractSet`, `List` ← `AbstractList`, `Map` ← `AbstractMap`
- **Class is private/package-private** and `equals` never invoked
  - ⚠️ Risk-averse option: override to throw `AssertionError`

## When to Override `equals`
- 🔑 When class has **logical equality** differing from object identity *and* no superclass already overrode it
- Typically true for **value classes** (e.g. `Integer`, `String`)
  - 💡 Lets instances serve reliably as map keys / set elements
- ❌ Exception: value classes using **instance control** (one object per value)
  - Enum types (Item 34) — logical equality *is* object identity

## The `equals` Contract (Equivalence Relation)
- 🔑 **Equivalence relation**: partitions elements into interchangeable equivalence classes
- ⚠️ Violations cause erratic behavior / crashes, hard to diagnose
- 💡 "No class is an island" — collections rely on the contract
- **Reflexive**: `x.equals(x)` must be `true`
- **Symmetric**: `x.equals(y)` ⇔ `y.equals(x)`
- **Transitive**: `x=y` and `y=z` ⇒ `x=z`
- **Consistent**: repeated calls return same result (absent modification)
- **Non-nullity**: `x.equals(null)` must return `false`

## Reflexivity
- 📌 An object must equal itself
- Hard to violate unintentionally
- ⚠️ Violation: a collection's `contains` may deny holding an instance you just added

## Symmetry
- 🔑 Any two objects must **agree** on equality
- ⚠️ `CaseInsensitiveString` example
  - `equals` naively interoperates with ordinary `String` (one-way)
  - `cis.equals(s)` → `true`, but `s.equals(cis)` → `false`
  - 💡 `list.contains(s)` result is unpredictable across JDK implementations
- ✅ Fix: drop `String` interoperability; compare only own type
  ```java
  @Override public boolean equals(Object o) {
    return o instanceof CaseInsensitiveString &&
      ((CaseInsensitiveString) o).s.equalsIgnoreCase(s);
  }
  ```

## Transitivity
- ⚠️ Danger: subclass that **adds a value component**
- `Point` / `ColorPoint` case study
  - Inherit `Point.equals` → ignores color (unacceptable)
  - Color-aware `ColorPoint.equals` → **breaks symmetry**
    - `p.equals(cp)`→true, `cp.equals(p)`→false
  - "Color-blind" mixed comparison → **breaks transitivity**
    - `p1=p2`, `p2=p3` true, but `p1=p3` false
    - ⚠️ Can cause infinite recursion (`StackOverflowError`) between sibling subclasses
- 💡 Fundamental truth: **no way** to extend an instantiable class and add a value component while preserving `equals`
- ❌ The `getClass` "fix" — violates **Liskov Substitution Principle**
  - 🔑 *LSP*: properties of a type must hold for all subtypes
  - Equates only identical implementation classes
  - `CounterPoint` (adds no value component) fails `onUnitCircle` test
  - ✅ `instanceof`-based `equals` keeps subclasses working
- ✅ Workaround: **favor composition over inheritance** (Item 18)
  - `ColorPoint` *holds* a private `Point` field + `asPoint()` view method
- 📌 Adding a value component to a subclass of an **abstract class** is OK
  - Safe if superclass can't be instantiated directly (e.g. `Shape` → `Circle`, `Rectangle`)
- ⚠️ `java.sql.Timestamp` extends `java.util.Date`, adds nanoseconds → violates symmetry; a mistake, don't emulate

## Consistency
- 📌 Equal objects stay equal unless one is modified
- Immutable objects (Item 17) → equality fixed for all time
- ⚠️ Never depend on **unreliable resources**
  - `java.net.URL.equals` compares host IP addresses → needs network, non-deterministic; a known mistake
- ✅ Perform only **deterministic computations on memory-resident objects**

## Non-nullity
- 📌 All objects must be unequal to `null`
- ⚠️ Real risk is accidental `NullPointerException`, not returning `true`
- ❌ Explicit `if (o == null) return false;` is **unnecessary**
- ✅ The `instanceof` check returns `false` for `null` (JLS 15.20.2) — handles null automatically

## Recipe for a High-Quality `equals`
- 1. Use `==` to check identity — performance optimization
- 2. Use `instanceof` to verify correct type, else `false`
  - 📌 May use an interface (`Set`, `List`, `Map`, `Map.Entry`) if it refines the contract
- 3. **Cast** argument to correct type (guaranteed to succeed)
- 4. Compare each **significant field**
  - Primitives (not float/double): `==`
  - Object references: recursive `equals`
  - `float`: `Float.compare`; `double`: `Double.compare`
    - ⚠️ Needed due to `NaN`, `-0.0f`
  - Arrays: `Arrays.equals`
  - Possibly-null fields: `Objects.equals`
- 💡 Store a **canonical form** for complex field comparisons (best for immutables)
- 💡 Order fields: compare those most likely to differ / cheapest first
- ❌ Don't compare non-logical fields (e.g. lock fields); derived fields optional
- 📌 Afterward ask: **symmetric? transitive? consistent?** — and write unit tests

## Worked Example
- `PhoneNumber` class with `areaCode`, `prefix`, `lineNum`
  ```java
  @Override public boolean equals(Object o) {
    if (o == this) return true;
    if (!(o instanceof PhoneNumber)) return false;
    PhoneNumber pn = (PhoneNumber)o;
    return pn.lineNum == lineNum && pn.prefix == prefix
        && pn.areaCode == areaCode;
  }
  ```

## Final Caveats
- 📌 Always override `hashCode` when overriding `equals` (Item 11)
- ⚠️ Don't be too clever — avoid aliasing logic (e.g. `File` doesn't equate symbolic links)
- ❌ Don't replace `Object` with another type in the signature
  - Creates an **overload**, not an override (Item 52)
  - ✅ Use `@Override` to catch the mistake at compile time (Item 40)
- 💡 Prefer **AutoValue** (Google) to auto-generate `equals`/`hashCode`
  - IDE generation acceptable too — verbose, but avoids human error

## Key Takeaways
- 💡 Don't override `equals` unless the class has true logical equality; the inherited `Object` version is often correct
- 🔑 If you override, satisfy all five provisions: **reflexive, symmetric, transitive, consistent, non-null**
- ⚠️ You cannot add a value component to an instantiable class without breaking the contract — use **composition**, not inheritance
- ✅ Follow the recipe: `==`, `instanceof`, cast, compare significant fields
- 📌 Never depend on unreliable resources; keep comparisons deterministic
- 📌 Always override `hashCode` alongside `equals`, and prefer tools like AutoValue