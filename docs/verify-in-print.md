# What to check in a printed muṣḥaf

Two questions. Everything else in the data is settled.

Nothing here is guessed in the output — each one is a place that carries a
`null`, an `absent`, or a scored disagreement instead of a value.

| | question | what to do | unlocks |
|---|---|---|---|
| ~~Q1~~ | ~~Do sūrah headings take a ruled line?~~ | **closed** | they do — and it was our bug |
| **Q2** | Where does Bazzī's juz 26 begin? | open 1 page | Bazzī's missing juz layer |
| **Q3** | Why do 6 āyāt lack imlāʾī? | read the KFGQPC column | 76 null words |
| ~~Q4~~ | ~~Who cites a Makkī end at 78:40?~~ | **closed** | al-Qāḍī, *al-Farāʾid al-Ḥisān* |

---

## ~~Q1 · Do sūrah headings take a ruled line?~~ — closed

**Answered from a printed page 587: yes, and so does the basmalah.** The page
sets سُورَةُ الانفِطَارِ, its basmalah, nine lines of text, سُورَةُ المُطَفِّفِينَ,
its basmalah and two more lines — 15 ruled lines, with 83:1 on line 14. The v2
CSV says the same and never exceeds 15.

So the muṣḥaf was never the problem. The reconstruction was charging a heading
**two** lines, and the fix took Ḥafṣ and Shuʿbah to exact — 6,236 of 6,236 —
with nothing left that is reconstruction error. See `docs/known-issues.md` §6.

---

## Q2 · Where does juz 26 begin in a Bazzī muṣḥaf?

> ### ▶ Do this
> **Open** a **Bazzī** muṣḥaf at page **502**.
> **Find** where juz 26 begins.
> **Answer:** does it start at **46:1** (the sūrah opening) or at **45:32**?

**One page** — and even it has a defensible answer already.

Bazzī has no juz layer because juz comes from the v2 CSVs and it has no v2
package; its document names no juz either (no جزء, حزب or ربع anywhere in it).
But mapped through the shared word numbering, the six editions that *do* have
juz agree on **26 of the 30** starts. Only juz 4, 7, 11 and 26 differ, and three
of those four are single- or double-edition outliers:

| juz | Ḥafṣ | Shuʿbah | Warsh | Qālūn | Dūrī | Sūsī | majority |
|---|---|---|---|---|---|---|---|
| 4 | 7709 | *7724* | 7709 | 7709 | 7709 | 7709 | **7709** |
| 7 | 15312 | 15312 | 15312 | 15312 | *15338* | *15338* | **15312** |
| 11 | *25547* | 25528 | 25528 | 25528 | *25505* | *25505* | **25528** |
| 26 | 64707 | 64707 | 64707 | 64707 | *64650* | *64650* | **64707** = 46:1 |

At juz 7 and 26 the only dissenters are **Dūrī and Sūsī — both rāwīs of Abū
ʿAmr**, and Bazzī is Ibn Kathīr's. So 46:1 is the majority position and the one
its closest relatives hold.

**What the print would settle** is whether Bazzī actually follows that majority.
The one argument the other way: 28 of 30 juz begin at the top of a page, and the
top of page 502 is 45:32 — but Ḥafṣ is itself an exception there, so the rule
already has exceptions at exactly this juz.

**The ۞ marks cannot help here, and they do not settle the others either.** No
edition prints a ۞ anywhere near juz 26 — 46:1 is a sūrah opening, and marks are
never printed at those (§7). Of the four disputed juz, only juz 7 has a mark
standing on the boundary at all; at juz 4 and 11 the nearest marks are 15 and 19
words away, which makes them neighbouring rubu_al_hizbs, not the division.

**If answered:** Bazzī gets a juz layer. It has none today.

*`docs/known-issues.md` §9.*

---

## Q3 · Why do six āyāt lack imlāʾī?

> ### ▶ Do this — not a print check
> A muṣḥaf does not print imlāʾī.
> **Open** `hafsData_v2-0.csv`, column `aya_text_emlaey`, at the six āyāt below.
> **Answer:** is the cell empty, or is it there and our alignment drops it?

| āyah | page | words | |
|---|---|---|---|
| 3:66 | 58 | 19 | هَٰٓأَنتُمۡ هَٰٓؤُلَآءِ حَٰجَجۡتُمۡ … |
| 4:109 | 96 | 18 | هَٰٓأَنتُمۡ هَٰٓؤُلَآءِ جَٰدَلۡتُمۡ … |
| 27:20 | 378 | 2 | مَا لِيَ |
| 28:48 | 391 | 26 | فَلَمَّا جَآءَهُمُ ٱلۡحَقُّ … |
| 36:22 | 441 | 2 | وَمَا لِيَ |
| 43:18 | 490 | 9 | أَوَمَن يُنَشَّؤُاْ … |

76 words of 77,432 — 0.098%. Four fall into two known pairs
(`هَٰٓأَنتُمۡ هَٰٓؤُلَآءِ`, `مَا لِيَ`). **28:48 and 43:18 are unexplained — start there.**

*`docs/known-issues.md` §10.*

---

## ~~Q4 · Who cites a Makkī āyah end at 78:40?~~ — closed

**Answered.** al-Qāḍī, *al-Farāʾid al-Ḥisān*: «قَرِيبًا الْبَصْرِى **وَخُلْفٌ
مَكِّهِمْ**» — «عده البصري **والمكي يُخْلَف عنه** وتركه الباقون». That is khilāf
*inside* the Makkī count, which is what the Bazzī edition follows.

al-Dānī's *al-Bayān* gives the point to Baṣrī alone, which is why it looked
unexplained; the two together settle it. Recorded in `data/counting/khilaf.json`
and emitted under `counting.khilaf` in `out/mushaf/bazzi.json`.
`open-findings.json` is now empty.

*`docs/known-issues.md` §1b.*

---

## Settled — do not re-open

- **Page.** Read from the documents, not inferred. Identical for all 77,432
  words across all seven editions, and agrees with every v2 CSV.
- **Bazzī's lines.** Word-for-word identical to Ḥafṣ, so they carry Ḥafṣ's
  accuracy, not an unknown one.
- **Line layout.** Two families, identical within each: Ḥafṣ, Shuʿbah, Dūrī,
  Sūsī, Bazzī — and Warsh, Qālūn.
- **Four Warsh/Qālūn āyāt** (4:44 p85, 20:86 p317, 24:36 p354, 24:42 p355) begin
  on the last ruled line and run onto the next page. The CSV records where they
  continue; we record where they begin. Bookkeeping, not typesetting.
- **The package differences** in `docs/known-issues.md` §§2–5, 7–8 are the
  publisher's choices. Recorded, not resolved.
