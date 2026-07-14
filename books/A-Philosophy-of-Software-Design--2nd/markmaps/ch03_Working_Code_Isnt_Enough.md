---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Working Code Isn't Enough (Strategic vs. Tactical Programming)

## 3.1 Tactical programming

### The tactical mindset
- 🔑 **Tactical programming**: main focus is getting something working (feature/bug fix) ASAP
- Seems reasonable at first — what matters more than working code?
- 💡 But makes producing a good system design nearly impossible

### Why it fails: short-sightedness
- Deadline pressure → planning for the future isn't a priority
- Accept "a bit of complexity" or small kludges to finish faster
- Complexity is **incremental** — accumulation of dozens/hundreds of small compromises
- Each shortcut seems like a reasonable trade-off in isolation

### The downward spiral
- Early shortcuts start causing problems
- Refactoring gets deferred: "next feature is more important"
- Quick patches → more complexity → more patches
- Eventually cleanup would take months; schedule can't tolerate it
- ⚠️ Once on the tactical path, it's difficult to change

### The tactical tornado
- 🔑 Prolific programmer who pumps out code far faster, totally tactically
- Fastest at quick features; management may treat them as heroes
- ❌ Leaves a wake of destruction others must clean up
- 💡 The engineers cleaning up the mess are the *real* heroes, yet appear slower

## 3.2 Strategic programming

### The core realization
- 📌 **Working code isn't enough** — unnecessary complexity to finish faster is unacceptable
- What matters most: the **long-term structure** of the system
- Most code is written by extending the existing code base
- 💡 Primary goal: produce a **great design that also happens to work**

### Investment mindset
- Invest time to improve system design, not the fastest path to done
- Slower short term, faster long term

### Proactive investments
- Try a couple of alternative designs per class; pick the cleanest
- Imagine future changes; ensure the design makes them easy
- Write good documentation

### Reactive investments
- Design mistakes are inevitable and become obvious over time
- ✅ When a design problem surfaces, fix it — don't ignore or patch around it
- Continual small improvements vs. tactical's continual small complexities

## 3.3 How much to invest?

### The right amount
- ❌ Huge up-front design of the whole system = **waterfall**, doesn't work
- Ideal design emerges in bits and pieces with experience
- ✅ Lots of **small, continual investments**
- 📊 Spend ~**10–20%** of total development time on investment

### The payback curve (Figure 3.1)
- Strategic: initial projects take 10–20% longer
- Benefits appear within a few months; soon developing 10–20%+ faster
- 💡 Investments become *free*: past gains fund future investments
- Tactical: 10–20% faster at first, then slows as complexity accumulates
- 📊 Poor code quality slows development by at least 20% (per those who've lived it)
- Note: curve shapes are qualitative — no empirical measurements

### Technical debt
- 🔑 Borrowing time from the future: faster now, slower later
- Payback exceeds the amount borrowed, like financial debt
- ⚠️ Unlike financial debt, mostly never fully repaid — you pay forever

### Crossover point
- No data exists; controlled experiments would be difficult
- Author's opinion: payback in **6–18 months**
- Driver: developer memory — after a few months, complex code slows you badly

## 3.4 Startups and investment

### Startup pressure toward tactics
- Intense pressure for fast early releases; even 10–20% feels unaffordable
- Rationalization: "hire engineers to clean up later if we succeed"
- ⚠️ Once a code base turns to spaghetti, it's nearly impossible to fix
- High development costs for the life of the product
- 💡 Payoff for design comes quickly — tactics may not even speed the first release

### Recruiting consequences
- Engineer quality is a top success factor; great engineers = far higher productivity at similar cost
- Best engineers care deeply about good design
- ❌ Wrecked code base → word gets out → harder recruiting → mediocre engineers → further degradation

### Case study: Facebook (tactical)
- Motto: *"Move fast and break things"*; new grads pushed commits to production in week one
- ✅ Reputation for empowering employees, few rules
- ❌ Unstable, hard-to-understand code; few comments or tests
- Motto later changed to *"Move fast with solid infrastructure"*
- In fairness: probably not much worse than the average startup

### Case study: Google & VMware (strategic)
- Same era as Facebook; emphasized high-quality code and good design
- Built sophisticated, reliable systems for complex problems
- Strong technical cultures → dominated hiring of top talent

### Verdict
- 💡 Companies can succeed with either approach
- But it's a lot more fun to work where design and clean code matter

## 3.5 Conclusion
- Good design isn't free — invest **continually** so small problems don't become big ones
- It pays for itself sooner than you might think
- Invest **today, not tomorrow**
- ⚠️ Slippery slope: deferring cleanup past "the crunch" — there's always another crunch
- The longer you wait, the bigger and more intimidating problems become
- ✅ Best approach: every engineer makes continuous small design investments

## Key Takeaways
- 📌 Working code isn't the goal — a great design that works is
- Tactical programming trades short-term speed for permanent, compounding complexity
- Strategic programming = investment mindset: ~10–20% of time, proactive + reactive
- Technical debt costs more than borrowed and is rarely fully repaid
- Payback arrives fast (est. 6–18 months); startups can't afford *not* to invest
- Consistency matters: continuous small investments by everyone, starting today