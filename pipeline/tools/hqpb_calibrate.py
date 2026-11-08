#!/usr/bin/env python3
"""Learn the HQPB glyph → Unicode table and score it.

    python3 pipeline/tools/hqpb_calibrate.py            # learn, identify, score, write
    python3 pipeline/tools/hqpb_calibrate.py --holdout  # leave-one-out accuracy only

Writes ``sources/islamweb/decoder/table-v1.json`` and ``calibration.json``.
Needs only the standard library and the pipeline; the glyph streams must
already exist (``hqpb_extract.py``).

**How the table is learned, and why nothing in it is guessed.**

1. *Calibration pairs.*  Three islamweb files are riwāyāt KFGQPC also
   publishes — Qālūn, Shuʿbah, Warsh.  Inside every āyah whose word count the
   two agree on, the n-th glyph word is paired with the n-th KFGQPC word.
2. *Type-level evidence.*  Pairs are collapsed to distinct (glyph sequence,
   target word) types, so a word printed three hundred times is one vote: a
   wrong alignment of a frequent word cannot become "confirmed" by repetition.
3. *Anchored alignment.*  Within each pair, glyphs already known pin the
   letters they stand for; the letters left over go to the unknown glyphs,
   and the combining marks left over in each letter unit go to its unknown
   mark glyphs.  The first round has no anchors and uses the association
   between a glyph and the letters of the words it occurs in, which is a
   statement about the corpus, not a guess about a glyph.  Rounds repeat
   until nothing new is learned.
4. *Identification across riwāyāt.*  A glyph the three calibration files
   never use (Abū Jaʿfar's ṣila wāw, the imāla dot of Ḥamzah's readers, …)
   is identified the same way, against the KFGQPC riwāyāt that *do* print
   that sign: each target word containing it is paired with every KFGQPC
   word of the same rasm at the same position in the sūrah, across all
   seven KFGQPC texts, and the residual is counted per word type.  Every
   entry records which KFGQPC texts supported it.
5. *Shape.*  What survives both is compared, as an outline, with every
   glyph already known in all the fonts: a coloured duplicate of a known
   sign is its twin.  Such entries are marked ``method: "shape"``.

The table also carries the notation decisions the targets were folded to
(``LIGHT``): one spelling of the waṣl alif, one sukūn, the Unicode 9 open
tanwīn, no yeh-barree.  They are a documented choice, listed in the table
file and in ``docs/method.md``, not a hidden normalisation.
"""

from __future__ import annotations

import gzip
import json
import math
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pipeline"))

from qurantext import chars, hqpb, normalize, sources   # noqa: E402

ISLAMWEB = ROOT / "sources" / "islamweb"
DECODER = ISLAMWEB / "decoder"
TABLE_VERSION = 1

#: islamweb slug -> KFGQPC registry key, for the three riwāyāt both publish.
CALIBRATION = {"qaloon": "qalun", "shuaba": "shubah", "warsh": "warsh"}
#: The files that become tier-2 muṣḥafs.
TARGETS = ["qunbol", "hesham", "khalaf", "khallad", "alhareth", "wardan", "jammaz", "ruwis", "rawh", "eshaq", "edris"]

KNOWN = 0.8          # share of a glyph's votes its best reading must have (letters)
SETTLED = 0.45       # a plurality is enough when every contending reading has the same rasm (ى/ي, ا/ٱ):
                     # the letters on the line are not in doubt, only the hand's spelling
KNOWN_MARK = 0.6     # marks: the KFGQPC hands differ among themselves on shaddah and waqf
                     # conventions, so a mark glyph's votes split by riwāyah, not by error
MIN_TYPES = 3        # distinct word types that must support an entry
WAQF = set("\u06d6\u06d7\u06d8\u06d9\u06da\u06db\u06dc\u08cc")
IMALAH_DOTS = {"\u06ea", "\u065c"}
PLAIN = set("\u064e\u064f\u0650\u0652\u0651\u06e1")   # fatha, damma, kasra, sukun, shadda
#: glyph keys seen in colour in the target documents while still unknown (filled by cross_pairs)
COLOURED: set = set()

# --------------------------------------------------------------------------
# notation the targets are folded to
# --------------------------------------------------------------------------

LIGHT = {k: v for k, v in chars.NOTATION_FOLD.items() if k not in "أإٱ۪۫"}
LIGHT.update({k: "ٱ" for k in chars.ATTACHED_ALEF_DECOMP})
LIGHT_NOTE = (
    "KFGQPC targets were folded before learning: Arabic Extended-B attached alefs and U+0671 all "
    "read as U+0671 ALEF WASLA, and the waṣl vowel cues on that alef (U+06EC, U+06EA, U+06EB, "
    "U+065C) are dropped; elsewhere U+06EA and U+065C are kept, since the Dūrī and Warsh releases "
    "use them as the imālah and taqlīl dots. U+06E1 (KFGQPC sukun head) reads as U+0652; the v2 "
    "open-tanwīn marks read as U+08F0–U+08F2; a tanwīn is written before the alef or alef maqṣūrah "
    "it sits on, as the documents and the 2022 releases write it; yeh barree U+06D2 reads as U+064A; "
    "alef madda U+0622 is decomposed so the madda stays a mark. Hamza seats (أ إ ؤ ئ) are kept. "
    "The decoded text is in this notation; compare across tiers through fold_notation."
)
_TANWIN_AFTER_SEAT = re.compile("([اى])([ًࣰٌࣱٍࣲ])")
_CUE_ON_WASL = re.compile("ٱ[\u06ec\u06ea\u06eb\u065c]+")


def light(word: str) -> str:
    w = "".join(LIGHT.get(c, c) for c in word if c != chars.TATWEEL and c not in chars.EDITORIAL)
    w = _CUE_ON_WASL.sub("ٱ", w)
    w = unicodedata.normalize("NFC", w)
    w = _TANWIN_AFTER_SEAT.sub(r"\2\1", w)
    return w.replace("آ", "آ")


def is_comb(cp: str) -> bool:
    o = ord(cp)
    return (unicodedata.combining(cp) != 0 or 0x064B <= o <= 0x065F or o == 0x0670
            or 0x06D6 <= o <= 0x06ED or 0x08D3 <= o <= 0x08FF or 0x0898 <= o <= 0x089F)


def split_u(u: str) -> list[list[str]]:
    out: list[list[str]] = []
    for cp in u:
        if is_comb(cp) and out:
            out[-1][1] += cp
        elif is_comb(cp):
            out.append(["", cp])
        else:
            out.append([cp, ""])
    return out


# --------------------------------------------------------------------------
# streams and pairs
# --------------------------------------------------------------------------

Key = tuple[str, int]


def stream_words(slug: str) -> tuple[dict, list[dict]]:
    """The stream and its tokens flattened: dicts with glyphs [(key, is_mark)], kind, printed n."""
    st = hqpb.load_stream(ISLAMWEB / slug / "glyphs.json.gz")
    fonts = st["fonts"]
    toks = []
    for page in st["pages"]:
        for line in page["lines"]:
            for t in line:
                toks.append(dict(kind=t["k"], n=t.get("n"), page=page["n"],
                                 glyphs=[((fonts[f], gid), bool(m)) for f, gid, _c, m in t["g"]]))
    return st, toks


def segments(toks: list[dict]) -> list[list[list]]:
    """Glyph words between consecutive markers (ignoring sūrah structure)."""
    segs, cur = [], []
    for t in toks:
        if t["kind"] == "m":
            segs.append(cur)
            cur = []
        elif t["kind"] in ("w", "h"):
            cur.append(t["glyphs"])
    return segs


def kfgqpc_texts() -> dict[str, list[tuple[int, int, str]]]:
    out = {}
    for spec in sources.REGISTRY:
        if spec.tier != 1:
            continue
        path = sources._extract(spec.primary_zip, spec.primary_member)
        out[spec.key] = [(a.surah, a.ayah, a.text) for a in sources.load_docx(path)]
    return out


def calibration_pairs(slug: str, kf: list[tuple[int, int, str]]) -> list[tuple[list, str]]:
    _st, toks = stream_words(slug)
    segs = segments(toks)
    numbered = [(s, a, light(t).split()) for s, a, t in kf if a > 0]
    pairs = []
    for seg, (_s, _a, words) in zip(segs, numbered):
        if len(seg) == len(words):
            pairs.extend(zip(seg, words))
    return pairs


def word_types(pairs):
    seen = {}
    for G, U in pairs:
        key = (tuple(G), U)
        seen.setdefault(key, (G, U))
    return list(seen.values())


# --------------------------------------------------------------------------
# the learner
# --------------------------------------------------------------------------

class Tables:
    def __init__(self):
        self.base: dict[Key, dict] = {}
        self.ctx: dict[tuple, dict] = {}
        self.mark: dict[Key, dict] = {}
        self.lig: dict[tuple, dict] = {}
        self.marklike: set[Key] = set()
        self.order: dict[str, int] = {}
        self.method: dict = {}

    def letters(self, prev, bk, marks):
        for key in ((prev, bk, tuple(marks)), (None, bk, tuple(marks))):
            v = self.ctx.get(key)
            if v and accepted(v, KNOWN) and v["n"] >= MIN_TYPES:
                return v["span"], True
        v = self.base.get(bk)
        if v:
            return v["span"], accepted(v, KNOWN)
        return None, False

    def as_hqpb(self) -> hqpb.Table:
        return hqpb.Table(self.to_json())

    def to_json(self) -> dict:
        entries = []
        joins = getattr(self, "joins", {"never_final": [], "never_initial": []})
        for (f, g), v in sorted(self.base.items()):
            if accepted(v, KNOWN) or v.get("n") == 0:
                entries.append(dict(font=f, gid=g, kind="base", text=v["span"], types=v["n"], share=round(v["share"], 3),
                                    **({"contested": True} if v["share"] < KNOWN else {}),
                                    **self.method.get(("base", (f, g)), {"method": "aligned"})))
        for (f, g), v in sorted(self.mark.items()):
            if v["share"] >= KNOWN_MARK or v.get("n") == 0:
                entries.append(dict(font=f, gid=g, kind="mark", text=v["span"], types=v["n"], share=round(v["share"], 3),
                                    **self.method.get(("mark", (f, g)), {"method": "aligned"})))
        for f, g in sorted(self.marklike):
            entries.append(dict(font=f, gid=g, kind="marklike", text="", method="aligned"))
        context = []
        for (prev, bk, marks), v in sorted(self.ctx.items(), key=str):
            if accepted(v, KNOWN) and v["n"] >= MIN_TYPES and (bk in self.base and self.base[bk]["share"] < KNOWN or bk not in self.base or v["alts"][0][1] == 0):
                context.append(dict(prev=list(prev) if prev else None, font=bk[0], gid=bk[1],
                                    marks=[list(m) for m in marks], text=v["span"], types=v["n"], share=round(v["share"], 3)))
        ligatures = []
        for (bk, marks), v in sorted(self.lig.items(), key=str):
            if v["share"] >= KNOWN_MARK and v["n"] >= 5:
                ligatures.append(dict(font=bk[0], gid=bk[1], marks=[list(m) for m in marks], text=v["span"],
                                      types=v["n"], share=round(v["share"], 3)))
        return dict(format="hqpb-decoder", version=TABLE_VERSION, notation=LIGHT_NOTE,
                    entries=entries, context=context, ligatures=ligatures, mark_order=self.order,
                    joins=joins)


def split_g(G, marklike):
    out = []
    for k, is_mark in G:
        if is_mark or k in marklike:
            if out:
                out[-1][1].append(k)
            else:
                out.append([None, [k]])
        else:
            out.append([k, []])
    return out


def association(types, marklike):
    co_b, tot_b = defaultdict(Counter), Counter()
    for G, U in types:
        gs, us = split_g(G, marklike), split_u(U)
        letters = {l for l, _ in us if l}
        bases = {bk for bk, _ in gs if bk is not None}
        for b in bases:
            tot_b[b] += 1
            for l in letters:
                co_b[b][l] += 1
    return {g: {l: c / tot_b[g] for l, c in cs.items()} for g, cs in co_b.items()}


def prior_span(bk, span, a_b):
    assoc = a_b.get(bk, {})
    if not span:
        best = max(assoc.values(), default=0.0)
        return math.log(max(1e-3, 1.0 - best)) - 0.5
    lp = sum(math.log(max(1e-3, assoc.get(l, 0.0))) for l in span)
    return lp - 0.3 * (len(span) - 1)


def align(gs, us, T, a_b):
    n, m = len(gs), len(us)
    NEG = -1e9
    dp = [[NEG] * (m + 1) for _ in range(n + 1)]
    bp = [[0] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0.0
    letters = [l for l, _ in us]
    for i in range(1, n + 1):
        bk, marks = gs[i - 1]
        prev = gs[i - 2][0] if i >= 2 else None
        exp, known = T.letters(prev, bk, marks) if bk is not None else (None, False)
        for j in range(m + 1):
            for k in (0, 1, 2, 3):
                if j - k < 0 or dp[i - 1][j - k] == NEG:
                    continue
                span = "".join(letters[j - k:j])
                if bk is None:
                    sc = 0.0 if k == 0 else -6.0
                elif known:
                    sc = 0.0 if span == exp else -8.0 - k
                else:
                    sc = prior_span(bk, span, a_b)
                v = dp[i - 1][j - k] + sc
                if v > dp[i][j]:
                    dp[i][j], bp[i][j] = v, k
    if dp[n][m] <= -8.0:
        return None
    j, spans = m, []
    for i in range(n, 0, -1):
        k = bp[i][j]
        spans.append(list(range(j - k, j)))
        j -= k
    spans.reverse()
    return spans


def learn_round(types, T, a_b):
    bco, cco, mco, lco = (defaultdict(Counter) for _ in range(4))
    used = 0
    for G, U in types:
        gs, us = split_g(G, T.marklike), split_u(U)
        if not gs or not us:
            continue
        spans = align(gs, us, T, a_b)
        if spans is None:
            continue
        used += 1
        for i, ((bk, marks), idx) in enumerate(zip(gs, spans)):
            prev = gs[i - 1][0] if i else None
            letters = "".join(us[t][0] for t in idx)
            cmarks = "".join(us[t][1] for t in idx)
            if bk is not None:
                bco[bk][letters] += 1
                cco[(None, bk, tuple(marks))][letters] += 1
                cco[(prev, bk, tuple(marks))][letters] += 1
                if len(idx) >= 2:
                    lco[(bk, tuple(marks))]["".join(us[t][0] + us[t][1] for t in idx)] += 1
            residual = Counter(cmarks)
            unknown, bad = [], False
            for mk in marks:
                kn = T.mark.get(mk)
                if kn and kn["share"] >= KNOWN_MARK:
                    for c in kn["span"]:
                        if residual[c] > 0:
                            residual[c] -= 1
                        else:
                            bad = True
                else:
                    unknown.append(mk)
            if bad:
                continue
            res = "".join(sorted(residual.elements(), key=lambda c: unicodedata.combining(c)))
            if len(unknown) == 1:
                mco[unknown[0]][res] += 1
            elif not unknown and not res:
                for mk in marks:
                    mco[mk][T.mark[mk]["span"]] += 1
    return used, bco, cco, mco, lco


def rasm_settled(v) -> bool:
    """True when every reading with real support shares one rasm."""
    tot = v["n"]
    # an empty reading is a hand that omits the sign, not a different letter
    skel = {normalize.rasm(sp) for sp, k in v["alts"] if k >= max(2, 0.05 * tot) and (sp or k >= 0.15 * tot)}
    return len(skel) == 1 and v["share"] >= SETTLED


def accepted(v, bar) -> bool:
    return v["share"] >= bar or rasm_settled(v)


def word_edge_forms(slugs) -> dict:
    """Base glyphs that never end, or never begin, a word in the calibration streams.

    The HQPB fonts are positional: a medial form cannot end a word and a final
    form cannot begin one.  A document that types a space inside a word (the
    Hishām file writes إِسۡرَٰٓءِيلَ as «إِ» + space + «سۡرَٰٓءِيلَ») leaves such a form
    at the edge, which is how the decoder knows to join the pieces again."""
    first, last, total = Counter(), Counter(), Counter()
    for slug in slugs:
        _st, toks = stream_words(slug)
        for t in toks:
            if t["kind"] != "w":
                continue
            bases = [k for k, is_mark in t["glyphs"] if not is_mark]
            if not bases:
                continue
            for k in bases:
                total[k] += 1
            first[bases[0]] += 1
            last[bases[-1]] += 1
    never_final = sorted([list(k) for k, n in total.items() if n >= 20 and last[k] == 0])
    never_initial = sorted([list(k) for k, n in total.items() if n >= 20 and first[k] == 0])
    return {"never_final": never_final, "never_initial": never_initial}


def table_from(co, marks=False):
    """Best reading per glyph with its share of the votes.

    For marks the votes are grouped with waqf signs removed: KFGQPC attaches an
    āyah-final ۖ to the last vowel, which is a fact about that hand, not about
    the vowel glyph.  A glyph whose only non-empty readings *are* waqf signs is a
    waqf glyph and is read as the commonest of them."""
    t = {}
    for g, c in co.items():
        tot = sum(c.values())
        if marks:
            nonempty = {sp for sp in c if sp}
            if nonempty and all(set(sp) <= WAQF for sp in nonempty):
                best, n = max(((sp, k) for sp, k in c.items() if sp), key=lambda kv: kv[1])
                t[g] = dict(span=best, share=n / sum(k for sp, k in c.items() if sp), n=tot, alts=c.most_common(4))
                continue
            grouped = Counter()
            for sp, k in c.items():
                grouped["".join(ch for ch in sp if ch not in WAQF)] += k
            if g in COLOURED:
                # a coloured glyph marks what the riwāyah does that Ḥafṣ does not; a plain
                # vowel is what Ḥafṣ has, so it cannot be this glyph's reading
                plain = [sp for sp in grouped if sp and set(sp) <= PLAIN]
                if len(plain) < len([sp for sp in grouped if sp]):
                    for sp in plain:
                        tot -= grouped.pop(sp)    # those votes say nothing about the sign
            best, n = grouped.most_common(1)[0]
            if best == "":
                # a drawn glyph stands for something; an empty reading only says that
                # hand omits the sign.  Prefer a sign with real support.
                signs = [(sp, k) for sp, k in grouped.most_common() if sp]
                if signs and signs[0][1] >= 0.3 * tot:
                    best, n = signs[0]
                    tot = tot - grouped[""]        # the empty votes say nothing about the sign
            if set(grouped) - {""} and set(grouped) - {""} <= IMALAH_DOTS:
                # the imālah dot (Dūrī) against the taqlīl dot (Warsh): one family of
                # phenomena under two KFGQPC signs; the tier-2 readers who carry a
                # coloured dot (Ḥamzah, al-Kisāʾī, Khalaf) read imālah, so its sign is written
                best = "\u06ea"; n = sum(k for sp, k in grouped.items() if sp)
            t[g] = dict(span=best, share=n / tot, n=sum(c.values()), alts=c.most_common(4))
        else:
            (best, n) = c.most_common(1)[0]
            t[g] = dict(span=best, share=n / tot, n=tot, alts=c.most_common(4))
    return t


def learn_order(types):
    prec = Counter()
    for _G, U in types:
        for _, cm in split_u(U):
            for i in range(len(cm)):
                for j in range(i + 1, len(cm)):
                    if cm[i] != cm[j]:
                        prec[(cm[i], cm[j])] += 1
    cps = {c for p in prec for c in p}
    return {c: sum(1 for d in cps if d != c and prec[(d, c)] > prec[(c, d)]) for c in cps}


def train(pairs, T=None, rounds=6, log=print):
    types = word_types(pairs)
    T = T or Tables()
    if not T.order:
        T.order = learn_order(types)
    log(f"  {len(pairs)} pairs -> {len(types)} word types")
    before = None
    for r in range(rounds):
        a_b = association(types, T.marklike)
        used, bco, cco, mco, lco = learn_round(types, T, a_b)
        for g, v in table_from(bco).items():
            if g not in T.base or v["n"] >= T.base[g]["n"] * 0.5:
                T.base[g] = v
        for g, v in table_from(cco).items():
            T.ctx[g] = v
        for g, v in table_from(mco, marks=True).items():
            if g not in T.mark or v["n"] >= T.mark[g]["n"] * 0.5:
                T.mark[g] = v
        for g, v in table_from(lco).items():
            T.lig[g] = v
        newly = {g for g, v in T.base.items() if v["span"] == "" and v["share"] >= KNOWN and v["n"] >= MIN_TYPES and g not in T.marklike}
        T.marklike |= newly
        for g in newly:
            T.base.pop(g, None)
        kb = sum(1 for v in T.base.values() if v["share"] >= KNOWN)
        km = sum(1 for v in T.mark.values() if v["share"] >= KNOWN_MARK)
        log(f"  round {r}: types used {used}/{len(types)}  bases {len(T.base)} ({kb} known)  marks {len(T.mark)} ({km} known)  marklike {len(T.marklike)}")
        if (used, kb, km) == before:
            break
        before = (used, kb, km)
    return T


# --------------------------------------------------------------------------
# identification of glyphs the calibration files never use
# --------------------------------------------------------------------------

def decode_tokens(toks, table: hqpb.Table):
    """Decoded word strings for the w/h tokens of a target, with the glyph lists and unknown flags."""
    out = []
    for t in toks:
        if t["kind"] == "w":
            d = hqpb.decode_word(t["glyphs"], table)
            out.append((t["glyphs"], d.text, bool(d.unknown)))
        elif t["kind"] == "h":
            out.append((t["glyphs"], hqpb.HIZB, False))
        elif t["kind"] == "m":
            out.append((None, hqpb.AYAH_SIGN, False))
    return out


def surah_chunks(decoded):
    """Split decoded tokens into sūrahs by the basmalah/number logic of hqpb.decode_stream is not
    available here, so use the marker numbers: a restart to 1 opens a sūrah."""
    # markers carry no number here; use hqpb.decode_stream on the stream instead (see identify()).
    raise NotImplementedError


def cross_pairs(slug: str, T: Tables, kf_all: dict) -> list[tuple[list, str]]:
    """Pairs for words with unknown glyphs: each paired with every KFGQPC word of equal rasm aligned
    at its position in the sūrah, across all seven KFGQPC texts."""
    import difflib
    st = hqpb.load_stream(ISLAMWEB / slug / "glyphs.json.gz")
    table = T.as_hqpb()
    surahs = hqpb.decode_stream(st, table)
    fonts = st["fonts"]
    # glyph lists per sūrah in word order (hqpb.Surah keeps only text; rebuild from the stream)
    toks = [t for page in st["pages"] for line in page["lines"] for t in line]
    glyph_words = iter([((fonts[f], gid), bool(m)) for f, gid, _c, m in t["g"]] for t in toks if t["k"] == "w")
    known = set(table.base) | set(table.mark) | set(table.marklike)
    colors = st["colors"]
    for t in toks:
        if t["k"] == "w":
            COLOURED.update((fonts[f], gid) for f, gid, c, m in t["g"] if colors[c] != "#000000" and (fonts[f], gid) not in known)
    coloured_unknown = iter(any(colors[c] != "#000000" and (fonts[f], gid) not in known for f, gid, c, m in t["g"])
                            for t in toks if t["k"] == "w")
    pairs = []
    for s in surahs:
        words, glyphs, coloured = [], [], []
        for w in s.words:
            if w == hqpb.AYAH_SIGN:
                continue
            words.append(w)
            if w != hqpb.HIZB:
                glyphs.append(next(glyph_words)); coloured.append(next(coloured_unknown))
            else:
                glyphs.append(None); coloured.append(False)
        has_unknown = [hqpb.UNKNOWN in w for w in words]
        if not any(has_unknown):
            continue
        rasm_d = [normalize.rasm(w.replace(hqpb.UNKNOWN, "")) for w in words]

        def aligned(key):
            ref_words = [w for ss, a, t in kf_all[key] if ss == s.index and a > 0 for w in light(t).split()]
            rasm_r = [normalize.rasm(w) for w in ref_words]
            sm = difflib.SequenceMatcher(None, rasm_r, rasm_d, autojunk=False)
            out = {}
            for tag, i1, i2, j1, j2 in sm.get_opcodes():
                if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
                    for ri, di in zip(range(i1, i2), range(j1, j2)):
                        out[di] = ref_words[ri]
            return out

        hafs_at = aligned("hafs")
        for key in kf_all:
            for di, ref_word in aligned(key).items():
                if not has_unknown[di] or glyphs[di] is None:
                    continue
                # A coloured glyph marks what the riwāyah does differently from Ḥafṣ:
                # a reference that reads the word as Ḥafṣ does cannot name it.
                if coloured[di] and (key in ("hafs", "shubah") or hafs_at.get(di) == ref_word):
                    continue
                pairs.append((glyphs[di], ref_word))
    return pairs


def identify(T: Tables, kf_all: dict, log=print) -> Tables:
    """Learn the target-only glyphs from cross-riwāyah pairs; record the supporting texts."""
    for round_ in range(3):
        pairs = []
        for slug in TARGETS:
            pairs.extend(cross_pairs(slug, T, kf_all))
        if not pairs:
            break
        known_before = set(T.base) | set(T.mark) | set(T.marklike)
        log(f"identification round {round_}: {len(pairs)} cross-riwāyah pairs")
        T = train(pairs, T, rounds=3, log=log)
        new = (set(T.base) | set(T.mark) | set(T.marklike)) - known_before
        for g in new:
            kind = "base" if g in T.base else "mark" if g in T.mark else "marklike"
            T.method[(kind, g)] = {"method": "aligned-cross"}
        log(f"  newly identified: {len(new)}")
        if not new:
            break
    return T


# --------------------------------------------------------------------------
# what alignment cannot settle: outline twins, then inspection
# --------------------------------------------------------------------------

def outlines() -> dict:
    """``(family, gid) -> outline signature`` for every glyph in the embedded fonts.

    Needs PyMuPDF and fontTools (``.venv``); without them this stage is skipped
    and says so.  A signature is the glyph's contour point list, translated to
    its own origin, so two glyphs drawn from the same design compare equal.
    """
    try:
        import io
        import pymupdf
        from fontTools.ttLib import TTFont
    except ImportError:
        return {}
    out = {}
    for d in sorted(ISLAMWEB.iterdir()):
        pdf = d / "quran.pdf"
        if not pdf.exists():
            continue
        doc = pymupdf.open(pdf)
        done = set()
        for pno in range(doc.page_count):
            for xref, _ext, _typ, name, *_ in doc.get_page_fonts(pno, full=True):
                fam = name.split("+")[-1]
                if xref in done or not (fam.startswith("HQPB") or fam in ("MSH-Quraan1", "Hamd2")):
                    continue
                done.add(xref)
                try:
                    tt = TTFont(io.BytesIO(doc.extract_font(xref)[3]))
                except Exception:
                    continue
                glyf = tt["glyf"]
                for gid, gname in enumerate(tt.getGlyphOrder()):
                    g = glyf[gname]
                    if g.numberOfContours in (0, None) or (fam, gid) in out:
                        continue
                    if g.isComposite():
                        out[(fam, gid)] = ("composite", tuple((c.glyphName, c.x, c.y) for c in g.components))
                        continue
                    coords, ends, _flags = g.getCoordinates(glyf)
                    x0 = min(x for x, _y in coords); y0 = min(y for _x, y in coords)
                    out[(fam, gid)] = (tuple(ends), tuple((x - x0, y - y0) for x, y in coords))
    return out


def twins(T: Tables, unknown: set, log=print) -> int:
    """Give an unknown glyph the reading of a known glyph with the identical outline."""
    sig = outlines()
    if not sig:
        log("  outline stage skipped: PyMuPDF/fontTools not available")
        return 0
    by_sig = defaultdict(list)
    for k, v in sig.items():
        by_sig[v].append(k)
    found = 0
    for g in sorted(unknown):
        if g not in sig:
            continue
        for twin in by_sig[sig[g]]:
            if twin == g:
                continue
            for kind, tab, bar in (("base", T.base, KNOWN), ("mark", T.mark, KNOWN_MARK)):
                v = tab.get(twin)
                if v and accepted(v, bar):
                    tab[g] = dict(v, twin=list(twin))
                    T.method[(kind, g)] = {"method": "shape", "twin": list(twin)}
                    found += 1
                    break
            else:
                if twin in T.marklike:
                    T.marklike.add(g); T.method[("marklike", g)] = {"method": "shape", "twin": list(twin)}
                    found += 1; break
                continue
            break
    log(f"  outline twins identified: {found}")
    return found


INSPECTED = DECODER / "inspected.json"


def inspected(T: Tables, log=print) -> int:
    """Entries read off rendered crops and recorded by hand in ``inspected.json``.

    Each entry names the glyph, its reading, who read it and from which page,
    so the one step that is not mechanical is at least on the record."""
    if not INSPECTED.exists():
        return 0
    n = 0
    for e in json.loads(INSPECTED.read_text(encoding="utf-8"))["entries"]:
        g = (e["font"], e["gid"])
        v = dict(span=e["text"], share=1.0, n=MIN_TYPES, alts=[[e["text"], 0]])
        if e["kind"] == "context":
            marks = tuple((f, gg) for f, gg in e.get("marks", []))
            prev = tuple(e["prev"]) if e.get("prev") else None
            T.ctx[(prev, g, marks)] = v
        elif e["kind"] == "base":
            T.base[g] = v
        elif e["kind"] == "mark":
            T.mark[g] = v
            if not g[0].startswith(("HQPB4", "HQPB5")):
                T.marklike.add(g)          # a sign in a letter font attaches to the letter before it
        else:
            T.marklike.add(g)
        T.method[(e["kind"], g)] = {"method": "inspected", "by": e.get("by", ""), "evidence": e.get("evidence", "")}
        n += 1
    log(f"  inspected entries applied: {n}")
    return n


# --------------------------------------------------------------------------
# scoring
# --------------------------------------------------------------------------

def score(slug: str, key: str, T: Tables, kf: list) -> dict:
    import difflib
    table = T.as_hqpb()
    st = hqpb.load_stream(ISLAMWEB / slug / "glyphs.json.gz")
    surahs = hqpb.decode_stream(st, table)
    ref = defaultdict(list)
    for s, a, t in kf:
        if a > 0:
            ref[s].extend(light(t).split())
    tot = eq_rasm = eq_light = 0
    unk_words = 0
    unknown = Counter()
    for s in surahs:
        words = [w for w in s.words if w != hqpb.AYAH_SIGN]
        unk_words += sum(hqpb.UNKNOWN in w for w in words)
        unknown.update(s.unknown)
        R = ref.get(s.index, [])
        sm = difflib.SequenceMatcher(None, [normalize.rasm(w) for w in R], [normalize.rasm(w) for w in words], autojunk=False)
        tot += len(R)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                eq_rasm += i2 - i1
                eq_light += sum(a == b for a, b in zip(R[i1:i2], words[j1:j2]))
    return dict(slug=slug, against=key, words=tot, rasm_agreement=round(eq_rasm / tot, 4),
                exact_light_agreement=round(eq_light / tot, 4), words_with_unknown_glyph=unk_words,
                unknown_glyphs=[{"font": f, "gid": g, "n": n} for (f, g), n in unknown.most_common()])


def coverage(slug: str, T: Tables) -> dict:
    table = T.as_hqpb()
    st = hqpb.load_stream(ISLAMWEB / slug / "glyphs.json.gz")
    surahs = hqpb.decode_stream(st, table)
    unknown = Counter()
    words = unk_words = 0
    for s in surahs:
        for w in s.words:
            if w == hqpb.AYAH_SIGN:
                continue
            words += 1
            unk_words += hqpb.UNKNOWN in w
        unknown.update(s.unknown)
    return dict(slug=slug, surahs=len(surahs), ayahs=sum(w == hqpb.AYAH_SIGN for s in surahs for w in s.words),
                words=words, words_with_unknown_glyph=unk_words,
                unknown_glyphs=[{"font": f, "gid": g, "n": n} for (f, g), n in unknown.most_common()],
                printed_number_slips=len(hqpb.printed_number_slips(surahs)))


# --------------------------------------------------------------------------

def main(argv):
    log = lambda *a: print(*a, flush=True)
    kf_all = kfgqpc_texts()
    if "--holdout" in argv:
        for held in CALIBRATION:
            pairs = []
            for slug, key in CALIBRATION.items():
                if slug != held:
                    pairs.extend(calibration_pairs(slug, kf_all[key]))
            log(f"== hold out {held}")
            T = train(pairs, log=log)
            r = score(held, CALIBRATION[held], T, kf_all[CALIBRATION[held]])
            log(f"   rasm {r['rasm_agreement']}  exact {r['exact_light_agreement']}  unknown-words {r['words_with_unknown_glyph']}")
        return
    pairs = []
    for slug, key in CALIBRATION.items():
        pairs.extend(calibration_pairs(slug, kf_all[key]))
    log("== learning from Qālūn, Shuʿbah, Warsh")
    T = train(pairs, log=log)
    T.joins = word_edge_forms(CALIBRATION)
    log(f"  word-edge forms: {len(T.joins['never_final'])} glyphs never end a word, {len(T.joins['never_initial'])} never begin one")
    log("== identifying target-only glyphs across the KFGQPC riwāyāt")
    T = identify(T, kf_all, log=log)
    log("== what alignment left: the inspected table, then outline twins of what is known")
    inspected(T, log=log)
    still = set()
    for slug in TARGETS:
        still.update((u["font"], u["gid"]) for u in coverage(slug, T)["unknown_glyphs"])
    if still:
        twins(T, still, log=log)
    DECODER.mkdir(parents=True, exist_ok=True)
    table = T.to_json()
    (DECODER / f"table-v{TABLE_VERSION}.json").write_text(json.dumps(table, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    log(f"table: {len(table['entries'])} entries, {len(table['context'])} context rules, {len(table['ligatures'])} ligatures")
    cal = {"table": f"table-v{TABLE_VERSION}.json", "calibration": {}, "targets": {},
           # glyphs the evidence does not settle: listed with their readings so the
           # next revision of the table can be argued from data
           "contested": sorted(
               [dict(font=g[0], gid=g[1], kind=kind, types=v["n"], share=round(v["share"], 3),
                     readings=[[sp, k] for sp, k in v["alts"]])
                for kind, tab, bar in (("base", T.base, KNOWN), ("mark", T.mark, KNOWN_MARK))
                for g, v in tab.items() if not accepted(v, bar) and v["n"] >= MIN_TYPES],
               key=lambda e: -e["types"])}
    for slug, key in CALIBRATION.items():
        cal["calibration"][slug] = score(slug, key, T, kf_all[key])
        log(f"  {slug}: rasm {cal['calibration'][slug]['rasm_agreement']} exact {cal['calibration'][slug]['exact_light_agreement']}")
    for slug in TARGETS:
        cal["targets"][slug] = coverage(slug, T)
        c = cal["targets"][slug]
        log(f"  {slug}: surahs {c['surahs']} ayahs {c['ayahs']} words {c['words']} words-with-unknown {c['words_with_unknown_glyph']} distinct-unknown {len(c['unknown_glyphs'])} slips {c['printed_number_slips']}")
    (DECODER / "calibration.json").write_text(json.dumps(cal, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1:])
