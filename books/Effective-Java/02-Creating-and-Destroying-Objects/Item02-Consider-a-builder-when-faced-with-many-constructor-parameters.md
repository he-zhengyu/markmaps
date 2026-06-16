---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 2: Consider a Builder When Faced with Many Constructor Parameters

## The Problem
- 🔑 Static factories and constructors **don't scale** to many optional parameters
- Motivating example: **`NutritionFacts`** label
  - Few required fields: *serving size, servings, calories*
  - 📊 More than **twenty** optional fields (fat, sodium, cholesterol…)
  - Most products use only a few of the optional fields
- Core question: what constructors/factories fit such a class?

## Approach 1 — Telescoping Constructor Pattern
- 🔑 Provide a constructor per parameter count: required only, +1 optional, +2 optional… up to all
- Each constructor delegates to the next via `this(...)`
- Client picks the **shortest constructor** covering wanted params
  - ```java
    new NutritionFacts(240, 8, 100, 0, 35, 27);
    ```
- ⚠️ Forces passing values for **unwanted** parameters (e.g. `0` for fat)
- ❌ Hard to **write** with many parameters
- ❌ Harder to **read** — reader must count parameters to decode meaning
- ⚠️ Long runs of same-typed params cause subtle bugs
  - Reversed args compile fine but **misbehave at runtime** (Item 51)

## Approach 2 — JavaBeans Pattern
- 🔑 Parameterless constructor, then **setter methods** for each field
  - ```java
    NutritionFacts c = new NutritionFacts();
    c.setServingSize(240);
    c.setServings(8);
    ```
- ✅ Easy to create instances; resulting code easy to read
- ⚠️ Construction split across multiple calls
  - ❌ Object may sit in an **inconsistent state** mid-construction
  - ❌ Cannot enforce consistency by validating constructor params
  - ❌ Failures appear *far removed* from the buggy code → hard to debug
- ❌ Precludes **immutability** (Item 17); adds thread-safety burden
- Workaround: manually **"freeze"** object after construction
  - ⚠️ Unwieldy, rarely used; compiler can't ensure `freeze` is called

## Approach 3 — Builder Pattern ✅
- 🔑 Combines telescoping **safety** with JavaBeans **readability**
- A form of the **Builder pattern** *[Gamma95]*
- ### How It Works
  - Call constructor/static factory with all **required** params → get a `Builder`
  - Call setter-like methods for each **optional** param of interest
  - Call parameterless `build()` → produces the (usually **immutable**) object
  - Builder is typically a **static member class** (Item 24) of the built class
- ### Fluent API
  - Setters `return this` so calls **chain**
  - ```java
    NutritionFacts cocaCola = new NutritionFacts.Builder(240, 8)
        .calories(100).sodium(35).carbohydrate(27).build();
    ```
  - 💡 Simulates **named optional parameters** found in Python and Scala
  - ✅ Immutable result; all default values in **one place**
- ### Validity Checking
  - Check params in the builder's **constructor and methods**
  - Check multi-parameter **invariants** in the constructor called by `build()`
  - 📌 Verify invariants on **object fields after copying** from builder (Item 50)
  - On failure: throw `IllegalArgumentException` naming the bad params (Items 72, 75)

## Builder Pattern for Class Hierarchies
- ✅ Well suited to hierarchies via a **parallel hierarchy of builders**
  - Abstract classes → abstract builders; concrete → concrete builders
- Example: abstract `Pizza` root with `Topping` enum
  - ```java
    abstract static class Builder<T extends Builder<T>> {
        public T addTopping(Topping t) {...; return self(); }
        abstract Pizza build();
        protected abstract T self();
    }
    ```
- 🔑 **Generic type with recursive type parameter** (Item 30) + abstract `self()`
  - Enables method chaining in subclasses **without casts**
  - 🔑 Known as the **simulated self-type idiom** (Java lacks a self type)
- Concrete subclasses
  - `NyPizza` — required `Size` parameter (SMALL/MEDIUM/LARGE)
  - `Calzone` — optional `sauceInside()` flag
- 🔑 **Covariant return typing**: each `build()` returns its own subtype
  - `NyPizza.Builder.build()` → `NyPizza`; `Calzone.Builder.build()` → `Calzone`
  - ✅ Clients use builders without casting
  - ```java
    NyPizza p = new NyPizza.Builder(SMALL)
        .addTopping(SAUSAGE).addTopping(ONION).build();
    ```

## Flexibility & Advantages
- ✅ Supports **multiple varargs** params (each gets its own method)
- ✅ Can aggregate params from repeated calls into one field (e.g. `addTopping`)
- ✅ One builder reused to build **multiple objects**
- ✅ Params can be **tweaked between** `build()` calls
- ✅ Can auto-fill fields (e.g. an incrementing **serial number**)

## Disadvantages ⚠️
- ❌ Must create the **builder first** — minor cost, but matters in performance-critical code
- ❌ More **verbose** than telescoping constructors
  - 📌 Worth it only with **four or more** parameters
- 💡 Anticipate future params: switching later leaves obsolete constructors that "stick out like a sore thumb"
  - 📌 Often **better to start with a builder** from the outset

## Key Takeaways
- 🔑 Use a **builder** when constructors/factories would have more than a handful of params
- 📌 Especially valuable when many params are **optional** or of **identical type**
- ✅ Builders are far **easier to read and write** than telescoping constructors
- ✅ Builders are much **safer** than JavaBeans (consistency + immutability)
- 💡 Builders extend cleanly to **class hierarchies** via recursive generics and covariant returns
- 📌 If in doubt about parameter count growth, **start with a builder**