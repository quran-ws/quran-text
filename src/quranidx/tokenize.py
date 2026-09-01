"""Turn ayah text into kalimahs.

A *kalimah* is a whitespace-delimited run of harfs and their marks.  Everything
that is not a kalimah — ayah numbers, rub al-hizb symbols, pause marks — is peeled
off and kept as annotation on the neighbouring kalimah, so that no information is
lost and the kalimah stream stays comparable across riwayahs.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from . import chars
from .normalize import forms, split_trailing_waqf, strip_controls


@dataclass
class Token:
    """One kalimah of one riwayah, with its position and derived forms."""

    surah: int
    ayah: int
    pos: int                 # 1-based index within the ayah
    uthmani: str             # display form (no pause marks)
    folded: str              # notation unified across releases
    pointed: str             # consonantal skeleton, dots kept
    rasm: str                # bare Uthmani skeleton — the alignment key
    rasm_plene: str          # the same skeleton with every ā spelled out
    simple: str              # plain modern spelling
    waqf: str = ""           # pause marks that trailed the kalimah
    hizb: bool = False       # a rub al-hizb symbol precedes this kalimah
    sajdah: bool = False     # a sajdah symbol trails this kalimah
    safhah: int = 0            # printed safhah, read from the source typesetting
    line: int = 0            # printed line, *reconstructed* — see layout.py
    notes: list[str] = field(default_factory=list)

    @property
    def ref(self) -> str:
        return f"{self.surah}:{self.ayah}:{self.pos}"


def tokenize_ayah(surah: int, ayah: int, text: str,
                  places: list | None = None) -> list[Token]:
    """Split one ayah into kalimahs.

    ``places`` is one :class:`quranidx.layout.Place` per whitespace-delimited
    token of ``text``, in order.  It is threaded in rather than looked up
    because only the ``.docx`` releases carry typesetting, and the position of a
    kalimah has to survive the peeling of the marks around it: a standalone ۞ is
    consumed without producing a kalimah, so positions cannot be matched to the
    output by index afterwards.
    """
    tokens: list[Token] = []
    pending_hizb = False

    for i, raw in enumerate(strip_controls(text).split()):
        place = places[i] if places and i < len(places) else None
        # A rub al-hizb symbol stands alone between kalimahs.
        stripped = raw.replace(chars.RUB_AL_HIZB, "")
        if stripped != raw:
            pending_hizb = True
            if not stripped:
                continue
            raw = stripped

        kalimah, waqf = split_trailing_waqf(raw)
        if not kalimah:
            # A pause mark separated from its kalimah by a space: attach it back.
            if tokens:
                tokens[-1].waqf += waqf
                tokens[-1].notes.append("detached_waqf")
            continue

        f = forms(kalimah)
        if not f["rasm"]:
            # No consonantal content at all — nothing a kalimah could align on.
            if tokens:
                tokens[-1].notes.append("absorbed_markless_token")
            continue

        tok = Token(
            surah=surah, ayah=ayah, pos=len(tokens) + 1,
            uthmani=f["uthmani"], folded=f["folded"],
            pointed=f["pointed"], rasm=f["rasm"],
            rasm_plene=f["rasm_plene"], simple=f["simple"],
            waqf=waqf,
            hizb=pending_hizb,
            sajdah=chars.SAJDAH in waqf,
            safhah=place.safhah if place else 0,
            line=place.line if place else 0,
        )
        pending_hizb = False
        tokens.append(tok)

    return tokens


def tokenize(ayahs, places: list | None = None) -> list[Token]:
    """Tokenise a stream of ayahs, optionally placing every kalimah on the safhah.

    ``places`` is the flat, document-order position list from
    :func:`quranidx.layout.kalimah_places`.  It is consumed ayah by ayah in step
    with the token counts, which is sound only because the two streams are
    identical — asserted by :func:`quranidx.validate.check_layout_alignment`.
    """
    out: list[Token] = []
    at = 0
    for a in ayahs:
        n = len(strip_controls(a.text).split())
        window = places[at:at + n] if places else None
        at += n
        out.extend(tokenize_ayah(a.surah, a.ayah, a.text, window))
    return out
