---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Chapter 1: Prompt Chaining

## Pattern Overview

### Core Concept
- 🔑 **Prompt Chaining** (aka **Pipeline pattern**): divide-and-conquer for LLM tasks
- Break complex problem into sequence of smaller sub-problems
- Each sub-problem handled by a dedicated prompt
- Output of one prompt → input of the next (**dependency chain**)
- 💡 LLM builds on prior work, progressively refining toward solution

### Benefits
- ✅ Modularity and clarity in LLM interactions
- ✅ Each step easier to understand, debug, optimize
- ✅ More accurate, focused outputs per step
- ✅ Enables integration of **external tools, APIs, databases** at each step
- 💡 Foundational technique for **AI agents**: plan, reason, act in dynamic environments
- Agent workflows mimic human multi-step reasoning and decision-making

### Limitations of Single Prompts
- ⚠️ **Instruction neglect** — parts of the prompt overlooked
- ⚠️ **Contextual drift** — model loses track of initial context
- ⚠️ **Error propagation** — early errors amplify downstream
- ⚠️ **Context window strain** — insufficient information to respond
- ⚠️ **Hallucination** — higher cognitive load raises incorrect outputs
- Example: one prompt asking to summarize a report + identify trends + draft email risks partial failure

### Enhanced Reliability via Sequential Decomposition
- Example pipeline for market research task
  - **Step 1 (Summarization)**: summarize key findings — sole focus improves accuracy
  - **Step 2 (Trend Identification)**: top 3 trends + supporting data from step 1's output
  - **Step 3 (Email Composition)**: draft email from step 2's trends and data
- ✅ Granular control: each step simpler, less ambiguous, lower cognitive load
- 💡 Analogous to a computational pipeline of functions
- 📌 Assign a distinct **role** per stage (e.g., "Market Analyst" → "Trade Analyst" → "Expert Documentation Writer")

### The Role of Structured Output
- ⚠️ Chain reliability depends on integrity of data passed between steps
- Ambiguous/poorly formatted output → downstream prompt failure
- ✅ Specify structured formats: **JSON** or **XML**
- Example: trends as JSON array with `trend_name` + `supporting_data`
- 💡 Machine-readable data parses precisely, minimizing natural-language interpretation errors

## Practical Applications & Use Cases

### 1. Information Processing Workflows
- Chain: extract text → summarize → extract entities → search knowledge base → generate report
- Domains: automated content analysis, AI research assistants, complex report generation

### 2. Complex Query Answering
- Multi-step reasoning/retrieval, e.g., "1929 crash causes + government response"
  - Identify sub-questions → research causes → research policy response → synthesize answer
- Needed when no single data point suffices; requires logical steps and diverse sources
- 💡 Hybrid workflows: **parallel processing** for independent extraction + **chaining** for dependent synthesis
  - Retrieve articles → extract concurrently → collate → synthesize draft → review/refine sequentially

### 3. Data Extraction and Transformation
- Iterative unstructured → structured conversion
  - Extract fields → validate → conditional re-prompt for missing/malformed → re-validate → output
- OCR example (PDF forms)
  - Text extraction → data normalization (e.g., "one thousand and fifty" → `1050`)
  - ⚠️ LLMs weak at precise math → delegate arithmetic to **external calculator tool**

### 4. Content Generation Workflows
- Phases: ideation → outlining → drafting → revision
  - Generate 5 topic ideas → select → detailed outline → draft each section with prior context → refine for coherence, tone, grammar
- Uses: creative narratives, technical documentation, structured content

### 5. Conversational Agents with State
- Chaining as foundational mechanism for conversational continuity
  - Process utterance, identify intent/entities → update state → generate response → repeat per turn
- 💡 Accumulating conversation history enables coherent multi-turn dialogue

### 6. Code Generation and Refinement
- Chain: pseudocode/outline → initial draft → identify errors (static analysis or LLM) → refine → docs/tests
- ✅ Allows **deterministic logic** between calls: validation, conditional branching
- Converts one multifaceted request into a managed sequence of operations

### 7. Multimodal & Multi-step Reasoning
- Example: image with embedded text, labels, and explanatory table
  - Extract/comprehend image text → link text with labels → interpret via table for final output

## Hands-On Code Example

### Frameworks
- **LangChain**: abstractions for linear sequences
- **LangGraph**: stateful, cyclical computations for agentic behaviors
- Others: **Crew AI**, **Google ADK**

### Setup
- `pip install langchain langchain-community langchain-openai langgraph`
- Configure API credentials (OpenAI, Google Gemini, or Anthropic)

### Two-Step Chain Demo
- Stage 1: extract technical specs from unstructured text
- Stage 2: transform specs into JSON (`cpu`, `memory`, `storage` keys)
- Key components
  - `ChatOpenAI(temperature=0)` for model calls
  - `ChatPromptTemplate` per step
  - `StrOutputParser()` converts message output to plain string
  - **LCEL** pipes: `prompt_extract | llm | StrOutputParser()`
  - `full_chain` feeds extraction output into `specifications` variable
- Input: laptop description → Output: formatted JSON specs

## Context Engineering vs Prompt Engineering

### Definition
- 🔑 **Context Engineering**: systematic design and delivery of a complete informational environment before token generation
- 💡 Output quality depends less on model architecture, more on richness of context

### Evolution Beyond Prompt Engineering
- Prompt engineering: optimizes phrasing of the immediate query
- Context engineering layers
  - **System prompt**: foundational operating instructions (e.g., "You are a technical writer; formal tone")
  - **Retrieved documents**: fetched from knowledge bases
  - **Tool outputs**: real-time data via external APIs (e.g., calendar availability)
  - **Implicit data**: user identity, interaction history, environmental state
- ⚠️ Even advanced models underperform with a limited or poorly constructed view

### Practice
- Reframes task: from answering a question → building an operational picture
- Example: agent integrates calendar + recipient relationship + meeting notes before drafting
- "Engineering": runtime data pipelines + feedback loops for context quality
- Automated tuning: [Vertex AI prompt optimizer](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-optimizer) refines prompts/instructions against sample inputs and metrics
- 💡 Advances stateless chatbots into situationally-aware systems

## At a Glance

- **What**: monolithic prompts overload LLMs → instruction neglect, lost context, errors
- **Why**: chaining splits tasks into focused, interconnected sub-tasks with logical data flow
- **Rule of thumb**: use when task is too complex for one prompt, has distinct stages, needs external tools between steps, or requires multi-step reasoning with state

## References

- [LangChain LCEL Documentation](https://python.langchain.com/v0.2/docs/core_modules/expression_language/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Prompt Engineering Guide — Chaining Prompts](https://www.promptingguide.ai/techniques/chaining)
- [OpenAI API Prompting Concepts](https://platform.openai.com/docs/guides/gpt/prompting)
- [Crew AI Documentation](https://docs.crewai.com/)
- [Google AI Prompting Guides](https://cloud.google.com/discover/what-is-prompt-engineering?hl=en)
- [Vertex Prompt Optimizer](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-optimizer)

## Key Takeaways

- 📌 Prompt Chaining = complex task → sequence of smaller, focused steps (aka Pipeline pattern)
- Each step: LLM call or processing logic, consuming the previous step's output
- ✅ Improves reliability and manageability of complex LLM interactions
- Frameworks (**LangChain/LangGraph**, **Google ADK**) define, manage, execute multi-step sequences
- 💡 Foundational for agents: multi-step reasoning, tool integration, state management