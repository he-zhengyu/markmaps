---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Inference Optimization

## Understanding Inference Optimization
### Inference Overview
- 🔑 **Inference** — running a trained model to generate outputs
- Two phases
  - **Prefill** — process the prompt (compute-bound, parallel)
  - **Decode** — generate tokens one-by-one (memory-bound, sequential)
- **Inference server** — manages requests, batching, scheduling

### Inference Performance Metrics
- **Latency**
  - 🔑 **TTFT** — time to first token
  - 🔑 **TPOT** — time per output token
- 📊 **Throughput** — tokens/sec across all requests
- **Goodput** — throughput meeting latency targets
- **Cost** & **utilization**
- ⚠️ Latency vs throughput is a fundamental **trade-off**

### AI Accelerators
- **GPU**, **TPU**, and specialized chips
- Key specs
  - **FLOP/s** — compute
  - **Memory bandwidth**
  - **Memory size**

## Inference Optimization
### Model Optimization
- **Model compression**
  - **Quantization** — lower precision
  - **Pruning** — remove weights
  - **Distillation** — train smaller student model
- **Overcoming autoregressive bottleneck**
  - **Speculative decoding** — draft model proposes, target verifies
  - Inference with reference / parallel decoding
- **Attention optimization**
  - 🔑 **KV cache** — reuse past key/value tensors
  - **Multi-query / grouped-query attention**
  - **FlashAttention** — IO-aware attention kernel
- **Kernels & kernel optimization**
  - Vectorization, parallelization, **operator fusion**, tiling

### Inference Service Optimization
- **Batching**
  - **Static**, **dynamic**, and **continuous** batching
  - 💡 Continuous batching keeps GPUs busy across requests
- **Decoupling prefill and decode**
  - Separate resources for the two phases
- **Prompt caching**
  - ✅ Reuse computation for repeated prompt prefixes
- **Parallelism**
  - **Data**, **tensor**, and **pipeline** parallelism

## Key Takeaways
- 💡 Inference splits into **prefill** (compute-bound) and **decode** (memory-bound) — optimize each differently
- Track **TTFT**, **TPOT**, throughput, and **goodput**, not just averages
- **Model-level**: quantization, pruning, distillation, speculative decoding, KV cache, FlashAttention
- **Service-level**: continuous **batching**, **prompt caching**, prefill/decode decoupling, parallelism
- ✅ The biggest wins often come from **batching** and **KV-cache** reuse
