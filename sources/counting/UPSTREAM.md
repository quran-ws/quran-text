# Vendored from quranpedia/qiraat-ayah-map

| file | upstream path | SHA-256 |
|---|---|---|
| `book-boundary-primitives.json` | `data/book-boundary-primitives.json` | `63f7bed237871b174a342d5a88688302c06929105af8dc3c3810b4e795a7e6f1` |
| `counting-systems.json` | `data/counting-systems.json` | `a4dfad8c302f3a7bd2172a07ecbd70045b448815edd955df2f0bedcb972b8117` |
| `qiraat.json` | `data/qiraat.json` | `fe5a6c7ff09315a506b54f98000309392c1a6d5de2cda107796a30995aee271f` |

- Repository: https://github.com/quranpedia/qiraat-ayah-map
- Commit: `076255281ec6f76241d7e901e27072733d02a18d` (`main`, 2026-09-05)
- Licence: MIT, Copyright (c) 2026 Quranpedia. The copies above are verbatim.

The primitives list every disputed āyah boundary, anchored by sūrah, Kūfī āyah
and the word the boundary follows, with the counting systems that count it.
Undisputed Kūfī ends are implicit. The build resolves each anchor to a shared
word number (`pipeline/qurantext/counting.py`), derives each edition's counting
system from its own `ayah_starts`, and checks the result against
`khilaf.json`, this repository's overlay for disagreements *inside* a system,
which upstream does not yet model (qiraat-ayah-map#11).

`qiraat.json` gives the ten qurrāʾ, their ruwāh, and the counting system each
qāriʾ is **associated with**. That is a fact about the qāriʾ and not about any
printing: Abū ʿAmr is `basri` there, while both of his muṣḥafs here measure onto
First Madani. The build carries it through as `system_associated_with_qari`
beside the derived `system` so the two questions are answerable separately
(issue #15). The rāwī keys are this repository's muṣḥaf keys, but for `shuba`,
which is `shubah` here.

`counting-systems.json` on this commit still gives First Madani a total of
6214; al-Dānī's 6217 (qiraat-ayah-map#7) is applied by `khilaf.json`'s
`system_corrections`. To refresh: copy the three files, update the SHA-256 and
commit above, rebuild, and delete from `khilaf.json` whatever upstream now
carries itself.
