---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Ch 20: Designing for Performance

## 20.1 How to think about performance

### Two extremes to avoid
- ❌ Optimizing every statement → slows development, adds complexity
- ⚠️ Many "optimizations" don't actually help performance
- ❌ Ignoring performance entirely → system 5–10x slower than needed
- ⚠️ **"Death by a thousand cuts"** — no single fix helps later

### Best approach: natural efficiency
- 💡 Use basic performance knowledge to pick designs both *clean* and *naturally efficient*
- Develop awareness of **fundamentally expensive operations**

### Expensive operations today
- 📊 **Network round-trips**: 10–50 µs in datacenter (tens of thousands of instructions); 10–100 ms wide-area
- 📊 **Secondary storage I/O**: disk 5–10 ms (millions of instructions); flash 10–100 µs; new NVM ~1 µs (~2000 instructions)
- **Dynamic memory allocation** (`malloc`, `new`): allocation, freeing, GC overhead
- 📊 **Cache misses**: DRAM fetch = few hundred instruction times; often dominates program performance

### Learn costs via micro-benchmarks
- 🔑 **Micro-benchmark**: small program measuring one operation in isolation
- RAMCloud framework: days to build, new benchmark in 5–10 min
- Used to measure existing libraries and new classes

### Choosing cheap operations
- Often the efficient approach is *just as simple*
  - **Hash table vs. ordered map**: hash table 5–10x faster; use it unless ordering needed
  - **Array of structures** (C/C++): store structures in array itself, one allocation ✅ — not pointers requiring per-structure allocation ❌

### When efficiency requires complexity
- Small, hidden complexity (no interface impact) → may be worthwhile
- ⚠️ Complexity is incremental — beware
- Lots of complexity or complicated interfaces → start simple, optimize later
- Clear evidence performance matters → implement faster approach immediately
- RAMCloud: kernel bypass networking for lowest latency, justified by prior measurements
  - 💡 Getting one big issue "right" made many other things easier

### Simplicity → speed
- 💡 Simpler code tends to run faster
- Defined-away special cases → no checking code needed
- **Deep classes** more efficient: more work per method call
- Shallow classes → more layer crossings → overhead

## 20.2 Measure before (and after) modifying

- ⚠️ Programmers' performance intuitions are **unreliable**, even for experts
- ❌ Tweaking by intuition wastes time and adds complexity
- 📌 Measure existing behavior *before* any changes

### Two purposes of measurement
- **Identify** where tuning has the biggest impact
  - Top-level metrics show *that* it's slow, not *why*
  - Measure deeper → find a few specific hot spots with improvement ideas
- **Baseline** for re-measuring after changes

### Post-change rule
- ✅ Re-measure to confirm improvement
- ❌ No measurable gain → back changes out (unless they simplified the system)
- 📌 Never retain complexity without a significant speedup

## 20.3 Design around the critical path

### Prefer fundamental fixes first
- E.g., introduce a **cache**, change algorithm (balanced tree vs. list)
- RAMCloud kernel bypass = fundamental fix
- Redesigning code for speed is a **last resort**

### Imagine "the ideal" code
- 🔑 **Critical path**: minimum code that must execute in the most common case
- Disregard existing code structure and special cases
- Imagine all relevant code in a single method
- Consider only data the critical path needs; pick the most convenient structure
  - E.g., combine multiple variables into a single value
- The ideal = simplest and fastest the code can ever be

### From ideal to real design
- Find a clean design as close to the ideal as possible
- Apply prior design ideas, constrained to keep the ideal (mostly) intact
- OK to add a bit of code for clean abstractions (e.g., a hash table method call)
- 💡 A clean design close to the ideal is almost always achievable

### Remove special cases from critical path
- Each special case adds conditionals/calls → slower code
- ✅ Ideal: a **single if statement** detecting all special cases with one test
- Normal case runs with no further tests
- Special-case handling branches off the path — structure it for *simplicity*, not speed

## 20.4 An example: RAMCloud Buffers

### What Buffers do
- Manage variable-length memory arrays (e.g., RPC request/response messages)
- Reduce memory copying and dynamic allocation overhead
- Appear as a linear byte array, stored as **discontiguous chunks**

### Chunk types
- 🔑 **External chunk**: storage owned by caller; Buffer keeps a reference; used for large data to avoid copies
- 🔑 **Internal chunk**: Buffer owns storage; caller's data is copied in; convenient for small data
- Small built-in allocation; extra allocations created and freed as needed

### Buffer as a fundamental fix
- Eliminates expensive memory copies
- E.g., response = internal header chunk + external chunk referencing large object, no copy

### Why optimize later
- Buffers used increasingly widely — ≥4 Buffers per RPC
- Speeding up Buffer could noticeably improve overall system performance

### Chosen critical path
- Allocate space for small new data in an internal chunk (e.g., message headers)
- Simplest case: enlarge the last chunk (if internal, with room)
- Ideal: one check, then adjust chunk size

### Problems in original code (Buffer::alloc)
- **Too many special cases**: 6 distinct condition tests
  - Checks for existing allocations; room checked twice; allocates without trying to expand last chunk; adjacency merge check
- **Too many shallow layers**
  - Two extra method calls; identical signatures & same abstraction — ⚠️ red flag
  - `Buffer::allocateAppend` nearly a pass-through method
  - Slower *and* more complicated

### The refactoring
- Design centered on the most performance-critical paths (alloc, total length, etc.)
- Eliminated shallow layers, deeper internal abstractions, fewer special cases
- 📊 20% smaller: 1476 lines vs. 1886 original

### New critical path
- Entire path in a **single method**; easier to read
- New variable `availableAppendBytes`: unused space right after last chunk
  - 💡 Zero covers three special cases at once (no space / last chunk not internal / no chunks)
- Trade-off: small `totalLength` update overhead kept, since fetching total length is common and recomputing would be expensive

### Results
- 📊 Append 1-byte string: 8.8 ns → 4.75 ns (~2x faster)
- 📊 Construct + append + destroy: 24 ns → 12 ns
- Many other operations sped up too

## 20.5 Conclusion & Key Takeaways
- 💡 **Clean design and high performance are compatible**
- Buffer rewrite: 2x faster, simpler design, 20% less code
- Complicated code is slow — it does extraneous/redundant work
- Clean simple code is usually fast enough from the start
- 📌 When optimizing: find critical paths and make them **as simple as possible**
- 📌 Measure first; intuition misleads; back out changes that don't measurably help
- 📌 Prefer naturally efficient, simple designs; know what operations are expensive