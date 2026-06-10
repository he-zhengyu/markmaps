---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# The Nature of Complexity

## 2.1 Complexity defined
- 🔑 **Complexity**: anything about a system's structure that makes it *hard to understand and modify*
- Forms it takes
  - Hard to understand how code works
  - Lots of effort for a small improvement
  - Unclear which parts to modify
  - Hard to fix one bug without creating another
- 💡 Think in terms of **cost vs. benefit**: in a simple system, larger improvements take less effort
- Not the same as size or sophistication
  - A large, feature-rich system *can* be simple if easy to work on
  - A small, unsophisticated system *can* be complex
  - ⚠️ But most large systems do end up complex
- 📌 Determined by the **most common activities**
  - Formula: `C = Σ (cₚ × tₚ)` — complexity of each part weighted by time spent on it
  - 💡 Isolating complexity where it's never seen ≈ eliminating it
- 💡 Complexity is more apparent to **readers than writers**
  - If others find your code complex, it *is* complex
  - 📌 Goal: write code others can work with easily, not just yourself

## 2.2 Symptoms of complexity
### Change amplification
- 🔑 A seemingly simple change requires edits in **many places**
- *Example*: web banner color hardcoded on every page vs. stored in one central value
- 📌 Good design reduces code affected by each design decision

### Cognitive load
- 🔑 How much a developer must **know** to complete a task
- ⚠️ Higher load → more learning time + greater bug risk
- *Example*: C function returns allocated memory; caller must `free` it → leak risk
  - ✅ Better: module that allocates also frees
- Arises from: many-method APIs, global variables, inconsistencies, inter-module dependencies
- 💡 Lines of code ≠ complexity
  - ❌ Fewer lines but cryptic
  - ✅ Sometimes more lines is *simpler* by reducing cognitive load

### Unknown unknowns
- 🔑 Not obvious *which* code to change or *what* you need to know
- *Example*: emphasis color is a darker shade hardcoded on some pages; changing central `bannerBg` silently breaks them
- ⚠️ **The worst** of the three symptoms
  - You can't know what you're missing until bugs appear
  - Change amplification & cognitive load are at least *visible*
  - Only sure fix = read every line (impossible at scale)
- 💡 Antidote: an **obvious** system — developer guesses correctly without thinking hard

## 2.3 Causes of complexity
### Dependencies
- 🔑 Code that **can't be understood or modified in isolation**
- *Examples*
  - Shared background color links all web pages
  - Network protocol: sender & receiver must match
  - Method signature ties implementation to all callers
- 📌 Fundamental & intentional — can't be eliminated, only minimized
- 💡 Goal: make remaining dependencies **simple and obvious**
  - Central `bannerBg` + API replaced a hidden dependency with an obvious one
  - ✅ Compilers help catch API dependency breakage

### Obscurity
- 🔑 Important information is **not obvious**
- *Examples*
  - Generic name like `time`
  - Units not documented
  - Hidden message table for a new error status
  - Inconsistency: one name, two purposes
- Often from inadequate documentation (➡️ Ch. 13)
- 💡 Extensive docs needed = red flag the design is off
- ✅ Best fix: simplify the design

### How they map to symptoms
- Dependencies → change amplification + cognitive load
- Obscurity → unknown unknowns + cognitive load

## 2.4 Complexity is incremental
- 💡 Not one catastrophe — accumulates in **small chunks**
- A single dependency/obscurity barely matters; hundreds build up over time
- ⚠️ Hard to control: "this bit of complexity is no big deal" × every developer = rapid growth
- ⚠️ Hard to remove once accumulated — no single fix moves the needle
- ✅ Adopt a **"zero tolerance"** philosophy (➡️ Ch. 3)

## 2.5 Key Takeaways
- 📌 Complexity = accumulated **dependencies + obscurity**
- It produces three symptoms: change amplification, cognitive load, unknown unknowns
- Result: more code per feature, more time to act safely, sometimes missing info entirely
- 💡 Recognizing complexity is a core design skill — easier to spot than to avoid
- 📌 Bottom line: complexity makes modifying a codebase **difficult and risky**