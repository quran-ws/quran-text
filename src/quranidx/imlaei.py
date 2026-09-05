"""Word-level imlāʾī, for the one release that supplies it.

The Ḥafṣ v2 release carries an ``aya_text_emlaey`` column — the same āyāt in
plain modern spelling.  No other package has it.  So imlāʾī is published for
Ḥafṣ and for nobody else, and it is never generated: deriving it by rule for the
other six would be this project asserting a spelling no source states.

The column is per āyah, so it has to be brought down to the word.  That is not
a re-export and it has not been attempted here before, so it is done
conservatively and every step is checked:

* Strip the āyah-number glyph and the standalone ۞ / ۩ from the ʿUthmānī side,
  since neither is a word.  **6,175 of 6,236 āyāt** then hold exactly as many
  imlāʾī tokens as ʿUthmānī ones, and map across position for position.
* In the remaining **61**, imlāʾī always has *more* tokens, never fewer, because
  it writes as two words what the ʿUthmānī line writes as one — ``أَوَلَا`` for
  ``أو لا``.  Those are matched on the dotted skeleton and the extra tokens are
  joined with a space, so ``e`` is always one string per word.
* The Ḥafṣ text of record is the 2026 ``.docx``, not this 2022 CSV, and the two
  tokenise differently in a few places.  The last hop aligns the CSV's tokens
  onto the word index on the rasm, the same key the muṣḥafs themselves are aligned
  on.

A word the chain cannot resolve gets no ``e`` field at all, and the count of
those is reported by the build.  An absent spelling is recoverable; a guessed
one is not.
"""

from __future__ import annotations

import difflib
from collections import defaultdict

from . import chars
from .build import Word
from .normalize import pointed, rasm
from .sources import Riwaya
from .tokenize import tokenize_ayah

#: Symbols that stand between words rather than being part of one.
_STANDALONE = (chars.RUB_EL_HIZB, chars.SAJDAH)


def _uthmani_tokens(text: str) -> list[str]:
    for sym in _STANDALONE:
        text = text.replace(sym, " ")
    return text.split()


def _pair(uth: list[str], iml: list[str]) -> list[str] | None:
    """One imlāʾī string per ʿUthmānī token, or ``None`` if they cannot be paired.

    Equal counts pair by position.  Where imlāʾī has more tokens, the extra ones
    are attached to the ʿUthmānī word whose skeleton they continue, which is
    decided by matching skeletons rather than by counting.
    """
    if len(uth) == len(iml):
        return iml
    if len(iml) < len(uth):
        return None

    matcher = difflib.SequenceMatcher(
        a=[_skeleton(t) for t in uth], b=[_skeleton(t) for t in iml],
        autojunk=False)
    out: list[str | None] = [None] * len(uth)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for off in range(i2 - i1):
                out[i1 + off] = iml[j1 + off]
        elif tag == "replace" and i2 - i1 == 1:
            # One ʿUthmānī word written as several imlāʾī ones.
            out[i1] = " ".join(iml[j1:j2])
        elif tag == "replace" and i2 - i1 == j2 - j1:
            for off in range(i2 - i1):
                out[i1 + off] = iml[j1 + off]
        else:
            return None
    return None if any(x is None for x in out) else out


def _skeleton(token: str) -> str:
    """A comparison key both spellings can reach: dots kept, vowels dropped."""
    return pointed(token).replace("ٱ", "ا").replace("أ", "ا").replace("إ", "ا")


def derive(words: list[Word], riwaya: Riwaya) -> tuple[dict[int, str], dict]:
    """``word id -> imlāʾī``, with a report of what could not be mapped.

    Asked of every riwāyah and answered for the one that can answer.  Having a
    v2 release is not enough — Warsh, Qālūn, Dūrī and Sūsī all have one, and
    none of them carries the column — so the test is whether the column holds
    anything, not whether it exists.
    """
    if not any((m.get("emlaey") or "").strip() for m in riwaya.meta.values()):
        return {}, {"available": False,
                    "reason": "release carries no imlāʾī column"}

    key = riwaya.key
    by_ayah: dict[tuple[int, int], list[Word]] = defaultdict(list)
    for w in words:
        if key in w.forms and key not in w.continuation:
            by_ayah[(w.sura, w.aya[key])].append(w)

    out: dict[int, str] = {}
    unpaired = unaligned = 0
    joined = 0
    for (sura, aya), meta in riwaya.meta.items():
        emlaey = (meta.get("emlaey") or "").split()
        source = riwaya.crosscheck.get((sura, aya))
        target = by_ayah.get((sura, aya))
        if not emlaey or not source or not target:
            continue

        uth = _uthmani_tokens(source)
        paired = _pair(uth, emlaey)
        if paired is None:
            unpaired += 1
            continue
        if len(emlaey) != len(uth):
            joined += 1

        # The CSV is a different release from the text of record; align on rasm.
        csv_toks = tokenize_ayah(sura, aya, " ".join(uth))
        if len(csv_toks) != len(paired):
            unaligned += 1
            continue
        matcher = difflib.SequenceMatcher(
            a=[t.rasm for t in csv_toks], b=[rasm(w.forms[key]) for w in target],
            autojunk=False)
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag != "equal":
                unaligned += 1
                continue
            for off in range(i2 - i1):
                out[target[j1 + off].id] = paired[i1 + off]

    return out, {
        "available": True,
        "source": riwaya.crosscheck_source,
        "column": "aya_text_emlaey",
        "words_mapped": len(out),
        "ayat_needing_join": joined,
        "ayat_unpaired": unpaired,
        "ayat_unaligned": unaligned,
        "note": "imlāʾī is published only where a release supplies it; it is "
                "never derived by rule",
    }
