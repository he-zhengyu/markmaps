---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 49: Check Parameters for Validity

## The Core Principle
- 📌 Document all parameter restrictions and enforce them with **checks at the start of the method body**
- 💡 A special case of: **detect errors as soon as possible** after they occur
- ⚠️ Failing to check makes errors less likely to be detected, and harder to trace once detected
- 🔑 Common restrictions: index values must be *non-negative*; object references must be *non-null*

## Why Fail Fast Matters
### With validity checks
- ✅ Method **fails quickly and cleanly** with an appropriate exception
### Without validity checks — escalating failure modes
- Method fails with a *confusing* exception mid-processing
- Worse: returns normally but **silently computes the wrong result**
- Worst: returns normally but leaves an object in a **compromised state**
  - Causes an error at an unrelated point, at an undetermined future time
- 💡 Net effect: a violation of **failure atomicity** (Item 76)

## Documenting Restrictions
### Public & protected methods
- Use the Javadoc `@throws` tag to document the exception thrown on violation (Item 74)
- 🔑 Typical exceptions: `IllegalArgumentException`, `IndexOutOfBoundsException`, `NullPointerException` (Item 72)
### Example: `BigInteger.mod`
- Doc states `@throws ArithmeticException if m is less than or equal to 0`
- Implementation: `if (m.signum() <= 0) throw new ArithmeticException(...)`
- 💡 `NullPointerException` for null `m` is **not** documented per-method
  - It's a byproduct of invoking `m.signum()`
  - Documented once in the **class-level** doc comment, applying to all public methods
  - ✅ Avoids the clutter of documenting NPE on every method
- May combine with `@Nullable`-style annotations
  - ⚠️ Not standard practice; multiple competing annotations exist

## Enforcement Tools
### `Objects.requireNonNull` (Java 7)
- 💡 Flexible and convenient — **no reason to do manual null checks anymore**
- Lets you specify your own detail message
- Returns its input, so you can check and assign at once
  - `this.strategy = Objects.requireNonNull(strategy, "strategy");`
- Can also be used as a freestanding null check (ignore return value)
### Range-checking facility (Java 9)
- Added to `java.util.Objects`: `checkFromIndexSize`, `checkFromToIndex`, `checkIndex`
- ⚠️ Less flexible than null-checking
  - ❌ Can't specify your own detail message
  - Designed solely for **list and array indices**
  - ❌ Does not handle closed ranges (both endpoints inclusive)
- ✅ Still a useful convenience when it fits

## Nonpublic Methods → Use Assertions
- 🔑 As package author you control the call sites, so you can guarantee valid inputs
- Use `assert` to claim conditions hold **regardless of client use**
  - `assert a != null;`
  - `assert offset >= 0 && offset <= a.length;`
- Behavior vs normal checks
  - Throw `AssertionError` on failure (not `IllegalArgumentException` etc.)
  - 💡 No effect and essentially **no cost** unless enabled via `-ea` / `-enableassertions`

## Special Cases
### Parameters stored for later use
- 📌 Especially important to validate these
- Example: static factory taking an `int` array, returning a `List` view
  - With check (`Objects.requireNonNull`) → NPE thrown immediately on null
  - ❌ Without check → `List` created, NPE thrown only when later used
  - ⚠️ By then the origin is hard to determine, complicating debugging
### Constructors
- 🔑 A special case of validating parameters stored for later use
- Critical to validate, to prevent constructing an object that **violates its class invariants**

## Exceptions to the Rule
### When the check is implicit and explicit checking is costly
- 💡 Skip explicit checks if validity is verified implicitly during computation
- Example: `Collections.sort(List)`
  - Elements must be mutually comparable
  - A bad element naturally triggers `ClassCastException` during comparison — exactly what `sort` should throw
  - ✅ Little point checking comparability up front
  - ⚠️ But indiscriminate reliance on implicit checks can lose failure atomicity (Item 76)
### When the natural exception is the *wrong* one
- The computation throws an exception that doesn't match the documented one
- Fix: apply the **exception translation idiom** (Item 73)

## Caveat: Don't Over-Restrict
- ❌ Do not infer that arbitrary parameter restrictions are good
- ✅ Design methods to be **as general as practical**
- 💡 Fewer restrictions are better — provided the method does something reasonable with all accepted values
- Note: some restrictions are *intrinsic* to the abstraction being implemented

## Key Takeaways
- 📌 Every time you write a method or constructor, think about what restrictions exist on its parameters
- 🔑 **Document** those restrictions and **enforce** them with explicit checks at the start of the body
- 💡 The modest effort pays back with interest the first time a check catches a bug
- ⚠️ Unchecked parameters threaten failure atomicity — failing fast is cheaper than debugging later
- ✅ Prefer `Objects.requireNonNull` for null checks; assertions for nonpublic methods; generality over needless constraints