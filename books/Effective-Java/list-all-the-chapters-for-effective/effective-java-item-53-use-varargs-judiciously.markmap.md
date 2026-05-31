# Item 53: Use varargs judiciously

## Core idea

- Varargs are useful for methods accepting a variable number of arguments
- They create an array at the call boundary
- Use them where they improve API clarity
- Avoid them where they hide constraints or cost

## Good use cases

- Natural zero-or-more arguments
- Formatting-style APIs
- Small convenience methods
- Test helpers
- Aggregation helpers
- API calls where individual arguments are more readable than a collection

## Require at least one argument

- Do not accept zero arguments if zero is invalid
- Use one required parameter plus varargs
- Pattern
  - first required argument
  - remaining optional arguments
- Benefit
  - Compile-time enforcement of minimum arity
  - Simpler runtime validation

## Runtime cost

- Each varargs call creates an array
- Cost is usually small
- Cost can matter in hot paths
- For performance-sensitive APIs, consider overloads for common arities
- Measure before complicating the API

## API clarity

- Varargs suggest all arguments have the same role
- Do not use varargs for unrelated parameters
- Avoid varargs when a named collection is clearer
- Prefer `Collection<T>` when caller naturally already has a collection

## Mutability and exposure

- Varargs parameter is an array
- Do not store the varargs array directly if callers can observe mutation risk
- Do not expose it as internal state
- Copy when retaining beyond the call
- Treat it like any other mutable array input

## Generic varargs

- Generic arrays are not reifiable
- Generic varargs can cause heap pollution
- Use `@SafeVarargs` only when actually safe
- Safe usually means
  - method does not write into the varargs array
  - method does not expose the array to untrusted code
- Prefer `List<T>` when safety is unclear

## `@SafeVarargs`

- Valid on final, static, or private methods and constructors
- It is a promise, not decoration
- Use only after auditing implementation
- Suppresses warnings at call sites
- Misuse can hide real type-safety bugs

## Overloading interaction

- Varargs overloads can conflict with fixed-arity overloads
- Resolution may surprise callers
- Avoid overload sets where varargs competes with boxing or widening
- Keep varargs overload as the obvious fallback

## Null handling

- Callers can pass null as the entire varargs array
- Callers can pass null elements
- Decide and document both policies
- Validate defensively if nulls are forbidden

## Defensive validation

- Check array itself if method can be called with a null array
- Check elements when null elements are invalid
- Check size constraints
- Check cross-element constraints
- Fail before mutation or external side effects

## Alternatives

- `Collection<T>` parameter
  - Better for many elements
  - Better when caller already has collection
- Builder
  - Better for complex heterogeneous options
- Explicit overloads
  - Better for very hot common arities
- Stream
  - Usually not ideal as input unless laziness matters

## Checklist

- Is variable arity truly natural?
- Is zero arguments valid?
- Should the first argument be required?
- Will allocation matter?
- Are element nulls allowed?
- Is generic varargs type-safe?
- Is `@SafeVarargs` justified?
- Would `Collection<T>` be clearer?

## Typical failure modes

- Accepting zero arguments accidentally
- Using varargs for unrelated options
- Storing the varargs array directly
- Unsafe generic varargs with hidden heap pollution
- Adding confusing varargs overloads
- Ignoring null array and null element cases
- Optimizing with many overloads before measurement

