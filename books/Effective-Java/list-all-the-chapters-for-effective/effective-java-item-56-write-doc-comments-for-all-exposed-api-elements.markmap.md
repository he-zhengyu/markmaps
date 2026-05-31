# Item 56: Write doc comments for all exposed API elements

## Core idea

- Public and protected API elements need documentation
- Documentation is part of the API contract
- Good comments explain what clients need to know, not implementation trivia

## What to document

- Public classes and interfaces
- Public and protected methods
- Public and protected constructors
- Public and protected fields
- Enum types and constants
- Annotation types and members
- Package-level behavior when useful

## Method documentation

- State what the method does
- Document preconditions
- Document postconditions
- Document side effects
- Document thread-safety behavior if relevant
- Document whether arguments or returns may be null
- Document units, ranges, formats, and ordering

## Tags

- `@param`
  - Explain each parameter's role and constraints
- `@return`
  - Explain result meaning
  - Include empty-result behavior
- `@throws`
  - Explain exception conditions
  - Match actual validation behavior
- `@implSpec`
  - Document implementation requirements for inheritors
- `@implNote`
  - Document implementation notes not required by contract
- `@apiNote`
  - Document API usage guidance

## Contract vs implementation

- Contract
  - What callers can rely on
  - What implementors must preserve
- Implementation
  - How current code achieves behavior
  - May change later
- Good docs emphasize contract
- Avoid exposing unnecessary implementation details

## Inheritance-sensitive APIs

- Document overridable method requirements
- Document when superclass methods call overridable methods
- Document synchronization expectations
- Document allowed exceptions
- Document whether override must call `super`
- Use `@implSpec` for subclass contracts

## Generics documentation

- Document type parameters with `@param <T>`
- Explain variance and constraints when not obvious
- Explain relationship between type parameter and arguments
- Avoid repeating what the signature already says
- Clarify wildcard behavior if callers may be confused

## Nullness

- State whether parameters accept null
- State whether return may be null
- Prefer explicit wording or annotations used by the project
- Keep null policy consistent across methods
- Avoid making callers infer from implementation

## Thread safety

- State whether class is immutable, thread-safe, conditionally thread-safe, or not thread-safe
- Document required external synchronization
- Document whether returned views are live and thread-safe
- Avoid vague claims like "handles concurrency"

## Side effects

- Mutates receiver
- Mutates argument
- Performs I/O
- Opens or closes resources
- Caches results
- Triggers callbacks
- Blocks, waits, or acquires locks

## Style

- Be concise
- Use active voice
- Start with a summary sentence
- Avoid implementation narration
- Use `{@code ...}` for code fragments
- Use `{@link ...}` when linking helps navigation
- Keep comments close to the declaration

## Examples

- Add examples when behavior is subtle
- Keep examples short
- Make examples compile if possible
- Do not let examples become the only specification
- Avoid examples that depend on unstable ordering or environment

## Maintenance

- Update docs with behavior changes
- Treat stale docs as bugs
- Review generated Javadoc output
- Use doclint or build checks when available
- Keep docs and tests aligned

## Checklist

- Is every exposed API element documented?
- Does each method have a clear summary?
- Are all parameters documented?
- Are return values documented?
- Are exceptions documented?
- Are nullness and mutability clear?
- Are thread-safety guarantees clear?
- Are implementation requirements separated from notes?

## Typical failure modes

- No Javadoc for protected methods
- Comments describe implementation instead of contract
- Missing `@throws` for validation exceptions
- Missing nullness policy
- Stale comments after code changes
- Overly verbose comments that hide the contract
- Ambiguous words like "valid", "normal", or "proper"

