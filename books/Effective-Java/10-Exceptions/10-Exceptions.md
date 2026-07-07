---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Effective Java Ch.10: Exceptions

## Item 69: Use Exceptions Only for Exceptional Conditions

### The Anti-Pattern
- ❌ Exception-based array loop: `catch (ArrayIndexOutOfBoundsException)` to terminate
- Misguided premise: VM bounds check makes explicit loop test "redundant"
- ✅ Standard idiom: `for (Mountain m : range) m.climb();`

### Three Flaws in the Performance Reasoning
- Exceptions designed for exceptional cases → JVMs don't optimize them for speed
- `try-catch` blocks **inhibit JVM optimizations**
- Standard loop checks often optimized away by JVMs anyway
- 📊 Exception idiom ~2x slower on 100-element arrays

### Why It's Worse Than Slow
- Obfuscates the code's purpose
- ⚠️ **Masks real bugs**: unrelated out-of-bounds errors misread as loop termination
- Proper idiom fails fast with full stack trace; abused idiom fails silently

### Implication for API Design
- 📌 A well-designed API must not force clients to use exceptions for control flow
- **State-dependent method** should pair with a **state-testing method**
  - Example: `Iterator.next()` paired with `hasNext()`
- Alternative: return **empty Optional** (Item 55) or distinguished value (e.g. `null`)

### Choosing: State-Testing vs. Optional/Distinguished Value
- Concurrent access without sync / external state transitions → **must use optional/distinguished value**
  - ⚠️ State may change between test call and dependent call
- State-testing method duplicates the work → performance favors optional/distinguished value
- All else equal → ✅ state-testing method mildly preferable
  - Better readability
  - Forgotten test → exception makes bug obvious; forgotten value check → subtle bug

## Item 70: Checked for Recoverable, Runtime for Programming Errors

### Three Kinds of Throwables
- 🔑 **Checked exceptions** — caller can reasonably be expected to **recover**
  - Forces caller to catch or propagate
  - Signals the condition is a possible outcome of invocation
- 🔑 **Runtime exceptions** — indicate **programming errors**
  - Majority indicate **precondition violations** (client breaks API contract)
  - Example: `ArrayIndexOutOfBoundsException` for out-of-range index
- 🔑 **Errors** — reserved (by convention) for JVM: resource deficiencies, invariant failures
  - Unchecked throwables behave identically: shouldn't be caught; recovery impossible

### Gray Areas
- Resource exhaustion: programming error or genuine shortage?
- Judgment call by API designer on recoverability
- 💡 When in doubt whether recovery is possible → throw **unchecked** (see Item 71)

### Rules for Custom Throwables
- ❌ Don't implement new `Error` subclasses
- ❌ Don't throw `Error` (except `AssertionError`)
- All your unchecked throwables should subclass `RuntimeException`
- ❌ Never define throwables outside `Exception`/`RuntimeException`/`Error` — no benefit, only confusion

### Exceptions Are Full-Fledged Objects
- Provide methods giving extra information about the failure condition
- ⚠️ Parsing an exception's string representation is fragile and nonportable
- 📌 Especially important on checked exceptions to aid recovery
  - Example: gift-card purchase failure → accessor for the shortfall amount

## Item 71: Avoid Unnecessary Checked Exceptions

### The Burden of Checked Exceptions
- Caller must catch or declare-and-propagate
- ⚠️ Java 8+: methods throwing checked exceptions can't be used directly in **streams**
- Burden much higher when it's the method's **sole** checked exception

### Litmus Test for Justification
- Justified only if **both** hold:
  - Condition can't be prevented by proper API use
  - Programmer can take **useful action** when confronted
- If best handling is `throw new AssertionError()` or `printStackTrace(); exit(1)` → use unchecked

### Ways to Eliminate a Checked Exception
- ✅ Return an **Optional** of the result type (Item 55)
  - ❌ Downside: can't convey additional failure detail like an exception's type/methods
- ✅ Split into two methods: boolean **state-testing** + unchecked-throwing action
  - `if (obj.actionPermitted(args)) obj.action(args); else ...`
  - Enables trivial call `obj.action(args)` when success is expected
  - ⚠️ Inappropriate under unsynchronized concurrent access or external state transitions
  - ⚠️ May be ruled out if `actionPermitted` duplicates `action`'s work

### Decision Order
- Callers can't recover → unchecked exception
- Recovery possible & want to force handling → first consider **Optional**
- Only if Optional gives insufficient failure info → checked exception

## Item 72: Favor Standard Exceptions

### Benefits of Reuse
- API easier to learn/use — matches established conventions
- Client code easier to read — no unfamiliar exceptions
- Smaller memory footprint, less class loading

### The Standard Repertoire
- `IllegalArgumentException` — non-null parameter value inappropriate (e.g. negative repeat count)
- `IllegalStateException` — object state wrong for invocation (e.g. not yet initialized)
- `NullPointerException` — null parameter where prohibited (not IAE)
- `IndexOutOfBoundsException` — out-of-range index parameter (not IAE)
- `ConcurrentModificationException` — detected concurrent modification where prohibited
  - ⚠️ At best a hint — reliable detection impossible
- `UnsupportedOperationException` — object doesn't support the operation
  - Rare; used for unimplemented optional interface operations (e.g. append-only List)

### Rules of Reuse
- ❌ Never reuse `Exception`, `RuntimeException`, `Throwable`, `Error` directly — treat as abstract
- 📌 Reuse must match **documented semantics**, not just the name
- Other reuse OK where fitting: `ArithmeticException`, `NumberFormatException` for arithmetic objects
- Subclassing to add detail is fine, but ⚠️ exceptions are serializable — good reason not to write your own

### Tie-Breaker: IAE vs. ISE
- 💡 If **no** argument value would have worked → `IllegalStateException`
- Otherwise → `IllegalArgumentException`
- Example: dealing a hand larger than cards remaining in deck

## Item 73: Throw Exceptions Appropriate to the Abstraction

### The Problem
- Propagating lower-level exceptions is disconcerting
- ⚠️ Pollutes higher-layer API with implementation details
- Later implementation changes alter thrown exceptions → breaks clients

### Exception Translation
- 🔑 Catch lower-level exception, throw one explainable at the higher abstraction
- Example: `AbstractSequentialList.get` translates `NoSuchElementException` → `IndexOutOfBoundsException`

### Exception Chaining
- 🔑 Pass lower-level **cause** into higher-level exception; retrieve via `getCause`
- Use when the cause helps debugging
- Chaining-aware constructors, e.g. `super(cause)` → `Throwable(Throwable)`
- No chaining constructor? Use `initCause`
- 💡 Integrates cause's stack trace into higher-level exception's trace

### Don't Overuse Translation
- ✅ Best: **avoid** lower-level exceptions — validate parameters before passing down
- Next best: higher layer silently works around them, insulating callers
  - Log via `java.util.logging` for later investigation
- Translate only when prevention/handling isn't feasible; chaining gives best of both worlds

## Item 74: Document All Exceptions Thrown

### Checked Exceptions
- Declare each **individually**; document exact throw conditions with `@throws`
- ❌ Don't declare superclasses like `throws Exception` / `throws Throwable`
  - Denies guidance; obscures other exceptions in same context
  - Sole exception: `main` may declare `throws Exception` (called only by VM)

### Unchecked Exceptions
- Document as carefully as checked ones, even though not required
- 💡 A documented list of unchecked exceptions = the method's **preconditions**
- Especially important in **interfaces** — part of the general contract across implementations
- 📌 Use `@throws` tag but **no** `throws` keyword for unchecked
  - The tag-without-clause is a visual cue that the exception is unchecked

### Practical Caveats
- Complete unchecked documentation is an ideal, not always achievable
- Adding new unchecked exceptions later doesn't break source/binary compatibility
  - Dependencies may propagate new undocumented exceptions
- Same exception thrown by many methods for same reason → document once at **class level**
  - Common example: `NullPointerException` for any null parameter

## Item 75: Include Failure-Capture Info in Detail Messages

### Why It Matters
- Stack trace (`toString`: class name + detail message) is often the **only** evidence
- Irreproducible failures may permit no further data collection

### What to Include
- 📌 Values of **all parameters and fields** contributing to the exception
- Example: `IndexOutOfBoundsException` should show lower bound, upper bound, and index
  - Each combination points to different bugs: fencepost error, wild value, invariant failure
- ⚠️ Security: never include passwords, encryption keys, etc. — traces are widely seen
- Lengthy prose superfluous — trace already pairs with docs/source and line numbers

### Detail Message ≠ User-Level Error Message
- Detail message: for programmers/SREs; information content > readability; rarely localized
- User message: must be intelligible to end users; often localized

### Constructor Idiom
- 💡 Require failure data in constructors instead of a String; auto-generate the message
  - e.g. `IndexOutOfBoundsException(int lowerBound, int upperBound, int index)`
- Centralizes high-quality message generation; makes it hard *not* to capture failure
- 📊 Java 9 added an `int index` constructor — but omits bounds
- Provide **accessor methods** for the captured data
  - More important on checked exceptions (aids recovery), advisable on all

## Item 76: Strive for Failure Atomicity

### The Principle
- 🔑 **Failure-atomic**: a failed invocation leaves the object in its pre-invocation state
- Especially important for checked exceptions, where recovery is expected

### Four Ways to Achieve It
- ✅ **Immutable objects** (Item 17) — failure atomicity is free
- ✅ **Check parameters first** (Item 49) — throw before modification begins
  - Example: `Stack.pop` size check; removing it leaves negative `size` and wrong exception type
- ✅ **Order the computation** — failure-prone parts before mutating parts
  - Example: `TreeMap.add` throws `ClassCastException` during search, before modification
- ✅ **Operate on a temporary copy**, swap in on success
  - Example: sorts copying list to array — performance win plus untouched input on failure
- Rare 4th option: **recovery code** rolling back state — mainly durable/disk-based structures

### Limits
- ⚠️ Not always achievable: unsynchronized concurrent modification leaves inconsistent state
  - Don't assume object usable after `ConcurrentModificationException`
- Errors unrecoverable → no need to preserve atomicity for `AssertionError`
- Not always desirable — may raise cost/complexity significantly
- 📌 If violated, API docs must state what state the object is left in

## Item 77: Don't Ignore Exceptions

### The Sin
- ❌ Empty `catch` block defeats exceptions' purpose
- 💡 Analogy: ignoring a fire alarm — and switching it off for everyone else
- ⚠️ Program continues silently, then fails later at an unrelated point

### When Ignoring Is Legitimate
- Example: closing a `FileInputStream` — no state changed, data already read
- Consider logging so recurring exceptions can be investigated
- 📌 Requirements when ignoring:
  - Comment in the catch block explaining why
  - Name the variable `ignored`
- Example: `TimeoutException | ExecutionException ignored` when a default value suffices

### Applies Universally
- Same rule for checked and unchecked exceptions
- Proper handling can avert failure; even mere propagation fails fast with debug info

## Key Takeaways
- Exceptions are for exceptional conditions — never ordinary control flow, in code or API design
- Checked = recoverable, runtime = programming error; when in doubt, unchecked
- Prefer Optionals or state-testing methods before imposing checked exceptions
- Reuse standard exceptions by documented semantics; never reuse base throwables directly
- Translate (and chain) lower-level exceptions to match your abstraction
- Document every exception with `@throws`; failure-capture data in detail messages
- Failed methods should leave objects unchanged; never ignore exceptions silently