---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Reasoning with AI

## What is AI Reasoning
- 🔑 **Reasoning engine** — AI thinks rigorously & at length given the right context
- Enables tackling **complex, multi-step tasks**
- Goes beyond simple Q&A → produces analyzed, synthesized output
- 💡 Shift in usage: from *answer machine* to *thinking partner*

## Motivating Example: Car Shopping
- **Inputs provided**
  - Spec sheets for multiple cars
  - Insurance plans
  - Car loan quotes
- **Prompt pattern**
  - *"What are the trade-offs for each car? Read everything and think hard before answering."*
- **What the model does**
  - Reads all uploaded documents
  - May perform online search
  - Determines **evaluation criteria** suited to you
  - Generates **pros/cons report** per car
- 💡 Mirrors how a human would research a big purchase

## Growth in Long-Running Task Ability
- **METR study** — task difficulty measured by *human time-to-complete*
- **Task difficulty spectrum**
  - Seconds → find a fact on the web
  - ~1 hour → summarize a few pages of text
  - A couple hours → write a blog post
  - Many hours → audit legal documents
  - Many hours → explore complex cybersecurity vulnerability
- **Progression timeline**
  - 📊 **2024–2025** → handles seconds to tens of minutes of human work
  - 📊 **2025** → decent success on tasks taking humans *many hours*
- 💡 AI often completes the task **faster than the human equivalent time**, but **longer than a few seconds**

## Evolution of Prompting Advice
- **Old era (≈2023–2024)**
  - Famous failure: *"How many R's in strawberry?"*
  - Common advice: **"Think step-by-step"**
- **Today**
  - ⚠️ *"Think step-by-step"* is **largely obsolete**
  - ✅ Just say **"think hard"** — models understand the intent
  - Models reason in **more complex ways**, not strictly linear steps
- **Modern-style prompts**
  - *"What are the trade-offs for each car?"*
  - *"Look at all this context and create a script for a custom podcast"*
- 📌 Use a **modern model** for complex tasks when possible

## How Reasoning Works Conceptually
- **Loop**: Prompt + Context → Reason → (Tool use?) → Reason more → Final answer
- **Two decision branches after thinking**
  - ✅ Satisfied → return final answer
  - 🔧 Needs more info → invoke a **tool**
- **Common tools**
  - Web search
  - Reading files on your computer (desktop apps)
- **Iterative cycle**
  - Multiple rounds of *gather → reason → gather → reason*
  - Continues until answer is *good enough*

## Example: Rome Itinerary
- Task: fastest way to visit **5 landmarks in Rome in one day**
- Steps the model may take
  - Web search for map distances
  - Estimate walking times
  - Look up opening hours
  - Reorder stops for optimality
  - Generate optimized itinerary

## How to Trigger Deep Thinking
- **UI thinking toggle** — many providers offer a *Thinking* option
- **Prompt keywords**
  - *"Think really hard about this"*
  - *"ultrathink"* — recognized cue to reason deeply
- **Expected thinking durations**
  - Tens of seconds
  - Several minutes
  - Sometimes **over 10 minutes**
- 💡 Longer thinking ≠ wasted time — it correlates with harder problems

## Best Practices for Reasoning Prompts
- ✅ **Use the best/most modern model** available
  - Often noticeably better than models **6–12 months older**
- ✅ **Give hard, real tasks** — not trivial ones
  - Example: *"Design a 12-month plan for a 4-person startup with limited cash"*
- ✅ **Provide full context** — everything a human expert would need
- ✅ **Activate thinking mode** or tell it to *think hard* in the prompt
- ⚠️ Don't under-prompt — missing context limits reasoning quality

## Bridge to Next Lesson
- Even cutting-edge models have flaws
- 🔑 **Sycophancy** — tendency to tell you what you want to hear
- 📌 Next video → managing sycophantic behavior

## Key Takeaways
- 💡 Modern AI is best used as a **reasoning engine**, not just an answer lookup
- 📌 *"Think step-by-step"* is outdated — say **"think hard"** or use **thinking mode**
- 📊 AI now handles tasks that take humans **many hours** of expert work
- 🔑 Reasoning = **loop of thinking + tool use** until the model is satisfied
- ✅ Three levers for success: **best model**, **rich context**, **hard task + thinking enabled**
- ⚠️ Watch for **sycophancy** even in the most advanced models