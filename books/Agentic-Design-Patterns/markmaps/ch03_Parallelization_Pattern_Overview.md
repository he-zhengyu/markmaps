---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Chapter 3: Parallelization

## Pattern Overview

### Context & Motivation
- Builds on **Prompt Chaining** (sequential) and **Routing** (dynamic decisions)
- Many complex agentic tasks contain sub-tasks that can run **simultaneously**
- 🔑 **Parallelization**: executing multiple components (LLM calls, tool usages, sub-agents) concurrently
- Reduces overall execution time for tasks decomposable into independent parts

### Sequential vs Parallel Research Example
- **Sequential approach**
  - Search Source A → Summarize A → Search Source B → Summarize B → Synthesize
- **Parallel approach**
  - Search A **and** B simultaneously
  - Summarize A **and** B simultaneously
  - Synthesize final answer (sequential — waits for parallel steps)

### Core Principle
- 💡 Identify workflow parts that **don't depend on other outputs**; run them in parallel
- Especially effective for **external services with latency** (APIs, databases)
- Requires frameworks supporting **async execution** or multi-threading/multi-processing

### Framework Support
- **LangChain (LCEL)**: combine runnables; `|` for sequential, branch structures for concurrency
- **LangGraph**: multiple nodes from a single state transition → parallel branches
- **Google ADK**: native mechanisms for concurrent multi-agent execution

## Practical Applications & Use Cases

### 1. Information Gathering & Research
- Use case: agent researching a company
- Parallel: news search, stock data, social media mentions, company database query
- ✅ Comprehensive view much faster than sequential lookups

### 2. Data Processing & Analysis
- Use case: analyzing customer feedback
- Parallel: sentiment analysis, keyword extraction, categorization, urgent-issue detection
- ✅ Multi-faceted analysis quickly

### 3. Multi-API or Tool Interaction
- Use case: travel planning agent
- Parallel: flight prices, hotel availability, local events, restaurant recommendations
- ✅ Complete travel plan faster

### 4. Content Generation with Multiple Components
- Use case: creating a marketing email
- Parallel: subject line, email body, relevant image, CTA button text
- ✅ Assembles final email more efficiently

### 5. Validation & Verification
- Use case: verifying user input
- Parallel: email format, phone number, address vs database, profanity check
- ✅ Faster feedback on input validity

### 6. Multi-Modal Processing
- Use case: social media post with text + image
- Parallel: text sentiment/keywords **and** image objects/scene description
- ✅ Integrates cross-modal insights more quickly

### 7. A/B Testing / Multiple Options Generation
- Use case: generating creative text options
- Parallel: three headlines via different prompts or models
- ✅ Quick comparison and selection of the best option

## Hands-On: LangChain (LCEL)

### Mechanism
- Structure multiple runnables in a **dictionary/list construct**
- LCEL runtime executes contained runnables **concurrently**
- LangGraph: parallel pathways from a common node, aggregated at a **convergence point**

### Example Workflow Structure
- Prerequisites: `langchain`, `langchain-community`, `langchain-openai`, API key
- Three independent chains on one topic
  - `summarize_chain` — concise topic summary
  - `questions_chain` — three interesting questions
  - `terms_chain` — 5–10 comma-separated key terms
- `RunnableParallel` bundles chains + `RunnablePassthrough` (keeps original topic)
- Synthesis prompt combines summary, questions, key terms, topic
- `full_parallel_chain = map_chain | synthesis_prompt | llm | StrOutputParser()`
- Invoked via `asyncio.run()` and `ainvoke`

### Key Technical Caveat
- ⚠️ `asyncio` provides **concurrency, not parallelism**
- Single thread + event loop switching between idle tasks (e.g., awaiting network I/O)
- Constrained by Python's **Global Interpreter Lock (GIL)**

## Hands-On: Google ADK

### Architecture
- Primitives: `LlmAgent`, `ParallelAgent`, `SequentialAgent`, `google_search` tool

### Researcher Sub-Agents (run in parallel)
- `RenewableEnergyResearcher` → `output_key="renewable_energy_result"`
- `EVResearcher` → `output_key="ev_technology_result"`
- `CarbonCaptureResearcher` → `output_key="carbon_capture_result"`
- Each: uses Gemini model + Google Search, outputs a 1–2 sentence summary to **session state**

### Orchestration
- `ParallelAgent` runs the three researchers concurrently; finishes when all populate state
- `MergerAgent` (LlmAgent) synthesizes state results
  - 📌 Grounded **exclusively** on input summaries — no external knowledge
  - Structured report: per-topic headings + brief overall conclusion
- `SequentialAgent` pipeline: parallel research **then** merger; set as `root_agent`

## At a Glance

### What (Problem)
- Sequential execution: total time = **sum of all task durations**
- Latency bottleneck with external I/O (multiple APIs, databases)

### Why (Solution)
- Simultaneous execution of **independent** tasks
- Frameworks provide built-in constructs to define/manage concurrency
- Main process invokes parallel sub-tasks, waits for all before proceeding

### Rule of Thumb
- 📌 Use when a workflow has multiple independent operations: multi-API fetches, data-chunk processing, multi-content generation for later synthesis

## References
- [LCEL Documentation (Parallelism)](https://python.langchain.com/docs/concepts/lcel/)
- [Google ADK Multi-Agent Systems](https://google.github.io/adk-docs/agents/multi-agents/)
- [Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html)

## Key Takeaways
- 💡 Parallelization = concurrent execution of **independent tasks** for efficiency
- Most valuable when tasks wait on external resources (e.g., API calls)
- ⚠️ Concurrency adds substantial complexity/cost: design, debugging, logging
- LangChain & Google ADK offer built-in parallel-execution support
- 🔑 LCEL: `RunnableParallel` runs multiple runnables side-by-side
- 🔑 ADK: **LLM-Driven Delegation** — Coordinator LLM triggers concurrent sub-agents
- Combining parallel + sequential (chaining) + conditional (routing) flows enables sophisticated, high-performance agentic systems