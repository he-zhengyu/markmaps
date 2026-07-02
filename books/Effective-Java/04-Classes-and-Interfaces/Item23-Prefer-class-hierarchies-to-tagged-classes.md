---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 23: Prefer Class Hierarchies to Tagged Classes

## Tagged Classes

### What They Are
- 🔑 A class whose instances come in **two or more flavors**, with a **tag field** indicating the flavor
- Single class holds fields and logic for *all* flavors
- Behavior branches on the tag, typically via `switch`

### Example: `Figure`
- Represents a circle *or* a rectangle in one class
- `enum Shape { RECTANGLE, CIRCLE }` plus a `final Shape shape` tag field
- Fields `length`, `width` used only for rectangles; `radius` only for circles
- Separate constructors set the tag and the relevant fields
- `area()` uses a `switch(shape)`, throwing `AssertionError` in the default case

```java
class Figure {
    enum Shape { RECTANGLE, CIRCLE };
    final Shape shape;        // tag field
    double length, width;     // RECTANGLE only
    double radius;            // CIRCLE only
    double area() {
        switch(shape) {
            case RECTANGLE: return length * width;
            case CIRCLE:    return Math.PI * (radius * radius);
            default: throw new AssertionError(shape);
        }
    }
}
```

### Shortcomings
- ⚠️ Cluttered with **boilerplate**: enum, tag field, `switch` statements
- ⚠️ Poor readability — multiple implementations jumbled in one class
- ⚠️ Inflated **memory footprint** — instances carry fields irrelevant to their flavor
- ⚠️ Fields can't be `final` unless constructors initialize irrelevant fields (more boilerplate)
- ⚠️ Constructors set tag + data fields with **no compiler help** — wrong init fails at *runtime*
- ⚠️ Can't add a flavor without modifying the source file
- ⚠️ Adding a flavor means updating *every* `switch`, or it fails at runtime
- ⚠️ Instance data type gives **no clue** as to its flavor
- 📌 In short: **verbose, error-prone, and inefficient**

## Class Hierarchies: The Better Alternative

### Core Idea
- 💡 Object-oriented **subtyping** is the right tool for one data type with multiple flavors
- 📌 A tagged class is *"a pallid imitation of a class hierarchy"*

### Transformation Recipe
- Define an **abstract root class** with an abstract method for each tag-dependent method
- In `Figure`, only `area()` depends on the tag → it becomes abstract
- Put any tag-*independent* methods/fields in the root (none exist in `Figure`)
- Define a **concrete subclass** for each flavor (here: `Circle`, `Rectangle`)
- Each subclass holds only its own fields and implements the abstract method(s)

### Result

```java
abstract class Figure {
    abstract double area();
}
class Circle extends Figure {
    final double radius;
    Circle(double radius) { this.radius = radius; }
    @Override double area() { return Math.PI * (radius * radius); }
}
class Rectangle extends Figure {
    final double length, width;
    Rectangle(double length, double width) {
        this.length = length; this.width = width;
    }
    @Override double area() { return length * width; }
}
```

### Advantages
- ✅ Simple, clear code — **no boilerplate**
- ✅ Each flavor in its own class, free of irrelevant fields
- ✅ All fields can be `final`
- ✅ Compiler enforces field initialization and full abstract-method implementation
- ✅ Eliminates runtime failure from a missing `switch` case
- ✅ Multiple programmers can **extend independently** without root source access
- ✅ A distinct **data type per flavor** — type-restrict variables and parameters

## Reflecting Natural Hierarchies

### Better Type Modeling
- 💡 Hierarchies can mirror **natural relationships** among types
- Gains flexibility and better **compile-time type checking**

### Example: Square as a Rectangle
- A square is a special kind of rectangle (assuming both immutable)
- `class Square extends Rectangle { Square(double side) { super(side, side); } }`
- ⚠️ Fields accessed directly here for brevity — poor design if the hierarchy were public (Item 16)

## Key Takeaways
- 📌 Tagged classes are **seldom appropriate** — verbose, error-prone, inefficient
- 💡 Prefer **class hierarchies** via subtyping for one type with multiple flavors
- ✅ Hierarchies are compiler-checked, extensible, and free of irrelevant fields
- 📌 If tempted to write a tag field, consider whether a hierarchy fits instead
- 📌 When you meet an existing tagged class, consider **refactoring** it into a hierarchy