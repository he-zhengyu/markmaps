---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Software Fault Isolation: WebAssembly

## Goal & Motivation
- Run **fast code** in web applications
  - JavaScript universally supported, but poor fit for:
    - High-performance code
    - Non-JS source languages
- 🔑 **Isolation** is the core challenge
  - ❌ Cross-site data tampering
  - ❌ Tampering with user's computer

## Why Another Isolation Mechanism?
- Existing mechanisms have limits
  - ⚠️ Some need **special privileges** (root for chroot, UIDs)
  - ⚠️ Some are **platform-specific**
    - Firecracker → Linux only
    - VMs → need hardware virtualization support
  - ⚠️ Some need **admin pre-configuration**
    - Containers (Docker/LXC), virtual net interfaces, UID namespaces
- 💡 **Software Fault Isolation (SFI)** answer
  - ✅ No hardware/OS support required
  - ✅ No special privileges to deploy
  - ✅ Resilient to some hw/os bugs
  - ⚠️ Requires **developer–device cooperation**
    - ❌ Cannot isolate an existing binary (unlike containers/VMs)

## WebAssembly as Modern SFI
- 🔑 **Wasm** — modern SFI system
- Runs anywhere
  - Command-line: `wasmtime main.wasm`
  - Whole apps (e.g. Python 3.12)
  - In-browser via `python -m http.server`
- 💡 Memory corruption in source (e.g. `memset`) is **caught** at runtime/browser

## Wasm Module Structure
- **Functions** — all module code
- **Globals** — global variables
- **Tables** — function-pointer targets
- **Memory** — contiguous `0`→`sz`
- **Imports / Exports** — share functions
- Inspect with `wasm2wat lib.wasm`

## Workflow
- App code (e.g. **C**)
  - → compiler emits **Wasm module**
    - → runtime (`vWasm`, `rWasm`, ...) → **native code**

## Threat Model & Guarantees
- 📌 Adversary may run **any** module function
- ❌ Must not access memory outside its sandbox

## Core Tension: Performance + Isolation
- Interpreter approach (JS-style, or qemu/x86)
  - ✅ Enforces boundary
  - ❌ Too slow
- Naive native isolation
  - Add **bounds check** before every access
  - ⚠️ Performance: too many checks
  - ⚠️ Security: code could **jump past** the check
- Why raw x86 is hard
  - Prevent **syscalls** + out-of-module memory
  - ⚠️ Computed jumps & computed addresses unknowable statically
  - ⚠️ Variable-length x86 instructions hide syscalls

## Why Wasm Beats Raw x86
- 💡 Clever design enables a **simple, secure, fast** compiler
- **Separate structured from unstructured data**
  - Code not accessible as data
  - Stack/locals/globals → no bounds-check needed
  - Only **pointer→memory** access needs checking
  - Pointer-accessed structures must live in memory
- **Structured control flow**
  - No address of arbitrary instruction
  - Scoped blocks; jumps only via predefined tables
  - 💡 Impossible to jump past a check
- SFI possible for x86/ARM too (e.g. **NaCl**)
  - ⚠️ More complex, slower, not portable

## Compilation to Native Code
- 💡 Aim for **one Wasm op → one native instruction** (arithmetic)
  - NaN float ops → **non-deterministic** (hardware bit differences)
- Be careful with **state** & **control flow**
  - State must stay inside module
  - Control flow only to "properly translated" code

## Bounds-Checking State (vWasm style)
- Accessible state: **stack values, locals, globals, heap**
- **Globals**
  - Count known at compile time → check offset statically
  - Arbitrary values fine; isolation ≠ value-dependent
- **Locals** (include call arguments)
  - Fixed count per function → static offset check
  - ⚠️ Recursion → must target current invocation's frame
  - Stored on native stack, interleaved with stack values
- **Stack locations**
  - 💡 Structured control flow → **known stack depth** everywhere
    - Converging control flow must agree on stack contents
    - Compile-time max-access bound
    - Locate locals by skipping known stack values
    - Runtime checks for stack exhaustion on entry
  - ⚠️ Must not corrupt saved return addresses / registers
- **Heap memory operations**
  - `i64.store` → addresses `A`..`A+7` must be in-region
  - Pattern: `if a+8 >= memsz { panic }; store`
  - ✅ Coalesce repeated checks (one check, four stores)

## Virtual-Memory Bounds-Check Trick
- Spec: memory ≤ **4GB**; address is 32-bit unsigned + static offset
- 💡 Effective address = `membase + address + offset` (≤ **8GB** out)
- Reserve **8GB** virtual region → OOB hits a **page fault**
- ⚠️ Trade-offs
  - Not fully deterministic (slightly-OOB may not stop)
  - Address **masking** alt: truncates OOB write → in-bounds corruption (safe, becomes correctness bug)

## Memory Safety Within a Module
- ⚠️ C→Wasm can still have **buffer overflow**
- Heap corruption possible *inside* sandbox
- ✅ But cannot affect the rest of the **system**

## Type Checking
- **Value types** (`i32` vs `i64`)
  - Enables load/store optimizations
- **Function types** (argument count)
  - Args are like locals → function modifies that many stack slots
  - ⚠️ Caller must supply enough args, or function reads/writes other slots (e.g. native return address)

## Control Flow Integrity (CFI)
- **Direct jumps** → compiler targets proper compiled code
- **Function calls** → set up stack as target expects
  - Args + return address at bottom of stack after call
  - Type safety ensures correct argument count
- **Indirect calls** → `call_indirect` via **table** of valid targets

## rWasm Runtime
- 💡 Compiles Wasm module → **Rust** code
  - Generated `add` → `func_1`, `memwrite` → `func_3`
  - Rust slice `&[u8]` `get`/`get_mut` checks bounds
- ✅ All generated code is **safe Rust** → no OOB possible
- Inspectable generated source
- ⚠️ Compilation times **prohibitively slow**
- Why Rust?
  - Other targets work too (JS, Python — slow; Go — decent)
  - ✅ Strong type system catches issues at **compile time** (vs runtime in JS/Python)
  - ✅ `#![forbid(unsafe_code)]` shrinks the trusted code

## Adoption & Ecosystem
- Browsers: Firefox, Chrome, Safari, Edge, mobile
- Serious apps: **Photoshop, Figma, Google Earth**
- Active proposals: threads, vector instructions
- Beyond the browser
  - CDNs: **Fastly**, **Cloudflare Workers** (low-overhead starts; compile once)
  - Cloudflare also uses JS-level sandboxing
  - **WASI** — standard system interface

## Real-World Vulnerabilities
- 💡 Bugs live in the **compiler/runtime**, not the design
- **Fastly compiler bug**
  - 32-bit optimization omitted truncation
  - Reloading register from stack **sign-extended** wrongly
    - `0x80000000` → `0xffffffff80000000`
  - ⚠️ Address subtracted from base instead of added
- **Wasmtime 64-bit bug** (`GHSA-ff4p-7xrq-q5r8`)
  - Bitshift translated as **64-bit** shift
  - 32-bit register grew → access >4GB OOB
- 💡 Reduce **TCB** with a **verifier**
  - Smaller than the compiler, yes/no on output
  - e.g. **VeriWasm** for Lucet/Wasmtime
- Reduce cost of **domain-transition** further (research)

## Key Takeaways
- 💡 **SFI / language-level isolation** builds strong sandboxes independent of OS/HW
- ✅ Can be **lower overhead** than OS/HW isolation (cheaper context switches)
- 🔑 Wasm separates **structured data + control flow** so checks are simple and unbypassable
- 📌 Only **pointer→memory** accesses need runtime bounds checks; VM tricks make them nearly free
- ⚠️ Sandbox stops escapes, **not** intra-module memory bugs (C overflows still possible)
- ⚠️ Security ultimately rests on a **correct compiler/runtime** — verifiers (VeriWasm) shrink the trusted base