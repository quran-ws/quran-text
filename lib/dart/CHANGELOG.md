# Changelog

## Unreleased

- `Hizb`, `RubuAlHizb` and `Thumn`: the 60 ḥizbs and their parts, as the
  printed muṣḥaf marks them. `Mushaf.hizb(n)`, `rubuAlHizb(n)` and `thumn(n)`,
  with `hizbAt`, `hizbCount`, `hizbs` and the same for the parts; `hizb`,
  `rubuAlHizb` and `thumn` on `Word` and `Span`.
- A muṣḥaf divides the ḥizb into four (Ḥafṣ, Shuʿbah) or into eight (Warsh,
  Qālūn, Dūrī, Sūsī), never both; asking for the other throws `StateError`
  with the reason from the file. Bazzī carries none of the three.

## 0.1.0

First published release. The Dart binding has existed in this repository since
before it had a version; this is the first time it is installable from pub.dev.

- `Mushaf.hafs()` reads the bundled Ḥafṣ muṣḥaf; `Mushaf.load()` reads any of
  the seven riwāyāt from a dataset file.
- Āyah, page, sūrah, juz and word access, with the shared word numbering that
  is the same word in every riwāyah.
- Waqf marks, sajdah āyāt, and search over the text.
- `AyahMap` converts an āyah number between riwāyāt.
- The KFGQPC Ḥafṣ font ships with the package, as an asset and a Flutter font
  family.
