"""Multiple-sequence alignment of the riwāyāt into one list of word columns.

The seven riwāyāt share a rasm that is identical almost everywhere, so a
progressive alignment is enough: start from Ḥafṣ's words, then fold in each
remaining riwāyah with a diff over the *rasm* (consonantal skeleton) and add a
new column wherever a riwāyah has a word the columns so far do not.

The result is a list of :class:`Column` per sūrah.  A column is one canonical
word: it carries at most one token from each riwāyah, and its index in the list
is the word's fixed number.  Words that only some riwāyāt have still get a
column, so a number means the same word everywhere it exists.

The numbering counts the **finest division** anyone prints.  Where one muṣḥaf
writes two words as one — ``وَأَلَّوِ`` at 72:16 for ``وَأَن لَّوِ`` — the two words
keep two columns and the joined token is placed in the first with the second
recorded as *covered* by it (:attr:`Column.covers`).  Those places are declared
in ``data/alignment/written-joined.json`` rather than inferred, because the unwritten nūn
changes the rasm and no rule can tell a join from a different reading.
"""

from __future__ import annotations

import difflib
import json
from collections import Counter
from dataclasses import dataclass, field, replace
from functools import lru_cache
from pathlib import Path

from .normalize import forms, rasm as rasm_of, split_by_rasm
from .tokenize import Token

WRITTEN_JOINED = "written_joined"
JOINS_FILE = Path("data/alignment/written-joined.json")


@dataclass(eq=False)   # identity, not value, semantics: columns are shared and mutated
class Column:
    """One canonical word position, shared by all riwāyāt that have it."""

    tokens: dict[str, Token] = field(default_factory=dict)
    #: Riwāyāt whose word here was produced by splitting or merging, or whose
    #: printed word covers this column and its neighbour (``written_joined``).
    boundary: dict[str, str] = field(default_factory=dict)
    #: Riwāyāt whose token sits in the *previous* column and covers this one
    #: too: the muṣḥaf prints the two words as one.  The token is repeated here
    #: so that ``forms`` and ``aya`` can be read off any column, but it is not a
    #: word of its own at this position.
    covers: dict[str, Token] = field(default_factory=dict)

    @property
    def rasm(self) -> str:
        """Majority rasm across the riwāyāt present — the column's identity.

        A riwāyah that writes this word joined to its neighbour is left out of
        the vote when anyone writes it apart: its token's rasm is the rasm of
        two words, and it would otherwise outvote the word the column is for.
        """
        apart = {k: t for k, t in self.tokens.items()
                 if self.boundary.get(k) != WRITTEN_JOINED}
        pool = apart or self.tokens
        if not pool:
            return ""
        counts = Counter(t.rasm for t in pool.values())
        top = max(counts.values())
        # Ties break on the earliest riwāyah, keeping the result deterministic.
        for tok in pool.values():
            if counts[tok.rasm] == top:
                return tok.rasm
        return ""

    def present(self, key: str) -> bool:
        return key in self.tokens or key in self.covers

    def token(self, key: str) -> Token:
        return self.tokens[key] if key in self.tokens else self.covers[key]


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


@lru_cache(maxsize=None)
def declared_joins(path: Path = JOINS_FILE) -> tuple[tuple[int, str, tuple[str, ...]], ...]:
    """``(sura, joined rasm, part rasms)`` for every declared written-joined word."""
    if not path.exists():
        return ()
    spec = json.loads(path.read_text(encoding="utf-8"))
    return tuple((j["sura"], rasm_of(j["joined"]),
                  tuple(rasm_of(p) for p in j["parts"]))
                 for j in spec["joins"])


def _overlap(a: str, b: str) -> int:
    """Length of the longest run of letters two rasms share."""
    best = 0
    prev = [0] * (len(b) + 1)
    for ca in a:
        cur = [0] * (len(b) + 1)
        for j, cb in enumerate(b, start=1):
            if ca == cb:
                cur[j] = prev[j - 1] + 1
                best = max(best, cur[j])
        prev = cur
    return best


def _assign(cols: list[Column], toks: list[Token]) -> list[tuple[int, int]]:
    """Which token belongs to which column, decided by shared letters.

    Order-preserving, and the shorter side is always fully paired, so the
    surplus falls on the longer side alone.  Pairing left to right instead
    would put Warsh's ``وَأَنْ`` against Ḥafṣ's ``أَوۡ`` at 40:26 — two words that
    share one letter — when the ``أَن`` beside it shares all of them.
    """
    n, m = len(cols), len(toks)
    score = [[_overlap(c.rasm, t.rasm) for t in toks] for c in cols]

    @lru_cache(maxsize=None)
    def best(i: int, j: int) -> tuple[int, tuple[tuple[int, int], ...]]:
        if i == n or j == m:
            return 0, ()
        options = []
        deeper, pairs = best(i + 1, j + 1)
        options.append((score[i][j] + deeper, ((i, j), *pairs)))
        if n - i - 1 >= m - j:              # this column goes unpaired
            options.append(best(i + 1, j))
        if m - j - 1 >= n - i:              # this token goes unpaired
            options.append(best(i, j + 1))
        return max(options, key=lambda o: o[0])   # first max wins: earlier column

    return list(best(0, 0)[1])


def _pair_by_letters(cols: list[Column], toks: list[Token], key: str,
                     out: list[Column]) -> None:
    """Emit a block whose two sides genuinely differ in wording.

    Each side keeps its own words in order.  A column the riwāyah has no word
    for stays as it is, and a word with no column of its own gets one, so no
    column is ever made to claim that two words correspond when the letters say
    they do not.
    """
    n, m = len(cols), len(toks)
    i = j = 0
    for ci, tj in [*_assign(cols, toks), (n, m)]:
        while i < ci:
            out.append(cols[i])                          # riwāyah lacks this word
            i += 1
        while j < tj:
            out.append(Column(tokens={key: toks[j]}))    # riwāyah alone has this word
            j += 1
        if ci < n:
            cols[ci].tokens[key] = toks[tj]
            out.append(cols[ci])
            i, j = ci + 1, tj + 1


def _declared_join(cols: list[Column], toks: list[Token], key: str,
                   out: list[Column], sura: int) -> bool:
    """Place a declared written-joined word, if this block contains one.

    Two shapes occur.  The riwāyah writes joined what the columns hold apart
    (Dūrī's ``أَلَّن`` against ``أَن لَّن``): its one token goes into the first
    column and is recorded as covering the second.  Or the columns hold one
    column for what the riwāyah writes apart (Warsh's ``وَأَن لَّوِ`` against
    Ḥafṣ's ``وَأَلَّوِ``): the column is split in two, every riwāyah already in it
    now covers both, and the riwāyah's two tokens take one column each.

    Whatever lies on either side of the join in the block is paired by letters
    as usual.  Returns ``False`` when no declared join fits, so the caller can
    fall through.
    """
    for jsura, joined, parts in declared_joins():
        if jsura != sura:
            continue
        k = len(parts)
        # Shape 1: one token, k columns.
        for tj, tok in enumerate(toks):
            if tok.rasm != joined:
                continue
            for ci in range(len(cols) - k + 1):
                if tuple(c.rasm for c in cols[ci:ci + k]) != parts:
                    continue
                _pair_by_letters(cols[:ci], toks[:tj], key, out)
                first, rest = cols[ci], cols[ci + 1:ci + k]
                first.tokens[key] = tok
                first.boundary[key] = WRITTEN_JOINED
                out.append(first)
                for col in rest:
                    col.covers[key] = tok
                    col.boundary[key] = WRITTEN_JOINED
                    out.append(col)
                _pair_by_letters(cols[ci + k:], toks[tj + 1:], key, out)
                return True
        # Shape 2: one column, k tokens.
        for ci, col in enumerate(cols):
            if col.rasm != joined:
                continue
            for tj in range(len(toks) - k + 1):
                if tuple(t.rasm for t in toks[tj:tj + k]) != parts:
                    continue
                _pair_by_letters(cols[:ci], toks[:tj], key, out)
                joined_here = dict(col.tokens)
                col.tokens[key] = toks[tj]
                for k2 in joined_here:
                    col.boundary[k2] = WRITTEN_JOINED
                out.append(col)
                for tok in toks[tj + 1:tj + k]:
                    more = Column(tokens={key: tok},
                                  covers=dict(joined_here),
                                  boundary={k2: WRITTEN_JOINED for k2 in joined_here})
                    out.append(more)
                _pair_by_letters(cols[ci + 1:], toks[tj + k:], key, out)
                return True
    return False


def _pair_replace(cols: list[Column], toks: list[Token], key: str,
                  out: list[Column]) -> None:
    """Resolve a replaced block: the same slot, spelled differently.

    Equal-length blocks pair one-to-one.  Unequal blocks are the interesting
    case, and are almost always a word-boundary disagreement rather than a
    different reading — most often a source that printed two words with no
    space between them.  When the letters on both sides agree, the words are
    re-segmented so the alignment keeps one column per word.  When they do not, a
    declared written-joined word is looked for first, and the rest of the
    block is a real difference of wording and goes to :func:`_pair_by_letters`.
    """
    if len(cols) == len(toks):
        for col, tok in zip(cols, toks):
            col.tokens[key] = tok
            out.append(col)
        return

    if "".join(c.rasm for c in cols) != "".join(t.rasm for t in toks):
        sura = toks[0].sura if toks else next(iter(cols[0].tokens.values())).sura
        if not _declared_join(cols, toks, key, out, sura):
            _pair_by_letters(cols, toks, key, out)
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
            # split apart so the alignment keeps one column per word, and the
            # join is recorded for review rather than judged here.
            tok = group_toks[0]
            pieces = split_by_rasm(tok.uthmani, [len(c.rasm) for c in group_cols])
            for offset, (col, piece) in enumerate(zip(group_cols, pieces)):
                col.tokens[key] = _retoken(tok, piece, tok.pos + offset)
                col.boundary[key] = "joined_in_source"
                out.append(col)
        elif len(group_cols) == 1 and len(group_toks) > 1:
            # The source writes as two words what the columns hold as one.
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


def merge(columns: list[Column], key: str, tokens: list[Token]) -> list[Column]:
    """Fold one riwāyah's word list into the columns aligned so far."""
    a = [c.rasm for c in columns]
    b = [t.rasm for t in tokens]
    out: list[Column] = []

    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if op == "equal":
            for col, tok in zip(columns[i1:i2], tokens[j1:j2]):
                col.tokens[key] = tok
                out.append(col)
        elif op == "replace":
            _pair_replace(columns[i1:i2], tokens[j1:j2], key, out)
        elif op == "delete":
            out.extend(columns[i1:i2])        # riwāyah has no word here
        elif op == "insert":
            for tok in tokens[j1:j2]:         # riwāyah has a word the columns lack
                col = Column()
                col.tokens[key] = tok
                out.append(col)
    return out


def align(streams: dict[str, list[Token]], order: list[str]) -> list[Column]:
    """Align every riwāyah in ``order`` into one list of columns."""
    first = order[0]
    columns = [Column(tokens={first: tok}) for tok in streams[first]]
    for key in order[1:]:
        columns = merge(columns, key, streams[key])
    return columns
