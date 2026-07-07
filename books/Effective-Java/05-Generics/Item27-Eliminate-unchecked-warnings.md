---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 27: Eliminate Unchecked Warnings

## Warnings You'll Encounter with Generics
- Unchecked **cast** warnings
- Unchecked **method invocation** warnings
- Unchecked **parameterized vararg type** warnings
- Unchecked **conversion** warnings
- 💡 Experience reduces warnings, but new code rarely compiles cleanly

## Easy Warnings: Fix Them Directly
### Example: Raw Type Declaration
- ❌ `Set<Lark> exaltation = new HashSet();`
- Compiler emits: `[unchecked] unchecked conversion` — *required:* `Set<Lark>`, *found:* `HashSet`
### The Fix: Diamond Operator
- ✅ `Set<Lark> exaltation = new HashSet<>();`
- 🔑 **Diamond operator** `<>` (Java 7+) — compiler infers the actual type parameter
- No need to repeat the type parameter explicitly

## Why Eliminate Every Warning
- Hard warnings require thought — **persevere!**
- ✅ Zero warnings ⇒ code is **typesafe**
- ✅ No `ClassCastException` at runtime
- ✅ Increased confidence the program behaves as intended

## Suppressing Warnings Safely
### When Suppression Is Allowed
- Only if you **can't eliminate** the warning
- AND you can **prove** the code is typesafe
- ⚠️ Suppressing without proof ⇒ false sense of security — runtime `ClassCastException` still possible
- ⚠️ Ignoring known-safe warnings instead of suppressing ⇒ real new warnings get lost in the noise
### Smallest Possible Scope
- `@SuppressWarnings("unchecked")` usable on any **declaration** — local variable up to entire class
- 📌 Always annotate the **smallest scope**: variable declaration or very short method/constructor
- ❌ **Never** on an entire class — masks critical warnings
- 💡 Method/constructor longer than one line ⇒ move annotation onto a new local variable declaration
### Example: `ArrayList.toArray`
- Warning: unchecked cast — *required:* `T[]`, *found:* `Object[]`
- ❌ Annotation on `return` statement is **illegal** — not a declaration [JLS, 9.7]
- ❌ Don't annotate the whole method
- ✅ Declare a local variable to hold the return value; annotate its declaration
- ```java
  @SuppressWarnings("unchecked") T[] result =
      (T[]) Arrays.copyOf(elements, size, a.getClass());
  return result;
  ```
- Result: compiles cleanly, suppression scope minimized
### Always Comment the Suppression
- 📌 Every `@SuppressWarnings("unchecked")` needs a comment explaining **why it's safe**
- Helps others understand the code
- Reduces odds someone modifies it into unsafe computation
- 💡 If the comment is hard to write, keep thinking — the operation may not be safe after all

## Key Takeaways
- Unchecked warnings matter — **don't ignore them**
- Every warning = potential runtime `ClassCastException`
- Eliminate every warning you can
- If unavoidable and provably typesafe: suppress with `@SuppressWarnings("unchecked")` in the **narrowest scope**
- Record the rationale for suppression in a comment