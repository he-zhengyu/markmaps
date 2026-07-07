# 1 Introduction *(p. 14)*
# 2 Creating and Destroying Objects *(p. 18)*
## Item 1: Consider static factory methods instead of constructors *(p. 18)*
## Item 2: Consider a builder when faced with many constructor parameters *(p. 23)*
## Item 3: Enforce the singleton property with a private constructor or an enum type *(p. 30)*
## Item 4: Enforce noninstantiability with a private constructor *(p. 32)*
## Item 5: Prefer dependency injection to hardwiring resources *(p. 33)*
## Item 6: Avoid creating unnecessary objects *(p. 35)*
## Item 7: Eliminate obsolete object references *(p. 39)*
## Item 8: Avoid finalizers and cleaners *(p. 42)*
## Item 9: Prefer try-with-resources to try-finally *(p. 47)*
# 3 Methods Common to All Objects *(p. 50)*
## Item 10: Obey the general contract when overriding equals *(p. 50)*
## Item 11: Always override hashCode when you override equals *(p. 63)*
## Item 12: Always override toString *(p. 68)*
## Item 13: Override clone judiciously *(p. 71)*
## Item 14: Consider implementing Comparable *(p. 79)*
# 4 Classes and Interfaces *(p. 86)*
## Item 15: Minimize the accessibility of classes and members *(p. 86)*
## Item 16: In public classes, use accessor methods, not public fields *(p. 91)*
## Item 17: Minimize mutability *(p. 93)*
## Item 18: Favor composition over inheritance *(p. 100)*
## Item 19: Design and document for inheritance or else prohibit it *(p. 106)*
## Item 20: Prefer interfaces to abstract classes *(p. 112)*
## Item 21: Design interfaces for posterity *(p. 117)*
## Item 22: Use interfaces only to define types *(p. 120)*
## Item 23: Prefer class hierarchies to tagged classes *(p. 122)*
## Item 24: Favor static member classes over nonstatic *(p. 125)*
## Item 25: Limit source files to a single top-level class *(p. 128)*
# 5 Generics *(p. 130)*
## Item 26: Don’t use raw types *(p. 130)*
## Item 27: Eliminate unchecked warnings *(p. 136)*
## Item 28: Prefer lists to arrays *(p. 139)*
## Item 29: Favor generic types *(p. 143)*
## Item 30: Favor generic methods *(p. 148)*
## Item 31: Use bounded wildcards to increase API flexibility *(p. 152)*
## Item 32: Combine generics and varargs judiciously *(p. 159)*
## Item 33: Consider typesafe heterogeneous containers *(p. 164)*
# 6 Enums and Annotations *(p. 170)*
## Item 34: Use enums instead of int constants *(p. 170)*
## Item 35: Use instance fields instead of ordinals *(p. 181)*
## Item 36: Use EnumSet instead of bit fields *(p. 182)*
## Item 37: Use EnumMap instead of ordinal indexing *(p. 184)*
## Item 38: Emulate extensible enums with interfaces *(p. 189)*
## Item 39: Prefer annotations to naming patterns *(p. 193)*
## Item 40: Consistently use the Override annotation *(p. 201)*
## Item 41: Use marker interfaces to define types *(p. 204)*
# 7 Lambdas and Streams *(p. 206)*
## Item 42: Prefer lambdas to anonymous classes *(p. 206)*
## Item 43: Prefer method references to lambdas *(p. 210)*
## Item 44: Favor the use of standard functional interfaces *(p. 212)*
## Item 45: Use streams judiciously *(p. 216)*
## Item 46: Prefer side-effect-free functions in streams *(p. 223)*
## Item 47: Prefer Collection to Stream as a return type *(p. 229)*
## Item 48: Use caution when making streams parallel *(p. 235)*
# 8 Methods *(p. 240)*
## Item 49: Check parameters for validity *(p. 240)*
## Item 50: Make defensive copies when needed *(p. 244)*
## Item 51: Design method signatures carefully *(p. 249)*
## Item 52: Use overloading judiciously *(p. 251)*
## Item 53: Use varargs judiciously *(p. 258)*
## Item 54: Return empty collections or arrays, not nulls *(p. 260)*
## Item 55: Return optionals judiciously *(p. 262)*
## Item 56: Write doc comments for all exposed API elements *(p. 267)*
# 9 General Programming *(p. 274)*
## Item 57: Minimize the scope of local variables *(p. 274)*
## Item 58: Prefer for-each loops to traditional for loops *(p. 277)*
## Item 59: Know and use the libraries *(p. 280)*
## Item 60: Avoid float and double if exact answers are required *(p. 283)*
## Item 61: Prefer primitive types to boxed primitives *(p. 286)*
## Item 62: Avoid strings where other types are more appropriate *(p. 289)*
## Item 63: Beware the performance of string concatenation *(p. 292)*
## Item 64: Refer to objects by their interfaces *(p. 293)*
## Item 65: Prefer interfaces to reflection *(p. 295)*
## Item 66: Use native methods judiciously *(p. 298)*
## Item 67: Optimize judiciously *(p. 299)*
## Item 68: Adhere to generally accepted naming conventions *(p. 302)*
# 10 Exceptions *(p. 306)*
## Item 69: Use exceptions only for exceptional conditions *(p. 306)*
## Item 70: Use checked exceptions for recoverable conditions and runtime exceptions for programming errors *(p. 309)*
## Item 71: Avoid unnecessary use of checked exceptions *(p. 311)*
## Item 72: Favor the use of standard exceptions *(p. 313)*
## Item 73: Throw exceptions appropriate to the abstraction *(p. 315)*
## Item 74: Document all exceptions thrown by each method *(p. 317)*
## Item 75: Include failure-capture information in detail messages *(p. 319)*
## Item 76: Strive for failure atomicity *(p. 321)*
## Item 77: Don’t ignore exceptions *(p. 323)*
# 11 Concurrency *(p. 324)*
## Item 78: Synchronize access to shared mutable data *(p. 324)*
## Item 79: Avoid excessive synchronization *(p. 330)*
## Item 80: Prefer executors, tasks, and streams to threads *(p. 336)*
## Item 81: Prefer concurrency utilities to wait and notify *(p. 338)*
## Item 82: Document thread safety *(p. 343)*
## Item 83: Use lazy initialization judiciously *(p. 346)*
## Item 84: Don’t depend on the thread scheduler *(p. 349)*
# 12 Serialization *(p. 352)*
## Item 85: Prefer alternatives to Java serialization *(p. 352)*
## Item 86: Implement Serializable with great caution *(p. 356)*
## Item 87: Consider using a custom serialized form *(p. 359)*
## Item 88: Write readObject methods defensively *(p. 366)*
## Item 89: For instance control, prefer enum types to readResolve *(p. 372)*
## Item 90: Consider serialization proxies instead of serialized instances *(p. 376)*