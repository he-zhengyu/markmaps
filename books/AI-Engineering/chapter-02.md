---
markmap:
  initialExpandLevel: 
  maxWidth: 0
  colorFreezeLevel: 3
---

# Understanding Foundation Models

## Training Data
- 💡 **Models are only as good as their data**
- Common sources
  - **Common Crawl** — 2–3B web pages/month
  - **C4** — Google's cleaned subset
  - ⚠️ Quality issues: clickbait, misinformation, propaganda
- Heuristic filtering
  - GPT-2: Reddit links with ≥3 upvotes
- 📌 "Use what we have, not what we want" → bias toward training tasks
- 💡 Quality often beats quantity
  - 7B tokens of high-quality code → 1.3B model beats much larger ones

### Multilingual Models
- 📊 **English dominates Common Crawl** (45.88%)
- Under-represented languages
  - Punjabi (231× under), Swahili, Urdu, Telugu
  - Considered *low-resource*
- Performance gaps
  - GPT-4 on MMLU: much better in English vs Telugu
  - Math: 3× better in English vs Armenian/Farsi
  - Failed all 6 questions in Burmese & Amharic
- ⚠️ Translation workaround pitfalls
  - Requires good translation model
  - Information loss (e.g., Vietnamese pronouns)
- ⚠️ **Tokenization inefficiency**
  - Burmese: 72 tokens vs English: 7 (median)
  - 10× slower & more expensive
- Non-English models
  - Chinese: ChatGLM, YAYI, Llama-Chinese
  - Others: CroissantLLM (FR), PhoGPT (VI), Jais (AR)

### Domain-Specific Models
- General models cover broad domains via web data
- ⚠️ Weak on specialized tasks unseen in training
- Data acquisition challenges
  - Drug discovery: protein/DNA/RNA data
  - Cancer screening: X-ray, fMRI (privacy-restricted)
- Notable examples
  - 🔑 **AlphaFold** — protein structures
  - **BioNeMo** (NVIDIA) — biomolecular drug discovery
  - **Med-PaLM2** (Google) — medical Q&A
- 💡 Many fields beyond biomedicine could benefit

## Modeling

### Model Architecture
- **Transformer** dominates language models
- Origin: solved seq2seq limitations
  - ⚠️ Bottleneck: only final hidden state passed to decoder
  - ⚠️ Sequential RNN processing → slow

#### Attention Mechanism
- 🔑 **Q (Query)** — current decoder state
- 🔑 **K (Key)** — represents previous tokens (page numbers)
- 🔑 **V (Value)** — actual token content (page contents)
- Computed via **dot product** of Q·K → weights V
- Formula: `softmax(QKᵀ/√d)V`
- **Multi-headed**: parallel attention to different token groups
  - Llama 2-7B: 32 heads × 128 dim = 4096

#### Transformer Block
- **Attention module** — Q, K, V, output projection matrices
- **MLP module** — linear layers + nonlinear activations
  - ReLU, GELU
- **Embedding module** (before blocks) — tokens + positions
- **Output layer / unembedding** (after blocks) → token probabilities

#### Inference: Two Steps
- 📌 **Prefill** — process input tokens in parallel
- 📌 **Decode** — generate output tokens sequentially
- ⚠️ Long sequences → many K/V vectors stored
  - Limits context length extension

#### Alternative Architectures
- **RWKV** — RNN-based, parallelizable
- **State Space Models (SSMs)**
  - **S4** — efficient SSMs
  - **H3** — recall mechanism (attention-like)
  - **Mamba** — linear-time, scales to 3B params
  - **Jamba** — hybrid Transformer–Mamba, 256K context
- ⚠️ Hard to dethrone transformer (heavily optimized since 2017)

### Model Size
- 💡 Three signals of scale
  - **Parameters** — learning capacity
  - **Training tokens** — how much was learned
  - **FLOPs** — training cost
- Memory rule of thumb
  - 7B params × 2 bytes ≈ 14 GB GPU memory
- **Sparse models**
  - Many zero-value params → less compute
  - 🔑 **Mixture-of-Experts (MoE)** — only some experts active per token
    - Mixtral 8×7B: 46.7B total, only 12.9B active per token
- Training token scale
  - Llama 1: 1.4T → Llama 2: 2T → Llama 3: 15T
  - RedPajama-v2: 30T tokens (~450M books)
- Compute measurement
  - 🔑 **FLOP** vs **FLOP/s** (often confused)
  - GPT-3-175B: 3.14 × 10²³ FLOPs
  - 256 H100s @ 70% util ≈ 256 days, ~$4M

#### Chinchilla Scaling Law
- 💡 **Tokens ≈ 20× model parameters** for compute-optimal training
- Double model → double training data
- ⚠️ Optimized for compute, not deployment
  - Llama: smaller-than-optimal for usability
- Cost dynamics
  - ✅ Cost for given performance ↓ over time
  - ⚠️ Cost for *improvement* stays high (last-mile problem)

#### Scaling Extrapolation
- 🔑 Predicting hyperparameters for large models from small ones
- ⚠️ Hard due to combinatorial explosion & emergent abilities
- Microsoft/OpenAI: transferred from 40M → 6.7B model

#### Scaling Bottlenecks
- ⚠️ **Training data exhaustion**
  - Internet data growth slower than dataset growth
  - 📌 Anything you publish may end up in training data
- ⚠️ **AI-generated data contamination**
  - Risk of model collapse via recursive training
- ⚠️ **Electricity / compute**
  - Data centers: 1–2% global electricity → 4–20% by 2030
- Proprietary data → competitive advantage
  - OpenAI deals with Axel Springer, AP
  - Reddit, Stack Overflow restricting scraping

## Post-Training
- 💡 Pre-training optimizes token-level; post-training optimizes response-level
- Two main steps
  - **SFT** — supervised finetuning
  - **Preference finetuning** — RLHF, DPO, RLAIF
- 📌 Only ~2% of compute (vs 98% pre-training)
- Analogy: 🐙 **Shoggoth with smiley face**

### Supervised Finetuning (SFT)
- Goal: make model converse, not just complete
- 🔑 **Demonstration data** = (prompt, response) pairs
  - Also called *behavior cloning*
- Labeler quality matters
  - InstructGPT: ~90% labelers had college degrees
  - Cost: ~$10/pair, ~30 min per long-context sample
- Alternative sources
  - LAION volunteers (⚠️ demographic skew: 90% male)
  - DeepMind heuristics for Gopher
  - AI-generated synthetic data

### Preference Finetuning
- Goal: align with human preferences
- ⚠️ Universal preference may not exist
- Controversial-topic dilemma
  - Too much censorship → boring model
  - Too little → upsets users

#### Reward Model
- Scores (prompt, response) pairs
- 🔑 **Comparison data** = (prompt, winning, losing)
- Pointwise scoring is unreliable; comparison preferred
- Cost (Llama-2): ~$3.50/comparison vs $25/written response
- Inter-labeler agreement: ~73% (InstructGPT)
- Loss objective
  - Maximize score difference between winning & losing
  - `-E[log σ(r(x,yw) - r(x,yl))]`

#### Finetuning with Reward Model
- **PPO** (Proximal Policy Optimization) — classic RLHF
- **DPO** — simpler, used by Llama 3
- **Best of N** — generate many, pick best (Stitch Fix, Grab)

## Sampling

### Fundamentals
- Model outputs **logit vector** → softmax → probabilities
- ⚠️ Greedy sampling → boring outputs
- ✅ Sample by probability distribution

### Sampling Strategies
- 🔑 **Temperature**
  - Higher → more creative, less coherent
  - Lower → more consistent, more boring
  - Recommended: ~0.7 for creative tasks
  - T=0 → pick highest logit (argmax)
- 🔑 **Top-k**
  - Sample only from top-k logits
  - Reduces softmax compute
- 🔑 **Top-p (nucleus)**
  - Cumulative probability threshold (0.9–0.95)
  - Dynamic candidate pool
- **Min-p** — minimum probability threshold
- **Stopping condition**
  - Token limit, stop tokens, EOS
  - ⚠️ Premature stop → malformed JSON
- 💡 **Logprobs** — log-scale probabilities
  - Avoid underflow
  - Useful for classification, evaluation

### Test Time Compute
- 💡 Generate multiple outputs → pick best
- Methods
  - Random sampling (best of N)
  - **Beam search**
  - Vary sampling vars for diversity
- Selection methods
  - Highest average logprob (OpenAI API)
  - Reward model / verifier scoring
  - Application heuristics
  - Most common answer (self-consistency)
- 📊 OpenAI verifier: ~30× model size equivalent boost
- ⚠️ OpenAI: performance peaks ~400 outputs, then declines
- ⚠️ Cost scales with outputs

### Structured Outputs
- Use cases
  - Semantic parsing (text-to-SQL, text-to-regex)
  - Downstream tool consumption (agentic workflows)
- Approaches by AI stack layer
  - **Prompting** — instruction-following dependent
  - **Post-processing** — fix common mistakes (LinkedIn: 90% → 99.99%)
  - **Test time compute** — retry until valid
  - **Constrained sampling** — filter logits by grammar
    - ⚠️ Format-specific, latency overhead
  - **Finetuning** — most reliable
    - Classifier head for fixed classes
- Frameworks
  - guidance, outlines, instructor, llama.cpp
  - OpenAI **JSON mode**

### Probabilistic Nature of AI
- 💡 Same input → potentially different outputs
- ✅ Great for creative tasks
- ❌ Pain for factual/consistent tasks

#### Inconsistency
- Same input → different outputs
- Slightly different input → drastically different output
- Mitigations
  - Cache responses
  - Fix temperature, top-p, top-k, **seed**
  - ⚠️ Hardware can still cause variation

#### Hallucination
- 🔑 Output not grounded in facts
- Hypothesis 1: **Self-delusion** (DeepMind)
  - Model can't distinguish given vs generated text
  - Snowballing — initial wrong assumption compounds
- Hypothesis 2: **Knowledge mismatch** (Leo Gao, Schulman)
  - SFT teaches model to mimic responses with knowledge it lacks
- Mitigations
  - Verification / cite sources
  - Better reward function
  - Concise responses prompt
  - "Say I don't know" prompts
  - RAG, prompt engineering
- ⚠️ RLHF results mixed (InstructGPT: worsened hallucination)

## Key Takeaways
- 💡 **Training data dictates capabilities** — English & high-resource domains dominate by default
- 💡 **Transformer remains king** but SSMs (Mamba, Jamba) are emerging challengers for long-context
- 📌 Three numbers define a model: **parameters, training tokens, FLOPs** — Chinchilla says scale them together (20:1 token:param)
- ⚠️ Scaling bottlenecks ahead: **data exhaustion, electricity, AI-contaminated training corpora**
- 🔑 Post-training (**SFT + preference finetuning**) unlocks pre-trained capabilities — only ~2% of compute, but transforms usability
- 💡 **Sampling** is underrated — temperature, top-k, top-p, and test-time compute can boost performance dramatically with little effort
- 📌 AI is **probabilistic by design** — inconsistency and hallucination are features of the architecture, not bugs to fully eliminate
- ✅ Build workflows around probabilistic nature: caching, structured outputs, verification, evaluation pipelines