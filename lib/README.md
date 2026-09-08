# Libraries

The Qurʾān for your app in one call. Ḥafṣ is bundled with every package; no
file to find, nothing to know about riwāyāt.

```python
from quran_text import Mushaf
m = Mushaf.hafs()
m.ayah(2, 255).text                                   # the words
m.ayah(2, 255).render(marks=True, ayah_marks=True)  # with waqf marks and ۝٢٥٥
m.page(3).lines                                       # a printed page, line by line
m.juz(30).ayahs                                        # a juz
m.search("مالك يوم الدين")                            # find text
```

The same six lines in every language:

| platform | package | Ḥafṣ | test |
|---|---|---|---|
| Python 3.9+ | [`python/`](python/), no dependencies | `Mushaf.hafs()` | `python3 -m unittest lib/python/test_quran_text.py` |
| JavaScript / TypeScript | [`js/`](js/), ESM with `.d.ts`, no dependencies | `await Mushaf.hafs()` | `cd lib/js && node --test` |
| PHP 8.1+ | [`php/`](php/), Composer, `QuranText\` | `Mushaf::hafs()` | `cd lib/php && php -d memory_limit=1G tests/run.php` |
| Dart / Flutter | [`dart/`](dart/), pub package `quran_text` | `await Mushaf.hafs(read: rootBundle.loadString)` | `cd lib/dart && dart test` |
| Swift (iOS, macOS) | [`swift/`](swift/), Swift Package `QuranText` | `try Mushaf.hafs()` | `cd lib/swift && swift test` |
| Kotlin (Android, JVM) | [`kotlin/`](kotlin/), Gradle, `org.json` only | `Mushaf.hafs()` | `cd lib/kotlin && gradle test` |

Every test suite runs against the built `data/` and checks the same facts, so
the six behave identically. Names follow each language's convention
(`ayah_marks` in Python, `ayahMarks` elsewhere); nothing else changes.

## What you can ask a muṣḥaf

Everything is a *span* of one `words` array, and every span has `words`,
`text`, `render(...)`, `ayahs`, `pages`, `page`, `juz`, `marks` and `word(i)`.

```
Mushaf
 ├─ surah(n)             Surah  — ayahs, ayah(n), nameAr, nameEn, revelation, firstPage, lastPage, basmalah
 ├─ ayah(surah, n)       Ayah  — key "2:255", page, juz, line, lines, next(), previous(), hasSajdah, marker
 ├─ page(n)             Page  — lines, line(n), ayahs, surahs, next(), previous()
 ├─ line(page, n)       Line  — page, number within the page, ayahs
 ├─ juz(n)              Juz   — ayahs, pages, firstAyah, lastAyah
 ├─ word(surah, ayah, i) Word  — text, rasm_imlai, number, marks, page, line, juz, render()
 ├─ span(start, end)    Span  — any run of positions
 ├─ wordAt / ayahAt / surahAt / pageAt / lineAt / juzAt (position)
 ├─ sajdat(), divisionMarks(), search(text)
 ├─ numberAt(position), wordByNumber(number)   — the numbering shared by all seven riwāyāt
 └─ has("juz"), layers, counting, provenance, ayahCount, pageCount …
```

`render(marks, ayahMarks, lines)`:

| option | what it adds |
|---|---|
| `marks` | the signs the muṣḥaf prints: `waqf` (attached to the word), `division` (`۞` before the word), `sajdah` (`۩`). `true` / `.all` for every kind, or a set of kinds |
| `ayahMarks` | `۝` with the āyah number in Arabic-Indic digits after each āyah that ends inside the span |
| `lines` | a newline where the printed line breaks (lines are reconstructed; see `docs/format.md`) |

Search matches on a fold that drops harakah and waqf marks and unifies
alif and yāʾ forms, so `مالك يوم الدين` finds `مَٰلِكِ يَوۡمِ ٱلدِّينِ`.

## The font

The text is set in a KFGQPC font that ships with it, and it is the only font
guaranteed to draw every codepoint the words use. Each muṣḥaf tells you which:

```python
m.font.family     # "KFGQPC HAFS Uthmanic Script"
m.font.file       # "data/fonts/UthmanicHafs-v-3.0.ttf"
```

Every package bundles the Ḥafṣ font next to `hafs.json`: Flutter gets it as
`TextStyle(fontFamily: m.font.family, package: 'quran_text')`, the web as
`m.fontFace()` for a `@font-face` rule, Swift and Kotlin as a file to register
with the system. For another riwāyah take its font from `data/fonts/` (or the
download service) and register it the same way.

## When you need another riwāyah

Ḥafṣ is one of seven riwāyāt here: Ḥafṣ, Shuʿbah, Warsh, Qālūn, Dūrī, Sūsī
and Bazzī, each a printed muṣḥaf of its own. Load one with `Mushaf.load(path)`
from `data/mushaf/<key>.json` (or download it from the service), and know three
things:

1. **Āyah numbers are the edition's own.** `warsh.ayah(2, 253)` is āyat
   al-Kursī; `warsh.ayah(2, 255)` is a different āyah. To convert a Ḥafṣ
   reference use `AyahMap`: `map.convert(2, 255, "warsh")` → `2:253-254 (split)`.
2. **The basmalah of al-Fātiḥah is unnumbered in Warsh, Qālūn, Dūrī and Sūsī.**
   There `surah(1).basmalah` holds it, `ayah(1, 1)` starts at الحمد, and
   `wordAt(0).ayah` is null. `basmalahCounted` says which case you are in.
3. **Bazzī has no juz layer and only Ḥafṣ has imlāʾī.** Check `has("juz")` /
   `has("rasm_imlai")` first; `juz(n)` on Bazzī fails with the reason from the file.

Warsh, Qālūn and Sūsī use Arabic Extended-B codepoints that general fonts
cannot draw; the text looks blank, but it is not missing. Ship the font named
in that muṣḥaf's `font` block, from `data/fonts/`.

**Mapping between riwāyāt** is one call each way, for āyāt and for words,
and it works between any two of the seven directly:

```python
hafs.ayah(2, 255).to(warsh)        # AyahMatch(2:253-254, split): .ayahs, .first, .last, .relation
warsh.ayah(2, 253).to(duri)       # AyahMatch(2:253, merged)
hafs.word(2, 255, 3).to(warsh)     # Word('إِلَٰهَ') — or None where that riwāyah does not read it
```

`relation` is `same`, `merged`, `split`, `shifted`, `unnumbered` (the
basmalah) or `missing`, with the same meaning as in `ayah-map.json`; the
result is computed from the shared numbering, so the two always agree.
(The method is `to`, not `in`, because `in` is a reserved word in four of the
six languages.)

`Word.number` is the numbering shared by all seven. `WordIndex`
(`data/word-index.json`, 50 MB, for servers and build steps rather than phones)
says what a number is everywhere:

```python
idx.word(11).forms            # {'hafs': 'مَٰلِكِ', 'warsh': 'مَلِكِ', …}
idx.find(2, 255, 3)           # by Ḥafṣ coordinates
idx.search("مالك")            # by plain spelling
```
