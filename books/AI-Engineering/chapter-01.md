---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Building AI Applications with Foundation Models

## The Rise of AI Engineering
### From Language Models to LLMs
- 🔑 **Language Model** — encodes statistical info about languages
  - Predicts likelihood of words in context
  - Roots: Shannon's 1951 *"Prediction and Entropy of Printed English"*
- 🔑 **Token** — basic unit (character, word, or word-part)
  - **Tokenization** — breaking text into tokens
  - **Vocabulary** — set of all tokens model knows
  - GPT-4: ~100,256 tokens; Mixtral 8x7B: 32,000
  - 💡 Tokens balance meaning (vs. characters) and efficiency (vs. words)
- **Two Types**
  - **Masked LM** (e.g., BERT)
    - Predicts missing tokens using *both* sides of context
    - Used for sentiment analysis, classification, code debugging
  - **Autoregressive LM**
    - Predicts next token using *only preceding* tokens
    - 📌 Default choice for text generation
- 💡 **Completion Machine** — many tasks (translation, summarization, classification) reframe as completion
  - ⚠️ Completions are *probabilistic*, not guaranteed correct

### Self-Supervision
- 🔑 **Self-supervision** — model infers labels from input data itself
- ❌ **Supervision** — needs labeled data (expensive, slow)
  - AI-added: ImageNet labeling cost ~$50K for 1M images
- ✅ Each text sequence yields many training samples
- 💡 Unlocks scaling — text is everywhere on the internet
- **Parameter** — variable updated during training
  - GPT-1 (2018): 117M → considered large then
  - GPT-2 (2019): 1.5B
  - Today: 100B+ is "large"
- 📌 Larger models need more data to maximize performance

### From LLMs to Foundation Models
- 🔑 **Foundation Model** — multimodal, general-purpose, built upon for many needs
- **Multimodal Models (LMMs)**
  - Process text + image + video + audio + 3D, etc.
  - GPT-4V, Claude 3, Gemini
- **CLIP** — language-image embedding model (OpenAI, 2021)
  - Used **natural language supervision**
  - 400M (image, text) pairs from internet — no manual labeling
- 💡 Shift from **task-specific** → **general-purpose** models
- **Adaptation Techniques**
  - **Prompt Engineering** — instructions + examples
  - **RAG** — retrieval-augmented generation
  - **Finetuning** — further training on task data

### From Foundation Models to AI Engineering
- 🔑 **AI Engineering** — building applications on top of existing foundation models
- **Three Enabling Factors**
  - 📊 **General-purpose AI capabilities** — more tasks possible
  - 📊 **Increased AI investment** — projected ~$200B globally by 2025
  - ✅ **Low entry barrier** — model-as-a-service APIs, plain-English prompts
- 📊 AI tools (AutoGPT, LangChain, Ollama) outpacing React/Vue in GitHub stars
- 💡 *"Teaching AI to behave is the fastest-growing career skill"* — ComputerWorld

## Foundation Model Use Cases
### Coding
- 📌 Most popular generative AI use case
- GitHub Copilot — $100M ARR within 2 years
- Specialized tasks: text-to-SQL, screenshot-to-code, code translation, doc generation, test creation
- 📊 McKinsey: 2× productivity on docs, 25–50% on code gen
- ⚠️ Less helpful for highly complex tasks
- 💡 AI better at frontend than backend

### Image & Video Production
- Midjourney, Adobe Firefly, Runway, Pika, Sora
- Midjourney — $200M ARR at 1.5 years old
- Enterprise: ad generation, A/B testing variants, seasonal/locale variations
- AI-generated headshots, profile photos

### Writing
- Email, social posts, blog posts, books
- 📊 MIT study: ChatGPT cut writing time 40%, raised quality 18%
- Enterprise: sales outreach, marketing copy, SEO, performance reports
- ⚠️ AI-generated content farms flooding the web

### Education
- Personalized lecture plans, adaptive formats
- Language learning roleplay (Duolingo)
- AI tutors, debate partners, quiz generation
- ⚠️ Disrupting incumbents (Chegg stock fell from $28 → $2)

### Conversational Bots
- General chatbots, AI companions, digital partners
- Enterprise: customer support, product copilots
- Voice assistants, 3D NPCs in games (Inworld, Convai)

### Information Aggregation
- 📊 74% of generative AI users use it to summarize (Salesforce 2023)
- Talk-to-your-docs, meeting/email/Slack summarization
- Instacart's "Fast Breakdown" template

### Data Organization
- Search across photos, videos, PDFs
- Auto-extract from receipts, contracts, IDs
- 📊 IDP industry projected $12.81B by 2030

### Workflow Automation
- Booking, refunds, trip planning, form filling
- Enterprise: lead mgmt, invoicing, data entry
- 🔑 **Agents** — AI that plans and uses external tools

## Planning AI Applications
### Use Case Evaluation
- **Why build?** (risk-ordered)
  - ⚠️ Existential threat from AI-enabled competitors
  - ✅ Boost profits and productivity
  - 💡 Avoid being left behind (R&D investment)
- **Role of AI vs. Humans**
  - **Critical vs. Complementary** — higher reliability bar if critical
  - **Reactive vs. Proactive** — proactive needs higher quality bar
  - **Dynamic vs. Static** — personalization vs. periodic updates
  - **Human-in-the-loop** — Microsoft's *Crawl-Walk-Run* framework
- **Defensibility — three moats**
  - **Technology** — mostly commoditized
  - **Data** — usage data builds flywheel
  - **Distribution** — favors big incumbents
  - ⚠️ Risk of being subsumed by underlying model upgrades

### Setting Expectations
- **Business Metrics** — % automation, throughput, response time, labor saved
- **Usefulness Threshold**
  - Quality metrics
  - Latency: 🔑 **TTFT**, 🔑 **TPOT**, total latency
  - Cost per inference
  - Interpretability, fairness

### Milestone Planning
- ⚠️ **Last-mile challenge**
  - 💡 *"0 to 60 is easy; 60 to 100 is exceedingly challenging"* (UltraChat)
  - LinkedIn: 1 month to 80%, 4 more months to 95%
- Demo ≠ Product

### Maintenance
- ⚠️ AI moves fast — must constantly re-evaluate
- Costs dropping rapidly, capabilities growing
- Easier: API convergence enables model swaps
- ⚠️ Harder: regulations (GDPR ~$9B compliance), export controls, IP uncertainty

## The AI Engineering Stack
### Three Layers
- **Application Development** *(top)*
  - Prompts, context, evaluation, interfaces
  - 📌 Most growth in 2023
- **Model Development** *(middle)*
  - Modeling, training, dataset engineering, inference optimization
- **Infrastructure** *(bottom)*
  - Serving, compute/data management, monitoring
  - Slower growth — needs persist across model generations

### AI Engineering vs. ML Engineering
- **3 Key Differences**
  - 💡 Use existing models vs. train from scratch → focus on **adaptation**
  - ⚠️ Bigger models → more inference optimization, GPU/cluster expertise
  - ⚠️ Open-ended outputs → evaluation is much harder
- **Adaptation Categories**
  - ✅ **Prompt-based** — no weight changes; easier, less data
  - ✅ **Finetuning** — updates weights; more data, better quality

### Model Development Layer
- **Modeling & Training**
  - 🔑 **Pre-training** — from scratch; ~98% of compute (InstructGPT)
  - 🔑 **Finetuning** — continue training a trained model
  - 🔑 **Post-training** — same as finetuning, framed from model-developer side
  - ⚠️ Prompt engineering ≠ training
- **Dataset Engineering**
  - Open-ended annotation harder than close-ended
  - Unstructured data focus: dedup, tokenization, retrieval, quality control
  - 💡 *"Models are commodities; data is the differentiator"*
- **Inference Optimization**
  - 📌 Increasingly critical with autoregressive generation
  - Target: ~100ms latency
  - Techniques: quantization, distillation, parallelism

### Application Development Layer
- **Evaluation**
  - 📌 Needed throughout adaptation lifecycle
  - ⚠️ Open-ended outputs lack ground truth
  - ⚠️ Same model performs differently across techniques (Gemini CoT@32 vs 5-shot example)
- **Prompt Engineering & Context Construction**
  - Instructions + context + tools + memory management
- **AI Interface**
  - Standalone apps, browser extensions, chat integrations, plug-ins/APIs
  - Voice, embodied (AR/VR) interfaces emerging
  - 💡 Conversational interfaces ease feedback collection but harden extraction

### AI Engineering vs. Full-Stack Engineering
- 💡 Build product first, invest in data/models once it shows promise
- Python still dominant; JS/TS rising (LangChain.js, Vercel AI SDK)
- AI engineers more involved in product decisions than traditional ML engineers

## Key Takeaways
- 💡 **Foundation models lower the barrier** — anyone can build AI apps without training a model
- 📌 AI engineering = **adaptation + evaluation**, not modeling from scratch
- 🔑 Three adaptation tools: **prompt engineering**, **RAG**, **finetuning** — pick by data, complexity, and quality needs
- ⚠️ **Last-mile is brutal** — 0→80% is fast, 80→95% takes months
- 💡 Defensibility comes from **data flywheel + distribution**, rarely from technology alone
- 📌 Evaluation is the hardest unsolved problem due to open-ended outputs
- ✅ Many ML engineering principles still apply; new challenges layer on top
- ⚠️ Plan for **fast change** — model prices, capabilities, and regulations shift overnight