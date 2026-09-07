# Contributing

The useful contribution to this repository is usually **evidence**, not code.

## What is most wanted

**A reading from a printed muṣḥaf.** `docs/verify-in-print.md` lists what this
repository does not know and the exact page to look at. Two questions are open;
both were narrowed to a single page by working out what the packages already
settle. Answering one closes a `null` or an `absent` in the data.

**A citation.** `docs/known-issues.md` records places where an edition does
something no source consulted here explains. One such entry was closed by a
photograph of a page of *al-Farāʾid al-Ḥisān*. A work, an edition and a locator
are enough.

**A defect in the derivation.** The word index, the alignment, the line
reconstruction and the counting analysis are this project's work and can be
wrong. The line layer was 98% for a year because a heading was charged two
lines; it is exact now because someone checked a printed page against it.

## The one rule about the sources

**The KFGQPC packages are the authority.** Where a package differs from another
package, from an earlier printing of itself, or from what a counting tradition
would lead you to expect, that is recorded as a difference and left alone. It is
not corrected, and it is not called a defect. See the standing rule at the top of
`docs/known-issues.md`.

So a pull request that changes the text to match an expectation will be
declined. One that records the difference, with a source, is the contribution.

## Before you open a pull request

```sh
python3 pipeline/build.py                     # ~3 min; exits non-zero on any finding
python3 -m unittest discover -s pipeline/tests
```

`out/` is generated and committed, so a change to `pipeline/` means rebuilding and
committing the result. CI runs both, plus the service suite and a terminology
audit.

**Names come from the [Quran.ws terminology standard](https://github.com/quran-ws/guidelines).**
One concept, one canonical name, across code, schemas, data and prose:
`surah` not `sura`, `ayah` not `verse`, `rasm_imlai` not `imlaei`. What this <!-- terminology: ignore -->
repository does not own — KFGQPC package, member, font and column names,
Unicode character names — is quoted rather than renamed, and listed in
`.terminology.json`. The audit reports 0 findings; keep it that way.

## Data, not opinion

Every claim in `docs/` should be checkable from something committed here, or
cited to something that is not. "This is how it is usually done" is not a
reason; a package, a printed page or a named work is.
