---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# A Philosophy of Software Design — Summaries

## Summary of Design Principles *(p. 206)*

### Complexity & Mindset
- 📌 **Complexity is incremental** — sweat the small stuff *(p. 11)*
- **Working code isn't enough** — avoid tactical programming *(p. 14)*
- 💡 Make **continual small investments** to improve system design *(p. 15)*

### Modules & Interfaces
- 🔑 **Modules should be deep** — much functionality behind a simple interface *(p. 23)*
- Design interfaces so the **most common usage is as simple as possible** *(p. 27)*
- ✅ Simple **interface** > simple **implementation** *(pp. 61, 74)*
- **General-purpose modules are deeper** *(p. 39)*
- **Separate general-purpose from special-purpose code** *(pp. 45, 68)*

### Layers & Abstractions
- **Different layers, different abstractions** *(p. 51)*
- **Pull complexity downward** — module handles it, not callers *(p. 61)*
- 💡 **Define errors out of existence** *(p. 81)*

### Design Process
- **Design it twice** — consider multiple alternatives *(p. 91)*
- Comments should describe things **not obvious from the code** *(p. 101)*
- 📌 Design for **ease of reading, not ease of writing** *(p. 151)*
- Increments of development should be **abstractions, not features** *(p. 156)*
- **Separate what matters from what doesn't** — emphasize what matters *(p. 171)*

## Summary of Red Flags *(p. 207)*

### Module Structure
- ⚠️ **Shallow Module** — interface not much simpler than implementation *(pp. 25, 110)*
- ⚠️ **Information Leakage** — one design decision reflected in multiple modules *(p. 31)*
- ⚠️ **Temporal Decomposition** — structure follows execution order, not information hiding *(p. 32)*
- ⚠️ **Overexposure** — API forces awareness of rare features to use common ones *(p. 36)*
- ⚠️ **Pass-Through Method** — merely forwards arguments to a similar signature *(p. 52)*

### Code Organization
- ⚠️ **Repetition** — nontrivial code repeated over and over *(p. 68)*
- ⚠️ **Special-General Mixture** — special-purpose code not cleanly separated *(p. 71)*
- ⚠️ **Conjoined Methods** — can't understand one without the other *(p. 75)*

### Comments & Documentation
- ⚠️ **Comment Repeats Code** — comment adds nothing beyond the adjacent code *(p. 104)*
- ⚠️ **Implementation Documentation Contaminates Interface** — interface comment exposes internals *(p. 114)*

### Naming & Clarity
- ⚠️ **Vague Name** — name too imprecise to convey useful information *(p. 123)*
- ⚠️ **Hard to Pick Name** — no precise, intuitive name exists; hints at design problem *(p. 125)*
- ⚠️ **Hard to Describe** — complete documentation must be long *(p. 133)*
- ⚠️ **Nonobvious Code** — behavior or meaning can't be easily understood *(p. 150)*

## Key Takeaways
- 💡 The book's core enemy is **complexity** — it accumulates in small increments, so fight it continuously
- 🔑 **Deep modules** with simple interfaces are the central structural ideal; shallow modules are the central red flag
- ✅ Invest strategically: design twice, pull complexity down, hide information
- ⚠️ Red flags are **symptoms** — each signals a deeper design problem worth revisiting
- 📌 Optimize for the **reader** of code: obviousness, precise names, meaningful comments