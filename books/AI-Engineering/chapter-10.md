---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# AI Engineering Architecture and User Feedback

## AI Engineering Architecture
- 💡 Start simple, then add components **step by step** as needs arise

### Step 1. Enhance Context
- Give the model the info it needs per query
- **RAG** (retrieval) and **tools / agents**
- 📌 Most impactful first improvement

### Step 2. Put in Guardrails
- **Input guardrails**
  - Block PII leakage, **jailbreaks**, malicious prompts
- **Output guardrails**
  - Catch quality failures, security issues, unsafe content
- ⚠️ Guardrails add latency — balance safety vs speed

### Step 3. Add Model Router and Gateway
- **Router**
  - 🔑 Route queries to the right model by intent/complexity
  - ✅ Save cost — cheap model for easy queries
- **Gateway**
  - Unified interface to multiple models/providers
  - Access control, **fallback**, rate limiting, monitoring

### Step 4. Reduce Latency with Caches
- **Cache Mechanisms**
  - **Exact / prompt cache** — identical inputs
  - **Semantic cache** — similar inputs via embeddings
  - ⚠️ Semantic cache risks wrong hits — validate similarity

### Step 5. Add Agent Patterns
- Add planning, tool use, multi-step **agentic** workflows
- ⚠️ Most complex — adds capability and failure modes

### Monitoring and Observability
- **Metrics** — quality, latency, cost, usage
- **Logs and Traces** — debug multi-step pipelines
- 💡 Observability is essential as systems grow

### AI Pipeline Orchestration
- Coordinate components (retrievers, models, tools) into a pipeline
- Frameworks chain steps reliably

## User Feedback
- 💡 Feedback is a **proprietary data moat** and an evaluation source

### Extracting Conversational Feedback
- **Natural language feedback** signals
  - **Sentiment** in replies
  - Explicit praise / complaints
  - **Early termination** (user gives up)
  - **Error correction** / rephrasing

### Feedback Design
- **Feedback Placement**
  - Where & when to ask (e.g. thumbs up/down, ratings)
  - ⚠️ Don't disrupt the user experience
- **Feedback Limitations**
  - ⚠️ **Bias** — only certain users respond
  - ⚠️ **Degenerate feedback loops** — model shapes the data it later learns from

### Feedback Loops
- Use feedback to evaluate, retrain, and improve
- 📌 Close the loop carefully to avoid reinforcing bias

## Key Takeaways
- 💡 Build architecture **incrementally**: context → guardrails → router/gateway → caches → agents
- **Routers** cut cost; **gateways** add control, fallback, and monitoring
- **Caching** (exact + semantic) is a key latency/cost lever — validate semantic hits
- **Monitoring, logs, and traces** are non-negotiable as pipelines grow
- ✅ **User feedback** is a powerful data asset — design for it, but guard against **bias** and **degenerate loops**
