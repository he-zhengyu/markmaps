---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Chapter 4: Reflection Pattern

## Pattern Overview

### Context & Motivation
- Builds on prior patterns: **Chaining**, **Routing**, **Parallelization**
- ⚠️ Initial agent output may not be optimal, accurate, or complete
- 🔑 **Reflection**: agent evaluates its own work/output/state to improve performance
- A form of **self-correction / self-improvement**
- Can be facilitated by a separate agent analyzing the initial agent's output
- 💡 Introduces a **feedback loop**, unlike simple chains or routing

### The Reflection Process
- **1. Execution**: perform task, generate initial output
- **2. Evaluation/Critique**: analyze result via another LLM call or rules
  - Checks: factual accuracy, coherence, style, completeness, instruction adherence
- **3. Reflection/Refinement**: decide how to improve
  - Refined output, adjusted parameters, or modified plan
- **4. Iteration** (optional but common): repeat until satisfactory or stop condition met

### Producer-Critic Model
- 🔑 Also called **"Generator-Critic"** or **"Producer-Reviewer"** model
- Two distinct logical roles → more robust, unbiased than self-reflection
- **Producer Agent**
  - Performs initial task execution
  - Focuses entirely on content generation (code, blog post, plan)
- **Critic Agent**
  - Sole purpose: evaluate Producer's output
  - Distinct persona (e.g., *"senior software engineer"*, *"meticulous fact-checker"*)
  - Finds flaws, suggests improvements, gives structured feedback
- 💡 Separation of concerns prevents **cognitive bias** of self-review
- Critic feedback guides Producer to generate refined version

### Implementation Considerations
- Requires workflow structured with feedback loops
- Iterative loops in code, or frameworks with **state management** + conditional transitions
- Single evaluation-refinement step: LangChain/LangGraph, ADK, or Crew.AI
- ⚠️ True iterative reflection needs more complex orchestration

### Synergies with Other Patterns
- **Goal Setting & Monitoring** (Ch. 11)
  - Goal = benchmark for self-evaluation; monitoring tracks progress
  - 💡 Reflection acts as **corrective engine**, adjusting strategy from monitored feedback
  - Transforms agent from passive executor into purposeful system
- **Memory** (Ch. 8)
  - Conversation history gives crucial context for evaluation
  - Enables learning from past critiques, avoids repeating errors
  - 📌 Without memory: reflection is self-contained; with memory: cumulative refinement

## Practical Applications & Use Cases

### 1. Creative Writing & Content Generation
- Use case: agent writing a blog post
- Draft → critique flow, tone, clarity → rewrite → repeat
- ✅ More polished and effective content

### 2. Code Generation & Debugging
- Use case: agent writing a Python function
- Write code → run tests/static analysis → fix errors/inefficiencies
- ✅ More robust and functional code

### 3. Complex Problem Solving
- Use case: agent solving a logic puzzle
- Propose step → check progress/contradictions → backtrack if needed
- ✅ Better navigation of complex problem spaces

### 4. Summarization & Information Synthesis
- Use case: summarizing a long document
- Initial summary → compare against key points → refine
- ✅ More accurate and comprehensive summaries

### 5. Planning & Strategy
- Use case: planning actions toward a goal
- Generate plan → simulate/check feasibility → revise
- ✅ More effective and realistic plans

### 6. Conversational Agents
- Use case: customer support chatbot
- Review conversation history + last message for coherence
- ✅ More natural and effective conversations

## Hands-On Code Example (LangChain)

### Setup
- Single reflection cycle demonstrable via **LCEL** compositional syntax
- Full iterative reflection: LangGraph or custom procedural code
- `pip install langchain langchain-community langchain-openai`
- Model: `gpt-4o`, `temperature=0.1` for deterministic output

### Task
- Create `calculate_factorial` Python function
- Requirements: docstring, edge case `0! = 1`, `ValueError` on negative input

### Loop Structure (`max_iterations = 3`)
- **Stage 1 — Generate/Refine**
  - Iteration 1: generate initial code from task prompt
  - Later iterations: refine using prior critiques
- **Stage 2 — Reflect**
  - `reflector_prompt`: *senior software engineer* persona reviews code
  - Checks bugs, style, missing edge cases, improvements
- **Stage 3 — Stopping condition**
  - Critique returns `CODE_IS_PERFECT` → break
  - Otherwise: bulleted critique appended to history
- 📌 `message_history` maintained across steps for context

## Hands-On Code Example (ADK)

### Generator-Critic Structure
- **`generator`** (`DraftWriter`, `LlmAgent`)
  - Writes short informative paragraph
  - Output saved to state key `draft_text`
- **`reviewer`** (`FactChecker`, `LlmAgent`)
  - Meticulous fact-checker persona reads `draft_text`
  - Outputs dictionary: `status` ("ACCURATE"/"INACCURATE") + `reasoning`
  - Saved to state key `review_output`
- **`SequentialAgent`** (`WriteAndReview_Pipeline`)
  - Ensures generator runs before reviewer
  - State-mediated data flow between agents
- Alternative: ADK's `LoopAgent` for iterative implementation

### Trade-offs
- ⚠️ Higher **cost and latency**: each loop may need a new LLM call
- ⚠️ Suboptimal for time-sensitive applications
- ⚠️ **Memory-intensive**: history grows with output + critique + refinements

## At a Glance
- **What**: initial outputs often suboptimal; basic workflows lack error self-recognition
  - Solved by self-evaluation or a separate critic agent
- **Why**: feedback loop of generation → evaluation → refinement
  - Progressively yields more accurate, coherent, reliable outcomes
- **Rule of thumb**
  - ✅ Use when quality/accuracy/detail matter more than speed and cost
  - ✅ Best for polished long-form content, code writing/debugging, detailed plans
  - ✅ Separate critic when objectivity or specialized evaluation is needed

## References
- [Training LLMs to Self-Correct via RL](https://arxiv.org/abs/2409.12917)
- [LCEL Documentation](https://python.langchain.com/docs/introduction/)
- [LangGraph Documentation](https://www.langchain.com/langgraph)
- [Google ADK Multi-Agent Docs](https://google.github.io/adk-docs/agents/multi-agents/)

## Key Takeaways
- 💡 Iterative self-correction yields higher quality, accuracy, instruction adherence
- Feedback loop: **execution → evaluation/critique → refinement**
- **Producer-Critic model** enhances objectivity via separation of concerns
- ⚠️ Costs: latency, compute, context-window risk, API throttling
- Full iteration needs stateful workflows (LangGraph); single step works in LCEL
- ADK enables reflection via sequential agent pipelines
- 📌 Reflection is a control structure composable with other agentic patterns