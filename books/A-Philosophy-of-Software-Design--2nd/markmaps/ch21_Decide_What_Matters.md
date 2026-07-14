---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Ch. 21: Decide What Matters

## Core Principle
- 🔑 Good design = **separating what matters from what doesn't**
- Structure the system around things that **matter**
- Things that matter → **emphasized**, made obvious
- Things that don't → **hidden**, impact minimized
- Underlies many earlier ideas
  - **Abstractions**: interface = what matters to users; implementation hides the rest
  - **Variable names**: pick words conveying the most information
  - **Performance** (Sec 20.4): structure design around the critical path — few method calls & special-case checks, yet clean and obvious

## 21.1 How to decide what matters?
- Sources of importance
  - Sometimes imposed as **external constraints** (e.g., performance)
  - More often the **designer** must determine it
  - Even with constraints, designer decides what matters *most* to meet them
- 💡 Look for **leverage**
  - One solution solves **many problems**, or one fact explains many things
  - Example: text storage (Sec 6.2)
    - General-purpose insert/delete of character ranges → solves many problems ✅
    - Specialized `backspace` method → solves only one ❌
    - At the text-class level, *why* text is deleted doesn't matter — only that it is
  - Example: **invariants**
    - Knowing one invariant predicts behavior in many situations
- Compare **multiple options**
  - Easier to judge importance with alternatives in hand
  - Naming: list related words, keep the most informative few
  - An instance of the **"design it twice"** principle
- When it's not obvious (esp. for junior developers)
  - Make a **hypothesis**: "I think *this* matters most"
  - Commit, build under that assumption, observe the outcome
  - Right → ask *why*; note clues for the future
  - Wrong → still OK; find the clues you missed
  - 💡 Either way you learn and gradually choose better

## 21.2 Minimize what matters
- 📌 Make as **little** matter as possible → simpler systems
- Reduce **how much** matters
  - Fewer required constructor parameters
  - **Default values** reflecting common usage
- Reduce **where** it matters
  - Information hidden in a module doesn't matter outside it
  - Exception handled entirely at a low level → invisible to the rest
  - Config parameter computed automatically → no longer matters to administrators

## 21.3 How to emphasize things that matter
- Three ways to emphasize
  - **Prominence**: appear where likely to be seen — interface docs, names, parameters of heavily used methods
  - **Repetition**: key ideas appear over and over
  - **Centrality**: at the heart of the system, shaping structure around them
    - Example: OS **device driver interface** — hundreds of drivers depend on it
- 💡 The converse holds: visible / repeated / structure-shaping ideas *are* the ones that matter
- De-emphasize what doesn't matter
  - Hide as much as possible
  - Encountered infrequently
  - No impact on system structure

## 21.4 Mistakes
- ❌ Mistake 1: treating **too many** things as important
  - Unimportant things clutter the design → complexity, cognitive load
  - Example: method arguments irrelevant to most callers
  - Example: **Java I/O** — forces buffered vs. unbuffered choice, though buffering is almost always wanted
  - ⚠️ Often produces **shallow classes**
- ❌ Mistake 2: **failing to recognize** something important
  - Important information ends up hidden
  - Missing functionality → developers continually recreate it
  - ⚠️ Impedes productivity; leads to **unknown unknowns**

## 21.5 Thinking more broadly
- **Technical writing**
  - Identify a few key concepts up front; structure the document around them
  - Tie details back to the overall concepts
- **Life philosophy**
  - Identify the few things that matter most to you
  - Spend your energy there; don't fritter time on the unrewarding
- 🔑 **Good taste** = the ability to distinguish important from unimportant
  - An essential trait of a good software designer

## Key Takeaways
- Design revolves around separating the important from the unimportant
- Find importance via **leverage**, comparing options, and testing hypotheses
- Minimize both *how much* matters and *where* it matters
- Emphasize via prominence, repetition, centrality; hide the rest
- Avoid both over-importance (clutter) and under-recognition (unknown unknowns)
- **Good taste** in judging importance defines a good designer