# Item 55: Return optionals judiciously

## Core idea

- Use `Optional<T>` to model an absent return value when absence is normal
- Do not use `Optional` everywhere
- It is mainly a return-type tool, not a universal nullable wrapper

## Good use cases

- Method may return no single result
- Absence is expected, not exceptional
- Caller must consciously handle absence
- Null would be ambiguous or dangerous
- Example shapes
  - lookup by key
  - maximum of possibly empty input
  - parse result without throwing

## Poor use cases

- Collection return values
  - Use empty collection instead
- Array return values
  - Use zero-length array instead
- Fields
  - Adds object overhead and awkward serialization
- Method parameters
  - Makes callers wrap values
  - Usually worse than overloads or nullable documentation
- Map values
  - Creates ambiguity between absent key and present empty optional

## Optional is not a collection

- It has at most one value
- Do not use it to replace normal containers
- Avoid `Optional<List<T>>` for ordinary searches
- Avoid nested optionals
- Avoid treating it as a general monad in simple Java code

## Null policy

- Never return null from a method declared to return `Optional`
- Return `Optional.empty`
- Use `Optional.of` when value must be non-null
- Use `Optional.ofNullable` when converting nullable result at boundary
- Do not store null inside Optional

## Caller-side patterns

- `orElse`
  - Good when default is cheap and already available
  - Argument is evaluated eagerly
- `orElseGet`
  - Good when default is expensive or lazy
  - Supplier evaluated only when empty
- `orElseThrow`
  - Good when absence is exceptional for this caller
- `ifPresent`
  - Good for side-effect action
  - Avoid complex logic hidden in callbacks

## Primitive optionals

- Use primitive specializations when appropriate
  - `OptionalInt`
  - `OptionalLong`
  - `OptionalDouble`
- Avoid boxing overhead for numeric hot paths
- No `OptionalBoolean`
- For booleans, consider whether absence is a separate state needing enum

## Exceptions vs Optional

- Use Optional when absence is normal
- Throw exception when absence indicates failure or contract violation
- Do not return Optional merely to avoid designing error handling
- Do not hide important error detail in empty optional

## API design impact

- Optional return type forces caller attention
- It makes absence explicit in signature
- It can be verbose for simple internal code
- Public APIs benefit more than private helpers
- Use consistently within a domain model

## Performance

- Optional is an object wrapper for reference values
- Usually fine for public boundary methods
- Avoid in very hot allocation-sensitive paths unless measured acceptable
- Primitive optionals reduce boxing for numeric values
- Do not prematurely reject Optional for performance in normal business APIs

## Serialization and frameworks

- Optional was not designed primarily as a field type
- Some serializers and ORMs handle it awkwardly
- Prefer nullable fields with clear boundaries or domain-specific absence types
- Convert to Optional at API return boundary if useful

## Alternatives

- Empty collection for zero-or-more results
- Exception for failure
- Null in tightly controlled internal code when documented and local
- Result type when absence needs error information
- Enum or sealed hierarchy for multiple meaningful states

## Checklist

- Is the method returning a single value?
- Is absence normal?
- Does caller need explicit handling?
- Would empty collection be better?
- Would exception be more accurate?
- Is this a return type, not a field or parameter?
- Is primitive Optional appropriate?
- Will framework integration be sane?

## Typical failure modes

- Returning null Optional
- Using Optional for collections
- Using Optional fields in persistence models
- Accepting Optional parameters
- Calling `get` without checking presence
- Using `orElse` with expensive default creation
- Hiding error causes as empty

