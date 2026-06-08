---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# RAG and Agents

## Core Idea
- 💡 Best AI apps **augment** a model with information & tools
- 🔑 Addresses key limit — model knowledge is **frozen at training time**
- Two patterns
  - **RAG** — give access to external *data*
  - **Agents** — give *tools* to gather info & act

## RAG
- 🔑 **Retrieval-Augmented Generation** — enhance generation with retrieved external info
- 💡 Not just "external data" — it's about **constructing the most relevant context** for a query
- ✅ Update memory without retraining → up-to-date knowledge

### RAG Architecture
- Two components
  - **Retriever** — fetches info from external memory
  - **Generator** — produces response from retrieved context
- 📌 System quality depends on **retriever quality**
- Retriever functions
  - **Indexing** — preprocess data for fast retrieval
  - **Querying** — fetch relevant data at request time

### Retrieval Algorithms
#### Term-based retrieval
- 🔑 *Lexical / keyword* search — match exact terms
- **TF-IDF** — term frequency × inverse document frequency
- **BM25** — refined TF-IDF, widely used (`Elasticsearch`)
- ✅ Fast, cheap, interpretable
- ⚠️ Misses synonyms / paraphrases

#### Embedding-based retrieval
- 🔑 *Semantic* search — match by **meaning**, not words
- Compute **embeddings** of query & documents
- **Vector database** stores embeddings, runs vector search
- Framed as **nearest-neighbor** search
  - **ANN** (approximate NN) for speed
  - Algorithms: `HNSW`, `IVF`, `PQ`, `LSH`, `Annoy`
- 💡 **Hybrid search** = term-based + embedding-based

#### Combining retrieval algorithms
- 🔑 **Hybrid search** — term-based + embedding-based
- **Sequential** — cheap retriever → rerank with precise one
- **Ensemble** — run in parallel, fuse rankings
- **Reciprocal Rank Fusion (RRF)** — combine rankings by reciprocal rank

#### Evaluating retrieval
- 📊 **Context precision** — fraction of retrieved that's relevant
- 📊 **Context recall** — fraction of relevant that's retrieved
- Ranking metrics — **NDCG**, **MAP**, **MRR**
- Embedding quality — **MTEB**; retrieval harness — **BEIR**

### Retrieval Optimization
- **Chunking strategy**
  - Split by fixed length, sentence, paragraph, or recursively
  - ⚠️ Small chunks → precise but lose context; large → context but noisy
- **Reranking**
  - Cheap retriever fetches candidates → costly model reorders
- **Query rewriting**
  - Reformulate query; resolve references in conversation
- **Contextual retrieval**
  - Augment chunks with metadata, titles, tags, summaries

### Retrieval Beyond Texts
- **Multimodal RAG** — retrieve images & other modalities
- **Tabular data** — often via **text-to-SQL**

## Agents
- 🔑 **Agent** — perceives its *environment* and *acts* upon it
- Defined by its **environment** + set of **actions**
- ⚠️ Errors **compound** across steps → needs **strong models**

### Agent Overview
- Actions are extended by the **tools** it can use
- **Tools** let it perceive (read) and act (write)
- **Planning** breaks complex tasks into steps

### Tools
- 🔑 **Tool inventory** — the set of tools available
- Categories
  - **Knowledge augmentation** — retriever, web search, SQL executor
  - **Capability extension** — calculator, calendar, code interpreter
  - **Write actions** — send email, execute transactions
- ⚠️ More tools = more power but harder to use well

### Planning
- **Plan generation**
  - 💡 *Decouple* planning from execution — generate → validate → execute
  - Often via **function calling**
- **Reflection & error correction**
  - Agent evaluates its own outputs, self-corrects
  - **ReAct** — interleave **rea**soning + **act**ing
- **Tool selection**
  - Depends on task; tune by trying tool combinations

### Memory
- Store & retrieve info across steps
- **Short-term** — context window
- **Long-term** — external storage
- **Memory management** — what to keep vs evict

## Key Takeaways
- 💡 RAG and agents both fix the same problem: a model's knowledge is **bounded by training data**
- **RAG** = construct the best *context*; quality is dominated by the **retriever**
- Modern retrieval blends **term-based** (BM25) and **embedding-based** (vector) search, plus **reranking**
- **Agents** = model + **tools** + **planning** + **memory**; power grows with tools but so does error compounding
- ✅ Decouple planning from execution and add **reflection** to make agents robust
