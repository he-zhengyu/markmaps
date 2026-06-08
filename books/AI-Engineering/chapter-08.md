---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Dataset Engineering

## Core Idea
- 🔑 **Dataset engineering** — building the data to train/finetune a model
- 💡 *Data-centric* — quality of data often matters more than model tweaks
- 📌 Goal: right **quality**, **coverage**, and **quantity**

## Data Curation
### Data Quality
- ✅ **Relevant** to the target task
- ✅ **Aligned** with desired behavior
- ✅ **Consistent** annotations
- ✅ **Correctly formatted**
- ✅ **Unique** (deduplicated)
- ✅ **Compliant** (privacy, licensing)

### Data Coverage
- 💡 Span the **diversity** of real use cases & input patterns
- ⚠️ Gaps → blind spots in model behavior

### Data Quantity
- Depends on
  - **Finetuning technique** (PEFT needs less than full)
  - **Task complexity**
  - **Base model** capability
- 📌 More isn't always better — quality first

### Data Acquisition and Annotation
- Sources: proprietary, public, purchased
- **Annotation** — human labels; costly but high-signal
- ⚠️ Annotation guidelines drive consistency

## Data Augmentation and Synthesis
### Why Data Synthesis
- ✅ Boost **quantity** & **coverage**
- ✅ **Privacy** — avoid sensitive real data
- ✅ **Distillation** — generate data from a stronger model
- ✅ Lower **cost** than manual annotation

### Traditional data synthesis techniques
- **Rule-based** generation / templates
- **Simulation** of scenarios

### AI-powered data synthesis
- Use an LLM to generate training examples
- **Verifying AI-generated data**
  - ✅ Filter, validate, or use a verifier model
- **Limitations of AI-generated data**
  - ⚠️ Quality ceiling of the generator
  - ⚠️ **Self-bias** — inherits generator's flaws
  - ⚠️ **Model collapse** from recursive synthetic training

## Data Processing
- **Inspect data** — explore distribution, spot issues
- **Deduplicate data** — remove near/exact duplicates
- **Clean and filter data** — drop low-quality, toxic, off-task
- **Format data** — match model's **chat template** / schema

## Key Takeaways
- 💡 **Data quality and coverage** usually beat raw quantity
- Curate for relevance, consistency, uniqueness, and compliance
- **Synthetic data** scales quantity, coverage, and privacy — but must be **verified**
- ⚠️ Beware **self-bias** and **model collapse** from over-reliance on AI-generated data
- ✅ Always inspect, deduplicate, clean, and correctly **format** before training
