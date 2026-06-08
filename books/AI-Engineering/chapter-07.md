---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Finetuning

## Finetuning Overview
- 🔑 **Finetuning** — adapt a pretrained model by continuing training on task data
- A form of **transfer learning** / post-training
- 💡 Changes the **model itself**, unlike prompting or RAG
- ⚠️ Memory-intensive at foundation-model scale → motivates efficient techniques

## When to Finetune
### Reasons to Finetune
- ✅ Improve **quality** on a specific task / domain
- ✅ Enforce **structured output** or style
- ✅ **Distill** a large model into a smaller, cheaper one
- ✅ Mitigate bias or undesired behaviors

### Reasons Not to Finetune
- ❌ Try **prompting** and **RAG** first — cheaper, faster
- ⚠️ Cost of data, compute, and ongoing **maintenance**
- ⚠️ Risk of degrading **general** capabilities

### Finetuning and RAG
- 💡 **RAG** adds *information*; **finetuning** changes *behavior/form*
- Knowledge gaps → RAG
- Output format / tone / skill → finetuning

## Memory Bottlenecks
### Backpropagation and Trainable Parameters
- Training stores **gradients** for every trainable parameter
- 📌 Reducing trainable params cuts memory sharply

### Memory Math
- Memory consumers
  - **Model weights**
  - **Activations**
  - **Gradients**
  - **Optimizer states** (Adam needs extra copies)
- 📊 Full finetuning needs **many× model size** in memory

### Numerical Representations
- 🔑 Formats: `FP32`, `FP16`, `BF16`
- Trade **precision** vs **memory/speed**

### Quantization
- 🔑 Reduce numerical precision (e.g. to `INT8`/`INT4`)
- **Post-training quantization** common for inference
- ✅ Less memory; ⚠️ possible quality loss

## Finetuning Techniques
### Parameter-Efficient Finetuning (PEFT)
- 💡 Update **few parameters**, freeze the rest
- **Partial finetuning** — train only some layers
- **Adapter-based methods** — insert small trainable modules

### LoRA
- 🔑 **Low-Rank Adaptation** — add trainable low-rank matrices
- **Reparameterization** — `W + A·B`, original weights frozen
- **Serving LoRA** — swap or merge adapters per task
- **QLoRA** — LoRA on a **quantized** base model
  - ✅ Finetune large models on limited hardware

### Model Merging and Multi-Task Finetuning
- Combine multiple finetuned models into one
- **Approaches** — weight summing, layer stacking, concatenation
- ✅ One model serving multiple tasks

### Finetuning Tactics
- **Frameworks & base models** — pick stable framework + right base
- **Hyperparameters**
  - Learning rate, batch size, epochs
  - Prompt loss weight

## Key Takeaways
- 💡 Finetune only **after** prompting and RAG fall short — it's the costliest option
- Use **RAG for knowledge**, **finetuning for behavior/form**
- **Memory** is the core bottleneck; weights + activations + gradients + optimizer states
- **PEFT / LoRA / QLoRA** make finetuning large models feasible on modest hardware
- ✅ Quantization and low-rank methods trade a little quality for large memory savings
