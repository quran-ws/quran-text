# islamweb muṣḥaf documents (tier 2)

Everything under this directory is derived from PDFs that islamweb hosts at
`https://dl2.islamweb.net/Audio_Path/quran_list/<slug>/quran.pdf`, one per
riwāyah. **They are not data releases by the muṣḥaf's publisher.** Each is a
Word document of unnamed authorship, set in the King Fahd Complex's 2005
"HQPB" symbol fonts and distilled to PDF between 2005 and 2018. Their
provenance is weaker than the KFGQPC packages', and the build says so in every
file it derives from them: `provenance.tier` is 2, `provenance.text.origin`
names the host and the document, and `provenance.decoder` names the table that
read it and the accuracy that table was measured at. See `docs/sources.md`,
*Tier 2*.

| in each `<slug>/` | what it is | committed |
|---|---|---|
| `quran.pdf` | the document as downloaded | no — 4–11 MB each; `SOURCE.json` records it |
| `SOURCE.json` | URL, SHA-256, size, the PDF's own metadata, when it was fetched, which extractor wrote the stream | yes |
| `glyphs.json.gz` | the glyph stream: pages → lines → tokens → `[font, glyph id, colour, is-mark]`, with āyah medallions, the basmalah ligature, ۞ and sūrah headers recognised | yes |

`decoder/table-v1.json` is the glyph → Unicode table and `decoder/calibration.json`
its measured accuracy. Both are written by `pipeline/tools/hqpb_calibrate.py`;
the streams by `pipeline/tools/hqpb_extract.py` (needs PyMuPDF in `.venv`).
The build (`pipeline/build.py`) reads only the committed stream and table.

## Which documents

| slug | riwāyah | used as |
|---|---|---|
| `qaloon`, `shuaba`, `warsh` | Qālūn, Shuʿbah, Warsh | **calibration only**: KFGQPC publishes these, so their documents teach and score the decoder and are never published from here |
| `qunbol` | Qunbul | calibration reserve: KFGQPC released a Qunbul package in 2021; not published from here |
| `hesham` | Hishām | tier-2 muṣḥaf `hisham` |
| `khalaf`, `khallad` | Khalaf, Khallād ʿan Ḥamzah | `khalaf`, `khallad` |
| `alhareth` | Abū al-Ḥārith ʿan al-Kisāʾī | `abu-al-harith` |
| `wardan`, `jammaz` | Ibn Wardān, Ibn Jammāz ʿan Abī Jaʿfar | `ibn-wardan`, `ibn-jammaz` |
| `ruwis`, `rawh` | Ruways, Rawḥ ʿan Yaʿqūb | `ruways`, `rawh` |
| `eshaq` | Isḥāq ʿan Khalaf al-ʿĀshir | `ishaq` |
| `edris` | labelled Idrīs; glyph-for-glyph identical to `eshaq` | **not published** (`docs/known-issues.md` §17) |

Not here: islamweb's `hafs`, `dori`, `alsosi`, `thakwaan` and `dori2` files are
page scans (img2pdf, April 2026) with no text layer, so **Ibn Dhakwān and
al-Dūrī ʿan al-Kisāʾī cannot be decoded**, and there is no file for al-Bazzī.
