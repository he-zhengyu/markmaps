---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Ch.10: Define Errors Out Of Existence

## 10.1 Why Exceptions Add Complexity
### What Counts as an Exception
- 🔑 **Exception**: any uncommon condition altering normal control flow
- Includes formal throw/catch mechanisms
- Also special return values signaling incomplete behavior
### Sources of Exceptions
- Caller provides **bad arguments** or configuration
- Invoked method **can't complete** (I/O failure, missing resource)
- Distributed systems: lost/delayed packets, unresponsive servers, unexpected peer behavior
- Code detects **bugs** or internal inconsistencies
- 📌 Large/fault-tolerant systems: exception handling is a big fraction of code
### Why Handling Is Hard
- Two ways to respond, both complicated
  - **Move forward** despite exception (resend packet, recover from redundant copy)
  - **Abort & report upward** — must restore consistent state, unwind partial changes
- Exception handling breeds **secondary exceptions**
  - Resent packet may duplicate → new condition for peer
  - Redundant copy may itself be lost
  - ⚠️ Secondary exceptions during recovery are subtler than primary ones
  - Must eventually stop the cascade without new exceptions
### Language Support Is Verbose & Clunky
- Java tweet-deserialization example: 5 catch clauses
- try-catch boilerplate outweighs normal-case code
- Hard to see where each exception originates
- Many small try blocks → broken flow, duplicated handlers
### Hard to Verify
- Some exceptions (I/O errors) hard to generate in tests
- Handler code rarely executes → bugs hide for years
- 💡 "Code that hasn't been executed doesn't work"
- 📊 >90% of catastrophic failures in distributed data-intensive systems caused by incorrect error handling (Yuan et al., OSDI 2014)

## 10.2 Too Many Exceptions
- Programmers over-define exceptions: "more errors detected = better"
- Over-defensive style → proliferation of unnecessary exceptions
### Case Study: Tcl `unset`
- Threw error when variable didn't exist
- Common use: cleaning up unpredictable temporary state
- Forced developers to wrap `unset` in catch-and-ignore
- Author calls it one of his biggest Tcl design mistakes
### Exceptions as Problem-Punting
- ⚠️ Throwing avoids figuring out a clean solution
- If you don't know what to do, the caller likely doesn't either
### Exceptions Are Interface
- Exceptions thrown by a class are **part of its interface**
- Many exceptions → complex interface → **shallower class**
- Exceptions propagate up the stack, affecting multiple interfaces
- 💡 Throwing is easy; handling is hard → reduce **places where handling occurs**
- Four techniques follow (10.3–10.8)

## 10.3 Technique 1: Define Errors Out of Existence
- 🔑 Design APIs so there are **no exceptions to handle**
- Fix for `unset`: redefine from "delete a variable" to "**ensure variable no longer exists**"
- If variable absent → work already done, just return
- 💡 Change semantics so normal behavior covers all cases

## 10.4 Example: File Deletion in Windows vs Unix
### Windows Approach
- ❌ Cannot delete a file open in a process
- Users hunt & kill processes, sometimes reboot just to delete
### Unix Approach
- ✅ Open file marked for deletion; delete returns success
- Name removed from directory; new same-name file can be created
- Open processes keep reading/writing normally
- Data freed once all processes close the file
### Two Errors Defined Away
- Delete no longer fails when file is in use
- No new exceptions forced on processes using the file
  - Alternative (invalidate opens) would create new errors
- 💡 Doomed-file access never caused significant problems in practice

## 10.5 Example: Java `substring` Method
### The Problem
- Out-of-range index → `IndexOutOfBoundsException`
- Common need: extract characters overlapping a range
- ⚠️ One-line call balloons to 5–10 lines of index clamping
### The Fix
- Redefine: "return characters with index ≥ beginIndex and < endIndex"
- Well-defined for negative indexes or beginIndex > endIndex
- ✅ Simpler API **plus** more functionality → **deeper method**
- Python precedent: out-of-range slices return empty result
### "But Errors Catch Bugs!" Objection
- Error-ful approach may catch some bugs
- ❌ But adds complexity → extra avoidance code → more bugs
- ❌ Or forgotten checks → unexpected runtime errors
- 💡 The best way to reduce bugs is to make software **simpler**

## 10.6 Technique 2: Mask Exceptions
- 🔑 Detect & handle at low level so higher levels never see it
- Common in distributed systems
### Example: TCP
- Packets dropped (corruption, congestion)
- TCP resends internally; clients unaware of loss
### Example: NFS (controversial)
- Server crash → client retries indefinitely; app just hangs
- Console: "NFS server xyzzy not responding still trying"
- Why hanging beats throwing exceptions
  - Apps can't do much without their files
  - Retry belongs in one place (NFS layer), not every file call
  - Aborting would cascade → collapse of user's environment
  - Apps resume seamlessly when server returns; users can kill apps manually
### Properties
- ✅ Deeper classes: smaller interface + more functionality
- 💡 An example of **pulling complexity downward**
- ⚠️ Doesn't work in all situations

## 10.7 Technique 3: Exception Aggregation
- 🔑 Handle many exceptions with **one handler** in one place
### Example: Web Server Missing Parameters
- ❌ Naive: separate handler around each `getParameter` call → duplicated code (Fig 10.1)
- ✅ Better: let `NoSuchParameter` propagate to top-level dispatcher; single handler builds error response (Fig 10.2)
- Extends to all error-response conditions (bad syntax, no permission)
  - Error message generated at throw site, carried in exception
  - Top handler extracts message into response
### Encapsulation Benefits
- Top handler knows response format, not specific errors
- `getParameter` knows extraction + human-readable messages, not HTTP
- New methods plug in via shared exception superclass — no other changes
### General Design Pattern
- 📌 Define an exception that aborts current request, cleans state, continues with next
- Caught once near top of request loop; subclasses for different conditions
- Distinguish clearly from system-fatal exceptions
### Aggregation vs Masking
- Aggregation: exception propagates **up** several levels → one high handler
- Masking: handled **low**, in shared library methods
- 💡 Both position the handler where it catches the most exceptions
### Example: RAMCloud Crash Recovery
- Replicated storage; recovers lost server data from copies
- **Error promotion**: corrupted object → crash the whole server
  - Server-crash recovery unavoidable anyway → reuse one mechanism
  - Less recovery code; recovery runs more often → bugs found & fixed
- ⚠️ Promotion raises recovery cost — fine only for rare errors
  - ❌ Can't crash a server per lost network packet
- 💡 Replaces special-purpose mechanisms with one **general-purpose** mechanism

## 10.8 Technique 4: Just Crash
- Some errors: hard/impossible to handle, rare → print diagnostics and abort
### Example: Out of Memory
- C `malloc` returns NULL → every caller must check
  - Forgotten checks → null dereference crash camouflaging real problem
- App can't do much: freeable memory would already be freed
- Memory exhaustion today usually indicates a bug
- ✅ Fix: `ckalloc` wrapper — checks result, aborts with message
- C++/Java `new` throws, but handler would likely fail allocating too
### Other Crash-Worthy Errors
- I/O error on open file (disk hard error)
- Network socket cannot be opened
- Internal inconsistencies (likely program bugs)
### Application-Dependent
- ⚠️ Replicated storage system must NOT abort on I/O error
- Recovery complexity is essential value there

## 10.9 Taking It Too Far
- Define-away/masking only valid if info **isn't needed** outside the module
- Counter-example: student module masked **all** network exceptions
  - Apps couldn't detect lost messages or dead peers
  - ❌ Impossible to build robust applications
- 📌 Must expose exceptions when the information is important
- 💡 Hide what's unimportant (the more the better); expose what matters (see Ch. 21)

## 10.10 Conclusion
- Special cases make code harder to understand, breed bugs
- Best: **redefine semantics** to eliminate error conditions
- Otherwise: **mask** at low level, or **aggregate** into one generic handler
- Together these significantly cut system complexity

## Key Takeaways
- 💡 Reduce the number of **places** exceptions must be handled
- Four techniques: define away → mask → aggregate → just crash
- Exceptions are interface: fewer exceptions → deeper classes
- Simplicity, not more error-checking, is the best bug prevention
- ⚠️ Never hide exceptions whose information callers genuinely need