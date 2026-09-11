# Quran Text

**The Qurʾān as text, exactly as the Madinah muṣḥaf prints it — in seven printed
editions, with one word number that means the same word in all seven.**

A *muṣḥaf* is a printed copy of the Qurʾān; a *riwayah* is one transmitted
reading of it, differing in spelling, vowelling, where āyāt end and how words are
written ([glossary](https://quran.ws/docs/concepts/glossary/#riwayah)). This
repository carries seven of them, taken unedited from the digital packages
published by the King Fahd Glorious Qurʾān Printing Complex (KFGQPC), and adds
the thing none of those packages contains: words, and a single numbering that
ties a word in one edition to the same word in the other six.

> نصُّ المصحف مطابق لطبعة مجمع الملك فهد بالمدينة، بسبع روايات، مرتبط بالإصدارات
> الرسمية للمجمع؛ كلُّ ملف يذكر الإصدار المأخوذ منه وتوقيعه. مع ترقيم لكلماته،
> يجعل لكل كلمة رقمٌ واحد يدلُّ عليها في الروايات السبع.

| Package | Version | Riwayat | Shared word numbers |
|---|---|---|---|
| `quran-text` — not published yet | `0.1.0` | 7 printed editions | 77,434 |

---

## What it provides

- **Seven complete printed muṣḥafs**, each on its own terms: its own spelling,
  its own waqf (pause) marks, its own āyah count, 604 pages and 8,820 lines.
  Not a font trick over one base text.
- **One shared word numbering.** Attach a translation, a grammar entry or an
  audio segment to a number once, and it is attached in all seven.
- **Surah, āyah, page, line and juz access** for each edition, plus waqf, sajdah
  and division marks, and a folded plain form for searching.
- **Provenance in every file**: the source package it was read from, the member
  inside it, the release year and its SHA-256 — plus each place the build
  departed from the package.
- **Six client libraries** — JavaScript, Python, PHP, Dart, Swift, Kotlin — with
  the same API and no dependencies. Ḥafṣ, the edition most of the world reads, is
  bundled inside each one, with the font it needs.

**Word 425**, from `data/differences.json` — sūrah 2, sixth word of āyah 28 in
Ḥafṣ, and of āyah 27 in five of the others:

| spelling | editions |
|---|---|
| فَأَحۡيَٰكُمۡ | Ḥafṣ · Shuʿbah · al-Dūrī · al-Sūsī |
| فَأَحۡيَٰكُمُۥ | al-Bazzī |
| فَأَحْيَاكُمْ | Qālūn |
| فَأَحْيٜاكُمْ | Warsh |

One number, four spellings, two different āyah numbers. Of the 77,434 numbers,
**277** are written differently somewhere — a different letter, a long ā written
or left out, a word boundary drawn elsewhere. The rest are the same word in every
edition that reads them. (Differences of vowelling and pointing alone are not in
that 277; they are in `data/word-index.json`, under each word's `groups`.)

## Use it when you need

- A text-based reader, search, or anything that stores Qurʾānic text.
- Access by surah, āyah, page, or juz.
- Stable word-level references that other data can hang off — translations,
  audio timings, annotations.
- More than one riwayah, and a way to say "the same word" across them.

## Not for

| You want | Use |
|---|---|
| The muṣḥaf as it looks on the printed page — geometry, not characters | [Quran SVG](https://quran.ws/blocks/quran-svg/) |
| Addressing a word or a mark *inside* the printed page | [Quran SVG Elements](https://quran.ws/blocks/quran-svg-elements/) |
| Rendering printed pages fast on a phone | [Quran Engine](https://quran.ws/blocks/quran-engine/) |
| Tajwīd colouring — the recitation rules, as spans over unchanged text | [Quran Tajweed](https://quran.ws/blocks/quran-tajweed/) |
| Converting an āyah reference between the six counting traditions | [Qiraat Ayah Map](https://quran.ws/blocks/qiraat-ayah-map/) |

This repository is the text: characters, not shapes. It never draws anything and
never colours anything. Of the three page-side siblings, Quran SVG is the archive
of vectorised muṣḥafs and addresses an āyah; Quran SVG Elements covers only the
muṣḥafs that have been split apart, and addresses a word or a mark inside them;
Quran Engine renders those same split muṣḥafs on a phone, where SVG does not
perform.

## See it work

<https://quran.ws/blocks/quran-text/> runs four things against the data
committed here:

- **How it is built** — seven files, one numbering, and a flat array of words
  with offsets instead of a tree.
- **One number, seven riwayat** — all 277 words that are spelt differently
  somewhere, each with its groups of editions.
- **Āyah lookup** — pick a reference and a riwayah and see the text with its
  shared word numbers, and the surah's āyah count change under you.
- **Download builder** — the URL patterns the `service/` directory serves.

## Supported riwayat

If you do not know which you need, it is **Ḥafṣ**. It is the default in every
library here, and it is what most of the world reads.

| riwayah | qāriʾ | counting system | āyāt printed | words printed | source release |
|---|---|---|---|---|---|
| Ḥafṣ | ʿĀṣim al-Kūfī | Kūfī | 6,236 | 77,432 | v3.0, 2026 |
| Shuʿbah | ʿĀṣim al-Kūfī | Kūfī | 6,236 | 77,432 | v3.0, 2026 |
| Warsh | Nāfiʿ al-Madanī | Last Madinan | 6,214 | 77,431 | v3.0, 2026 |
| Qālūn | Nāfiʿ al-Madanī | Last Madinan | 6,214 | 77,431 | v3.0, 2026 |
| al-Dūrī | Abū ʿAmr al-Baṣrī | First Madinan | 6,217 | 77,431 | **V20, 2022** |
| al-Sūsī | Abū ʿAmr al-Baṣrī | First Madinan | 6,218 | 77,431 | v3.0, 2026 |
| al-Bazzī | Ibn Kathīr al-Makkī | Makkī | 6,220 | 77,432 | v3.0, 2026 |

Six editions are built from KFGQPC's 2026 v3.0 packages; **al-Dūrī is built from
the 2022 `UthmanicDouri_V20.zip`**, because no later release exists. It is also
the one edition whose two source packages are both from 2022, so it cannot be
cross-checked the way the others are.

Juz is recorded for every edition except al-Bazzī, whose source carries none —
the file says so itself, in `layers.absent`, rather than throwing at you later.

### Why 77,434, 77,432 and 77,431 are all correct

Three word counts appear in this repository, and they are not in conflict:

- **77,432 / 77,431** — the words a given edition *prints*.
- **77,434** — the shared numbers. The numbering counts the finest division any
  of the seven makes, so it is a superset of every edition.

An edition reaches the total two ways: some numbers it does not read at all
(`numbering.missing`), and some words it prints joined where another prints two
(`numbering.written_joined`), so one printed word covers two numbers.

```sh
$ cd data/mushaf && node -e '
for (const k of ["hafs","warsh","susi"]) {
  const d = require(`./${k}.json`), n = d.numbering;
  const j = n.written_joined.reduce((a, r) => a + r.numbers.length - 1, 0);
  console.log(k, d.words.length, "+", j, "+", n.missing.length,
              "=", d.words.length + j + n.missing.length, "==", n.total);
}'
hafs 77432 + 1 + 1 = 77434 == 77434
warsh 77431 + 0 + 3 = 77434 == 77434
susi 77431 + 1 + 2 = 77434 == 77434
```

`words.length + Σ(joined run − 1) + missing.length == numbering.total` holds in
all seven files. The build asserts it.

### A muṣḥaf's āyah count is not its counting system's total

This is the trap. *Āyah-counting* is a scholarly tradition about where āyāt end
([glossary](https://quran.ws/docs/concepts/glossary/#ayah-counting)), and there
are six such systems. An edition follows one of them — and still does not print
that system's published total, because there are recorded points of disagreement
*inside* a system.

al-Sūsī is the clearest case. Its file records the First Madinan system, and it
prints **6,218** āyāt, while
[qiraat-ayah-map](https://quran.ws/blocks/qiraat-ayah-map/) publishes First
Madinan's total as **6,214**. Both numbers are right about different things.
Never derive one from the other, and never hard-code either.

> **Unresolved, and stated here rather than decided.** `quran-text` measures
> al-Dūrī and al-Sūsī against the six systems and puts both under First Madinan
> (distance 0 and 1 āyah ends, against 97 and 98 to the Baṣran set).
> `qiraat-ayah-map` assigns their qāriʾ, Abū ʿAmr al-Baṣrī, to the Baṣran
> counting, total 6,204. Neither KFGQPC package declares a system, so nothing in
> either repository settles it. This needs a ruling from someone qualified in
> qirāʾāt; until then the two repositories disagree, and anyone joining them
> should know it.

## Provenance

The text is KFGQPC's own, unedited. Every muṣḥaf file names the package it came
from and that package's SHA-256:

```json
"provenance": { "text": { "package": "UthmanicHafs-v-3.0.zip",
                          "member":  "UthmanicHafs-v-3.0.docx",
                          "release_year": 2026,
                          "sha256": "cdec7341b7c684e7b8dd469c4b68988914d2784e924c7e6cbb9cb4b57c24f013" } }
```

`python3 pipeline/build.py` rebuilds everything in `data/` from the committed
packages, offline, with no dependencies. Nothing is hand-edited, and the build
fails if a letter moves.

**What that proves, and what it does not.** The checks prove the data is faithful
to the packages; they do not prove the packages are faithful to a printed
muṣḥaf. Word boundaries are derived from KFGQPC's own typesetting, not from any
doctrinal source. The rasm — the bare consonantal skeleton
([glossary](https://quran.ws/docs/concepts/glossary/#rasm)) — is reconstructed by
normalising the vowelled text, not transcribed from a manuscript. Seven riwayat
is four of the seven canonical qāriʾs: Qunbul, Ibn ʿĀmir, Ḥamzah and al-Kisāʾī
are absent, so this is not a complete qirāʾāt comparison.
[`docs/limitations.md`](docs/limitations.md) states all of it, and says plainly
that **before any use where correctness of the sacred text matters, this needs
review by someone qualified in qirāʾāt against printed maṣāḥif.**

Two more things worth knowing before you build on it:

- **Join on `key`, not on the number.** The shared number is a position, so a
  future release that adds a word shifts every number after it. `key`
  (`sūrah:pointed#occurrence`, e.g. `2:فاحياكم#1`) and the Ḥafṣ `{surah, ayah,
  position}` coordinates come from the text itself and survive.
- **Ship the font.** Some words use codepoints Unicode only added in 2021, and
  almost no general font draws them — 19,431 words in Warsh, 19,183 in al-Sūsī,
  17,527 in Qālūn. Without the right font your users see empty boxes. Every file
  names the font KFGQPC ships with its text, and the build copies it to
  `data/fonts/`.

## Quick start

**There is nothing to install yet.** The repository is private, has no releases,
and nothing is published on npm, PyPI, Packagist, pub.dev or Maven Central. The
package manifests are complete and `v1.0.0` is being held deliberately until two
format-visible questions are settled — see [`docs/launch.md`](docs/launch.md).

Until then: clone the repository and point at `lib/<language>/` directly. Every
library bundles Ḥafṣ, so only the Warsh line below reads a file from `data/`.

```js
import { Mushaf } from "./lib/js/quran-text.js";

const m = await Mushaf.hafs();                            // bundled, no download
const warsh = await Mushaf.load("data/mushaf/warsh.json"); // another riwayah, Node

m.ayah(2, 255).render({ marks: true, ayahMarks: true });
m.word(1, 4, 1).number;
m.search("مالك يوم الدين")[0];
m.word(2, 255, 3).to(warsh).number;
m.ayah(2, 255).to(warsh).key;
```

Those five expressions, run against commit
`fea25cd0f781ead81fc33ce91225f6ce17f8283f`, give:

```
ٱللَّهُ لَآ إِلَٰهَ إِلَّا هُوَ ٱلۡحَيُّ ٱلۡقَيُّومُۚ … وَهُوَ ٱلۡعَلِيُّ ٱلۡعَظِيمُ ۝٢٥٥
11                       ← the shared number of مَٰلِكِ, sūrah 1 āyah 4
start 10, end 13         ← the words مَٰلِكِ يَوۡمِ ٱلدِّينِ matched
5177 إِلَٰهَ              ← the same word, in Warsh
2:253-254  (split)       ← Ḥafṣ's 2:255 is two āyāt in Warsh
```

The same lines exist in Python, PHP, Dart, Swift and Kotlin
(`pip install ./lib/python` and equivalents), tested against the same facts.
[`lib/README.md`](lib/README.md) has the full API.

**In a browser**, use `Mushaf.fromJson(await (await fetch(url)).json())`;
`Mushaf.load` is Node only. Note the size before you decide: a muṣḥaf file is the
smallest unit there is — 1.9–3.1 MB of JSON, about 550 KB gzipped for Ḥafṣ —
and there is no per-surah file. The `service/` directory answers by scope on the
server, but is not deployed anywhere public yet.

## Works with

| | |
|---|---|
| [Quran Tajweed](https://quran.ws/blocks/quran-tajweed/) | Colours this text without changing a character — it ships positions, not text. |
| [Qiraat Ayah Map](https://quran.ws/blocks/qiraat-ayah-map/) | Converts an āyah reference between counting systems. Its boundaries are vendored here at a pinned commit. |
| [Quran SVG Elements](https://quran.ws/blocks/quran-svg-elements/) | Links a word number to the printed shape of that word on the page. |
| [Quran Engine](https://quran.ws/blocks/quran-engine/) | Search and highlight by word number, rendered fast on a phone. |

## Documentation

[`design.md`](docs/design.md) why the format is shaped this way ·
[`format.md`](docs/format.md) the spec ·
[`files.md`](docs/files.md) every file in `data/` ·
[`method.md`](docs/method.md) how it is built ·
[`sources.md`](docs/sources.md) what it is built from ·
[`known-issues.md`](docs/known-issues.md) and
[`limitations.md`](docs/limitations.md) what to be careful with ·
[`verify-in-print.md`](docs/verify-in-print.md) what is still unknown, and where
in a printed muṣḥaf to look ·
[`launch.md`](docs/launch.md) what stands between this and a public release.

Long-form, with no Qurʾānic background assumed:
<https://quran.ws/docs/reference/quran-text/>.

## Licence

**One licence, CC BY 4.0, across the whole repository** — the dataset, the
pipeline, the docs and all six client libraries.

That is deliberate, and against the usual advice. MIT is what a developer
pulling this from npm or PyPI would expect, but every client package *bundles
the dataset*: `hafs.json` travels inside it. An MIT wrapper around CC BY 4.0
data would put two licences in one package and, in practice, let the data reach
people with the attribution stripped — the one thing this licence exists to
prevent. If you need the library code under different terms, ask.

Attribution is **waived for use inside a product**, and required on
republication — if a third party can obtain the data *as data* from what you
ship, that is republication:

> quran-text by quran-ws — https://github.com/quran-ws/quran-text — CC BY 4.0

**The Qurʾānic text itself is not this project's to license.** The KFGQPC source
packages in `sources/kfgqpc/` and the fonts in `data/fonts/` are the King Fahd
Glorious Qurʾān Printing Complex's, included as received, under their own terms.
[`LICENSE`](LICENSE) and [`NOTICE.md`](NOTICE.md) draw the line precisely.
