# Item 49: Check parameters for validity

## Core idea

- Validate method and constructor parameters before using them
- Fail fast near the source of the bug
- Make API contracts explicit and enforceable
- Treat validation as part of the method's semantic boundary

## Why it matters

- Prevents corrupted object state
- Produces clearer exceptions
- Avoids mysterious failures later in execution
- Protects invariants in public APIs
- Makes misuse easier to diagnose in tests and production logs

## Where to validate

- Public methods
  - Validate all externally supplied arguments
  - Document constraints in Javadoc
  - Throw conventional exceptions
- Constructors
  - Validate before assigning fields
  - Preserve class invariants from object birth
- Setters and mutators
  - Validate before mutation
  - Avoid partial updates
- Private methods
  - Use assertions when caller correctness is an internal invariant
  - Prefer normal checks if bad inputs can still occur in practice

## Common constraints

- Nullability
  - Required argument must not be null
  - Use `Objects.requireNonNull`
  - Include meaningful parameter names in messages when useful
- Numeric ranges
  - Minimum and maximum bounds
  - Non-negative, positive, bounded size, valid index
- State compatibility
  - Argument must match current object state
  - Example: capacity cannot be smaller than current size
- Format and syntax
  - Strings, paths, identifiers, regex-like patterns
  - Validate enough to preserve the method contract
- Cross-parameter relationships
  - `start <= end`
  - `offset + length <= array.length`
  - Mutually exclusive arguments are not both set

## Exception choices

- `NullPointerException`
  - Null argument where null is forbidden
  - Often produced by `Objects.requireNonNull`
- `IllegalArgumentException`
  - Argument value is inappropriate
  - Example: negative size
- `IndexOutOfBoundsException`
  - Invalid index, offset, length, or range
- `IllegalStateException`
  - Object state makes the operation invalid
  - Not purely a parameter problem
- Domain-specific exception
  - Use only when it adds semantic value
  - Avoid custom exceptions for routine validation

## Documentation

- State parameter constraints in `@param`
- State thrown exceptions in `@throws`
- Keep docs synchronized with implementation
- Document null policy explicitly
- Avoid vague phrases
  - Weak: "must be valid"
  - Better: "must be between 0 and size, inclusive"

## Timing

- Validate before expensive work
- Validate before changing state
- Validate before starting I/O or external side effects
- Validate before storing references
- Validate copied inputs when mutability creates race risk

## Defensive design patterns

- Centralized validation helper
  - Good for repeated range checks
  - Keep helper names precise
- Value object
  - Move validation into construction
  - Reduces repeated parameter validation
- Type-level constraints
  - Prefer stronger types over raw `String` or `int`
  - Example: `EmailAddress` instead of unconstrained `String`
- Builder validation
  - Validate required fields
  - Validate cross-field invariants in `build`

## Private method assertions

- Use `assert` for assumptions guaranteed by callers
- Do not rely on assertions for public API validation
- Assertions may be disabled at runtime
- Good use cases
  - Internal index already checked by caller
  - Algorithm invariant
  - Non-null internal field after construction

## Edge cases

- Validation can be too strict
  - Do not reject values the API can correctly support
  - Avoid future-hostile constraints
- Validation can be too late
  - State may already be mutated
  - Exception may be misleading
- Validation can be incomplete
  - Single argument is valid, but combination is invalid
- Validation can leak implementation detail
  - Error messages should help callers, not expose internals

## Performance

- Simple validation is usually cheap
- Avoid redundant deep validation on hot paths unless needed
- Expensive validation may need clear API boundaries
- Cache validated derived state only if profiling proves value
- Do not skip validation in public APIs for speculative performance

## Checklist

- Are all public inputs constrained?
- Are constructor invariants protected?
- Are null policies explicit?
- Are exception types conventional?
- Are error messages useful?
- Are cross-parameter relationships checked?
- Is validation before mutation?
- Are private assumptions asserted or otherwise protected?

## Typical failure modes

- Trusting callers of public APIs
- Validating after assignment
- Throwing a generic `RuntimeException`
- Returning silently on invalid input
- Conflating invalid argument with invalid object state
- Forgetting null checks before dereference
- Checking individual parameters but not their relationships

