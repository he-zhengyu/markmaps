---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Chapter 11: Design it Twice

## Core Principle
- 🔑 **Design it twice**: consider multiple options for each major design decision
- 💡 Software design is hard — first thoughts rarely produce the best design
- Comparing alternatives leads to a much better result

## Example: Text Class for a GUI Editor

### Step 1: Sketch Alternative Interfaces
- **Line-oriented**: insert, modify, delete whole lines
- **Character-oriented**: individual character insertions/deletions
- **String-oriented (range)**: arbitrary character ranges crossing line boundaries
- No need to pin down every feature — sketch the most important methods
- 📌 Pick approaches **radically different** from each other — you learn more
- Even if certain only one approach is reasonable, consider a second anyway
  - Contrasting a bad design's weaknesses is instructive

### Step 2: List Pros and Cons
- 📌 Most important criterion: **ease of use for higher-level software**
  - ❌ Line-oriented: callers must split/join lines for partial-line & multi-line ops (e.g., cut/paste)
  - ❌ Character-oriented: callers need loops for multi-character operations
- Other factors to weigh
  - Does one alternative have a **simpler interface**?
  - Is one interface more **general-purpose**?
  - Does one enable a more **efficient implementation**?
    - ❌ Character-oriented likely much slower: one call per character

### Step 3: Identify the Best Design
- May be one of the alternatives
- Or **combine features** of multiple alternatives into a better new design
- If none is attractive: devise **additional schemes**
  - Use problems in original alternatives to drive new designs
  - ⚠️ Red flag: text class forcing callers to do extra text manipulation
  - 💡 Interface should match operations of higher-level software
  - This reasoning leads to the **range-oriented API**, eliminating earlier problems

## Applying at Many Levels
- **Module interface**: pick the interface first (as above)
- **Module implementation**: apply again after the interface
  - Text class candidates: linked list of lines, fixed-size character blocks, **gap buffer**
  - 📌 Implementation goals differ: **simplicity and performance** matter most
- **Higher system levels**
  - Choosing features for a user interface
  - Decomposing a system into major modules
- 💡 In each case, comparing a few alternatives makes the best approach easier to spot

## Cost vs. Benefit
- Doesn't take much extra time
  - Small module (class): an hour or two vs. days/weeks of implementation
  - Better design **more than pays for** the time invested
- Larger modules: more design-exploration time, but longer implementation and higher benefit too

## Why Smart People Resist It
- Growing up, first quick ideas earned good grades → **bad work habits**
- Promotions bring harder problems; eventually first ideas aren't good enough
- 📌 Large software systems: no one gets it right on the first try
- Insisting on the first idea → underperforming true potential, frustrating to work with
- Subconscious belief: "smart people get it right the first time" — ❌ false
- 💡 It isn't that you aren't smart; the problems are **really hard**
  - And that's good: hard problems requiring careful thought are more fun

## Improves Your Design Skills
- Devising and comparing approaches teaches what makes designs better or worse
- Over time: easier to rule out bad designs and hone in on great ones

## Key Takeaways
- 📌 Always sketch **≥2 radically different designs** before committing
- 📌 Compare pros/cons; ease of use for callers is the top interface criterion
- 💡 Best design may combine alternatives or emerge from their identified problems
- 📌 Apply at every level: interface, implementation, UI features, system decomposition
- 💡 Small time cost, large payoff — and it trains your design judgment
- Needing multiple attempts isn't a lack of smarts; the problems are genuinely hard