---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Ch. 3 — Working Code Isn't Enough (Strategic vs. Tactical Programming)

## 3.1 Tactical programming
- 🔑 **Tactical programming**: main focus is just getting something working (feature/bug fix)
- Seems reasonable, but makes good system design nearly impossible
- Core flaw: **short-sighted**
  - Finish task as fast as possible (e.g. hard deadline)
  - Planning for the future isn't a priority
  - Accept "a bit of complexity" or small kludges to ship faster
- How systems become complicated
  - 💡 Complexity is **incremental** — accumulation of dozens/hundreds of small things
  - Each shortcut seems like a reasonable compromise
  - Complexities accumulate rapidly, especially when *everyone* programs tactically
- The downward spiral
  - Early shortcuts start causing problems
  - "Next feature matters more than refactoring" → quick patches instead
  - Patches create more complexity → more patches
  - Eventually cleanup would take months; schedule can't tolerate it
  - ⚠️ Once on the tactical path, it's difficult to change
- 🔑 The **tactical tornado**
  - Prolific programmer, pumps out code fastest, totally tactical
  - Management may treat them as heroes
  - ❌ Leaves a wake of destruction in the code
  - Other engineers (the *real* heroes) clean up the mess — and look slower for it

## 3.2 Strategic programming
- 📌 First step to good design: realize **working code isn't enough**
  - Unacceptable to add unnecessary complexity to finish faster
  - What matters most: **long-term structure of the system**
- 💡 Most code is written by extending the existing code base
  - Your most important job: **facilitate future extensions**
  - Primary goal: a great design *that also happens to work*
- 🔑 **Strategic programming** = an **investment mindset**
  - Invest time to improve system design
  - Slows you down a bit short-term, speeds you up long-term (Figure 3.1)
- **Proactive investments**
  - Take extra time to find a *simple* design for each new class
  - Try a couple of alternative designs; pick the cleanest
  - Imagine future changes; make sure design handles them easily
  - Write good documentation
- **Reactive investments**
  - Design mistakes are inevitable and become obvious over time
  - ✅ When you find a design problem, fix it — don't ignore or patch around it
  - Continual small improvements ↔ opposite of tactical's continual small complexities

## 3.3 How much to invest?
- ❌ Huge up-front investment (design entire system) doesn't work — that's **waterfall**
  - Ideal design emerges in bits and pieces, with experience
- ✅ Best approach: **lots of small investments, continually**
  - 📊 Suggested: **10–20% of total development time**
  - Small enough not to hurt schedules; large enough for significant benefit
- Strategic trajectory
  - Initial projects take 10–20% longer
  - Benefits start within a few months; soon developing 10–20% *faster*
  - 💡 Investments become **free**: past gains cover future investment costs
- Tactical trajectory
  - First projects 10–20% faster
  - Speed decays as complexity accumulates → soon 10–20% slower
  - Savings given back quickly; slower for the rest of the system's lifetime
  - 📊 Badly degraded code bases slow development by at least 20%
- 🔑 **Technical debt**
  - Borrowing time from the future: faster now, slower later
  - Payback exceeds what was borrowed
  - ⚠️ Unlike financial debt, mostly never fully repaid — you pay forever
- Crossover point (when strategy pays for itself)
  - No empirical data; hard to test with controlled experiments
  - Author's opinion: **6–18 months** to payback
  - Driven by developer memory: after a few months, authors forget code details
  - Complex code then slows development significantly, erasing tactical gains
- Figure 3.1: qualitative only — ⚠️ no empirical measurements of the curve shapes

## 3.4 Startups and investment
- Pressure against strategy
  - Early-stage startups feel pressure to ship early releases quickly
  - Even 10–20% investment may seem unaffordable
  - Rationalization: "if successful, we'll hire engineers to clean up later"
- Why the rationalization fails
  - ⚠️ Once a code base turns to **spaghetti**, it's nearly impossible to fix
  - High development costs for the life of the product
  - 💡 Design payoff comes quickly — tactical may not even speed the *first* release
- Hiring effect
  - Engineer quality is a top success factor
  - Great engineers ≈ similar cost, **tremendously higher productivity**
  - Best engineers care deeply about good design
  - ❌ Wrecked code base → word gets out → harder recruiting → mediocre engineers → further degradation
- Case study: **Facebook** (tactical)
  - Motto: *"Move fast and break things"*
  - New grads pushed commits to production in their first week
  - ✅ Reputation for empowering employees; few rules/restrictions
  - ❌ Code unstable, hard to understand, few comments/tests, painful to work with
  - Motto changed to *"Move fast with solid infrastructure"*
  - In fairness: probably not much worse than average startup — just highly visible
- Case studies: **Google** and **VMware** (strategic)
  - Same era as Facebook; emphasized high-quality code and good design
  - Built sophisticated, reliable systems for complex problems
  - Strong technical cultures → won the competition for top talent
- 💡 Companies can succeed either way — but it's more fun where design is valued

## 3.5 Conclusion
- Good design isn't free: invest **continually** so small problems don't become big ones
- Good design eventually pays for itself — sooner than you might think
- ⚠️ The crunch trap (slippery slope)
  - Tempting to defer cleanups until "after the crunch"
  - There's always another crunch, and another
  - Delays become permanent; culture slips into tactical mode
  - The longer you wait, the bigger and more intimidating problems become
- ✅ Most effective: **every engineer** makes continuous small design investments

## Key Takeaways
- 📌 Working code isn't enough — the goal is a great design that also works
- Tactical programming is short-sighted; incremental complexity quietly destroys systems
- Strategic programming = investment mindset, both proactive and reactive
- Invest ~10–20% of dev time; payback in roughly 6–18 months, then investments are free
- Technical debt costs more than it borrowed and is rarely fully repaid
- Tactical culture damages hiring; strategic culture attracts top engineers (Google/VMware vs. early Facebook)
- Invest today, not tomorrow — consistency prevents permanent slide into tactics