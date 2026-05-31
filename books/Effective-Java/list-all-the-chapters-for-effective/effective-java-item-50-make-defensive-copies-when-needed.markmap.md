# Item 50: Make defensive copies when needed

## Core idea

- Protect internal state from external mutation
- Copy mutable inputs and outputs at API boundaries
- Preserve invariants even when callers hold references
- Prefer immutability when possible

## The problem

- Java passes object references by value
- A caller can mutate an object after passing it to you
- Returning internal mutable objects exposes representation
- Invariants can be broken without calling your public methods
- Bugs often look like random state corruption

## When defensive copies are needed

- Constructor receives mutable objects
- Setter receives mutable objects
- Getter returns mutable internal state
- Method stores an argument for later use
- Method exposes arrays, collections, dates, buffers, or builders
- Class promises immutability but contains mutable components

## Mutable input parameters

- Copy before storing
- Validate the copied value when mutation race is possible
- Avoid keeping caller-owned references
- Do not assume callers are well-behaved
- Do not assume callers are single-threaded

## Mutable return values

- Return a copy, not the internal object
- For arrays, return `array.clone()` or another fresh array
- For collections, consider immutable copies
  - `List.copyOf`
  - `Set.copyOf`
  - `Map.copyOf`
- Be clear whether returned collection is snapshot or live view

## Copy-before-validate rule

- For mutable inputs, copy first
- Then validate the copy
- Reason
  - Caller could mutate between validation and copying
  - This is a time-of-check/time-of-use risk
- Exception
  - If copying itself requires preliminary null checks
  - Use `Objects.requireNonNull` before copy if needed

## Prefer immutable components

- Use immutable classes instead of mutable legacy types
- Prefer `Instant`, `LocalDate`, `LocalDateTime` over mutable date-like designs
- Prefer value objects
- Prefer unmodifiable state at construction
- Prefer records only when component mutability is acceptable or controlled

## Collections

- `Collections.unmodifiableList`
  - Wrapper around existing collection
  - Still reflects changes to backing collection
- `List.copyOf`
  - Snapshot-style immutable copy
  - Better for defensive ownership
- Returning internal collection
  - Usually wrong for immutable classes
  - Can be acceptable for documented live views in mutable APIs

## Arrays

- Arrays are always mutable
- Never expose internal arrays directly from immutable classes
- Copy on input and output
- Be careful with arrays of mutable elements
  - Shallow copy protects array structure
  - Does not protect element objects
- Deep copy if element mutation can violate invariants

## `clone`

- Avoid relying on `clone` for untrusted non-final classes
- A malicious subclass can return an unexpected object
- Prefer copy constructors or static factories when available
- Array `clone` is generally safe for copying array structure

## Serialization risk

- Deserialization can bypass constructors
- Validate and defensively copy in deserialization hooks
- Treat serialized input as untrusted
- Preserve invariants after `readObject`

## API design choices

- Immutable snapshot
  - Caller cannot affect internal state
  - Clear and safe
- Live view
  - Reflects current state
  - Must be explicitly documented
  - Often needs controlled mutation rules
- Ownership transfer
  - Caller promises not to mutate
  - Rarely safe for public APIs
  - More plausible in package-private performance paths

## Cost trade-offs

- Copies allocate memory
- Copies cost CPU
- Safety usually dominates for public APIs
- Avoid copies only when all are true
  - Class is package-private or tightly controlled
  - Caller ownership is clear
  - Performance pressure is measured
  - Documentation is explicit

## Checklist

- Does the class claim immutability?
- Are constructor arguments mutable?
- Are mutable arguments stored?
- Are mutable internals returned?
- Are collection wrappers true copies or live wrappers?
- Are arrays copied?
- Are mutable elements also protected if needed?
- Is serialization preserving invariants?

## Typical failure modes

- Returning an internal array
- Storing caller-owned collection directly
- Using unmodifiable wrapper around caller-owned collection
- Validating before copying mutable arguments
- Forgetting deep copy when elements are mutable
- Trusting `clone` from an unknown class
- Optimizing away copies without measurement

