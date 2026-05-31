# Item 54: Return empty collections or arrays, not nulls

## Core idea

- Return an empty collection or array when there are no results
- Do not return null to mean "empty"
- Make caller code simple, safe, and uniform

## Why null is harmful here

- Forces special-case checks
- Increases `NullPointerException` risk
- Makes loops and streams awkward
- Obscures the method contract
- Pushes defensive burden onto every caller

## Collections

- Return empty immutable collections for no results
- Common choices
  - `Collections.emptyList`
  - `Collections.emptySet`
  - `Collections.emptyMap`
  - `List.of`
  - `Set.of`
  - `Map.of`
- Prefer immutable empties unless mutation is explicitly promised
- Avoid returning null for "no elements"

## Arrays

- Return a zero-length array
- Zero-length arrays are normal values
- Callers can iterate safely
- Can reuse a constant empty array when appropriate
- Be careful with exposing mutable array constants

## Performance

- Empty collections are cheap
- Shared immutable empty collections avoid allocation
- Zero-length arrays are usually cheap
- Do not use null for performance without measurement
- Simpler caller code often matters more than tiny allocation concerns

## API consistency

- A method returning many values should always return a container
- Empty result is a valid container state
- Null should mean "no container exists" only in rare, well-documented designs
- Prefer consistent behavior across related methods

## Optional comparison

- `Optional<T>` can represent absence of a single scalar result
- `Collection<T>` already represents zero-or-more results
- Avoid `Optional<List<T>>` for ordinary empty-result cases
- Empty collection is usually clearer than optional collection

## Mutability contract

- If returned collection is immutable, document or make it expected
- If caller must mutate result, return a new mutable collection
- Do not return shared mutable empties
- Avoid returning internal mutable collections directly

## Caller experience

- Good
  - `for (Item item : items())`
  - `items().isEmpty()`
  - `items().stream()`
- Bad
  - `if (items() != null)`
  - duplicated null checks
  - defensive wrappers at every call site

## Error vs empty

- Empty means the operation succeeded with no results
- Exception means operation failed
- Null should not blur this distinction
- Example distinctions
  - no matching records -> empty list
  - database unavailable -> exception
  - invalid query -> exception

## Interoperability

- Most Java APIs expect non-null collections
- Streams work naturally with empty collections
- Serialization and JSON output are clearer with empty arrays/lists
- Frameworks often distinguish null from empty in surprising ways

## Checklist

- Does the method return multiple values?
- Is "no result" a normal successful outcome?
- Can caller iterate without null check?
- Is mutability policy clear?
- Is empty distinct from failure?
- Are related methods consistent?
- Is `Optional<Collection<T>>` avoidable?

## Typical failure modes

- Returning null for no matches
- Returning null to avoid allocation
- Returning shared mutable empty collection
- Mixing null and empty inconsistently
- Using `Optional<List<T>>` unnecessarily
- Making callers remember special semantics
- Hiding failures as empty results

