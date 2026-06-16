---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Item 9: Prefer try-with-resources to try-finally

## The Problem: Resources Must Be Closed
- 🔑 Many Java resources require a manual `close()` call
- Examples: `InputStream`, `OutputStream`, `java.sql.Connection`
- ⚠️ Closing is often overlooked by clients → dire performance consequences
- Finalizers used as a *safety net*, but **don't work well** (Item 8)

## The Old Way: try-finally
### Single resource
- Guarantees closing even on exception or `return`
- Looks acceptable for one resource
- ```java
  static String firstLineOfFile(String path) throws IOException {
    BufferedReader br = new BufferedReader(new FileReader(path));
    try {
      return br.readLine();
    } finally {
      br.close();
    }
  }
  ```
### Multiple resources
- ❌ Becomes ugly with nested try-finally blocks
- ```java
  static void copy(String src, String dst) throws IOException {
    InputStream in = new FileInputStream(src);
    try {
      OutputStream out = new FileOutputStream(dst);
      try {
        byte[] buf = new byte[BUFFER_SIZE];
        int n;
        while ((n = in.read(buf)) >= 0)
          out.write(buf, 0, n);
      } finally { out.close(); }
    } finally { in.close(); }
  }
  ```
### Easy to get wrong
- 📊 Two-thirds of `close()` uses in Java libraries were **wrong** in 2007
- 💡 Even good programmers got it wrong most of the time
- Author himself got it wrong (*Java Puzzlers*, p.88) — unnoticed for years

## Hidden Flaw: Exception Obliteration
- ⚠️ Both `try` block and `finally` block can throw exceptions
- 💡 Second exception (from `close()`) completely **obliterates** the first
- No record of first exception in the stack trace
- 📌 Usually the *first* exception is the one needed to diagnose the problem
- Suppression code was possible but too verbose → virtually no one wrote it

## The Solution: try-with-resources (Java 7)
### Requirement
- 🔑 Resource must implement `AutoCloseable`
- Interface = single `void`-returning `close()` method
- Many JDK & third-party classes now implement/extend it
- ✅ Custom resource classes should implement `AutoCloseable` too
### Single resource rewritten
- Shorter and more readable
- ```java
  static String firstLineOfFile(String path) throws IOException {
    try (BufferedReader br = new BufferedReader(new FileReader(path))) {
      return br.readLine();
    }
  }
  ```
### Multiple resources rewritten
- *Short and sweet* — resources declared in one header
- ```java
  static void copy(String src, String dst) throws IOException {
    try (InputStream in = new FileInputStream(src);
         OutputStream out = new FileOutputStream(dst)) {
      byte[] buf = new byte[BUFFER_SIZE];
      int n;
      while ((n = in.read(buf)) >= 0)
        out.write(buf, 0, n);
    }
  }
  ```

## Better Diagnostics
- 💡 Exception from `close()` is **suppressed** in favor of the one you want
- Multiple exceptions may be suppressed to preserve the meaningful one
- Suppressed exceptions are *not discarded* — printed in stack trace with a note
- 🔑 Access them via `getSuppressed()`, added to `Throwable` in Java 7

## Adding catch Clauses
- ✅ `catch` clauses work just like in try-finally
- 💡 Handle exceptions without an extra layer of nesting
- Example: return a default value if the file can't be opened/read
- ```java
  static String firstLineOfFile(String path, String defaultVal) {
    try (BufferedReader br = new BufferedReader(new FileReader(path))) {
      return br.readLine();
    } catch (IOException e) {
      return defaultVal;
    }
  }
  ```

## Key Takeaways
- 📌 **Always** prefer try-with-resources over try-finally for closeable resources
- ✅ Code is shorter, clearer, and easier to write correctly
- ✅ Generated exceptions are more useful (suppression preserves the real cause)
- 💡 Correct resource handling was *practically impossible* with try-finally alone
- 🔑 Make your own closeable types implement `AutoCloseable`