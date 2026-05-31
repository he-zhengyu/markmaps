# Item 51: Design method signatures carefully

## Core idea

- Method signatures are long-lived API commitments
- Small signature choices shape usability, correctness, and evolution
- Prefer clear, stable, type-safe signatures over clever convenience

## Naming

- Choose names that reveal intent
- Follow platform naming conventions
- Use consistent verbs across related APIs
- Avoid overloaded names that hide different semantics
- Prefer discoverability in IDE autocomplete

## Parameter count

- Keep parameter lists short
- Long lists are hard to read and easy to misuse
- Three or fewer parameters is often better
- More parameters may be acceptable for simple homogeneous operations
- Repeated same-typed parameters are high risk

## Reducing long parameter lists

- Break method into smaller methods
- Use helper objects
- Use parameter object
- Use builder for optional or many parameters
- Use domain-specific value types
- Group related parameters into meaningful abstractions

## Parameter types

- Prefer interface types for inputs
  - `List` or `Collection` over concrete implementation when appropriate
  - Enables more callers
- Prefer the least specific type that supports the operation
- Avoid weak types when stronger types encode meaning
  - Weak: `String userId`
  - Stronger: `UserId userId`
- Avoid same-type adjacent parameters when order mistakes are likely

## Return types

- Prefer interface return types when implementation should vary
- Return concrete types when callers need concrete guarantees
- Do not expose internal representation accidentally
- Avoid returning null for collections or arrays
- Use `Optional` selectively for absent scalar results

## Boolean parameters

- Avoid boolean parameters when they obscure meaning
- Prefer two methods if behavior is substantially different
- Prefer enum with two values when mode may grow or clarity improves
- Bad smell
  - `setVisible(true)`
  - `repaint(false)`
  - `find(name, true)`

## Method overloading

- Use with care
- Avoid overloads that can confuse readers or compilers
- Prefer distinct names when semantics differ
- Be careful with lambdas, varargs, boxing, and generics
- Constructors may benefit from static factories with names

## Consistency

- Align names, parameter order, and return types across the API
- Common ordering patterns
  - receiver-like object first
  - source before destination
  - start before end
  - key before value
- Inconsistent order causes subtle bugs

## API evolution

- Adding parameters breaks callers
- Adding overloads can introduce ambiguity
- Returning a narrower type can restrict future implementation
- Exposing concrete mutable types is hard to retract
- Prefer signatures that leave room for compatible growth

## Convenience methods

- Add only when they materially improve common use
- Too many methods make APIs harder to learn
- Convenience should not duplicate semantics inconsistently
- Prefer a small coherent surface

## Exceptions in signatures

- Checked exceptions are part of the API
- Do not expose implementation-specific exceptions
- Throw exceptions appropriate to the abstraction
- Keep exception behavior consistent across related methods

## Generics

- Use generics to express type relationships
- Avoid raw types
- Use bounded wildcards for flexible input/output where appropriate
- Do not make signatures generic just to look abstract

## Varargs

- Good for truly variable arity
- Bad for performance-sensitive hot paths if allocation matters
- Be careful with generic varargs and heap pollution
- Prefer explicit collection parameter when caller already has a collection

## Checklist

- Is the method name precise?
- Is parameter order obvious?
- Are there too many parameters?
- Can stronger types prevent mistakes?
- Is a boolean parameter hiding two operations?
- Does the signature expose representation?
- Will this signature evolve cleanly?
- Does it match nearby API conventions?

## Typical failure modes

- Long parameter lists with repeated `String` or `int`
- Boolean flags that change semantics
- Concrete implementation types in public APIs
- Inconsistent parameter ordering
- Overloads that differ only subtly
- Null return values for absence
- Convenience explosion

