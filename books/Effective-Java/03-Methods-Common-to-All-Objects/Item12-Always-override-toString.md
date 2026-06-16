---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 12: Always Override `toString`

## Why the Default Falls Short
- `Object.toString` returns *class name* `@` *hex hash code*
  - Example: `PhoneNumber@163b91`
- ⚠️ Concise, but **not informative** vs. `707-867-5309`
- 🔑 General contract: a "concise but informative representation that is easy for a person to read"
  - Contract recommends **all subclasses override** it

## Benefits of a Good `toString`
- 💡 Makes the class **more pleasant to use** and easier to debug
- Less critical than `equals`/`hashCode` contracts (Items 10, 11), but still valuable
- Automatically invoked by many operations
  - `println`, `printf`
  - string concatenation operator (`+`)
  - `assert`
  - printed by a debugger
- 📌 Others may call it even if you never do
  - e.g. logged error messages embedding your object
- Clean diagnostics become trivial
  - `System.out.println("Failed to connect to " + phoneNumber);`
- Extends to **containing objects**, especially collections
  - ✅ `{Jenny=707-867-5309}`
  - ❌ `{Jenny=PhoneNumber@163b91}`

## What to Include in the Output
- When practical, return **all interesting information** in the object
- ⚠️ Impractical when object is large or state isn't string-friendly
  - Return a summary instead
    - `Manhattan residential phone directory (1487536 listings)`
    - `Thread[main,5,main]`
- 💡 String should ideally be **self-explanatory**
  - The `Thread` example flunks this test
- ⚠️ Omitting info yields useless test reports
  - `Assertion failure: expected {abc, 123}, but was {abc, 123}.`

## Decision: Specify the Format?
### ✅ Advantages of Specifying
- Serves as a **standard, unambiguous, human-readable** representation
- Usable for input/output and persistent data (e.g. CSV files)
- 📌 Provide a matching **static factory or constructor** to round-trip
  - Used by `BigInteger`, `BigDecimal`, boxed primitives
### ❌ Disadvantages of Specifying
- ⚠️ Once specified, you're **stuck with it for life** (if widely used)
  - Programmers parse, generate, and embed the representation
  - Changing it later breaks their code and data
- Not specifying preserves **flexibility** to improve the format later

### Document Your Intentions Either Way
- If specified → document **precisely**
  - `PhoneNumber` example: `"XXX-YYY-ZZZZ"`, fields padded with leading zeros
  - `String.format("%03d-%03d-%04d", areaCode, prefix, lineNum)`
- If unspecified → state details are subject to change
  - Show a *typical* example: `"[Potion #9: type=love, smell=turpentine, look=india ink]"`
  - 💡 Programmers depending on undocumented details "have no one but themselves to blame"

## Always Provide Programmatic Access
- 📌 Expose the data via **accessors** (area code, prefix, line number)
- ⚠️ Otherwise programmers must **parse the string**
  - Reduces performance, error-prone, fragile systems
- 💡 Failing to do so turns the string format into a **de facto API**

## When *Not* to Write `toString`
- ❌ Static utility classes (Item 4)
- ❌ Most enum types (Item 34) — Java provides a good one
- ✅ Abstract classes whose subclasses share a representation
  - e.g. collection implementations inherit from abstract collection classes

## Automatic Generation
- Google's open-source **AutoValue** (Item 10) generates `toString`; most IDEs do too
- 💡 Great for listing fields, but **not specialized** to the class's meaning
  - ❌ Inappropriate for `PhoneNumber` (has a standard representation)
  - ✅ Acceptable for `Potion`
- 📌 Generated `toString` still far preferable to `Object`'s default

## Key Takeaways
- 📌 Override `toString` in **every instantiable class** unless a superclass already has
- 🔑 Return a **concise, useful, aesthetically pleasing** description of the object
- 💡 Improves usability and aids debugging across the whole system
- ✅ Include all interesting info (or a clear summary), document the format choice, and provide accessors to that info