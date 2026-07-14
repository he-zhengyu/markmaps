---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# 12: Why Write Comments? The Four Excuses

## Introduction: Why Comments Matter

- Comments help developers **understand a system** and work efficiently
- 🔑 Documentation is essential to **abstraction** — without comments, you can't hide complexity
- 💡 Writing comments, done correctly, **improves a system's design**
- Good design loses much of its value if poorly documented
- Reality: much production code has essentially **no comments**
  - Many developers see comments as a waste of time or drudge work
  - Resulting documentation is often mediocre
  - Inadequate documentation creates a huge, unnecessary drag on development
- The four excuses developers use
  - "Good code is self-documenting"
  - "I don't have time to write comments"
  - "Comments get out of date and become misleading"
  - "The comments I have seen are all worthless; why bother?"
- Three claims of the coming chapters
  - Good comments make a big difference in software quality
  - It isn't hard to write good comments
  - Writing comments can actually be *fun*

## 12.1 Good code is self-documenting

- A "delicious myth" — like a rumor that ice cream is healthy
- Good code reduces the need for comments (e.g., good variable names) but doesn't eliminate it
- Much design information **can't be represented in code**
  - Informal aspects of an interface: high-level description of what a method does, meaning of its result
  - Rationale for a design decision
  - Conditions under which it makes sense to call a method
- ❌ "Just read the method's code" doesn't work
  - Time-consuming and painful to deduce the abstract interface
  - Pushes developers toward many **shallow methods**
  - Readers must still understand all nested methods
  - Impractical for large systems
- Comments are fundamental to **abstractions**
  - 🔑 Abstraction: simplified view preserving essentials, omitting ignorable details
  - If users must read the code to use a method, there is *no abstraction*
  - A declaration alone (name, argument/result types) is missing too much
  - Example: substring(`start`, `end`) — is `end` inclusive? What if `start > end`?
  - Comments capture what callers need while hiding implementation
  - Human language: less precise than code, but more **expressive power**
- 📌 If you want abstractions to hide complexity, comments are essential

## 12.2 I don't have time to write comments

- The temptation: new features always seem higher priority
- ⚠️ If documentation can be de-prioritized, you'll end up with none
- Counter-argument: the **investment mindset**
  - Extra time up front creates structure for long-term efficiency
  - Good comments hugely improve **maintainability**; effort pays for itself quickly
- The cost is small
  - 📊 Typing code is likely under ~10% of development time
  - Matching that for comments is a safe upper bound → ~10% added time
  - Benefits of good documentation quickly offset this cost
- 💡 The most important comments (class/method abstractions) should be written **during design**
  - Writing them serves as a design tool that improves the design
  - These comments pay for themselves immediately

## 12.3 Comments get out of date and become misleading

- True sometimes, but need not be a major problem in practice
- Keeping docs current doesn't require enormous effort
  - Large doc changes only follow large code changes
  - Code changes take more time than the doc changes
- How to keep documentation maintainable (Chapter 16)
  - ✅ Avoid duplicated documentation
  - ✅ Keep documentation close to the corresponding code
- ✅ **Code reviews** detect and fix stale comments

## 12.4 All the comments I have seen are worthless

- Probably the excuse with the **most merit**
- Everyone has seen useless comments; most existing docs are so-so at best
- 💡 The problem is solvable: writing solid documentation isn't hard once you know how
- Coming chapters provide a framework for writing and maintaining good documentation

## 12.5 Benefits of well-written comments

- 🔑 Core idea: capture information in the **designer's mind** that can't be represented in code
  - Low-level: e.g., a hardware quirk motivating tricky code
  - High-level: e.g., the rationale for a class
- Future developers work more quickly and accurately
  - Without docs: rederive or guess original knowledge → wasted time, risk of bugs from misunderstanding
  - Valuable even for the original designer — details are forgotten after a few weeks
- Comments vs. the three manifestations of complexity (Chapter 2)
  - Change amplification — not directly addressed
  - ✅ **Cognitive load**: provides needed information; makes irrelevant info easy to ignore
  - ✅ **Unknown unknowns**: clarifies system structure — what code and info matter for a change
- Against the root causes of complexity
  - Clarifies **dependencies**
  - Fills in gaps to eliminate **obscurity**

## 12.6 A different opinion: comments are failures

- Robert Martin (*Clean Code*): comments are "at best, a necessary evil"
  - Claims comments compensate for failure to express intent in code
- Ousterhout's rebuttal
  - Good design can reduce comments (especially in method bodies), but comments are **not failures**
  - Comment information is different from code's and **can't be represented in code today**
  - Code and comments each suit what they represent; both provide important benefits
- 💡 A purpose of comments: make reading the code **unnecessary**
  - A short interface comment gives everything needed to invoke a method
- ❌ Martin's alternative: replace comments with tiny named methods
  - Produces cryptic long names like `isLeastRelevantMultipleOfNextLargerPrimeFactor`
  - Less information than a well-written comment
  - Developers effectively retype the documentation at every call site
- ⚠️ Cultural danger: developers avoid comments to not seem like failures
  - Good designers may face false criticism: "What's wrong with your code that it requires comments?"
- 📌 Well-written comments increase code's value; fundamental to abstractions and complexity management

## Key Takeaways

- Code alone cannot express all design information — comments complete the **abstraction**
- The four excuses don't hold up: self-documenting code is a myth, cost is ~10%, staleness is manageable, bad comments are fixable
- Comments reduce **cognitive load** and **unknown unknowns**, clarifying dependencies and eliminating obscurity
- Write abstraction comments during design — they double as a **design-improvement tool**
- Contra Martin: comments are not failures; they are essential to managing complexity