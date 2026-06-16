---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 13: Override `clone` Judiciously

## The `Cloneable` Interface
- 🔑 Intended as a **mixin interface** (Item 20) to advertise that a class permits cloning
- 💡 Atypical interface: contains **no methods**
  - Instead, modifies behavior of `Object`'s protected `clone`
  - If class implements `Cloneable` → `clone` returns field-by-field copy
  - Otherwise → throws `CloneNotSupportedException`
- ⚠️ Primary flaw: lacks a `clone` method; `Object.clone` is **protected**
  - Can't invoke `clone` just because a class implements `Cloneable`
  - Requires reflection (Item 65), which may still fail
- ⚠️ Implementing it modifies a superclass's protected method — not to be emulated
- 📌 Despite flaws, in **wide use** — worth understanding

## The General Contract for `clone`
- 💡 The contract is **weak** and not absolutely binding
- Expectations for any object `x`:
  - `x.clone() != x` → typically **true**
  - `x.clone().getClass() == x.getClass()` → typically **true**
  - `x.clone().equals(x)` → typically true, *not required*
- 📌 By convention, returned object should come from calling `super.clone`
  - Guarantees correct class if all superclasses (except `Object`) obey it
- 📌 Returned object should be **independent** of the original
- ⚠️ Vaguely like constructor chaining, but **not enforced**
  - If `clone` uses a constructor instead of `super.clone`, a subclass's `super.clone` yields the wrong class
- 🔑 `clone` effectively functions as a **constructor** that creates objects *without calling a constructor* — fragile, dangerous, extralinguistic

## Implementing `clone`
### Immutable / Primitive-Only Fields
- 💡 Simplest case: call `super.clone`, no further processing needed
- Example: `PhoneNumber` (Item 11)
  - ⚠️ Immutable classes should **never** provide `clone` — encourages wasteful copying
- ✅ Use **covariant return types**: override returns the class itself, not `Object`
  - Eliminates client casts
- `super.clone` wrapped in `try-catch` for `CloneNotSupportedException`
  - 💡 Boilerplate shows the exception should have been **unchecked** (Item 71)
- ```java
  @Override public PhoneNumber clone() {
      try {
          return (PhoneNumber) super.clone();
      } catch (CloneNotSupportedException e) {
          throw new AssertionError(); // Can't happen
      }
  }
  ```

### Mutable State — Recursive `clone`
- ⚠️ Naïve `super.clone()` makes the copy **share** mutable fields (e.g. `Stack.elements` array)
  - Modifying one corrupts the other → nonsense results or `NullPointerException`
- ✅ Copy internals: call `clone` recursively on the array
- ```java
  @Override public Stack clone() {
      try {
          Stack result = (Stack) super.clone();
          result.elements = elements.clone();
          return result;
      } catch (CloneNotSupportedException e) {
          throw new AssertionError();
      }
  }
  ```
  - 💡 No cast needed: array `clone` returns the same type
  - 📌 Arrays are the **sole compelling use** of the `clone` facility
- ⚠️ Fails if the field is `final` — `clone` can't reassign it
  - 🔑 `Cloneable` is incompatible with `final` fields referring to mutable objects
  - May force removing `final` modifiers

### Complex Mutable State — Deep Copy
- ⚠️ Recursive `clone` alone is insufficient (e.g. `HashTable` of bucket linked lists)
  - Cloning only the bucket array still **shares the linked lists**
- ✅ Add a `deepCopy` method to copy each bucket's linked list
- ⚠️ Recursive `deepCopy` consumes one stack frame per element → **stack overflow** on long lists
  - ✅ Replace recursion with **iteration**
- ```java
  Entry deepCopy() {
      Entry result = new Entry(key, value, next);
      for (Entry p = result; p.next != null; p = p.next)
          p.next = new Entry(p.next.key, p.next.value, p.next.next);
      return result;
  }
  ```
- Alternative: call `super.clone`, reset fields to initial state, regenerate via high-level methods (e.g. `put`)
  - ✅ Simple, reasonably elegant
  - ❌ Slower; antithetical to the field-by-field `Cloneable` architecture

## Rules & Pitfalls
- ⚠️ Like a constructor, `clone` must **never invoke an overridable method** (Item 19)
  - Subclass override would run before its state is fixed → corruption
  - Helper methods like `put` should be `final` or `private`
- ✅ Public `clone` methods should **omit the `throws` clause** (Item 71)
- ⚠️ Some fields always need fixing even if primitive/immutable — e.g. a **serial number / unique ID**
- 🔑 Thread-safe class implementing `Cloneable` must provide a **synchronized** `clone` (Item 78)
  - `Object.clone` is not synchronized

## Designing Classes for Inheritance
- 📌 A class designed for inheritance should **not** implement `Cloneable`
- Two acceptable options:
  - ✅ Mimic `Object`: provide a protected `clone` declared to throw `CloneNotSupportedException`
    - Lets subclasses choose to implement `Cloneable` or not
  - ✅ Prevent cloning with a degenerate implementation
- ```java
  @Override
  protected final Object clone() throws CloneNotSupportedException {
      throw new CloneNotSupportedException();
  }
  ```

## Better Alternative: Copy Constructors & Factories
- 🔑 **Copy constructor**: takes a single argument of its own type
  - `public Yum(Yum yum) { ... }`
- 🔑 **Copy factory**: static-factory analogue (Item 1)
  - `public static Yum newInstance(Yum yum) { ... }`
- ✅ Advantages over `Cloneable`/`clone`:
  - No risk-prone extralinguistic object creation
  - No unenforceable, thinly documented conventions
  - No conflict with `final` fields
  - No unnecessary checked exceptions
  - No casts required
- 💡 Can take an **interface** argument → *conversion constructors / factories*
  - Client chooses the copy's implementation type
  - Example: copy a `HashSet` as a `TreeSet` via `new TreeSet<>(s)`

## Key Takeaways
- 📌 `Cloneable` is **deeply flawed**: understand it, but avoid it
- 📌 New interfaces should **not extend** `Cloneable`; new extendable classes should **not implement** it
- ✅ As a rule, provide copy functionality via **copy constructors or factories**
- ⚠️ If you extend a class that already implements `Cloneable`, you must write a well-behaved `clone`
  - First call `super.clone`, then fix fields holding mutable "deep structure"
- ✅ Final classes may implement `Cloneable` only as a justified **performance optimization** (Item 67)
- 📌 Notable exception: **arrays** are best copied with `clone`