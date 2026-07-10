---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Chapter 2: Routing

## Routing Pattern Overview

### Why Routing Is Needed
- **Prompt chaining** = deterministic, linear workflows only
- Real-world agents must arbitrate between multiple actions
- Contingent factors: environment state, user input, prior outcomes
- 🔑 **Routing**: dynamic decision-making directing control flow to specialized functions, tools, or sub-processes
- Shifts from fixed path → dynamic evaluation of criteria
- 💡 Enables flexible, **context-aware** system behavior

### Example: Customer Inquiry Agent
- Step 1: Analyze the user's query
- Step 2: Route by intent
  - "check order status" → order database tool chain
  - "product information" → product catalog search chain
  - "technical support" → troubleshooting guides / human escalation
  - Unclear intent → clarification sub-agent

### Routing Mechanisms
#### LLM-based Routing
- LLM prompted to output a category identifier
- e.g., output only: `Order Status`, `Product Info`, `Technical Support`, `Other`
- System reads output and directs workflow

#### Embedding-based Routing
- Query → vector embedding (see RAG, Chapter 14)
- Compared to embeddings of candidate routes
- Routes to most similar embedding
- 💡 **Semantic routing**: decision based on meaning, not keywords

#### Rule-based Routing
- Predefined logic: if-else, switch cases
- Based on keywords, patterns, structured data
- ✅ Faster and more deterministic
- ❌ Less flexible for nuanced or novel inputs

#### ML Model-based Routing
- Discriminative model (classifier) trained on labeled data
- Supervised **fine-tuning** encodes routing logic in learned weights
- ⚠️ Distinct from LLM-based: no generative model at inference time
- LLMs may generate synthetic training data, but not decide in real time

### Where Routing Applies
- At the outset: classify the primary task
- Intermediate points: determine next action in a chain
- Within subroutines: select the best tool from a set

### Framework Support
- **LangChain**, **LangGraph**, **Google ADK** offer conditional-logic constructs
- LangGraph's **state-based graph** suits state-contingent routing decisions
- ADK provides foundational components for capabilities & interaction models
- Developers define paths + transition-dictating evaluations between graph nodes

## Practical Applications & Use Cases

### Human-Computer Interaction
- Virtual assistants, AI tutors interpret **user intent**
- Actions: invoke retrieval tool, escalate to human, select next curriculum module
- Moves beyond linear dialogue flows

### Data & Document Processing Pipelines
- Routing as **classification & distribution** function
- Inputs: emails, support tickets, API payloads
- Analyzed by content, metadata, or format
- Directed to: sales lead ingestion, JSON/CSV transformation, urgent escalation

### Multi-Tool / Multi-Agent Systems
- Routing as **high-level dispatcher**
- Research system: assigns tasks to search / summarize / analyze agents
- AI coding assistant: identifies language + intent (debug, explain, translate) → correct tool

### Overall Value
- 💡 Logical arbitration → functionally diverse, context-aware systems
- Transforms static executor → dynamic decision-making system

## Hands-On Code Example (LangChain)

### Setup
- `pip install langchain langgraph google-cloud-aiplatform langchain-google-genai google-adk deprecated pydantic`
- API key env var required (e.g., `GOOGLE_API_KEY`)
- Model: `gemini-2.5-flash`, temperature 0

### Architecture
- **Coordinator** routes requests to simulated sub-agent handlers
- Handlers: `booking_handler`, `info_handler`, `unclear_handler`

### Key Components
- `coordinator_router_chain`: `ChatPromptTemplate` → LLM → `StrOutputParser`
  - Prompt outputs ONE word: `booker`, `info`, or `unclear`
- `RunnableBranch`: routes on router decision
  - `.strip()` applied to decision for robust matching
  - `unclear` branch as default fallback
- `coordinator_agent`: combines router decision + `RunnablePassthrough` of request → branch → extract output

### Demonstration
- "Book me a flight to London." → booker
- "What is the capital of Italy?" → info
- "Tell me about quantum physics." → unclear
- ✅ Error handling for LLM initialization failure included

## Hands-On Code Example (Google ADK)

### ADK Routing Paradigm
- Structured environment for agent capabilities & behaviours
- Routing via discrete **tools**, not explicit computational graphs
- Framework's internal logic matches intent → functional handler

### Architecture
- `FunctionTool` wraps handler functions: `booking_tool`, `info_tool`
- Sub-agents (model `gemini-2.0-flash`)
  - **Booker**: flight & hotel booking requests
  - **Info**: general information questions
- **Coordinator** parent agent
  - Instruction: analyze & delegate only, never answer directly
  - 📌 `sub_agents` presence enables **Auto-Flow** LLM-driven delegation
- ⚠️ `unclear_handler` defined but not used in delegation flow

### Execution Logic
- `InMemoryRunner` + user/session IDs (`uuid`)
- `runner.run` yields events; extract text on `is_final_response()`
- Fallback: iterate `event.content.parts` for text

### Demonstration
- "Book me a hotel in Paris." → Booker
- "What is the highest mountain in the world?" → Info
- "Tell me a random fact." → Info
- "Find flights to Tokyo next month." → Booker

## At a Glance

### What (Problem)
- Linear sequential workflows can't decide based on context
- Without routing: rigid, non-adaptive systems
- Real-world requests are complex and variable

### Why (Solution)
- Conditional logic in the agent's operational framework
- Analyze query intent → direct flow to best tool/function/sub-agent
- Methods: LLM prompting, predefined rules, embedding similarity
- 💡 Static path → flexible, context-aware workflow

### Rule of Thumb
- 📌 Use when the agent must choose among distinct workflows, tools, or sub-agents
- Essential for triage/classification of incoming requests
- e.g., support bot: sales vs. technical support vs. account management

## LangChain vs. Google ADK Approaches
- **LangGraph**: visual, explicit states & transitions
  - ✅ Ideal for complex, multi-step workflows with intricate routing logic
- **Google ADK**: defines discrete capabilities (Tools), framework routes requests
  - ✅ Simpler for agents with a well-defined set of discrete actions

## References
- [LangGraph Documentation](https://www.langchain.com/)
- [Google Agent Developer Kit Documentation](https://google.github.io/adk-docs/)

## Key Takeaways
- Routing = dynamic next-step decisions based on conditions
- Handles diverse inputs; adapts behavior beyond linear execution
- Implementations: **LLM-based**, **rule-based**, **embedding similarity**, **fine-tuned ML classifiers**
- LangGraph & Google ADK structure routing with different architectures
- 💡 Foundation for versatile, robust, context-aware agentic applications