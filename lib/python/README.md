# quran-text for Python

No dependencies, Python 3.9+. Ḥafṣ is bundled. Copy `quran_text.py` and
`quran_text_data/` into your project, or `pip install` this directory.

```python
from quran_text import Mushaf, AyahMap

m = Mushaf.hafs()                                    # bundled Ḥafṣ
m.ayah(2, 255).text                                  # plain words
m.ayah(2, 255).render(marks=True, ayah_markers=True) # with pause marks and ۝٢٥٥
m.page(3).render(marks=True, ayah_markers=True, lines=True)
m.sura(112).ayat                                     # [Ayah(112:1), …]
m.juz(30).first_ayah.key                             # "78:1"
m.word(1, 4, 1).number                               # 11, the same word in every riwāyah
m.sajdat()                                           # every āyah printed with ۩
m.search("مالك يوم الدين")                           # [Span(10, 13)]

w = Mushaf.load("out/mushaf/warsh.json")            # another riwāyah
AyahMap.load("out/ayah-map.json").convert(2, 255, "warsh")   # AyahRef(2, 253, 'split', 254)
```

The font the text needs is bundled too: `m.font.family` names it and `m.font.path`
is the `.ttf`. For another riwāyah `Mushaf.load(path)` finds its font beside
`out/fonts/`.

Wrong numbers raise `IndexError`; a layer the file lacks (juz in Bazzī) raises
`KeyError` with the reason from the file. The full API is in
[`../README.md`](../README.md).

Test: `python3 -m unittest lib/python/test_quran_text.py` from the repo root.
