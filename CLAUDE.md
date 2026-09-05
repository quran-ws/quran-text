# API clarity guidelines

- Design public APIs from the caller's perspective, not around internal architecture.
- Prefer simple, obvious names that describe intent: `create()`, `find()`, `send()`, `cancel()`, `exists()`.
- Make code read naturally, almost like a sentence.
- Use a small, consistent vocabulary of verbs across the codebase.
- Keep the common case short; provide sensible defaults instead of requiring configuration everywhere.
- Apply progressive disclosure: simple API first, optional chaining/configuration for advanced cases.
- Prefer expressive methods such as `findOrFail()` over behavioral flags like `find($id, true)`.
- Hide repositories, adapters, factories, drivers, and other implementation details unless callers genuinely need them.
- Use fluent APIs when they improve readability, but don't chain merely for style.
- Keep naming and behavior predictable: similar concepts should use similar conventions.
- Distinguish meaning clearly: `make()` vs `create()`, `first()` vs `firstOrFail()`, `has()` vs `exists()`.
- Avoid unnecessary abbreviations, technical jargon, generic names such as `process()`, and overly long implementation-derived names.
- Minimize parameters. If an option has an obvious default, make it optional.
- Before adding a public method, ask: "What would a developer naturally guess this method is called?"
- Refactor until common usage can be understood without reading the implementation or documentation.
- Optimize for clarity at the call site, even if the internals need additional complexity.

The north-star test is: **a developer unfamiliar with this code should be able
to correctly guess how to use its public API.**
