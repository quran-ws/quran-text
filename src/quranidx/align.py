"""Multiple-sequence alignment of the riwāyāt into one word spine.

The seven riwāyāt share a rasm that is identical almost everywhere, so a
progressive alignment is enough: take Ḥafṣ as the initial spine, then fold in
each remaining riwāyah with a diff over the *rasm* (consonantal skeleton) and
extend the spine with a new column wherever a riwāyah has a word the spine does
not.

The result is a list of :class:`Column` per sūrah. A column is one shared slot:
it carries at most one token from each riwāyah. Words that only some riwāyāt
have still get a slot, and exceptional n:m wording is recorded over a range of
slots instead of pretending that every column is an independent 1:1 pairing.
"""

from __future__ import annotations

import difflib
from collections import Counter
from dataclasses import dataclass, field, replace

from .normalize import forms, split_by_rasm
from .tokenize import Token


@dataclass(eq=False)   # identity, not value, semantics: columns are shared and mutated
class Column:
    """One shared slot, carrying at most one token from each riwāyah."""

    tokens: dict[str, Token] = field(default_factory=dict)
    #: Riwāyāt whose word here was produced by splitting or merging.
    boundary: dict[str, str] = field(default_factory=dict)
    #: Unequal genuine-wording replacements this slot participates in.  The
    #: markers are identity objects because progressive alignment may discover
    #: the same final interval more than once; :func:`alignment_ranges` merges
    #: only markers whose final intervals actually overlap.
    alignment_markers: set[AlignmentMarker] = field(default_factory=set)

    @property
    def rasm(self) -> str:
        """Majority rasm across the riwāyāt present — the column's identity."""
        if not self.tokens:
            return ""
        counts = Counter(t.rasm for t in self.tokens.values())
        top = max(counts.values())
        # Ties break on the earliest riwāyah, keeping the result deterministic.
        for tok in self.tokens.values():
            if counts[tok.rasm] == top:
                return tok.rasm
        return ""


@dataclass(eq=False, frozen=True)
class AlignmentMarker:
    """One raw n:m wording event discovered while folding in a riwāyah."""

    riwaya: str


def _retoken(tok: Token, text: str, pos: int) -> Token:
    """A new token carrying part of ``tok``'s text."""
    f = forms(text)
    return replace(tok, uthmani=f["uthmani"], folded=f["folded"],
                   pointed=f["pointed"], rasm=f["rasm"],
                   rasm_plene=f["rasm_plene"], simple=f["simple"],
                   pos=pos, notes=[*tok.notes, "resegmented"])


def _distribute(cols: list[Column], toks: list[Token]) -> list[tuple[list[Column], list[Token]]]:
    """Group columns and tokens that cover the same letters.

    Walks both sides, extending whichever side is short, so a group is 1:1,
    n:1 (the source dropped a space between two words) or 1:n (the source
    split one word in two).
    """
    groups: list[tuple[list[Column], list[Token]]] = []
    i = j = 0
    while i < len(cols) and j < len(toks):
        ci, tj = i, j
        clen, tlen = len(cols[i].rasm), len(toks[j].rasm)
        i, j = i + 1, j + 1
        while clen != tlen:
            if clen < tlen and i < len(cols):
                clen += len(cols[i].rasm)
                i += 1
            elif tlen < clen and j < len(toks):
                tlen += len(toks[j].rasm)
                j += 1
            else:
                break
        groups.append((cols[ci:i], toks[tj:j]))
    if i < len(cols) or j < len(toks):
        groups.append((cols[i:], toks[j:]))
    return groups


def _pair_replace(cols: list[Column], toks: list[Token], key: str,
                  out: list[Column]) -> None:
    """Resolve a replaced block: the same slot, spelled differently.

    Equal-length blocks pair one-to-one.  Unequal blocks are the interesting
    case, and are almost always a word-boundary disagreement rather than a
    different reading — most often a source that printed two words with no
    space between them.  When the letters on both sides agree, the words are
    re-segmented so the spine keeps one column per word.
    """
    if len(cols) == len(toks):
        for col, tok in zip(cols, toks):
            col.tokens[key] = tok
            out.append(col)
        return

    if "".join(c.rasm for c in cols) != "".join(t.rasm for t in toks):
        # Genuinely different wording: pair as far as the shorter side goes,
        # then let the remainder stand as present on one side only.  Keep an
        # event marker across the whole block so the published slot layer can
        # say honestly that this is n:m alignment rather than independent 1:1
        # word correspondences.
        marker = AlignmentMarker(key)
        n = min(len(cols), len(toks))
        for i in range(n):
            cols[i].tokens[key] = toks[i]
        block = list(cols)
        for tok in toks[n:]:
            block.append(Column(tokens={key: tok}))
        for col in block:
            col.alignment_markers.add(marker)
        out.extend(block)
        return

    for group_cols, group_toks in _distribute(cols, toks):
        if len(group_cols) == len(group_toks):
            for col, tok in zip(group_cols, group_toks):
                col.tokens[key] = tok
                out.append(col)
        elif len(group_toks) == 1 and len(group_cols) > 1:
            # One printed word covering several canonical words.  Sometimes
            # that is the source's own orthography (Bazzī's لَأُاْقۡسِمُ), sometimes
            # a dropped space (Dūrī's كَانُواْيَعۡمَلُونَ); either way the words are
            # split apart so the spine keeps one column per word, and the
            # join is recorded for review rather than judged here.
            tok = group_toks[0]
            pieces = split_by_rasm(tok.uthmani, [len(c.rasm) for c in group_cols])
            for offset, (col, piece) in enumerate(zip(group_cols, pieces)):
                col.tokens[key] = _retoken(tok, piece, tok.pos + offset)
                col.boundary[key] = "joined_in_source"
                out.append(col)
        elif len(group_cols) == 1 and len(group_toks) > 1:
            # The source writes as two words what the spine holds as one.
            for offset, tok in enumerate(group_toks):
                col = group_cols[0] if offset == 0 else Column()
                col.tokens[key] = tok
                col.boundary[key] = "split_in_source"
                out.append(col)
        else:
            n = min(len(group_cols), len(group_toks))
            for i in range(n):
                group_cols[i].tokens[key] = group_toks[i]
                group_cols[i].boundary[key] = "unresolved_boundary"
                out.append(group_cols[i])
            out.extend(group_cols[n:])
            for tok in group_toks[n:]:
                out.append(Column(tokens={key: tok}, boundary={key: "unresolved_boundary"}))


def merge(spine: list[Column], key: str, tokens: list[Token]) -> list[Column]:
    """Fold one riwāyah's word list into the spine."""
    a = [c.rasm for c in spine]
    b = [t.rasm for t in tokens]
    out: list[Column] = []

    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if op == "equal":
            for col, tok in zip(spine[i1:i2], tokens[j1:j2]):
                col.tokens[key] = tok
                out.append(col)
        elif op == "replace":
            _pair_replace(spine[i1:i2], tokens[j1:j2], key, out)
        elif op == "delete":
            out.extend(spine[i1:i2])          # riwāyah has no word here
        elif op == "insert":
            for tok in tokens[j1:j2]:         # riwāyah has a word the spine lacks
                col = Column()
                col.tokens[key] = tok
                out.append(col)
    return out


def build_spine(streams: dict[str, list[Token]], order: list[str]) -> list[Column]:
    """Align every riwāyah in ``order`` into one list of columns."""
    first = order[0]
    spine = [Column(tokens={first: tok}) for tok in streams[first]]
    for key in order[1:]:
        spine = merge(spine, key, streams[key])
    return spine


def alignment_ranges(spine: list[Column]) -> list[tuple[int, int]]:
    """Return final 0-based inclusive intervals for genuine n:m replacements.

    A progressive merge can rediscover one region for several riwāyāt.  Raw
    markers are translated to their positions only after the spine is final,
    then overlapping intervals are coalesced.  Merely adjacent events remain
    distinct; adjacency alone is not evidence that two variants are one span.
    """
    positions: dict[AlignmentMarker, list[int]] = {}
    for index, col in enumerate(spine):
        for marker in col.alignment_markers:
            positions.setdefault(marker, []).append(index)
    intervals = sorted((min(xs), max(xs)) for xs in positions.values() if xs)
    merged: list[tuple[int, int]] = []
    for start, end in intervals:
        if merged and start <= merged[-1][1]:
            old_start, old_end = merged[-1]
            merged[-1] = (old_start, max(old_end, end))
        else:
            merged.append((start, end))
    return merged
