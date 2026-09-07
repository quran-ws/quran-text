# Security

## Reporting

Email **service@quran.ws**, or open a private advisory through GitHub's
*Report a vulnerability* on this repository. Please do not open a public issue
for a vulnerability.

## What is in scope

The **download service** in `service/` is the only part that runs as a server:
a FastAPI application that reads the committed dataset and returns files. Path
traversal, resource exhaustion and anything that lets a caller read outside
`out/` are in scope.

The **build pipeline** in `pipeline/` parses `.docx` and `.zip` files from `sources/`.
It is meant to be run on the committed inputs, whose SHA-256 is recorded in
`out/manifest.json`. Pointing it at a hostile archive is not a supported use,
but a crash or an escape from the working directory is still worth reporting.

The **client libraries** in `lib/` parse JSON that ships inside them. A crafted
`hafs.json` is not a threat model — the file is the package — but a parser that
can be made to consume unbounded memory on the data as shipped is.

## What is not

The dataset itself. The text is the King Fahd Complex's, reproduced unchanged
and hashed in every file; a disagreement about the text is not a vulnerability.
`docs/known-issues.md` is where those are recorded, and
`docs/verify-in-print.md` is where the open ones live.

## Integrity

Every published file carries a SHA-256 in `out/manifest.json`, and each muṣḥaf
names the KFGQPC package it was cut from with that package's hash. If you have a
copy of this data and want to know whether it is intact, compare those. A
mismatch between a file you hold and the hash published here is worth reporting
even if you think it is your own copy that is wrong.
