<div align="center">

<img src=".github/banner.svg" alt="Quran Text — Data, Beta" width="820">

**Source-verified Quran text in seven printed riwayat, with a shared word identity that connects corresponding words across them.**

<a href="https://quran.ws/blocks/quran-text"><img alt="See it work" src="https://img.shields.io/badge/See_it_work-15705D?style=for-the-badge&labelColor=102F29"></a>
<a href="https://quran.ws/docs/reference/quran-text"><img alt="Documentation" src="https://img.shields.io/badge/Documentation-102F29?style=for-the-badge&labelColor=102F29"></a>
<a href="https://text.quran.ws"><img alt="Download the text" src="https://img.shields.io/badge/Download_the_text-D6AD64?style=for-the-badge&labelColor=102F29"></a>

</div>

Use it when your application needs Quran text, supports multiple riwayat, or needs to match words and positions across different riwayat.

> نصوص القرآن في سبع روايات مطبوعة، موثّقة المصدر، مع معرّف موحّد للكلمات يربط نظائرها بين الروايات.
>
> استخدمه عندما تحتاج نصّ القرآن في تطبيقك، أو تريد دعم أكثر من رواية، أو مطابقة الكلمات والمواضع بينها.

| | |
|---|---|
| **Package** | `@quran.ws/text` · `0.1.0` |
| **Riwayat** | 7 printed |
| **Words** | 77,434 numbered |
| **Licence** | CC BY 4.0 (the work), attribution waived for use inside a product · KFGQPC terms (the text) |

```sh
pip install ./lib/python
```

## Where the documentation is

Everything about using it lives on the site. This repository is the source.

| | |
|---|---|
| **Overview and demo** | [quran.ws/blocks/quran-text](https://quran.ws/blocks/quran-text) |
| **Reference** | [quran.ws/docs/reference/quran-text](https://quran.ws/docs/reference/quran-text) |
| **Download the text** | [text.quran.ws](https://text.quran.ws) |
| **Display Qur'an text** | [quran.ws/docs/build/display-text](https://quran.ws/docs/build/display-text) |
| **Search the text** | [quran.ws/docs/build/search](https://quran.ws/docs/build/search) |
| **Support multiple riwayat** | [quran.ws/docs/build/multiple-riwayat](https://quran.ws/docs/build/multiple-riwayat) |
| **Licensing in full** | [quran.ws/docs/reference/licensing](https://quran.ws/docs/reference/licensing) |

## What is in here

| | |
|---|---|
| `data/` | the seven built editions, plus the shared word index and the 277 differences |
| `lib/` | six client libraries — JavaScript, Python, PHP, Dart, Swift, Kotlin — one API, no dependencies |
| `service/` | the download API behind text.quran.ws |
| `pipeline/` | KFGQPC packages → `data/`, reproducible from `sources/` |
| `sources/` | the published packages this is built from, each with its SHA-256 |
| `schema/` | the JSON shapes every file in `data/` conforms to |
| `conformance/` | the gates that must stay green |
| `skills/` | the agent skill for working with this data |
| `docs/` | how to work on this repository |

Issues and pull requests are welcome here. Everything that is not about *changing* this repository is on the site.
