---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# AI Critique

## Why Use AI for Editing
- ⏰ Always available, unlike human reviewers
- 💡 Great at reading and refining your work
- Pairs well with **anti-sycophancy** techniques
- Useful for both **line edits** and **holistic feedback**

## Piece-by-Piece Editing
- 🔑 **Core idea** — edit one chunk at a time
  - One sentence, or one paragraph
  - Nail it down before moving on
- **Workflow**
  - Brainstorm rephrasings of a single sentence
  - Iterate until satisfied
  - Move to next sentence/paragraph
  - Repeat through the whole article
- **Example prompt**
  - Original: *"The public thinks achieving AGI means computers will be as smart as people."*
  - Ask AI for variations:
    - **Punchy** version
    - **Visionary** version
    - **Conversational** version
- ✅ Manageable workflow
- ❌ Avoid editing the entire article in one shot
  - Too many changes to track
  - Hard to judge what improved

## Holistic Feedback with Rubrics
### The Sycophancy Problem
- ⚠️ Without guidance, AI says *"fantastic work!"*
- AI is **not a good objective critic** by default
- Example: sci-fi story gets praised regardless of quality

### What is a Rubric
- 🔑 **Rubric** — explicit grading criteria
- Forces AI to be **objective**, not flattering
- Removes ambiguity from evaluation

### Building a Good Rubric
- **Define weighted categories** (sum to 100)
  - Characters — 25 pts
  - Plot — 25 pts
  - World-building — 25 pts
  - Writing craft — 25 pts
- **Specify sub-criteria per category**
  - Characters example:
    - Every main character has a goal — 10 pts
    - Conflict between characters' goals — *X* pts
- 📌 Each criterion must be **binary** (true/false, yes/no)
- 💡 Stuck? Brainstorm the rubric **with AI** first

### Using the Rubric
- Provide **rubric + work** to the AI
- Prompt instructions:
  - Critique objectively
  - **Assign a score per category**
  - **Sum scores at the end**
  - Then ask for **improvement suggestions** tied to the rubric
- ✅ Focused, dimension-specific feedback

### Poorly Written Rubrics
- ❌ *"Score my story out of 100"* first
  - AI jumps to a conclusion, then justifies it
- ❌ Vague categories with no scoring rules
- ⚠️ Tends to produce **inflated scores**
- Encourages sycophancy and fuzzy reasoning

## Cross-Model Critique
- 💡 One AI can critique another AI's output
- **Workflow example**
  - ChatGPT writes user manual for an RPG
  - Gemini critiques it using a rubric
  - Or vice versa
- **Benefits**
  - Integrates knowledge from two models
  - Slightly better results than self-critique
- ⚠️ Improvement is **modest**, not dramatic
  - Self-critique with a rubric often works fine
- 📌 Reassuring when an *independent* model agrees

## Switching Between Models
### Jagged Intelligence
- 🔑 **Jagged intelligence** — uneven capability profile
- AI beats humans at some tasks
  - Reading tons of web pages fast
  - Tricky math problems
- AI underperforms humans at other tasks
- Different models are **jagged in different ways**

### Competitive Model Landscape
- ChatGPT, Claude, Gemini, and many others
- 📊 New, better models released **constantly**
- Best model for *your* task **changes over time**

### Practical Habit
- Feed the **same prompt** to multiple models
- Compare outputs side by side
- 💡 Continuously hones intuition for *which model, which task*

## Key Takeaways
- ✅ **Edit piece by piece** — one sentence/paragraph at a time beats whole-article rewrites
- 🔑 Use a **rubric** with weighted, binary criteria to get objective critique instead of flattery
- ⚠️ Ask for **scores per category, summed at the end** — never "score out of 100" first
- 💡 **Cross-model critique** (e.g., Gemini grading ChatGPT) gives a small but real boost
- 📌 AI has **jagged intelligence** — routinely switch models to find the best fit per task
- AI is a powerful **thought partner** for reasoning, brainstorming, writing, editing, and critique