# The Madinah muṣḥaf approved in 1405H: page starts, line starts, waqf signs

`data/print/hafs-1405.json` says where this printed edition starts its pages
and lines, and which waqf signs it prints. It holds **no words**. Its positions
point into the 77,432 words of `data/mushaf/hafs.json`, which are unchanged.
The differences from the current Ḥafṣ are in
`data/reports/hafs-1405-differences.md`.

**The print is the reference.** The two lists it was checked against are credited
below. Where a list and the print had disagreed, the print would have been
published. They did not disagree.

## The scans

| id | file | what the book says of itself |
|---|---|---|
| a | `مصحف-المدينة_1406.pdf` | printed in 1406H; review decision dated 1 Jumādā al-Ūlā 1405H; «حقوق الطبع محفوظة» |
| b | `02. مصحف المدينة الإصدار القديم - 1405_1985.pdf` | no year of printing; the same decision of 1405H; thanks a ministry whose name is later than the one in a |

Hashes and full colophons are in `sources/prints/hafs-1405/print.json`. The
scans are not committed and the build does not read them.

Two cautions:

- **The file names are not evidence.** The PDF named 1405/1984 holds the same
  images as scan a, and scan b is probably a later printing than 1985. The
  edition is named after the review decision, which both books print.
- **The two scans differ in no page start, line start or waqf sign that was
  read.** No copy proved to be printed in 1405H was available.

## How it was read

| layer | published | matched in both scans | looked at in both scans | unproved |
|---|---|---|---|---|
| page starts | 604 | from the line starts | from the line starts | 0 |
| line starts | 8,820 | 8,774 | 46 | 0 |
| waqf signs | 4,359 | 4,234 | 125 | 0 |

*Matched* means that a drawing of the word or sign was compared with the ink of
each scan separately. *Looked at* means that a vision model compared crops of
both scans, one by one. It is not a person's reading. The repository owner
confirmed nine waqf signs.

For line starts, the first word of the line and the last word before it must
both score above 0.75 in both scans. For waqf signs, the same one of six
templates must win in both scans, at the same place.

The search for signs that the list lacks was made three ways, without the list:
over every word, over every whole page, and over every place with ink that no
drawn letter or vowel explains. It found none. The thresholds and results are
in `print.json`, under `method`.

## What it was checked against

| list | used for | result |
|---|---|---|
| [QUL, mushaf layout 15](https://qul.tarteel.ai/resources/mushaf-layout/15) | page and line starts | all 8,820 are the print's |
| [Tanzil](https://tanzil.net), Uthmani text 1.1 ([updates](https://tanzil.net/updates/)) | waqf signs | all 4,359 are in the print; no other was found |

No text of Tanzil is published here.

## Limits

- The scores come from word drawings whose place was fitted on these same
  scans. The neighbouring-line test and the reading by eye are the checks on
  that.
- The search cannot rule out a sign that is missing from the list, badly
  printed in both scans and covered by a drawn vowel. For ۘ, which resembles a
  ḍammah, only the search for unexplained ink counts.
- Absent, because they were not read from the print: the letters and vowels,
  the sajdah sign and line, the saktah sīn, ۞, the ḥizb and its parts, and the
  juz. The list is in `layers.absent`.

## Open questions

No copy proved to be printed in 1405H was available. The Complex's published
usage rights in `LICENSE` cover the print (see `NOTICE.md`).

## Use

```python
import hashlib, json
layers = json.load(open("data/print/hafs-1405.json"))
hafs = json.load(open(layers["base"]["file"]))
assert hashlib.sha256("\n".join(hafs["words"]).encode()).hexdigest() == layers["base"]["words_sha256"]
start, end = layers["line_starts"][0:2]
print(hafs["words"][start:end])
```
