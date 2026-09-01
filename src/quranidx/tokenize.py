"""Turn āyah text into words.

A *word* is a whitespace-delimited run of letters and their marks.  Everything
that is not a word — āyah numbers, rub-el-ḥizb symbols, pause marks — is peeled
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

    sura: int
    aya: int
    pos: int                 # 1-based index within the āyah
    uthmani: str             # display form (no pause marks)
    folded: str              # notation unified across releases
    rasm: str                # consonantal skeleton — the alignment key
    simple: str              # plain modern spelling
    waqf: str = ""           # pause marks that trailed the word
    hizb: bool = False       # a rub-el-ḥizb symbol precedes this word
    sajdah: bool = False     # a sajdah symbol trails this word
    notes: list[str] = field(default_factory=list)

    @property
    def ref(self) -> str:
        return f"{self.sura}:{self.aya}:{self.pos}"


def tokenize_ayah(sura: int, aya: int, text: str) -> list[Token]:
    tokens: list[Token] = []
    pending_hizb = False

    for raw in strip_controls(text).split():
        # A rub-el-ḥizb symbol stands alone between words.
        stripped = raw.replace(chars.RUB_EL_HIZB, "")
        if stripped != raw:
            pending_hizb = True
            if not stripped:
                continue
            raw = stripped

        word, waqf = split_trailing_waqf(raw)
        if not word:
            # A pause mark separated from its word by a space: attach it back.
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
            sura=sura, aya=aya, pos=len(tokens) + 1,
            uthmani=f["uthmani"], folded=f["folded"],
            rasm=f["rasm"], simple=f["simple"],
            waqf=waqf,
            hizb=pending_hizb,
            sajdah=chars.SAJDAH in waqf,
        )
        pending_hizb = False
        tokens.append(tok)

    return tokens


def tokenize(ayat) -> list[Token]:
    out: list[Token] = []
    for a in ayat:
        out.extend(tokenize_ayah(a.sura, a.aya, a.text))
    return out
