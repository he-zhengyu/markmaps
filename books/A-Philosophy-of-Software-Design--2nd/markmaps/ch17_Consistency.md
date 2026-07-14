---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Chapter 17: Consistency

- 🔑 **Consistency**: similar things done in similar ways, dissimilar things done in different ways
- 💡 Creates **cognitive leverage**: learn once, apply everywhere
- Reduces mistakes
  - Inconsistent system → familiar-looking patterns may mislead
  - Consistent system → assumptions from familiar patterns are safe
- Result: developers work faster with fewer errors

## 17.1 Examples of consistency

### Names
- Consistent naming (see Chapter 14)

### Coding style
- Style guides restrict structure beyond compiler rules
- Cover: indentation, brace placement, declaration order, naming, commenting, dangerous features
- ✅ Easier to read, fewer errors

### Interfaces
- Interface with **multiple implementations**
- Understand one implementation → others become easier

### Design patterns
- 🔑 Generally-accepted solutions to common problems
- Example: **model-view-controller** for UI design
- ✅ Faster implementation, more likely to work, more obvious code
- Detailed in Section 19.5

### Invariants
- 🔑 A property of a variable/structure that is **always true**
- Example: every text line terminated by a newline
- ✅ Fewer special cases; easier to reason about behavior

## 17.2 Ensuring consistency

- ⚠️ Hard to maintain with many people over long time
  - Groups unaware of each other's conventions
  - Newcomers violate rules, create conflicting conventions

### Document
- List key conventions (e.g., style guidelines)
- Place where developers will see it (e.g., project Wiki)
- New members read it; existing members review periodically
- Consider starting from published style guides on the Web
- Localized conventions (e.g., invariants): document in the code
- 📌 Unwritten conventions won't be followed

### Enforce
- 💡 Best enforcement: a **tool that checks violations**, blocking commits that fail
- Works especially well for low-level syntactic conventions
- Case study: line termination characters
  - Unix uses newline; Windows uses carriage-return + newline
  - Editors rewrote terminators → every line appeared modified
  - ⚠️ Convention alone failed; every new developer caused problems
  - Fix: **pre-commit script** aborting commits with carriage returns
  - Script also repairs damaged files
  - ✅ Instantly eliminated problems and trained new developers
- **Code reviews** enforce conventions and educate newcomers
  - Nit-picky reviewers → faster learning, cleaner code

### When in Rome...
- 📌 Most important convention: *do as the Romans do*
- In a new file, observe existing structure
  - Public before private declarations?
  - Methods alphabetical?
  - `firstServerName` (camel case) vs `first_server_name` (snake case)?
- Anything that looks like a convention: follow it
- For design decisions, find similar existing examples and mimic them

### Don't change existing conventions
- ⚠️ A "better idea" is not sufficient excuse for inconsistency
- 💡 Value of consistency almost always exceeds value of one approach over another
- Two questions before breaking a convention
  - Significant **new information** unavailable when convention was set?
  - New approach worth **updating all old uses**?
- If both "yes": upgrade fully, leaving no trace of old convention
- ⚠️ Others may still reintroduce the old approach later
- 📌 Reconsidering established conventions is rarely a good use of time

## 17.3 Taking it too far

- Consistency also means **dissimilar things done differently**
- ⚠️ Forcing dissimilar things into one approach creates complexity
  - Same variable name for genuinely different things
  - Design pattern applied to a task that doesn't fit
- 💡 Benefit requires confidence: *"if it looks like an x, it really is an x"*

## 17.4 Conclusion

- Consistency exemplifies the **investment mindset**
- Upfront costs
  - Deciding conventions
  - Building automated checkers
  - Finding similar situations to mimic
  - Educating the team via code reviews
- Return: more **obvious** code

## Key Takeaways

- Similar things alike; dissimilar things differently — both halves matter
- Consistency gives cognitive leverage: faster work, fewer bugs
- Document conventions, then **enforce with tools** and code reviews
- Follow existing conventions ("When in Rome"); resist "improving" them
- ⚠️ Over-applied consistency creates confusion, not clarity
- An investment now for more obvious code later