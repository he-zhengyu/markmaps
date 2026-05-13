---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Evaluate AI Systems

## Evaluation Criteria

### 💡 Evaluation-Driven Development
- Define **evaluation criteria** *before* building
- Inspired by *test-driven development*
- 📌 Evaluation is the **biggest bottleneck** to AI adoption
- Common production apps have clear metrics
  - Recommender systems → engagement
  - Fraud detection → money saved
  - Coding → functional correctness
  - Classification tasks → easy to verify

### Four Buckets of Criteria
- **Domain-specific capability**
- **Generation capability**
- **Instruction-following capability**
- **Cost and latency**

### Domain-Specific Capability
- Constrained by model **architecture, size, training data**
- Evaluated via domain benchmarks (public/private)
- **Coding**: functional correctness
  - Also: efficiency, memory, readability
  - `BIRD-SQL` measures runtime vs ground truth
  - ⚠️ Readability hard to measure exactly
- **Non-coding**: close-ended tasks
  - Multiple-choice questions (MCQs)
  - Classification (F1, precision, recall)
- MCQ pros & cons
  - ✅ Easy to create, verify, reproduce
  - ✅ Random baseline well-defined (e.g., 25%)
  - ⚠️ Sensitive to small prompt changes
  - ⚠️ Tests **discrimination**, not generation

### Generation Capability
- Roots in **NLG** (natural language generation)
- Legacy metrics
  - *Fluency* — grammatical, natural-sounding
  - *Coherence* — logical structure
  - *Faithfulness* (translation)
  - *Relevance* (summarization)
- 💡 Modern models made fluency/coherence less critical
- New pressing issues
  - **Factual consistency** (hallucinations)
  - **Safety** (toxicity, bias)
- App-specific qualities
  - Controversiality, friendliness, conciseness, creativity

#### Factual Consistency
- 🔑 **Local** — output vs given context
  - For summarization, customer support, business analysis
- 🔑 **Global** — output vs open knowledge
  - For general chatbots, fact-checking
- ⚠️ Hardest part: determining what *is* a fact
- Evaluation methods
  - **AI as a judge** (GPT-3.5/4 strong)
  - **Self-verification** — `SelfCheckGPT`
    - Generate N responses, check consistency
    - ⚠️ Expensive
  - **Knowledge-augmented** — `SAFE` (DeepMind)
    - Decompose → self-contain → search → verify
  - **Textual entailment**
    - Entailment / Contradiction / Neutral
    - Specialized scorers (e.g., `DeBERTa-v3-base-mnli-fever-anli`)
- Benchmark: **TruthfulQA**
  - 817 questions, 38 categories
  - Comes with `GPT-judge` (90–96% accuracy)
  - Human expert baseline: 94%
- 📌 Critical for **RAG** systems

#### Safety
- Categories of unsafe content
  - Inappropriate language / explicit content
  - Harmful tutorials (e.g., self-harm)
  - Hate speech (racism, sexism, etc.)
  - Violence and threats
  - Stereotypes
  - Political/religious bias
- Detection options
  - General-purpose AI judges (GPT, Claude, Gemini)
  - Specialized smaller models
    - Facebook hate speech detector
    - Skolkovo toxicity classifier
    - Perspective API
- Benchmarks
  - **RealToxicityPrompts** — 100K toxic-leaning prompts
  - **BOLD** — bias in open-ended generation

### Instruction-Following Capability
- 📌 Bad instruction-following → bad outputs regardless of prompt quality
- Examples of failures
  - Outputting `HAPPY` instead of `POSITIVE`
  - Ignoring length/word constraints
- ⚠️ Easily conflated with domain or generation capability
- Benchmarks
  - **IFEval** (Google)
    - 25 auto-verifiable instruction types
    - Keywords, length, format, language, JSON, etc.
  - **INFOBench**
    - Format + content + linguistic + style rules
    - Yes/no decomposition criteria
    - GPT-4 judge: reliable & cost-effective
- 📌 **Curate your own benchmark** for your instructions

#### Roleplaying
- Two purposes
  - Character for users (gaming, companions)
  - Prompt-engineering technique
- 📊 8th most common use case (LMSYS, 1M convos)
- Benchmarks: **RoleLLM**, **CharacterEval**
- Evaluate **style + knowledge**
  - ⚠️ Watch "negative knowledge" leaks (gaming spoilers)
- AI judges with role-specific prompts

### Cost and Latency
- 🔑 **Pareto optimization** — multi-objective tradeoffs
- Latency metrics
  - Time to first token
  - Time per token / between tokens
  - Time per query
- Latency depends on prompt + sampling
- Cost models
  - Model APIs → per-token charges
  - Self-hosting → fixed compute, cheaper at scale
  - 📌 Many models sized to GPU memory (7B, 65B params)
- 💡 Differentiate **must-have** vs **nice-to-have** latency

## Model Selection

### Selection Workflow
- Hard vs soft attributes
  - 🔑 **Hard**: licenses, size, privacy policy
  - 🔑 **Soft**: accuracy, toxicity, latency (improvable)
- Four iterative steps
  1. Filter by hard attributes
  2. Narrow via public info & leaderboards
  3. Run experiments with own pipeline
  4. Monitor in production

### Model Build vs Buy
- Question: commercial API vs self-host open source

#### Open Source Terminology
- **Open weight** — weights public, data hidden
- **Open model** — weights + training data public
- ⚠️ Most "open source" today is open weight only
- Licenses vary
  - MIT, Apache 2.0, GPL, BSD, Creative Commons
  - Llama Community License, BigCode RAIL-M
- Key license questions
  - Commercial use allowed?
  - Restrictions (e.g., Llama: 700M MAU limit)?
  - Outputs usable for training (distillation)?

#### Comparison Axes
- **Data privacy**
  - ⚠️ Samsung leaked secrets via ChatGPT (2023)
  - Models can memorize training data (StarCoder: 8%)
- **Data lineage & copyright**
  - ⚠️ IP laws around AI still evolving
  - Commercial contracts may protect users
- **Performance**
  - Gap closing on MMLU
  - 💡 Strongest models likely stay proprietary
- **Functionality**
  - Scalability, function calling, structured outputs, guardrails
  - ⚠️ APIs may not expose `logprobs`
  - ⚠️ Finetuning limited by provider
- **Cost**
  - APIs: pay-per-use, scales with traffic
  - Self-host: engineering cost, fixed compute
- **Control, access, transparency**
  - 📌 Top reasons enterprises pick open source (a16z 2024)
  - ⚠️ Commercial models: rate limits, version drift, censoring
  - ⚠️ Provider could shut down or be banned
- **On-device deployment**
  - APIs impossible offline
  - Privacy: data stays local

### Navigate Public Benchmarks
- 📊 Thousands exist (BIG-bench: 214; lm-evaluation-harness: 400+)
- 🔑 **Evaluation harness** — runs many benchmarks

#### Benchmark Selection & Aggregation
- Two questions
  - Which benchmarks to include?
  - How to aggregate scores?
- Public leaderboards
  - **Hugging Face Open LLM** — 6 benchmarks
    - ARC-C, MMLU, HellaSwag, TruthfulQA, WinoGrande, GSM-8K
  - **Stanford HELM Lite** — 10 benchmarks
    - Only MMLU & GSM-8K overlap with HF
- ⚠️ Benchmark correlation matters
  - WinoGrande, MMLU, ARC-C strongly correlated
  - TruthfulQA only moderately correlated
- Aggregation methods
  - HF: simple averaging
  - HELM: **mean win rate**
- 📌 Benchmarks **saturate quickly**
  - HF revamped 2024: MATH lvl 5, MMLU-PRO, GPQA, MuSR, BBH, IFEval

#### Custom Leaderboards
- Build private leaderboard for your use case
- Find latest, reliable benchmarks
- ⚠️ Running benchmarks is expensive
  - HELM: ~$80K–$100K for 30 models
- Aggregate scores by **importance weighting**

#### Data Contamination
- 🔑 Training on the test set
- Causes
  - Web scraping pulls public benchmarks
  - Indirect: shared sources (textbooks)
  - Intentional: improving model before release
- Detection
  - **N-gram overlap** — accurate, expensive
  - **Perplexity** — cheaper, less accurate
- 📌 GPT-3 had ≥40% overlap on 13 benchmarks
- Mitigation
  - Remove benchmarks from training data
  - Disclose contamination % in reports
  - Keep private hold-out sets
- ⚠️ "A benchmark stops being useful as soon as it becomes public"

## Design Your Evaluation Pipeline

### Step 1: Evaluate All Components
- Evaluate **end-to-end** AND each component
- Levels
  - **Per intermediate output**
  - **Per turn** — each model response
  - **Per task** — full goal completion
- Example: PDF → text → extract employer
- 📌 Task-based evaluation matters most to users
- ⚠️ Hard to define task boundaries in chats
- Example: BIG-bench `twenty_questions`

### Step 2: Create Evaluation Guideline
- 📌 The most important step
- Define what app **should** AND **shouldn't** do
- 💡 A correct response ≠ a good response
  - LinkedIn: "You're a terrible fit" is correct but unhelpful

#### Define Criteria
- Average ~2.3 criteria per app (LangChain 2023)
- Example for customer support
  - Relevance
  - Factual consistency
  - Safety

#### Scoring Rubrics
- Choose scale: binary, 1–5, [0,1], -1/0/1
- Build rubric **with examples**
- Validate with humans
- ✅ Reusable for finetuning data later

#### Tie to Business Metrics
- Map AI scores → business outcomes
  - 80% factual consistency → automate 30% of support
  - 90% → 50%
  - 98% → 90%
- Define **usefulness threshold**
- ⚠️ Stickiness/engagement metrics can incentivize harmful design

### Step 3: Methods and Data

#### Select Methods
- Mix and match per criterion
  - Toxicity → small classifier
  - Relevance → semantic similarity
  - Factual consistency → AI judge
- Tiered approach
  - Cheap classifier on 100% of data
  - Expensive judge on 1%
- Use **logprobs** when available
  - Confidence, perplexity, fluency
- Keep **human evaluation** as North Star
  - LinkedIn: up to 500 daily manual reviews

#### Annotate Data
- Use real production data when possible
- 🔑 **Slicing** — analyze data subsets
  - ✅ Find biases
  - ✅ Debug failures
  - ✅ Avoid ⚠️ **Simpson's paradox**
- Multiple evaluation sets
  - Production distribution
  - Known failure cases
  - Out-of-scope inputs
  - User-typo inputs
- Sample size guidance (OpenAI)
  - 📊 30% diff → ~10 samples
  - 📊 10% diff → ~100 samples
  - 📊 3% diff → ~1,000 samples
  - 📊 1% diff → ~10,000 samples
  - 💡 3× smaller diff → 10× more samples
- Reference: lm-evaluation-harness median = 1,000 examples
- Use **bootstrapping** to test reliability

#### Evaluate the Pipeline Itself
- Right signals? Better scores → better outcomes?
- Reliability — same input, same score?
  - 📌 Set AI judge `temperature = 0`
- Metric correlations — redundant or contradictory?
- Cost & latency added by evaluation

#### Iterate
- Criteria evolve with users
- Track all variables: data, rubric, prompts, sampling configs
- ⚠️ Avoid constant churn — undermines comparability

## Key Takeaways
- 💡 **Evaluation is the biggest bottleneck** to AI adoption
- 📌 Define evaluation criteria **before** building (evaluation-driven development)
- Four core criterion buckets: **domain capability, generation, instruction-following, cost/latency**
- 🔑 Distinguish **local** (vs context) from **global** (vs open knowledge) factual consistency
- ⚠️ Public benchmarks filter out bad models but **won't find the best** for your app
- ⚠️ Benchmark **contamination is widespread** — assume leaks, not purity
- Build vs buy hinges on **7 axes**: privacy, lineage, performance, functionality, cost, control, on-device
- 💡 A *correct* response is not always a *good* response — encode this in rubrics
- 📌 Slice your evaluation data to avoid Simpson's paradox and surface hidden failures
- ✅ Combine cheap automatic metrics + targeted human review + AI judges for layered confidence
- 📊 For each 3× decrease in score gap, need ~10× more eval samples to be confident