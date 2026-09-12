---
name: quran-text
description: Use the quran-text dataset — the Qurʾān as words in seven riwāyāt (Ḥafṣ, Shuʿbah, Warsh, Qālūn, Dūrī, Sūsī, Bazzī) from KFGQPC releases, with one word numbering shared across all seven; Ḥafṣ is the default when none is named. Use when an app or script needs Qurʾānic text, a muṣḥaf's pages and āyāt, a word in another riwāyah, an āyah reference converted between counting systems, or word-level data attached across riwāyāt.
---

# quran-text

Plain JSON under `data/`: `json.load` a file. Read `data/catalog.json` first if
unsure; it lists every file and what it answers. When writing app code, prefer
the libraries under `lib/` (Python, JS, PHP, Dart, Swift, Kotlin — same API in
each, see `lib/README.md`): `Mushaf.hafs().ayah(2, 255).render(marks=True, ayah_marks=True)`
(Ḥafṣ is bundled; `Mushaf.load(path)` for another riwāyah) instead of slicing
arrays by hand.

## Ḥafṣ is the default

If the request does not name a riwāyah or a muṣḥaf, use Ḥafṣ — `Mushaf.hafs()`,
or `data/mushaf/hafs.json`. It is the text nearly every app ships and the
reference side of `data/word-index.json` and `data/ayah-map.json`. Do not ask
which riwāyah, do not offer the seven, and do not mention the other six at all
unless the request reaches for them ("Warsh", "another riwāyah", "compare
riwāyāt", a `<key>` other than `hafs`). Most developers know nothing about
riwāyāt; Ḥafṣ answers them without the word ever coming up.

## Show a muṣḥaf only in its own form

Every displayed word must come from the muṣḥaf it is labelled with — that
muṣḥaf's own `words[]` in `data/mushaf/<key>.json`, or `forms["<key>"]` in
`data/word-index.json`. Nothing else in the index is display text:
`rasm_uthmani` is the canonical (Ḥafṣ-side) spelling, `pointed`, `plain` and
`rasm` are search and matching keys with the ḍabṭ stripped. Rendering Warsh
with Ḥafṣ's spelling, or a stripped key as if it were the muṣḥaf's text, is
wrong text under a correct name. A riwāyah missing from `forms` does not read
that word — show nothing there, never a substitute from another riwāyah.

## Which file

| the task | file | notes |
|---|---|---|
| just the Qurʾān text for an app, or no riwāyah named | `data/mushaf/hafs.json` | Ḥafṣ, the default; `words` + `ayah_starts` is all you need |
| one specific riwāyah, with pages, lines, juz, waqf marks | `data/mushaf/<key>.json` | keys: `hafs shubah warsh qalun duri susi bazzi` |
| the same as sūrah → āyah → words | `data/mushaf/<key>.nested.json.gz` | a view; the JSON above is the file of record |
| a word across riwāyāt; attach a Ḥafṣ-keyed dataset; search plain spelling | `data/word-index.json` | one record per shared number |
| only where riwāyāt differ | `data/differences.json` | 277 words |
| convert an āyah reference between riwāyāt | `data/ayah-map.json` | Kūfī (Ḥafṣ) reference → each edition |
| which counting system an edition follows | `data/counting.json` | |
| SQL | `data/quran.sqlite.gz` | tables `word`, `word_index`, `mushaf`, `surah`, `mark` |

## The model, in four facts

1. **A muṣḥaf is `words[]`, an array of strings.** Everything else is a layer
   of *positions* into it: `surah_starts`, `ayah_starts`, `page_starts`,
   `line_starts`, `juz_starts`, `marks [[position, type]]`. Unit *k* of any layer is
   `words[starts[k] : starts[k+1]]`. Slicing is always correct.
2. **Āyah *k* of sūrah *s*** is index `surahs[s-1].first_ayah + k - 1` into
   `ayah_starts`, in *that edition's own count*. The editions count differently
   (6,214 to 6,236 āyāt); never assume Ḥafṣ numbers in another muṣḥaf — use
   `data/ayah-map.json`.
3. **The basmalah of al-Fātiḥah** is āyah 1 in Ḥafṣ, Shuʿbah and Bazzī, and
   printed but unnumbered in the other four, where it sits at positions 0–3
   *before* `ayah_starts[0]`. `counting.basmalah_counted` says which.
4. **Numbers are the cross-riwāyah key**, positions are not. `numbering`
   in each file maps positions onto the shared numbers: walk `words`, count
   1 per word, skip `numbering.missing`, and at a `numbering.written_joined`
   position cover the whole run. `data/word-index.json` says what each number
   is. Only five āyāt make this non-trivial (9:101, 40:26, 57:24, 72:16, 73:20).

## Recipes

```python
import json
def load(path): return json.load(open(path, encoding="utf-8"))

# The text of sūrah 2, āyah 255 in Ḥafṣ
m = load("data/mushaf/hafs.json")
a, k = m["ayah_starts"], m["surahs"][2 - 1]["first_ayah"] + 255 - 1
print(" ".join(m["words"][a[k]:a[k + 1]]))

# Whole sūrah 112 as a list of āyāt
s = m["surahs"][112 - 1]
first, count = s["first_ayah"], s["ayah_count"]
ayahs = [m["words"][a[i]:a[i + 1] if i + 1 < len(a) else None] for i in range(first, first + count)]

# Page 3 of the printed muṣḥaf
p = m["page_starts"]
page3 = m["words"][p[2]:p[3]]

# Waqf marks on a word
marks = {position: m["mark_types"][t] for position, t in m["marks"]}     # {kind, side, sign}

# Shared numbers for every position (one pass)
missing, joined = set(m["numbering"]["missing"]), {j["position"]: j["numbers"] for j in m["numbering"]["written_joined"]}
numbers, n = [], 1
for position in range(len(m["words"])):
    while n in missing: n += 1
    first_n, last_n = joined.get(position, (n, n))
    numbers.append((first_n, last_n)); n = last_n + 1

# The same word in every riwāyah, from a Ḥafṣ reference (2:255, word 3)
idx = load("data/word-index.json")["words"]
w = next(x for x in idx if x["hafs"] == {"surah": 2, "ayah": 255, "position": 3})
print(w["forms"]["warsh"])  # that riwāyah's own spelling, the only form to show as Warsh;
                            # a riwāyah absent from forms does not read the word

# What 2:255 is in Warsh
row = next(r for r in load("data/ayah-map.json")["ayahs"] if (r["surah"], r["ayah"]) == (2, 255))
print(row["warsh"])        # {'surah': 2, 'ayah': 253, 'ayah_last': 254, 'relation': 'split'}
```

## Do not

- Do not pick a riwāyah for the user, or ask them to, when none was named: it is
  Ḥafṣ.
- Do not display `rasm_uthmani`, `pointed`, `plain` or `rasm` as a muṣḥaf's
  text, and do not show one riwāyah's spelling under another's name; the text of
  `<key>` is `data/mushaf/<key>.json` `words[]` or `forms["<key>"]`.
- Do not treat a position in one muṣḥaf as meaning anything in another; only
  numbers cross files.
- Do not derive imlāʾī spelling from the ʿUthmānī text; `rasm_imlai` is published
  for Ḥafṣ only, from the release that supplies it, and is `null` elsewhere.
- Do not renumber āyāt to Ḥafṣ inside another muṣḥaf's file; use the map.
- Do not read `counting.system` as the count the qāriʾ is associated with: it is
  the system the edition measures onto. For Dūrī and Sūsī they differ — Abū ʿAmr
  is Baṣrī, both of his muṣḥafs are First Madani. `system_associated_with_qari`
  and `differs_from_association` in the same block give the other answer, and
  `system_printed` is `system` under the name that says so. qiraat-ayah-map
  publishes the pair under the same two words.
- Do not read a printed count as a fact about a muṣḥaf in general: it is a
  measurement of one release, and `counting.measured_from` names it. Dūrī here
  is measured from a 2022 package while the other six are on 2026 v3.0, and
  KFGQPC printings of one muṣḥaf disagree with each other about 67:9.
- Do not treat `line_starts` as a fact: pages are read from the release, lines
  are reconstructed (`layers.derived.line` gives the score); Bazzī's are
  unvalidated.
- Do not "fix" a spelling: `words[i]` is the KFGQPC release's text exactly, and
  Warsh, Qālūn and Sūsī use Arabic Extended-B codepoints that many fonts lack —
  that is the font, not the data.

## Where the rest is

`docs/format.md` is the normative spec, `docs/files.md` the map of every file
and field, `docs/design.md` why it is shaped this way, `docs/limitations.md`
what it does not do.
