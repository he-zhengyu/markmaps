
# Item 52: Use overloading judiciously

## Core idea

- Overload resolution happens at compile time
- Overriding dispatch happens at runtime
- APIs should not rely on callers understanding subtle overload selection
- Prefer clarity over overloaded cleverness

## Overloading vs overriding

- Overloading
  - Same method name
  - Different parameter types
  - Chosen by declared compile-time types
- Overriding
  - Same method signature in subclass
  - Chosen by runtime receiver type
- Confusion arises when users expect overloading to behave like overriding

## Main risk

- The method called may not be the method the reader expects
- Static type of the argument controls overload choice
- Runtime type of the argument is usually irrelevant for overload selection
- Refactoring variable declarations can change behavior

## Dangerous overload sets

- Same number of parameters
- Related parameter types
  - `Object`
  - `String`
  - `CharSequence`
  - `Collection`
  - `List`
- Primitive and boxed variants
  - `int`
  - `Integer`
  - `long`
  - `Long`
- Varargs mixed with fixed arity
- Generic overloads with erased similarities
- Functional interface overloads used with lambdas

## Lambdas and method references

- Lambda expressions need target types
- Multiple functional-interface overloads can be ambiguous
- Similar functional interfaces make APIs hard to call
- Prefer distinct method names for different functional semantics
- Avoid forcing users to add casts to choose overloads

## Constructors

- Constructors have no names beyond the class name
- Heavy constructor overloading can be unclear
- Static factory methods can provide semantic names
- Builders can handle many optional variants

## Safe overloading

- Overloads with clearly different arity
- Overloads with unrelated parameter types
- Overloads that perform exactly equivalent semantics
- Convenience overload delegates to canonical implementation
- No meaningful behavioral difference based only on parameter type

## Bad signs

- User must know overload resolution rules
- User must cast arguments to call intended method
- `null` argument is ambiguous
- Similar overloads produce different behavior
- IDE autocomplete shows many confusing variants
- Test failures depend on declared variable type

## Design alternatives

- Use different method names
  - Best when semantics differ
- Use static factories
  - Names describe construction path
- Use builder
  - Good for many optional parameters
- Use strategy object
  - Good for behavioral variation
- Use enum mode
  - Good for small explicit mode selection

## Interaction with autoboxing

- Primitive widening, boxing, and varargs have priority rules
- Readers rarely remember exact selection order
- `Integer` vs `int` overloads can surprise
- Avoid overload sets that differ only by primitive/boxed forms

## Interaction with generics

- Type erasure can prevent certain overloads
- Generic overloads may become ambiguous
- Raw types can select less specific overloads
- Wildcards can make overload resolution harder to predict

## Testing implications

- Test calls through different declared types
- Test `null` behavior if accepted
- Test lambda and method reference call sites
- Test primitive and boxed arguments
- Prefer compile-time clarity over test-only safety

## Checklist

- Do overloads have clearly different arity?
- If same arity, are parameter types unrelated?
- Do all overloads have the same semantic meaning?
- Can `null` create ambiguity?
- Can lambdas create ambiguity?
- Would distinct names be clearer?
- Can a static factory or builder replace constructor overloads?

## Typical failure modes

- Same-name methods with different semantics
- `Object` overload swallowing calls unexpectedly
- Primitive and boxed overload confusion
- Varargs overload competing with fixed-arity overload
- Lambda overload ambiguity
- Constructor overloads with unreadable argument lists

