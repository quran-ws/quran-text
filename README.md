# quran-text

**The Qurʾān exactly as the Madinah muṣḥaf prints it.** Seven riwāyāt,
unedited — every file names the package it came from and its SHA-256.

And every word carries one number that means the same word in all seven.

**Building an app** → [Use it in your app](#use-it-in-your-app) ·
**Just need the files** → [Download the text](#download-the-text) ·
**Checking the source** → [Where the text comes from](#where-the-text-comes-from)

نصُّ المصحف كما يطبعه مجمع الملك فهد بالمدينة، في سبع روايات، دون تعديل؛ كلُّ
ملف يذكر الإصدار المأخوذ منه وبصمته. ولكلِّ كلمة رقمٌ واحد يدلُّ عليها في
الروايات السبع جميعًا.

ابدأ من `lib/` إن كنت تبني تطبيقًا، ومن `service/` إن أردت تنزيل النص بالصيغة
التي تريد، ومن `data/` إن كنت تعمل على البيانات مباشرة.

## Use it in your app

Ḥafṣ is bundled with every library; nothing to download, nothing to know about
riwāyāt.

```python
from quran_text import Mushaf

m = Mushaf.hafs()
m.ayah(2, 255).render(marks=True, ayah_marks=True)  # ٱللَّهُ لَآ إِلَٰهَ إِلَّا هُوَ ٱلۡحَيُّ ٱلۡقَيُّومُۚ …
m.page(3).lines                                     # a printed page, line by line
m.juz(30).ayahs
m.search("مالك يوم الدين")                          # → [Span(10, 13)]
```

The same six lines in Python, JavaScript, PHP, Dart, Swift and Kotlin — one
package each, no dependencies, tested against the same facts.
[`lib/`](lib/) has the full API.

**Nothing is on PyPI or npm yet.** Install from the directory
(`pip install ./lib/python`) or copy the file in.

**Ship the font.** Some words use codepoints Unicode only added in 2021, and
almost no general font draws them — without the right font your users see empty
boxes. Every muṣḥaf file names the font that ships with its source package, and
the build copies it to [`data/fonts/`](data/fonts/); Warsh, Qālūn and Sūsī
need it most.

**Join on `key`, not on the number.** The shared number is a position, so a
future release that adds a word shifts it. `key` (`sūrah:pointed#occurrence`)
and the Ḥafṣ `{surah, ayah, position}` coordinates come from the text itself
and survive.

**Ship it commercially**, no permission needed — keep the attribution line
below. The Qurʾānic text itself stays its publisher's, under their terms.

Āyah numbers are the edition's own, and the libraries convert:

```python
warsh = Mushaf.load("data/mushaf/warsh.json")

m.ayah(2, 255).to(warsh)      # AyahMatch(2:253-254, split)
m.word(2, 255, 3).to(warsh)   # Word(5176, 'إِلَٰهَ')
```

## One number, seven riwāyāt

**Word 425** — sūrah 2, āyah 28, sixth word:

| | |
|---|---|
| Ḥafṣ · Shuʿbah · Dūrī · Sūsī | فَأَحۡيَٰكُمۡ |
| Bazzī | فَأَحۡيَٰكُمُۥ |
| Qālūn | فَأَحْيَاكُمْ |
| Warsh | فَأَحْيٜاكُمْ |

One number, four spellings. There are **77,434 numbers**; **277** read like
this and the rest are the same word everywhere. Attach a translation, a grammar
entry or an audio segment to a number once, and it is attached in all seven.

None of the published Madinah packages contain word-level data — every one of
them is āyah-level ([`docs/sources.md`](docs/sources.md)). The words, and the
number that ties them together, are what this repository derives.

## Download the text

Any riwāyah, any scope, six formats — the URL *is* the file:

```text
/download?edition=hafs&surah=2&format=txt

# quran-text — Ḥafṣ (حفص), ʿĀṣim al-Kūfī, Kufi Numbering count, 6236 āyāt
# source: UthmanicHafs-v-3.0.zip :: UthmanicHafs-v-3.0.docx  sha256 cdec7341…
2|1|الٓمٓ
2|2|ذَٰلِكَ ٱلۡكِتَٰبُ لَا رَيۡبَۛ فِيهِۛ هُدࣰى لِّلۡمُتَّقِينَ
```

`txt` `json` `csv` `xml` `sql` `md` · rasm ʿUthmānī, imlāʾī or plain · waqf,
sajdah and division marks on or off · by sūrah, juz, page or āyah range · by
āyah or by word. Every response carries that provenance header and an
`X-Checksum-SHA256` of the body. The work here is CC BY 4.0; the text stays the
publisher's, under their terms. [`service/`](service/) runs it in two commands.

## Where the text comes from

The text is the Madinah muṣḥaf's own: the digital packages published by the King
Fahd Glorious Qurʾān Printing Complex (KFGQPC), unedited. Every file names the
package it came from and its SHA-256, and lists in the file itself each place
the build departed from it:

```json
"hafs": { "text": { "package": "UthmanicHafs-v-3.0.zip",
                    "sha256": "cdec7341b7c684e7b8dd469c4b68988914d2784e924c7e6cbb9cb4b57c24f013" } }
```

`python3 pipeline/build.py` rebuilds every file in `data/` from those
committed packages, offline, with no dependencies. Nothing in the text is
hand-edited, and the build fails if a letter moves.

The checks prove the data is faithful to the packages, not that the packages are
faithful to a printed muṣḥaf. [`limitations.md`](docs/limitations.md) says
exactly what is and is not verified.

## Which riwāyah do you need?

If you don't know, **Ḥafṣ** — it is what most of the world reads, and it is the
default in every library here. The other six are there for when you need them.

| riwāyah | qāriʾ | counting | āyāt | words |
|---|---|---|---|---|
| Ḥafṣ | ʿĀṣim al-Kūfī | Kūfī | 6,236 | 77,432 |
| Shuʿbah | ʿĀṣim al-Kūfī | Kūfī | 6,236 | 77,432 |
| Warsh | Nāfiʿ al-Madanī | Madanī (last) | 6,214 | 77,431 |
| Qālūn | Nāfiʿ al-Madanī | Madanī (last) | 6,214 | 77,431 |
| Dūrī | Abū ʿAmr al-Baṣrī | Madanī (first) | 6,217 | 77,431 |
| Sūsī | Abū ʿAmr al-Baṣrī | Madanī (first) | 6,218 | 77,431 |
| Bazzī | Ibn Kathīr al-Makkī | Makkī | 6,220 | 77,432 |

Each is a printed muṣḥaf on its own terms: 604 pages, 8,820 lines, its own
spelling, waqf marks and āyah count — not a font trick over Ḥafṣ. Juz is
recorded for all but Bazzī, whose source carries none.

## Where to go

| you are… | go to |
|---|---|
| working with the data | [`data/`](data/) — start at [`catalog.json`](data/catalog.json); [`docs/files.md`](docs/files.md) maps every file |
| an agent | [`skills/quran-text/SKILL.md`](skills/quran-text/SKILL.md) |

## Build

Python 3.11, no dependencies:

```sh
python3 pipeline/build.py                          # ~3 min, writes data/
python3 -m unittest discover -s pipeline/tests
```

## Licence

**[CC BY 4.0](LICENSE)** — anywhere, commercially, no permission needed. One
condition: keep the link.

> quran-text by quran-ws — https://github.com/quran-ws/quran-text — CC BY 4.0

That covers the work done here: the word index and its numbering, the
alignment, the counting analysis, the code and the docs. It does **not** cover
the Qurʾānic text or the KFGQPC packages and fonts in `sources/kfgqpc/` and
`data/fonts/`, which remain KFGQPC's under KFGQPC's terms.
[`NOTICE.md`](NOTICE.md) draws the line precisely.

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
[`launch.md`](docs/launch.md) what stands between this and a public release
