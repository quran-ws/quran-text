"""Publish each muṣḥaf on its own, as words by position with layers over them.

``data/`` already answers *how do the muṣḥafs differ?*  It does not answer *give
me Warsh*: a consumer who wants one muṣḥaf has to take the comparison and
project it back out.  This module writes the other view — one self-contained
file per muṣḥaf.

**A muṣḥaf is an ordered array of word strings.  Everything else is a layer over
that array, addressed by position.**  ``words[i]`` is the *i*-th word of this
muṣḥaf; ``ayah_starts``, ``page_starts``, ``line_starts``, ``juz_starts`` and
``surah_starts`` are sorted lists of positions, so unit *k* of any layer is
``words[starts[k]:starts[k+1]]`` — a slice, correct in all seven files.

Two kinds of integer appear and are kept apart.  A **position** is an index
into ``words`` of *this* muṣḥaf; every key ending in ``_starts`` holds
positions, as do ``marks[][0]`` and ``resegmentation[].positions``.  A
**number** is the shared numbering that means the same word in all seven; only
the ``numbering`` block holds numbers.  A consumer who works in one muṣḥaf
never reads it.

Only ``data/mushaf/<key>.json`` and ``data/word-index.json`` are normative.  The
nested, CSV and SQLite forms in :mod:`qurantext.views` are generated from the
same build and are labelled views, so that whichever one turns out to
be most convenient cannot quietly become the standard.

Nothing here is asserted that the packages do not say.  Where a fact is derived
rather than read it is marked derived, where it is unavailable the field is
absent and the absence is explained, and where this build departs from the
source's own word spacing every instance is listed in the file itself.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path

from . import chars, counting, fonts, rasm_imlai, sources
from . import paths, stamp
from .build import DATA, Word
from .word_index import boundary_events
from .sources import ISLAMWEB, ISLAMWEB_URL, PACKAGES, RELEASE_POLICY, TIER_POLICY, Riwayah
from .surahs import names

FORMAT = "quran-mushaf"
FORMAT_VERSION = "1.1"

MUSHAF_DIR = DATA / "mushaf"

#: Signs that can attach to a word, with the Unicode name of each.  Emitted in
#: every file so a consumer never has to hard-code a codepoint table.
MARK_NAMES = {
    "ۖ": "ARABIC SMALL HIGH LIGATURE SAD WITH LAM WITH ALEF MAKSURA",
    "ۗ": "ARABIC SMALL HIGH LIGATURE QAF WITH LAM WITH ALEF MAKSURA",
    "ۘ": "ARABIC SMALL HIGH MEEM INITIAL FORM",
    "ۙ": "ARABIC SMALL HIGH LAM ALEF",
    "ۚ": "ARABIC SMALL HIGH JEEM",
    "ۛ": "ARABIC SMALL HIGH THREE DOTS",
    "ۜ": "ARABIC SMALL HIGH SEEN",
    "۞": "ARABIC START OF RUB EL HIZB",
    "۩": "ARABIC PLACE OF SAJDAH",
    "ۤ": "ARABIC SMALL HIGH MADDA",
    "࣌": "ARABIC SMALL HIGH WORD SAH",
    "࢈": "ARABIC RAISED ROUND DOT",
}

#: The editorial signs, each published as a kind of its own so a consumer can
#: keep or drop them by name rather than by codepoint.
EDITORIAL_KINDS = {"࣌": "sah", "࢈": "raised_dot"}


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _provenance(r: Riwayah) -> dict:
    """Which KFGQPC release every part of this file came from.

    Recorded in the file itself and not only in the manifest, because a muṣḥaf
    file will be copied, mirrored and vendored on its own, and a text whose
    edition cannot be named is not a citable one.
    """
    spec = r.spec
    if spec.primary_kind == "hqpb":
        return _provenance_tier2(r)
    text = PACKAGES / f"{spec.primary_zip}.zip"
    out = {
        "tier": 1,
        "authority": spec.authority,
        "text": {
            "package": text.name,
            "member": spec.primary_member,
            "release_year": spec.primary_year,
            "sha256": _sha256(text),
            # Always empty for a primary .docx: the archive does not hold one.
            "origin": sources.origin("", text.name),
        },
        "policy": RELEASE_POLICY,
    }
    if spec.csv_zip:
        layout = PACKAGES / f"{spec.csv_zip}.zip"
        out["layout"] = {
            "package": layout.name,
            "member": spec.csv_member,
            "release_year": spec.csv_year,
            "sha256": _sha256(layout),
            "origin": sources.origin(spec.csv_slug, layout.name),
            "used_for": ["juz", "line_check"],
        }
    return out


def _marks(w: Word, key: str) -> list[dict]:
    """Every sign printed against this word, with the side it sits on."""
    out = []
    if key in w.division:
        out.append({"kind": "division", "side": "before", "sign": "۞"})
    for sign in w.waqf.get(key, ""):
        if sign == "۩":
            continue                       # emitted below, as its own kind
        out.append({"kind": "waqf", "side": "after", "sign": sign})
    # Order matters: where a word carries both — ``يَسۡجُدُونَۤ۩`` at 7:206 and
    # 84:21 — the release writes the line inside the sign, and re-attaching the
    # marks in the order emitted has to reproduce the printed token.
    if key in w.sajdah_line:
        out.append({"kind": "sajdah_line", "side": "after",
                    "sign": chars.SAJDAH_LINE})
    if key in w.sajdah:
        out.append({"kind": "sajdah", "side": "after", "sign": "۩"})
    for sign in w.editorial.get(key, ""):
        out.append({"kind": EDITORIAL_KINDS[sign], "side": "after", "sign": sign})
    # The kinds above are collected one at a time, which loses the order the
    # release wrote them in.  Where the release kept it, it wins: Warsh writes
    # the ṣaḥḥa *before* ۩ at all 13 of its sajdah words (``يَسْجُدُونَ࣌۩``), and
    # emitting ۩ first re-attaches into a token the release never printed.
    # Each sign takes the first place in ``trailing`` not already taken, so a
    # sign written twice keeps both places; one the string lacks goes last.
    # ``sort`` is stable, so a word without ``trailing`` keeps the order above.
    printed = w.trailing.get(key, "")
    if printed:
        taken: set[int] = set()

        def place(m: dict) -> tuple[bool, int]:
            if m["side"] != "after":
                return (False, 0)
            at = printed.find(m["sign"])
            while at in taken:
                at = printed.find(m["sign"], at + 1)
            if at < 0:
                return (True, len(printed))
            taken.add(at)
            return (True, at)

        out.sort(key=place)
    return out


def _starts(values: list) -> list[int]:
    """Positions at which a per-position value changes — one per unit."""
    out: list[int] = []
    prev = object()
    for i, v in enumerate(values):
        if v != prev:
            out.append(i)
            prev = v
    return out


class Printed:
    """One printed word of one muṣḥaf: its position, and the numbers it covers.

    Almost every printed word covers one number.  At 72:16 and 73:20 a muṣḥaf
    that writes ``وَأَلَّوِ`` or ``أَلَّن`` as one word covers two.  ``word`` is the
    :class:`Word` of the first number, which carries the text, the āyah and
    the place; the covered numbers carry the same token and add nothing.
    """

    __slots__ = ("position", "first", "last", "word")

    def __init__(self, position: int, word: Word):
        self.position = position
        self.first = self.last = word.id
        self.word = word


def printed_words(words: list[Word], key: str) -> tuple[list[Printed], list[int]]:
    """Walk the numbering and return this muṣḥaf's printed words and its gaps."""
    printed: list[Printed] = []
    missing: list[int] = []
    for w in words:
        if key not in w.forms:
            missing.append(w.id)
        elif key in w.continuation:
            printed[-1].last = w.id
        else:
            printed.append(Printed(len(printed), w))
    return printed, missing


def numbering(printed: list[Printed], missing: list[int], total: int) -> dict:
    """How this muṣḥaf's positions map onto the shared numbering.

    ``missing`` lists the numbers this muṣḥaf does not read — the only way a
    number can fail to be covered.  ``written_joined`` lists the printed words
    that cover more than one number — the only way a position can cover more
    than one.  Everything else is one word, one number, in step, and is not
    stored.  See ``docs/format.md``, *Numbering*, for the invariants.
    """
    return {
        "total": total,
        "missing": missing,
        "written_joined": [{"position": p.position, "numbers": [p.first, p.last]}
                           for p in printed if p.last > p.first],
    }


def numbers_of(doc: dict) -> list[tuple[int, int]]:
    """position -> ``(first, last)`` run of shared numbers, for a published file.

    The one-pass walk the spec describes: advance one per word, skip
    ``missing``, advance by the run length at a ``written_joined`` position.
    Raises ``AssertionError`` where the block does not tile ``1 … total``.
    """
    key = doc["mushaf"]["key"]
    block = doc["numbering"]
    missing = set(block["missing"])
    joined = {j["position"]: j["numbers"] for j in block["written_joined"]}
    runs, n = [], 1
    for position in range(len(doc["words"])):
        while n in missing:
            n += 1
        first, last = joined.get(position, (n, n))
        if first != n:
            raise AssertionError(f"{key}: run at {position} starts {first}, expected {n}")
        if last < first:
            raise AssertionError(f"{key}: run at {position} is empty")
        runs.append((first, last))
        n = last + 1
    while n in missing:
        n += 1
    if n != block["total"] + 1:
        raise AssertionError(f"{key}: runs and missing do not tile 1…total")
    return runs


def _surahs(key: str, printed: list[Printed], ayah_starts: list[int],
           r: Riwayah) -> list[dict]:
    """The 114-row sūrah header, in full, in every muṣḥaf's own file.

    Duplicated across the seven rather than shared, because a file that needs a
    second download before it can name a sūrah is not a muṣḥaf that ships alone.
    It costs 114 rows against 77,000 words.
    """
    basmalah_printed = {a.surah for a in r.ayahs if a.ayah == 0} | {1}
    by_surah: dict[int, list[Printed]] = defaultdict(list)
    for p in printed:
        by_surah[p.word.surah].append(p)
    first_ayah_of: dict[int, int] = {}
    for k, position in enumerate(ayah_starts):
        first_ayah_of.setdefault(printed[position].word.surah, k)

    out = []
    for surah, ps in sorted(by_surah.items()):
        info = names()[surah]
        out.append({
            "number": surah,
            "name_ar": info["name_ar"],
            "name_en": info["name_en"],
            "revelation": info["revelation"],
            "has_basmalah": surah in basmalah_printed,
            "ayah_count": max(p.word.ayah.get(key, 0) for p in ps),
            "first_ayah": first_ayah_of[surah],
        })
    return out


def _resegmentation(key: str, words: list[Word], at: dict[int, int]) -> list[dict]:
    """Every place this build changed the source's own word spacing.

    A shared numbering is only stable because the alignment occasionally
    overrides a package's spacing — splitting what one source printed joined —
    so a file claiming to *be* that muṣḥaf has to say where it did so.  The
    list is present even when empty, so silence is never ambiguous.

    A word a muṣḥaf *really* prints joined — ``written_joined`` in
    ``numbering`` — is not here: that is a fact about the muṣḥaf, not a
    departure from it.
    """
    out = []
    for event in boundary_events(words):
        if key not in event["riwayahs"]:
            continue
        ids = event["word_ids"]
        mine = [w for w in words if w.id in set(ids) and key in w.forms]
        source = next((t for t, ks in event["texts"].items() if key in ks), "")
        out.append({
            "positions": sorted({at[i] for i in ids if i in at}),
            "surah": event["surah"],
            "ayah": event["ayah"],
            "kind": event["kind"],
            "source_text": source,
            "emitted": [w.forms[key] for w in mine],
            "riwayahs_agree": event["agree"],
        })
    return out


def _line_check(key: str, printed: list[Printed], r: Riwayah) -> dict:
    """Re-check the reconstructed lines against the release that states them.

    The page is read from the document; the line is inferred from its flow (see
    :mod:`qurantext.layout`).  The v2 CSV states the line of every āyah, so the
    inference can be scored rather than merely asserted — and the āyāt it gets
    wrong are listed, so a consumer can exclude them instead of discovering them.

    Bazzī has no v2 release, so it is not scored here.  That is a gap in the
    *check*, not in the data: its lines are identical, word for word, to Ḥafṣ's
    (``docs/known-issues.md`` §6), so they carry Ḥafṣ's accuracy.
    """
    if not r.meta:
        return {"validated": False,
                "reason": "no v2 package released for this riwāyah"}

    by_ayah: dict[tuple[int, int], list[Word]] = defaultdict(list)
    for p in printed:
        by_ayah[(p.word.surah, p.word.ayah[key])].append(p.word)

    checked = agreed = 0
    wrong = []
    for k, meta in r.meta.items():
        ws = by_ayah.get(k)
        if not ws or not meta["line_end"].isdigit():
            continue
        checked += 1
        got = max(w.place[key][1] for w in ws if key in w.place)
        want = int(meta["line_end"])
        if got == want:
            agreed += 1
        else:
            wrong.append({"surah": k[0], "ayah": k[1], "derived": got, "source": want})
    return {
        "validated": True,
        "against": r.crosscheck_source,
        "ayahs_checked": checked,
        "ayahs_agreeing": agreed,
        "disagreements": wrong,
    }


#: What the colours in the islamweb documents mean, from the legends the Warsh
#: and Hishām files print.  The other files use the same palette unlabelled.
COLOR_LEGEND = {
    "#ff00ff": "الحرف المخالف لحفص — the letter that differs from Ḥafṣ",
    "#ff0000": "الإدغام — idghām",
    "#00ccff": "التقليل — taqlīl",
    "#3365ff": "مد البدل — madd al-badal",
    "#00ff00": "الراءات المرققة — tarqīq al-rāʾ",
    "#0000ff": "اللامات المغلظة / الإدغام — taghlīẓ al-lām (Warsh legend) or idghām (Qālūn, Hishām)",
    "#ff6500": "صلة ميم الجمع — ṣilat mīm al-jamʿ",
    "#9acc00": "مد اللين — madd al-līn",
    "#33cccc": "الإمالة — imālah (Hishām legend)",
}


def _colors(key: str, printed, r: Riwayah) -> tuple[list | None, list | None]:
    """``[[position, type]]`` for every coloured word of a tier-2 file, and the types.

    Colour is per glyph in the document; a word's type is the set of colours on
    it.  The decoded words are aligned to the printed words sūrah by sūrah, so
    a word the build re-segmented still carries its colour.  The legend text is
    quoted from the two files that print one.
    """
    import difflib
    if not r.decoded:
        return None, None
    printed_by_surah: dict[int, list] = defaultdict(list)
    for p in printed:
        printed_by_surah[p.word.surah].append(p)
    colored = defaultdict(dict)                      # surah -> word index -> colours
    for surah, n, cols in r.decoded["colors"]:
        colored[surah][n - 1] = cols
    types: list[dict] = []
    index: dict[tuple, int] = {}
    out: list[list[int]] = []
    for surah, decoded in r.decoded["words"].items():
        if not colored.get(surah):
            continue
        plist = printed_by_surah.get(surah, [])
        pw = [p.word.forms[key] for p in plist]
        sm = difflib.SequenceMatcher(None, decoded, pw, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            pairs = zip(range(i1, i2), range(j1, j2)) if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1) else ()
            for di, pi in pairs:
                cols = colored[surah].get(di)
                if not cols:
                    continue
                sig = tuple(sorted(cols))
                if sig not in index:
                    index[sig] = len(types)
                    types.append({"colors": list(sig),
                                  "meaning": [COLOR_LEGEND.get(c, "not in any printed legend") for c in sig]})
                out.append([plist[pi].position, index[sig]])
    out.sort()
    return out, types


def _text_note(mark_count: int) -> dict:
    """How to get this muṣḥaf's printed text out of ``words``.

    ``words`` is the text *without* the mark layer, which is not the same
    string as the text the muṣḥaf prints and not what the download service
    returns.  A consumer who joins ``words`` with a space gets a plausible
    muṣḥaf and no sign that it is missing anything — and every character
    offset after the first sign is a different number.  Saying so here, beside
    the layer list, costs one block and saves the measurement.
    """
    return {
        "words_exclude": ["marks"],
        "how": (
            "words[i] carries no mark: the waqf signs, ۩, the sajdah line and "
            "۞ are in `marks`, addressed by position, and not in the string. "
            "Joining words with a single space therefore gives the text "
            f"without this muṣḥaf's {mark_count:,} signs — a different string, "
            "and a different offset for every character after the first one."),
        "reattach": (
            "To print what the release prints, re-attach each word's marks in "
            "the order `marks` lists them: a mark whose `side` is \"after\" is "
            "appended to the word with no space, and a mark whose `side` is "
            "\"before\" — ۞ — is written before it, separated by a space."),
        "download_service": (
            "https://text.quran.ws/download returns the text with the marks "
            "in place, so a digest taken over joined `words` will not match "
            "it. The client libraries under lib/ do the re-attaching: "
            "Word.render() and Span.render(marks=...)."),
    }


def _provenance_tier2(r: Riwayah) -> dict:
    """Which document a decoded text came from, and what decoded it.

    The document is not a publisher's data release: it is a PDF of unnamed
    authorship hosted by islamweb, so the record says who hosts it, what it is,
    its checksum, and which table — with what measured accuracy — turned its
    glyphs into text.  Weaker provenance, stated rather than glossed.
    """
    spec = r.spec
    src = r.decoded["source"]
    table_path = ISLAMWEB / "decoder" / r.decoded["table"]["file"]
    calibration = json.loads((ISLAMWEB / "decoder" / "calibration.json").read_text(encoding="utf-8"))
    return {
        "tier": 2,
        "authority": spec.authority,
        "text": {
            "package": "quran.pdf",
            "member": f"islamweb/{spec.slug}/glyphs.json.gz",
            "release_year": r.release_year,
            "sha256": src["sha256"],
            "origin": {
                "recorded": True,
                "url": ISLAMWEB_URL.format(slug=spec.slug),
                "fetched": src["fetched"],
                "bytes": src["bytes"],
                "publisher": "islamweb.net",
                "author": "not stated in the document",
                "document": src.get("pdf", {}),
                "note": "A Word document set in KFGQPC's 2005 HQPB fonts and distilled to PDF, "
                        "hosted by islamweb; not a data release by the muṣḥaf's publisher. The PDF "
                        "is not committed (sources/islamweb/<slug>/SOURCE.json records it); the glyph "
                        "stream extracted from it is.",
            },
        },
        "decoder": {
            "table": table_path.name,
            "version": r.decoded["table"]["version"],
            "sha256": _sha256(table_path),
            "learned_from": sorted(calibration["calibration"]),
            "calibration": {k: {"rasm_agreement": v["rasm_agreement"],
                                "exact_agreement": v["exact_light_agreement"]}
                            for k, v in calibration["calibration"].items()},
            "unknown_glyphs": sum(r.decoded["unknown"].values()),
        },
        "policy": TIER_POLICY,
    }


def _layers(r: Riwayah, line_check: dict, has_juz: bool, mark_count: int) -> dict:
    """What this file carries, and why it lacks whatever it lacks."""
    present = ["surahs", "ayahs", "pages", "lines", "marks"]
    absent: dict[str, str] = {}
    if has_juz:
        present.append("juz")
    else:
        absent["juz"] = "no v2 package released for this riwāyah"
    absent["rasm_imlai"] = "column not present in this riwāyah's release"

    derived = {
        "line": {
            "how": "reconstructed from the document's line breaks, "
                   "paragraph boundaries and sūrah headings; printed lines "
                   "are not encoded in the release",
            **{k: v for k, v in line_check.items() if k != "disagreements"},
        },
    }
    if r.decoded:
        present.append("colors")
        derived["line"] = {"how": "read from the glyph positions of the PDF page; every "
                                  "line is one typeset line of the document",
                           "validated": False,
                           "reason": "no second source states this document's lines"}
        derived["text"] = {
            "how": "decoded glyph by glyph from the document with the shared table; "
                   "every codepoint is a table lookup, none is inferred",
            "table": r.decoded["table"]["file"],
            "unknown_glyph_occurrences": sum(r.decoded["unknown"].values()),
            "unknown_glyphs": [{"font": f, "gid": g, "occurrences": n}
                               for (f, g), n in r.decoded["unknown"].most_common()],
            "printed_ayah_number_slips": r.decoded["printed_number_slips"],
            "notation": "the 2022 KFGQPC notation: U+0671 alef wasla, U+0652 sukun, "
                        "U+08F0–U+08F2 open tanwīn, U+064A for the dotless final yāʾ; "
                        "waṣl vowel cues are not carried",
        }
    return {
        "present": present,
        "absent": absent,
        "text": _text_note(mark_count),
        "derived": derived,
        "notes": {
            "page": ("read from the PDF page each glyph is drawn on" if r.decoded else
                     "read from explicit page breaks in the release, not inferred"),
            "kashida": "a kashida (U+0640) that carries a mark is a seat and is "
                    "kept inside the word: where a hamzah, a small high yeh or "
                    "a dagger alif has no letter of its own, the release writes "
                    "it on a kashida. What precedes the seat belongs to the "
                    "letter before it and what follows the seat belongs to the "
                    "sign on it, which is the only place a stacked mark's owner "
                    "is written down. A kashida carrying nothing is typography "
                    "and is dropped",
            "waqf": "waqf-mark conventions differ by muṣḥaf and are not "
                    "comparable across them: Warsh and Qālūn print one general "
                    "sign where Ḥafṣ, Dūrī and Sūsī print seven distinct ones",
            "division": "the ۞ symbol is emitted exactly as the release prints it. "
                    "The releases disagree about how often to print it — 199 "
                    "times in Ḥafṣ, Shuʿbah and Bazzī against 433–437 in the "
                    "others — and nothing here reconciles them",
        },
    }


def _juz_per_position(printed: list[Printed], key: str, r: Riwayah) -> list[int] | None:
    """The juz of every printed word, from the v2 CSV, or ``None`` without one.

    The CSV is per numbered āyah.  The unnumbered basmalah of Al-Fātiḥah has no
    row, so its words take the juz of the āyah that follows them.
    """
    if not r.meta:
        return None
    out: list[int | None] = []
    for p in printed:
        meta = r.meta.get((p.word.surah, p.word.ayah[key]))
        jozz = meta["jozz"] if meta and meta["jozz"].isdigit() else None
        out.append(int(jozz) if jozz else None)
    for i in range(len(out) - 2, -1, -1):        # fill gaps from the right
        if out[i] is None:
            out[i] = out[i + 1]
    for i in range(1, len(out)):                  # then from the left
        if out[i] is None:
            out[i] = out[i - 1]
    return out                                    # type: ignore[return-value]


def document(words: list[Word], r: Riwayah,
             rasm_imlai: dict[int, str] | None = None) -> dict:
    """The whole of one muṣḥaf, in the canonical shape.

    The ``counting`` block is filled in by :func:`qurantext.counting.derive`
    once the file's own āyah layer exists, since it is derived from it.
    """
    key = r.key
    printed, missing = printed_words(words, key)
    at = {}                                      # number -> position
    for p in printed:
        for n in range(p.first, p.last + 1):
            at[n] = p.position

    line_check = _line_check(key, printed, r)
    ayahs = [(p.word.surah, p.word.ayah[key]) for p in printed]
    ayah_starts = [i for i in _starts(ayahs) if ayahs[i][1] > 0]
    surah_starts = _starts([p.word.surah for p in printed])
    places = [p.word.place.get(key) for p in printed]
    page_starts = _starts([pl[0] for pl in places]) if all(places) else None
    line_starts = _starts([pl for pl in places]) if all(places) else None
    juz = _juz_per_position(printed, key, r)

    mark_types: list[dict] = []
    type_index: dict[tuple, int] = {}
    marks: list[list[int]] = []
    for p in printed:
        for m in _marks(p.word, key):
            sig = (m["kind"], m["side"], m["sign"])
            if sig not in type_index:
                type_index[sig] = len(mark_types)
                mark_types.append(m)
            marks.append([p.position, type_index[sig]])

    doc = {
        "format": FORMAT,
        "format_version": FORMAT_VERSION,
        "generated": stamp.generated(),
        "mushaf": {
            "key": key,
            "name_en": r.name_en,
            "name_ar": r.name_ar,
            "qiraah_en": r.qiraah_en,
            "qiraah_ar": r.qiraah_ar,
            "word_count": len(printed),
        },
        "counting": None,
        "normalization": {"applied": "none", "note": "words[i] and the word index's rasm_uthmani hold the release's own codepoints, unnormalised. NFC is canonically equivalent but is not what the package writes: it reorders the marks on a letter — the releases write a shaddah before its vowel, NFC after it, in 22,000 of Ḥafṣ's 84,000 tokens — and composes ا + ٓ into آ in 2,946 more. The derived forms (rasm, pointed, plain, and the search fold) are computed from the NFC form, so comparison is unaffected. For text comparison across datasets, normalize both strings to NFC before comparing."},
        "provenance": _provenance(r),
        "font": fonts.describe(r.spec),
        "colors": _colors(key, printed, r)[0],
        "color_types": _colors(key, printed, r)[1],
        "layers": _layers(r, line_check, juz is not None, len(marks)),
        "words": [p.word.forms[key] for p in printed],
        "rasm_imlai": ([rasm_imlai.get(p.first, rasm_imlai.get(p.last)) for p in printed]
                   if rasm_imlai else None),
        "numbering": numbering(printed, missing, words[-1].id),
        "surah_starts": surah_starts,
        "ayah_starts": ayah_starts,
        "page_starts": page_starts,
        "line_starts": line_starts,
        "juz_starts": _starts(juz) if juz else None,
        "surahs": _surahs(key, printed, ayah_starts, r),
        "marks": marks,
        "mark_types": mark_types,
        "mark_signs": {s: {"cp": f"U+{ord(s):04X}", "unicode_name": n}
                       for s, n in MARK_NAMES.items()},
        "resegmentation": _resegmentation(key, words, at),
        "line_disagreements": line_check.get("disagreements", []),
    }
    if r.decoded:
        doc["normalization"] = {
            "applied": "decoded",
            "note": "words[i] is decoded from the document's glyphs with the table named in "
                    "provenance.decoder and is NFC. The notation is the 2022 KFGQPC one (see "
                    "layers.derived.text.notation). Compare across datasets by normalising both "
                    "sides to NFC.",
        }
    for layer in ("page_starts", "line_starts", "juz_starts", "colors", "color_types"):
        if doc[layer] is None:
            del doc[layer]
    return doc


def _dump(path: Path, doc: dict) -> None:
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=1),
                    encoding="utf-8")


def write_mushafs(words: list[Word], riwayahs: list[Riwayah]) -> dict[str, dict]:
    """Write every muṣḥaf's own file, and return the documents by key.

    Imlāʾī is derived here for whichever release supplies it, and the
    ``counting`` block once the file's own āyah layer exists.
    """
    MUSHAF_DIR.mkdir(parents=True, exist_ok=True)
    for stale in MUSHAF_DIR.glob("*.min.json"):
        stale.unlink()
    docs = {}
    for r in riwayahs:
        mapping, report = rasm_imlai.derive(words, r)
        doc = document(words, r, mapping if report.get("available") else None)
        if report.get("available"):
            doc["layers"]["derived"]["rasm_imlai"] = report
            doc["layers"]["present"].append("rasm_imlai")
            doc["layers"]["absent"].pop("rasm_imlai", None)
        doc["counting"] = counting.derive(doc, words)
        _dump(MUSHAF_DIR / f"{r.key}.json", doc)
        docs[r.key] = doc
    return docs


def write_manifest(docs: dict[str, dict]) -> dict:
    """Every emitted file and every source package, each with its SHA-256.

    A dataset becomes citable when a reader can prove which release a file came
    from without trusting the person who published it.  The manifest is that
    proof: the source hashes let anyone re-derive the build, and the output
    hashes let anyone check that the copy they hold is the one described here.
    """
    files = sorted(p for p in DATA.rglob("*")
                   if p.is_file() and p.name != "manifest.json")

    manifest = {
        "format": FORMAT,
        "format_version": FORMAT_VERSION,
        "generated": stamp.generated(),
        "normative": [f"data/mushaf/{k}.json" for k in docs]
                     + ["data/word-index.json", "data/word-index.csv"],
        "note": "Only the files listed under `normative` define the format. "
                "Everything else is a generated view of them.",
        "sources": {
            **{k: {n: {kk: vv for kk, vv in part.items() if kk != "used_for"}
                   for n, part in doc["provenance"].items()
                   if isinstance(part, dict)}
               for k, doc in docs.items()},
            "qiraat-ayah-map": counting.provenance(),
        },
        "files": [
            {"path": p.relative_to(paths.ROOT).as_posix(),
             "bytes": p.stat().st_size,
             "sha256": _sha256(p)}
            for p in files
        ],
    }
    _dump(DATA / "manifest.json", manifest)
    return manifest
