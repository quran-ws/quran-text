# Design: why the text is flat, and what a number means

The seven riwāyāt almost always print the same words in the same order, and
disagree far more about where āyāt end than about words. That one fact decides
the shape of everything under `data/`.

```
sūrah  →  [ word, word, word, … ]
```

Not `sūrah → āyah → word`. The āyah number is an *attribute* of a word, not a
level of nesting — because **the count belongs to the printed edition, not to
the riwāyah**:

| edition | counting system | āyāt | at the points of khilāf inside the system |
|---|---|---|---|
| Ḥafṣ, Shuʿbah | Kūfī | 6,236 | — |
| Warsh, Qālūn | Last Madani | 6,214 | — |
| Dūrī | First Madani | 6,217 | 67:9 not counted, following Abū Jaʿfar |
| Sūsī | First Madani | 6,218 | 67:9 counted, following Shayba |
| Bazzī | Makkī | 6,220 | 78:40 counted, [not yet cited](known-issues.md) |

Each system is derived from what the edition prints, not assumed from the
riwāyah — the two Abū ʿAmr editions are First Madani, not Baṣrī, and they
differ from each other at exactly one documented point. Nesting words under
āyāt would make a number mean a different word in each edition. Flattening to
the sūrah makes one number stable across all of them, and the āyah boundaries
become their own layer over the word index: [`data/counting.json`](../data/counting.json).

The editions count 6,214 to 6,236 āyāt, so `2:255:3` names a different word
in each of them. Nesting words under āyāt would put the unstable coordinate on
the outside and make the seven files incomparable. Flattening to the sūrah
makes one number stable across all of them, and the āyah boundaries become a
layer over the words: `ayah_starts` in each muṣḥaf file, `counting.json` for
the systems.

## The count belongs to the edition

An āyah count is not a property of the riwāyah. It belongs to the **edition**,
and there is a level in between:

| level | what it is | example |
|---|---|---|
| **counting system** | one of the six madhhabs of ʿadd al-āy, as the classical sources define it | المدني الأول |
| **transmission within the system** | the system reached us through more than one authority, and at some points they differ | Abū Jaʿfar and Shayba differ at 3:92, 3:97, 37:167, 67:9, 80:24, 81:26 |
| **edition** | one printing declares a system and, at the points of khilāf inside it, follows one authority, a stated rule, or sets them aside | the 1429 KFGQPC Dūrī: «(٦٢١٤) … ما عدا الآيات المختلف فيها بين أبي جعفر وشيبة» |

Three KFGQPC printings of the Dūrī muṣḥaf carry two different āyah divisions
and three different colophons. None of that is an error; it is the third level
doing its job, and a string cannot hold it.
So the muṣḥaf file carries a `counting` block that names the derived system,
what the edition declares, and what it does at every point of khilāf inside
the system, specified in [`format.md`](format.md). What is left unexplained is
an open finding in [`known-issues.md`](known-issues.md).

## What makes a number mean one word

Words are identified by their **bare ʿUthmānic rasm** — undotted, unvowelled,
without hamzah — because that is what the seven riwāyāt actually share. The
codices were written that way, and a single skeleton carries several qiraahs
on purpose:

```
تَعۡمَلُونَ  ┐
           ├─►  ٮعملوں   one rasm, one number, two qiraahs
يَعۡمَلُونَ  ┘
```

Everything a scribe added later to fix a qiraah — dots, hamzah, vowels — is
exactly what the riwāyāt are allowed to disagree about, so none of it is part
of a word's identity. Each riwāyah's own spelling is kept in `forms`.

The numbering counts the **finest division** any muṣḥaf prints. Where one
muṣḥaf writes two words as one — `وَأَلَّوِ` at 72:16, `أَلَّن` at 73:20 — both
words keep a number and the joined word covers both; where a muṣḥaf does not
read a word — Bazzī's `مِن` at 9:101, Nāfiʿ's absent `هُوَ` at 57:24, `أَوۡ` at
40:26 — the number is simply missing from it. Nothing false is ever stated,
and each concept means one thing. Specified in
[`format.md`](format.md).

## Headline numbers

**77,434** numbers · **114** sūrahs · **7** riwāyāt.

| status | words | share | meaning |
|---|---|---|---|
| `identical` | 40,558 | 52.4% | one qiraah, one spelling, everywhere |
| `diacritic_variant` | 36,261 | 46.8% | same letters and dots — the vowelling differs |
| `dotting_variant` | 338 | 0.44% | one rasm, pointed two ways |
| `alif_variant` | 198 | 0.26% | one ā, on the line in one hand and above it in the other |
| `rasm_variant` | 60 | 0.08% | the riwāyāt disagree about the letters |
| `word_boundary` | 16 | 0.02% | a source joins the word to its neighbour, or a muṣḥaf really prints it joined |
| `partial` | 3 | 0.004% | the word is absent from some riwāyah |

So **615 words in 77,434** — one in 126 — are anything more than a difference
of vowelling, and only **60** of those are a letter one codex has and another
does not. The other 198 letter-level differences are an ā the two typesettings
place differently, on the line in one hand and above it in the other. They are
counted apart because the corpus says they belong apart: all 198 divide the
seven riwāyāt along one line, Warsh+Qālūn against the rest, in both directions
and without an exception, while the 60 divide them fourteen different ways.
Ḥadhf/ithbāt al-alif does vary between the codices of the amṣār — but not by
publisher. Rasm agreement between any two riwāyāt is **99.5 %–100 %**.

## A word

```json
{
 "number": 11, "surah": 1, "index": 11, "key": "1:مالك#1",
 "rasm": "ملك", "pointed": "مالك", "rasm_uthmani": "مَٰلِكِ", "plain": "مالك",
 "status": "dotting_variant",
 "hafs":  { "surah": 1, "ayah": 4, "position": 1 },
 "ayah":  { "hafs": 4, "shubah": 4, "warsh": 3, "qalun": 3,
            "duri": 3, "susi": 3, "bazzi": 4 },
 "forms": { "hafs": "مَٰلِكِ", "shubah": "مَٰلِكِ", "warsh": "مَلِكِ", "qalun": "مَلِكِ",
            "duri": "مَلِكِ", "susi": "مَّلِكِ", "bazzi": "مَلِكِ" }
}
```

One number, one word. `ayah` records that this word is in āyah 4 for the Kūfī
and Makkī counts and āyah 3 for the Madanī ones. `forms` records that Ḥafṣ and
Shuʿbah read *māliki* where the rest read *maliki* — and `rasm` records that
the codex writes `ملك` either way. Ḥafṣ's ā is printed as a superscript alef,
which is precisely the scribal cue that it is *not* on the line: one skeleton,
deliberately written to carry both qiraahs.

## Read next

- [`format.md`](format.md) — the normative format: words by position, the numbering, the counting block
- [`files.md`](files.md) — every file under `data/`, and every field
- [`method.md`](method.md) — how words are derived and aligned
