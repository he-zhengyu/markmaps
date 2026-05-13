---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Evaluation Methodology

## Why Evaluation Matters
- ⚠️ **Catastrophic failures** as AI use grows
  - Suicide after chatbot encouragement
  - Hallucinated legal evidence
  - Air Canada chatbot misinformation
- 💡 Biggest hurdle in AI adoption
- Often consumes majority of dev effort
- 📌 *"Evals are surprisingly often all you need"* — Greg Brockman
- ❌ **Word of mouth** / *vibe checks* are insufficient
- ✅ Need **systematic evaluation**

## Challenges of Evaluating Foundation Models
- **Smarter models, harder to evaluate**
  - Easy to grade 1st-grade math, hard to grade PhD math
  - Requires fact-checking + domain expertise
- **Open-ended outputs break ground-truth comparison**
  - Many valid responses per input
  - Can't enumerate correct outputs
- **Black-box models**
  - Architecture, training data often hidden
  - Can only observe outputs
- **Benchmarks saturate fast**
  - GLUE (2018) → SuperGLUE (2019)
  - NaturalInstructions (2021) → Super-NaturalInstructions (2022)
  - MMLU (2020) → MMLU-Pro (2024)
- **Expanded scope**
  - Discover *new* model capabilities
  - Explore limits beyond human ability
- ⚠️ Investment in evaluation **lags** behind modeling/training tools

## Language Modeling Metrics
- 💡 LM performance correlates with downstream performance
- 🔑 Four interrelated metrics — know one, derive others

### Entropy
- 🔑 Average information per token
- Higher entropy → more bits needed, less predictable
- Example: 2-token language = 1 bit; 4-token = 2 bits

### Cross Entropy
- 🔑 Difficulty for model to predict next token in dataset
- $H(P,Q) = H(P) + D_{KL}(P||Q)$
  - $H(P)$ = data entropy
  - $D_{KL}$ = divergence of learned dist. from true dist.
- Training minimizes cross entropy
- ⚠️ Not symmetric: $H(P,Q) \neq H(Q,P)$

### BPC and BPB
- **BPC** — bits-per-character
  - Normalizes across tokenization schemes
- **BPB** — bits-per-byte
  - Standardizes across encodings (ASCII, UTF-8)
- 💡 Tells how efficiently model **compresses** text

### Perplexity (PPL)
- 🔑 Exponential of cross entropy
- $PPL(P,Q) = 2^{H(P,Q)}$ (bits) or $e^{H(P,Q)}$ (nats)
- Measures **uncertainty** in next-token prediction
- **Interpretation rules**
  - 📊 More structured data → lower PPL (e.g. HTML)
  - 📊 Bigger vocabulary → higher PPL
  - 📊 Longer context → lower PPL
- **Use cases**
  - ✅ Proxy for model capability
  - ✅ Detect **data contamination** (low PPL on benchmark)
  - ✅ Training data **deduplication**
  - ✅ Detect abnormal/gibberish text
- ⚠️ Unreliable after **post-training** (SFT, RLHF) — entropy collapse
- ⚠️ Quantization can shift PPL unexpectedly

## Exact Evaluation
- 🔑 Produces unambiguous judgment

### Functional Correctness
- 🔑 Does the system perform its intended function?
- 📌 **Ultimate metric** for application performance
- **Code generation** → execution accuracy
  - Unit tests / test cases
  - **pass@k** metric
  - Benchmarks: HumanEval, MBPP
- **Text-to-SQL**: Spider, BIRD-SQL, WikiSQL
- **Game bots, optimization tasks** with measurable objectives

### Similarity to Reference Data
- Format: `(input, reference responses)`
- 🔑 Reference = *ground truth* / *canonical response*
- **Reference-based** vs **reference-free** metrics
- ⚠️ Bottlenecked by reference data generation cost
- **Four similarity approaches**
  - **Exact match**
    - ✅ Works for short, factual answers
    - ❌ Fails for translation, open-ended tasks
    - ⚠️ Loose matching can accept wrong answers
  - **Lexical similarity** — surface overlap
    - *Approximate string matching* (edit distance / fuzzy matching)
      - Deletion, insertion, substitution (± transposition)
    - *N-gram similarity* (unigrams, bigrams, …)
    - Metrics: **BLEU**, **ROUGE**, METEOR, TER, CIDEr
    - Benchmarks: WMT, COCO Captions, GEMv2
    - ⚠️ Needs comprehensive references
    - ⚠️ References themselves can be wrong (WMT 2023)
    - ⚠️ Higher BLEU ≠ better correctness (HumanEval)
  - **Semantic similarity** — meaning-based
    - Compare **embeddings** via cosine similarity
    - Metrics: **BERTScore**, MoverScore
    - ✅ Less dependent on reference coverage
    - ⚠️ Quality depends on embedding model
    - ⚠️ Compute-intensive
  - **AI evaluator** *(see next section)*

### Embedding Primer
- 🔑 Numerical vector capturing meaning
- Sizes typically 100–10,000 (BERT 768/1024, OpenAI 1536/3072)
- Models: BERT, CLIP, Sentence Transformers
- ✅ Good embedding → similar texts have closer vectors
- **Multimodal embeddings**
  - **CLIP** — text + image joint space
  - **ULIP** — text, images, 3D point clouds
  - **ImageBind** — 6 modalities
- Benchmark: **MTEB**
- Used in: classification, RAG, recommenders, search

## AI as a Judge
- 🔑 Using AI to evaluate AI responses
- 📊 58% of LangChain platform evals (2023)

### Why Use It
- ✅ Fast, cheap, easy vs human evaluators
- ✅ Works **without reference data**
- ✅ Flexible — any criterion (toxicity, coherence, etc.)
- ✅ Can **explain** its judgments
- 📊 GPT-4 ↔ human agreement: 85% (vs 81% human-human) on MT-Bench

### How to Use It
- **Three prompt patterns**
  - Score a single response (e.g., 1–5)
  - Compare generated vs reference (match/mismatch)
  - Compare two responses pairwise (A vs B)
- **Prompt design**
  - Define the task clearly
  - Specify detailed criteria
  - Choose scoring system
    - ✅ Classification works best
    - ✅ Discrete numerical (1–5) > continuous
    - ⚠️ Wider ranges degrade performance
  - Include examples with justifications
- 📌 Judge = model + prompt + sampling params

### Limitations
- ⚠️ **Inconsistency**
  - Same input → different scores
  - Examples in prompt boost consistency (65% → 77.5%) but quadruple cost
- ⚠️ **Criteria ambiguity**
  - Non-standardized: MLflow, Ragas, LlamaIndex all define *faithfulness* differently
  - Scores not comparable across tools
  - Judges drift over time → breaks longitudinal tracking
  - 📌 Don't trust a judge whose model + prompt you can't see
- ⚠️ **Cost & latency**
  - Doubles/quadruples API calls
  - Mitigation: weaker judge models, **spot-checking**
  - Production guardrails add latency
- ⚠️ **Biases**
  - **Self-bias** — favors own outputs (GPT-4: +10%, Claude-v1: +25%)
  - **First-position bias** (humans have *recency bias*)
  - **Verbosity bias** — prefers longer answers, even with errors
  - Privacy/IP concerns with proprietary judges

### What Models Can Judge?
- **Stronger judge** ✅ best correlation with humans
  - ⚠️ No judge for the strongest model
- **Same model** — *self-evaluation / self-critique*
  - ✅ Sanity check, can prompt revisions
  - ⚠️ Self-bias risk
- **Weaker judge**
  - 💡 Judging may be easier than generating
- **Specialized judges**
  - 🔑 **Reward model** — `(prompt, response) → score` (e.g., Cappy, 360M params)
  - 🔑 **Reference-based judge** — BLEURT, Prometheus
  - 🔑 **Preference model** — predicts which response users prefer (PandaLM, JudgeLM)

## Comparative Evaluation

### Concept
- Rank models from **pairwise comparisons**, not absolute scores
- 💡 Easier to compare than to score (esp. subjective tasks)
- First used by Anthropic (2021)
- Powers **LMSYS Chatbot Arena**

### Process
- Each comparison = a **match**
- **Win rate** = % of A's wins vs B
- **Rating algorithms**: Elo, Bradley–Terry, TrueSkill
- 📌 LMSYS switched Elo → Bradley–Terry (Elo too order-sensitive)
- A ranking is *correct* if higher-ranked model wins more often

### ⚠️ Not All Questions Suit Preference
- Correctness questions ≠ preference questions
- Voters must be knowledgeable
- ✅ Works when AI is assistant for known tasks
- ❌ User can't validate unknown answers

### Distinct from A/B Testing
- A/B test: one output at a time
- Comparative: multiple outputs side-by-side

### Challenges
- **Scalability**
  - Pairs grow quadratically (57 models → 1,596 pairs)
  - **Transitivity** assumption (A>B, B>C ⇒ A>C) may not hold
  - New/private models hard to add
  - Better matching algorithms can help
- **Standardization & quality control**
  - Crowdsourced prompts vary wildly
  - 📊 0.55% of LMSYS prompts were just "hello"/"hi"
  - Voters may prefer plausible-but-wrong answers
  - Doesn't reflect production use (e.g., RAG pipelines)
  - Mitigations: hard-prompt filtering, trained evaluators (Scale), in-product voting
- **Comparative ≠ absolute performance**
  - Tells which is better, not whether either is good enough
  - 51% win rate ↛ predictable production gain
  - Hard to do cost–benefit analysis

### Future
- ✅ Captures human preference directly
- ✅ Won't saturate as models improve
- ✅ Hard to game vs reference-based benchmarks
- 💡 Complements offline benchmarks and online A/B tests

## Key Takeaways
- 💡 **Evaluation is the biggest bottleneck** in shipping AI applications — invest systematically, don't rely on vibes
- 📌 Foundation models are uniquely hard to evaluate: open-ended outputs, black-box internals, fast-saturating benchmarks
- 🔑 **Perplexity** is a strong proxy for base model capability and powerful for **data contamination detection** and **deduplication** — but unreliable after post-training
- ✅ Prefer **functional correctness** when measurable; fall back to **similarity** (lexical → semantic) otherwise
- 💡 **AI as a judge** is the rising standard — fast, flexible, reference-free — but ⚠️ inconsistent, biased (self/position/verbosity), and non-standardized across tools
- 📌 An AI judge = **model + prompt + params** — never trust a judge whose components you can't inspect
- 💡 **Comparative evaluation** captures human preference and resists saturation, but ⚠️ scales quadratically and doesn't tell you absolute quality
- ✅ Best practice: **combine** exact metrics + AI judges + human review — no single method suffices