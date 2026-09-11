# Licence and attribution

`LICENSE` is the **Creative Commons Attribution 4.0 International** licence
(CC BY 4.0), verbatim and unmodified. This file says what it covers, what it cannot cover, and the
attribution it asks you to carry.

## What is licensed

Everything in this repository that this project authored:

| | |
|---|---|
| the word index and its numbering | `data/word-index.*`, `data/ayah-map.*` |
| the seven muṣḥaf files and derived layers | `data/mushaf/`, `data/counting.json` |
| the counting analysis and its citations | `sources/counting/khilaf.json`, `declared.json`, `open-findings.json` |
| the alignment data | `sources/alignment/` |
| the pipeline and the service | `pipeline/`, `service/` |
| the schemas, the reports, the documentation | `schema/`, `data/reports/`, `docs/` |

Word-level data is **derived** here — no source package contains it — and that
derivation, together with the alignment, the numbering and the counting
analysis, is the work being licensed. See `docs/sources.md`.

## The client libraries are CC BY 4.0 too

`lib/` carries the same licence as everything else, and each package ships a
copy of it. One licence covers the whole repository: the dataset, the pipeline,
the docs and the six client libraries.

That is a deliberate choice against the usual advice. Creative Commons
discourage CC BY for software — it grants no patent rights and does not define
"source form" — and MIT is what a developer pulling `quran-text` from PyPI, npm,
Packagist, pub.dev or Maven Central would expect. But every one of those
packages **bundles the dataset**: `hafs.json` and its font travel inside them.
Licensing the wrapper under MIT while the data it carries is CC BY 4.0 would put
two licences in one package and, in practice, let the data reach people with the
attribution stripped — which is the one thing this licence exists to prevent.

So the link requirement holds wherever the data goes. If you need the library
code under different terms, ask.

## What is not licensed here

**The Qurʾānic text is not this project's to license.** Nor are the packages it
was read from:

| | |
|---|---|
| `sources/kfgqpc/*.zip` | KFGQPC distributions, redistributed unmodified |
| `data/fonts/*.ttf` | KFGQPC fonts, copied unmodified from those packages |

These are the work of the **King Fahd Glorious Qurʾān Printing Complex**, are
included as received, and remain under KFGQPC's own terms. The packages state
none in their `read.me` files. Nothing in `LICENSE` grants any right in them,
and this project makes no claim about what KFGQPC permits — satisfy yourself
before redistributing them.

`sources/counting/book-boundary-primitives.json` and `counting-systems.json` are
copied verbatim from
[quranpedia/qiraat-ayah-map](https://github.com/quranpedia/qiraat-ayah-map)
(MIT) at a pinned commit; see `sources/counting/UPSTREAM.md`.

## Attribution

CC BY 4.0 asks you to credit the source and, under §3(a)(1)(A)(v), to carry a
link to it. **The link is the point** — it is how anyone who receives this data
from you can reach corrections and later releases. Please keep it:

> quran-text by quran-ws — https://github.com/quran-ws/quran-text — CC BY 4.0

That is the attribution requested under §3(a)(1)(A)(i). In a UI, an about
screen or a data-source note is enough; in a package, the repository field and
this file travelling with the data are enough. If you changed the data, say so:
§3(a)(1)(B) asks you to mark modifications, and it matters here more than in
most datasets.

Copyright © 2026 quran-ws.