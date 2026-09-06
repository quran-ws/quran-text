---
name: quran-text
description: Use the quran-text dataset — the Qurʾān as words in seven riwāyāt (Ḥafṣ, Shuʿbah, Warsh, Qālūn, Dūrī, Sūsī, Bazzī) from KFGQPC releases, with one word numbering shared across all seven. Use when an app or script needs Qurʾānic text, a muṣḥaf's pages and āyāt, a word in another riwāyah, an āyah reference converted between counting systems, or word-level data attached across riwāyāt.
---

# quran-text

Plain JSON under `out/`: `json.load` a file. Read `out/catalog.json` first if
unsure; it lists every file and what it answers. When writing app code, prefer
the libraries under `lib/` (Python, JS, PHP, Dart, Swift, Kotlin — same API in
each, see `lib/README.md`): `Mushaf.hafs().ayah(2, 255).render(marks=True, ayah_markers=True)`
(Ḥafṣ is bundled; `Mushaf.load(path)` for another riwāyah) instead of slicing
arrays by hand.

## Which file

| the task | file | notes |
|---|---|---|
| just the Qurʾān text for an app | `out/mushaf/hafs.json` | Ḥafṣ, the text nearly every app uses; `words` + `ayah_starts` is all you need |
| one specific riwāyah, with pages, lines, juz, pause marks | `out/mushaf/<key>.json` | keys: `hafs shuba warsh qaloun douri sousi bazzi` |
| the same as sūrah → āyah → words | `out/mushaf/<key>.nested.json.gz` | a view; the JSON above is the file of record |
| a word across riwāyāt; attach a Ḥafṣ-keyed dataset; search plain spelling | `out/word-index.json` | one record per shared number |
| only where riwāyāt differ | `out/differences.json` | 277 words |
| convert an āyah reference between riwāyāt | `out/ayah-map.json` | Kūfī (Ḥafṣ) reference → each edition |
| which counting system an edition follows | `out/counting.json` | |
| SQL | `out/quran.sqlite.gz` | tables `word`, `word_index`, `mushaf`, `sura`, `mark` |

## The model, in four facts

1. **A muṣḥaf is `words[]`, an array of strings.** Everything else is a layer
   of *positions* into it: `sura_starts`, `ayah_starts`, `page_starts`,
   `line_starts`, `juz_starts`, `marks [[pos, type]]`. Unit *k* of any layer is
   `words[starts[k] : starts[k+1]]`. Slicing is always correct.
2. **Āyah *k* of sūrah *s*** is index `suras[s-1].first_ayah + k - 1` into
   `ayah_starts`, in *that edition's own count*. The editions count differently
   (6,214 to 6,236 āyāt); never assume Ḥafṣ numbers in another muṣḥaf — use
   `out/ayah-map.json`.
3. **The basmalah of al-Fātiḥah** is āyah 1 in Ḥafṣ, Shuʿbah and Bazzī, and
   printed but unnumbered in the other four, where it sits at positions 0–3
   *before* `ayah_starts[0]`. `counting.basmalah_counted` says which.
4. **Numbers are the cross-riwāyah key**, positions are not. `numbering`
   in each file maps positions onto the shared numbers: walk `words`, count
   1 per word, skip `numbering.missing`, and at a `numbering.written_joined`
   position cover the whole run. `out/word-index.json` says what each number
   is. Only five āyāt make this non-trivial (9:101, 40:26, 57:24, 72:16, 73:20).

## Recipes

```python
import json
def load(path): return json.load(open(path, encoding="utf-8"))

# The text of sūrah 2, āyah 255 in Ḥafṣ
m = load("out/mushaf/hafs.json")
a, k = m["ayah_starts"], m["suras"][2 - 1]["first_ayah"] + 255 - 1
print(" ".join(m["words"][a[k]:a[k + 1]]))

# Whole sūrah 112 as a list of āyāt
s = m["suras"][112 - 1]
first, count = s["first_ayah"], s["ayah_count"]
ayat = [m["words"][a[i]:a[i + 1] if i + 1 < len(a) else None] for i in range(first, first + count)]

# Page 3 of the printed muṣḥaf
p = m["page_starts"]
page3 = m["words"][p[2]:p[3]]

# Pause marks on a word
marks = {pos: m["mark_types"][t] for pos, t in m["marks"]}     # {kind, side, sign}

# Shared numbers for every position (one pass)
missing, joined = set(m["numbering"]["missing"]), {j["position"]: j["numbers"] for j in m["numbering"]["written_joined"]}
numbers, n = [], 1
for pos in range(len(m["words"])):
    while n in missing: n += 1
    first_n, last_n = joined.get(pos, (n, n))
    numbers.append((first_n, last_n)); n = last_n + 1

# The same word in every riwāyah, from a Ḥafṣ reference (2:255, word 3)
idx = load("out/word-index.json")["words"]
w = next(x for x in idx if x["hafs"] == {"sura": 2, "ayah": 255, "pos": 3})
print(w["forms"])          # {'hafs': …, 'warsh': …, …}; a riwāyah absent here does not read the word

# What 2:255 is in Warsh
row = next(r for r in load("out/ayah-map.json")["ayat"] if (r["sura"], r["ayah"]) == (2, 255))
print(row["warsh"])        # {'sura': 2, 'ayah': 253, 'ayah_last': 254, 'relation': 'split'}
```

## Do not

- Do not treat a position in one muṣḥaf as meaning anything in another; only
  numbers cross files.
- Do not derive imlāʾī spelling from the ʿUthmānī text; `imlaei` is published
  for Ḥafṣ only, from the release that supplies it, and is `null` elsewhere.
- Do not renumber āyāt to Ḥafṣ inside another muṣḥaf's file; use the map.
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
