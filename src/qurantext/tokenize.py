"""Turn āyah text into words.

A *word* is a whitespace-delimited run of letters and their marks.  Everything
that is not a word — āyah numbers, ۞ signs, waqf marks — is peeled
off and kept as annotation on the neighbouring word, so that no information is
lost and the word stream stays comparable across riwāyāt.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from . import chars
from .normalize import forms, split_trailing_waqf, strip_controls


@dataclass
class Token:
    """One word of one riwāyah, with its position and derived forms."""

    surah: int
    ayah: int
    position: int                 # 1-based index within the āyah
    rasm_uthmani: str             # display form (no waqf marks)
    folded: str              # notation unified across releases
    pointed: str             # consonantal skeleton, dots kept
    rasm: str                # bare ʿUthmānic skeleton — the alignment key
    rasm_plene: str          # the same skeleton with every ā spelled out
    plain: str              # plain modern spelling
    waqf: str = ""           # waqf marks that trailed the word
    division: bool = False       # a ۞ sign precedes this word
    sajdah: bool = False     # a sajdah symbol trails this word
    page: int = 0            # printed page, read from the source typesetting
    line: int = 0            # printed line, *reconstructed* — see layout.py
    notes: list[str] = field(default_factory=list)

    @property
    def ref(self) -> str:
        return f"{self.surah}:{self.ayah}:{self.position}"


def tokenize_ayah(surah: int, ayah: int, text: str,
                  places: list | None = None) -> list[Token]:
    """Split one āyah into words.

    ``places`` is one :class:`qurantext.layout.Place` per whitespace-delimited
    token of ``text``, in order.  It is threaded in rather than looked up
    because only the ``.docx`` releases carry typesetting, and the position of a
    word has to survive the peeling of the marks around it: a standalone ۞ is
    consumed without producing a word, so positions cannot be matched to the
    output by index afterwards.
    """
    tokens: list[Token] = []
    pending_division = False

    for i, raw in enumerate(strip_controls(text).split()):
        place = places[i] if places and i < len(places) else None
        # A ۞ sign stands alone between words.
        stripped = raw.replace(chars.RUBU_AL_HIZB, "")
        if stripped != raw:
            pending_division = True
            if not stripped:
                continue
            raw = stripped

        word, waqf = split_trailing_waqf(raw)
        if not word:
            # A waqf mark separated from its word by a space: attach it back.
            if tokens:
                tokens[-1].waqf += waqf
                tokens[-1].notes.append("detached_waqf")
            continue

        f = forms(word)
        if not f["rasm"]:
            # No consonantal content at all — nothing a word could align on.
            if tokens:
                tokens[-1].notes.append("absorbed_markless_token")
            continue

        tok = Token(
            surah=surah, ayah=ayah, position=len(tokens) + 1,
            rasm_uthmani=f["rasm_uthmani"], folded=f["folded"],
            pointed=f["pointed"], rasm=f["rasm"],
            rasm_plene=f["rasm_plene"], plain=f["plain"],
            waqf=waqf,
            division=pending_division,
            sajdah=chars.SAJDAH in waqf,
            page=place.page if place else 0,
            line=place.line if place else 0,
        )
        pending_division = False
        tokens.append(tok)

    return tokens


def tokenize(ayahs, places: list | None = None) -> list[Token]:
    """Tokenise a stream of āyāt, optionally placing every word on the page.

    ``places`` is the flat, document-order position list from
    :func:`qurantext.layout.word_places`.  It is consumed āyah by āyah in step
    with the token counts, which is sound only because the two streams are
    identical — asserted by :func:`qurantext.validate.check_layout_alignment`.
    """
    out: list[Token] = []
    at = 0
    for a in ayahs:
        n = len(strip_controls(a.text).split())
        window = places[at:at + n] if places else None
        at += n
        out.extend(tokenize_ayah(a.surah, a.ayah, a.text, window))
    return out
