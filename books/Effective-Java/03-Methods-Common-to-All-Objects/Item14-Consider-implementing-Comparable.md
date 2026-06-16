---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 14: Consider Implementing `Comparable`

## What `Comparable` Is
- 🔑 `compareTo` is **not** declared in `Object`
- 🔑 Sole method of the `Comparable` interface
- Like `equals`, but adds **order comparisons** (not just equality)
- Is **generic**
- 💡 Implementing it declares instances have a **natural ordering**
- The interface
  ```java
  public interface Comparable<T> {
      int compareTo(T t);
  }
  ```

## Why Implement It
- Sorting becomes trivial: `Arrays.sort(a)`
- Easy to **search**, **find extremes**, maintain **sorted collections**
- 💡 Interoperates with all generic algorithms & collections that depend on it
- Example: alphabetized, dedup'd word list via `TreeSet`
  ```java
  public class WordList {
      public static void main(String[] args) {
          Set<String> s = new TreeSet<>();
          Collections.addAll(s, args);
          System.out.println(s);
      }
  }
  ```
- 📌 Great power for little effort
- 💡 Nearly all value classes & all enum types already implement it
- ✅ Implement when there's an obvious natural order
  - alphabetical
  - numerical
  - chronological

## The `compareTo` General Contract
### Return Value
- 🔑 Returns **negative / zero / positive** as this is `<`, `=`, or `>` the argument
- Throws `ClassCastException` if argument's type can't be compared
- *Notation:* `sgn(expr)` = signum, returns -1, 0, or 1

### Three Required Provisions
- **Anti-symmetry**: `sgn(x.compareTo(y)) == -sgn(y.compareTo(x))`
  - Implies one throws ⟺ the other throws
- **Transitivity**: `(x>y && y>z)` implies `x>z`
- **Consistency of equals-results**: `x.compareTo(y)==0` implies equal `sgn` vs any `z`
- 💡 Plain-language reading: reversing direction reverses result; chains carry through; equal objects compare identically to all others

### Strong Suggestion (Not Required)
- 📌 `(x.compareTo(y)==0) == (x.equals(y))` → *consistent with equals*
- ⚠️ If violated, recommend documenting:
  > "Note: This class has a natural ordering that is inconsistent with `equals`."

### Scope vs `equals`
- 💡 Unlike `equals` (global equivalence on all objects), `compareTo` need **not** work across types
- ⚠️ Confronted with different types → may throw `ClassCastException` (usually does)
- Intertype comparisons permitted, typically via a shared interface

## Consequences & Caveats
- ⚠️ Violating the contract breaks `TreeSet`, `TreeMap`, `Collections`, `Arrays`
- Equality test must obey **reflexivity, symmetry, transitivity** (same as `equals`)
- ⚠️ No way to extend an instantiable class with a new value component while preserving the contract
  - ✅ Workaround: **composition** — hold an instance, expose a `view` method
- 📊 *Inconsistent-with-equals* example: `BigDecimal`
  - `new BigDecimal("1.0")` vs `new BigDecimal("1.00")`
  - `HashSet` → **2 elements** (uses `equals`, unequal)
  - `TreeSet` → **1 element** (uses `compareTo`, equal)
  - 💡 Not catastrophic, but be aware

## Writing a `compareTo` Method
### vs Writing `equals`
- 💡 Interface is parameterized → method is **statically typed**
- ❌ No type check or cast needed; wrong type won't compile
- `null` argument → `NullPointerException` on member access

### Comparing Fields
- 🔑 Fields compared for **order**, not equality
- Object reference fields → invoke `compareTo` recursively
- ⚠️ Field not `Comparable` or needs nonstandard order → use a `Comparator`
- Example: single field via existing comparator
  ```java
  public final class CaseInsensitiveString
          implements Comparable<CaseInsensitiveString> {
      public int compareTo(CaseInsensitiveString cis) {
          return String.CASE_INSENSITIVE_ORDER.compare(s, cis.s);
      }
  }
  ```
  - 📌 Implements `Comparable<CaseInsensitiveString>` — comparable only to same type (normal pattern)

### Multiple Significant Fields
- 🔑 Compare from **most** to **least** significant
- 💡 Return as soon as a comparison is non-zero
- Example: `PhoneNumber`
  ```java
  public int compareTo(PhoneNumber pn) {
      int result = Short.compare(areaCode, pn.areaCode);
      if (result == 0) {
          result = Short.compare(prefix, pn.prefix);
          if (result == 0)
              result = Short.compare(lineNum, pn.lineNum);
      }
      return result;
  }
  ```

### Avoid `<` and `>`
- ⚠️ Old advice (prior editions): relational ops for integrals, `Double.compare`/`Float.compare` for floats
- 💡 Java 7 added static `compare` to all boxed primitives
- ❌ `<` and `>` are verbose, error-prone, **no longer recommended**

## Comparator Construction Methods (Java 8)
- 🔑 Enable **fluent** construction of comparators usable inside `compareTo`
- ✅ Pro: concise, many programmers prefer it
- ⚠️ Con: modest cost — 📊 ~**10% slower** sorting on author's machine
- 📌 Tip: use static import to reference methods by simple name
- Example: `PhoneNumber`
  ```java
  private static final Comparator<PhoneNumber> COMPARATOR =
      comparingInt((PhoneNumber pn) -> pn.areaCode)
          .thenComparingInt(pn -> pn.prefix)
          .thenComparingInt(pn -> pn.lineNum);

  public int compareTo(PhoneNumber pn) {
      return COMPARATOR.compare(this, pn);
  }
  ```

### `comparingInt`
- Static method taking a **key extractor** → key of type `int`
- Returns comparator ordering by that key
- ⚠️ Type inference too weak here → must specify `(PhoneNumber pn)` explicitly

### `thenComparingInt`
- Instance method taking an `int` key extractor
- Applies original comparator first, breaks ties with extracted key
- 💡 Stack freely → **lexicographic** ordering
- 💡 Parameter type **can** be inferred here (no explicit type needed)

### Full Complement
- Primitive analogues: `comparingInt`/`thenComparingInt` plus `long`, `double` versions
  - `int` versions cover narrower integrals (e.g. `short`)
  - `double` versions cover `float`
- Object reference: `comparing` (2 overloads), `thenComparing` (3 overloads)
  - key extractor (+ natural order), or key extractor + comparator on keys

## ⚠️ Avoid Difference-Based Comparators
- ❌ BROKEN — violates transitivity
  ```java
  static Comparator<Object> hashCodeOrder = new Comparator<>() {
      public int compare(Object o1, Object o2) {
          return o1.hashCode() - o2.hashCode();
      }
  };
  ```
- ⚠️ Danger from **integer overflow** and IEEE 754 floating-point artifacts
- 💡 Not meaningfully faster than correct approaches
- ✅ Fix 1 — static `compare` method
  ```java
  static Comparator<Object> hashCodeOrder = new Comparator<>() {
      public int compare(Object o1, Object o2) {
          return Integer.compare(o1.hashCode(), o2.hashCode());
      }
  };
  ```
- ✅ Fix 2 — comparator construction method
  ```java
  static Comparator<Object> hashCodeOrder =
      Comparator.comparingInt(o -> o.hashCode());
  ```

## Key Takeaways
- 📌 Implement `Comparable` on any value class with a sensible ordering → easy sort, search, comparison-based collections
- ❌ Never use `<` and `>` in `compareTo` implementations
- ✅ Use static `compare` methods of boxed primitives **or** `Comparator` construction methods
- ⚠️ Honor the contract (anti-symmetry, transitivity, consistency) or risk breaking sorted collections
- 💡 Strive to keep ordering *consistent with `equals`*; document clearly when it isn't