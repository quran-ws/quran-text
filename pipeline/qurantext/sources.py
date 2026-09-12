"""Loaders for the KFGQPC packages shipped in ``sources/``.

None of the packages contain word-level data — every one of them is
āyah-level.  These loaders bring each release into one shape,
``list[Ayah]``, so the tokeniser downstream never has to care whether a
riwāyah arrived as a 2022 CSV or a 2026 Word document.
"""

from __future__ import annotations

import csv
import io
import re
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from . import chars, paths
from .normalize import strip_controls

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

PACKAGES = paths.SOURCES / "kfgqpc"
WORK = paths.WORK / "raw"


@dataclass(frozen=True)
class Ayah:
    surah: int
    ayah: int
    text: str


@dataclass
class Riwayah:
    key: str
    name_en: str
    name_ar: str
    qiraah_en: str
    qiraah_ar: str
    #: No counting field: the āyah count belongs to the printed edition, not
    #: the riwāyah, and is derived from the package itself.  See
    #: :mod:`qurantext.counting` and ``counting`` in each muṣḥaf file.
    source: str              # provenance of ``ayahs``
    ayahs: list[Ayah] = field(default_factory=list)
    #: (surah, ayah) -> {jozz, page, line_start, line_end}, from the v2 CSVs.
    meta: dict[tuple[int, int], dict] = field(default_factory=dict)
    #: (surah, ayah) -> text, from the *other* release of the same riwāyah.
    crosscheck: dict[tuple[int, int], str] = field(default_factory=dict)
    crosscheck_source: str = ""
    release_year: int = 0
    crosscheck_year: int = 0
    #: One :class:`qurantext.layout.Place` per token of :attr:`ayahs`, flat and in
    #: document order.  Empty for a riwāyah whose primary release is a CSV,
    #: which carries no typesetting.
    places: list = field(default_factory=list)
    #: The registry entry this riwāyah was built from, for the provenance block.
    spec: object = None


# --------------------------------------------------------------------------
# .docx
# --------------------------------------------------------------------------

def docx_paragraphs(path: Path) -> list[str]:
    """Text of every non-empty paragraph, in document order."""
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    out = []
    for paragraph in root.iter(W + "p"):
        # Only <w:t> carries literal text; walking the element tree (rather
        # than regexing the XML) keeps <w:pPr> attribute noise out.
        text = "".join(node.text or "" for node in paragraph.iter(W + "t"))
        if text.strip():
            out.append(text)
    return out


_SURAH_HEAD = re.compile(r"^\s*سُ?ورَ?ةُ?\s")
_AR_NUM = "".join(chars.ARABIC_DIGITS)

# v3.0 marks an āyah with NBSP + U+06DD + digits; the 2022 Dūrī release omits
# the U+06DD and leaves only NBSP + digits.
_AYAH_MARK = re.compile(rf"[  ]?۝?([{_AR_NUM}]+)")

#: The basmalah as printed, from which the needle is derived at run time.
#: Deriving it rather than hard-coding a skeleton is deliberate: a literal
#: skeleton silently ceases to match the day the normalisation changes, and when
#: it did, 113 sūrahs quietly absorbed their opening basmalah into āyah 1.
_BASMALAH_REFERENCE = "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ"


def _arabic_int(s: str) -> int:
    return int("".join(chars.ARABIC_DIGITS[c] for c in s))


def _is_heading(paragraph: str) -> bool:
    return bool(_SURAH_HEAD.match(paragraph)) and not re.search(rf"[{_AR_NUM}]", paragraph)


#: A sūrah heading stranded at the end of the previous sūrah's paragraph.
#: The v3.0 Qālūn document types "سُورَةُ البَقَرَةِ" after Al-Fātiḥah's last āyah
#: mark rather than in its own paragraph, which would otherwise prepend two
#: heading words to Baqarah 2:1.  Anchoring on "text after the final āyah
#: mark of a paragraph" keeps 24:1 ("سُورَةٌ أَنزَلۡنَٰهَا"), which is scripture,
#: safely out of reach.
_TRAILING_HEAD = re.compile(rf"(?<=[{_AR_NUM}])(\s*سُ?ورَ?ةُ\s+[^{_AR_NUM}۝]{{1,40}})$")


def _strip_trailing_heading(paragraph: str) -> str:
    return _TRAILING_HEAD.sub("", paragraph)


def _is_bare_basmalah(paragraph: str) -> bool:
    """A basmalah printed as a sūrah opening rather than counted as an āyah."""
    if re.search(rf"[{_AR_NUM}]", paragraph):
        return False          # numbered: it *is* āyah 1 (Kufi/Makki Al-Fātiḥah)
    from .normalize import pointed
    return pointed(paragraph).replace(" ", "") == _basmalah_needle()


@lru_cache(maxsize=1)
def _basmalah_needle() -> str:
    from .normalize import pointed
    return pointed(_BASMALAH_REFERENCE).replace(" ", "")


def load_docx(path: Path) -> list[Ayah]:
    """Split a KFGQPC Word mushaf into āyāt.

    Sūrah boundaries come from resets in the āyah numbering, not from the
    headings: the v3.0 Qālūn document is missing the heading for Baqarah, so
    heading-driven segmentation silently shifts every sūrah after it by one.
    Numbering resets are intrinsic to the text, and let us assert at the end
    that there are 114 sūrahs of contiguous 1..N āyāt.

    A basmalah that is printed above a sūrah without a number of its own is
    emitted as āyah ``0``.  Whether it counts as an āyah is a property of the
    counting tradition, not of the text: Ḥafṣ, Shuʿbah and Bazzī number the
    basmalah of Al-Fātiḥah as 1:1, the others print the same words unnumbered.
    Keeping it as āyah 0 lets the builder decide, rather than losing the words.
    """
    # A sentinel that cannot occur in Arabic text, used to remember where an
    # unnumbered basmalah sat once the paragraphs are joined into one stream.
    MARK = "\x00"

    parts = []
    for paragraph in docx_paragraphs(path):
        if _is_heading(paragraph):
            continue
        if _is_bare_basmalah(paragraph):
            parts.append(MARK + strip_controls(paragraph).strip() + MARK)
            continue
        parts.append(_strip_trailing_heading(paragraph))
    body = strip_controls(" ".join(parts))

    # Walk the numbered āyāt, remembering any unnumbered basmalah seen first.
    chunks: list[tuple[int, str, str]] = []      # (number, text, opening)
    position = 0
    for m in _AYAH_MARK.finditer(body):
        raw = body[position:m.start()]
        position = m.end()
        opening = ""
        if MARK in raw:
            before, _, raw = raw.partition(MARK)[0], None, raw
            head, _, rest = raw.partition(MARK)
            opening, _, rest = rest.partition(MARK)
            raw = head + " " + rest
        chunks.append((_arabic_int(m.group(1)), raw.strip(), opening.strip()))
    tail = body[position:].strip().strip(MARK)
    if tail:
        raise ValueError(f"{path.name}: {len(tail)} chars trail the last āyah mark: {tail[:80]!r}")

    ayahs: list[Ayah] = []
    surah, prev = 0, 1 << 30      # force the first āyah to open sūrah 1
    for n, text, opening in chunks:
        if n <= prev:            # numbering restarted -> next sūrah
            surah += 1
            prev = 0
        if n != prev + 1:
            raise ValueError(f"{path.name}: sūrah {surah} jumps from āyah {prev} to {n}")
        if opening:
            ayahs.append(Ayah(surah, 0, opening))
        ayahs.append(Ayah(surah, n, text))
        prev = n
    if surah != 114:
        raise ValueError(f"{path.name}: found {surah} sūrahs, expected 114")
    return ayahs


# --------------------------------------------------------------------------
# v2 CSV
# --------------------------------------------------------------------------

def load_csv(path: Path) -> tuple[list[Ayah], dict[tuple[int, int], dict]]:
    """Read a ``*Data_v2-*.csv`` release.

    The v2 files encode the āyah number as a single Arabic Presentation
    Forms-A codepoint (U+FC00 + n - 1).  It is stripped here and, since the
    row already carries ``aya_no``, used only as a consistency check.
    """
    ayahs: list[Ayah] = []
    meta: dict[tuple[int, int], dict] = {}
    with path.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            surah, ayah = int(row["sura_no"]), int(row["aya_no"])
            text = "".join(
                ch for ch in row["aya_text"]
                if chars.ayah_number_from_ligature(ch) is None
            )
            ayahs.append(Ayah(surah, ayah, strip_controls(text).strip()))
            meta[(surah, ayah)] = {
                "jozz": row.get("jozz", ""),
                "page": row.get("page", ""),
                "line_start": row.get("line_start", ""),
                "line_end": row.get("line_end", ""),
                "emlaey": row.get("aya_text_emlaey", ""),
            }
    return ayahs, meta


# --------------------------------------------------------------------------
# registry
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class SourceSpec:
    key: str
    name_en: str
    name_ar: str
    qiraah_en: str
    qiraah_ar: str
    primary_zip: str
    primary_member: str
    primary_kind: str          # "docx" | "csv"
    csv_zip: str | None = None
    csv_member: str | None = None
    #: Release years, used to decide which spelling wins when the two releases
    #: of one riwāyah disagree.  See ``RELEASE_POLICY``.
    primary_year: int = 2026
    csv_year: int = 2022
    #: The ``.ttf`` shipped beside the primary text, which is the only font
    #: guaranteed to draw it.  See :mod:`qurantext.fonts`.
    font_member: str = ""
    #: This package's slug in the KFGQPC archive, which is what makes its
    #: download URLs derivable.  Empty where the archive does not hold the
    #: package — which is the case for every primary ``.docx``.  See
    #: :data:`ARCHIVE` and ``docs/sources.md``.
    csv_slug: str = ""


#: **The one place this pipeline assumes anything about the sources.**
#:
#: When two files *for the same riwāyah* conflict, the later release is taken
#: as a correction of the earlier one, and the later one is the text.  The 2026
#: Ḥafṣ separates ``مَا لِيَ`` where the 2022 CSV joins it as ``مَالِيَ``; the
#: newer release is the publisher's own latest word on its own muṣḥaf, so it is
#: the one published here.
#:
#: The assumption is deliberately narrow and applies **only within a riwāyah**.
#: Nothing is inferred from one riwāyah about another, and no difference
#: between packages is treated as a mistake by either: fawāṣil, rasm and
#: spacing are editorial choices the publisher is entitled to make differently
#: in different muṣḥafs.  See the standing rule in ``docs/known-issues.md``.
#:
#: It also cannot discriminate for Dūrī, whose two packages are both from 2022.
#: There the differing word boundaries are recorded and left alone.
RELEASE_POLICY = ("within one riwāyah the later release is a correction; "
                  "across riwāyāt nothing is assumed")


#: Where the packages come from, and why that needs saying.
#:
#: ``qurancomplex.gov.sa`` answers requests from inside Saudi Arabia only: from
#: anywhere else DNS resolves and the connection then times out or is refused.
#: So the publisher's own URL, which is the citable one, is not the fetchable
#: one, and both are recorded rather than choosing between them.
#:
#: The archive keeps each published file byte-for-byte and records its official
#: URL and checksums; ``ARCHIVE_COMMIT`` is the revision these URLs were read
#: at, so the provenance is pinned rather than merely plausible.
ARCHIVE = "https://github.com/quran-ws/kfgqpc-resources"
ARCHIVE_COMMIT = "925b94346c2bd6a82df92a5ba3cfbec0bc63c512"
OFFICIAL_URL = "https://download.qurancomplex.gov.sa/resources_dev/{file}"
MIRROR_URL = "https://cdn.quran.ws/KFGQPC/resources/quran-dev/{slug}/{file}"
GEO_NOTE = ("The official host serves Saudi Arabia only; from elsewhere it "
            "times out. Use the mirror, which is the same bytes.")

#: Why six packages have an origin and seven do not.  Stated in the data, not
#: only in the prose, because a consumer reading the manifest is exactly the
#: person who needs to know a package cannot be re-fetched.
NO_ORIGIN_NOTE = (
    "No source URL is recorded for this package — not here, not in this "
    "repository's history, and not in the KFGQPC archive, which does not hold "
    "it. The file is verifiable against the SHA-256 above but cannot be "
    "obtained again or checked against the publisher. No URL is guessed: the "
    "archive's /quran-dev/ page does not serve this package. See "
    "docs/sources.md."
)


def origin(slug: str, package: str) -> dict:
    """The download record for one package, or an honest blank.

    A package the archive does not hold gets ``recorded: false`` and the reason,
    never an inferred URL — a plausible-but-wrong source is worse than an
    admitted gap, because it looks checked.
    """
    if not slug:
        return {"recorded": False, "note": NO_ORIGIN_NOTE}
    return {
        "recorded": True,
        "url": OFFICIAL_URL.format(file=package),
        "mirror": MIRROR_URL.format(slug=slug, file=package),
        "geo_restricted": GEO_NOTE,
        "archive": ARCHIVE,
        "archive_commit": ARCHIVE_COMMIT,
    }


REGISTRY: list[SourceSpec] = [
    SourceSpec("hafs", "Ḥafṣ", "حفص", "ʿĀṣim al-Kūfī", "عاصم الكوفي",
               "UthmanicHafs-v-3.0", "UthmanicHafs-v-3.0.docx", "docx",
               "UthmanicHafs_v2-0", "UthmanicHafs_v2-0 data/hafsData_v2-0.csv",
               csv_slug="uthmanic-hafs",
               font_member="UthmanicHafs-v-3.0.ttf"),
    SourceSpec("shubah", "Shuʿbah", "شعبة", "ʿĀṣim al-Kūfī", "عاصم الكوفي",
               "UthmanicShubah-v-3.0", "UthmanicShubah-v-3.0.docx", "docx",
               "UthmanicShuba_v2-0", "UthmanicShuba_v2-0 data/shubaData_v2-0.csv",
               csv_slug="uthmanic-shuba",
               font_member="UthmanicShubah-v-3.0.ttf"),
    SourceSpec("warsh", "Warsh", "ورش", "Nāfiʿ al-Madanī", "نافع المدني",
               "UthmanicWarsh-v-3.0", "UthmanicWarsh-v-3.0.docx", "docx",
               "UthmanicWarsh_v2-1", "UthmanicWarsh_v2-1 data/warshData_v2-1.csv",
               csv_slug="uthmanic-warsh",
               font_member="UthmanicWarsh-v-3.0.ttf"),
    SourceSpec("qalun", "Qālūn", "قالون", "Nāfiʿ al-Madanī", "نافع المدني",
               "UthmanicQaloun-v-3.0", "UthmanicQaloun-v-3.0.docx", "docx",
               "UthmanicQaloun_v2-1", "UthmanicQaloun_v2-1 data/QalounData_v2-1.csv",
               csv_slug="uthmanic-qaloun",
               font_member="UthmanicQaloun-v-3.0.ttf"),
    SourceSpec("duri", "Dūrī", "الدوري", "Abū ʿAmr al-Baṣrī", "أبو عمرو البصري",
               "UthmanicDouri_V20", "UthmanicDouri V20.docx", "docx",
               "UthmanicDouri_v2-0", "UthmanicDouri_v2-0 data/DouriData_v2-0.csv",
               csv_slug="uthmanic-douri",
               primary_year=2022, csv_year=2022, font_member="UthmanicDouri V20.ttf"),
    SourceSpec("susi", "Sūsī", "السوسي", "Abū ʿAmr al-Baṣrī", "أبو عمرو البصري",
               "UthmanicSousi-v-3.0", "UthmanicSousi-v-3.0.docx", "docx",
               "UthmanicSousi_v2-0", "UthmanicSousi_v2-0 data/SousiData_v2-0.csv",
               csv_slug="uthmanic-sousi",
               font_member="UthmanicSousi-v-3.0.ttf"),
    SourceSpec("bazzi", "Bazzī", "البزي", "Ibn Kathīr al-Makkī", "ابن كثير المكي",
               "UthmanicBazzi-v-3.0", "UthmanicBazzi-v-3.0.docx", "docx",
               font_member="UthmanicBazzi-v-3.0.ttf"),
]


def _extract(zip_name: str, member: str) -> Path:
    """Pull one member out of a data zip into ``work/raw`` and return its path."""
    dest = WORK / zip_name / member
    if dest.exists():
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(PACKAGES / f"{zip_name}.zip") as z:
        with z.open(member) as src, dest.open("wb") as out:
            out.write(src.read())
    return dest


def load_all() -> list[Riwayah]:
    riwayahs = []
    for spec in REGISTRY:
        path = _extract(spec.primary_zip, spec.primary_member)
        if spec.primary_kind == "docx":
            ayahs = load_docx(path)
            source = f"{spec.primary_zip}.zip :: {spec.primary_member}"
        else:
            ayahs, _ = load_csv(path)
            source = f"{spec.primary_zip}.zip :: {spec.primary_member}"

        r = Riwayah(spec.key, spec.name_en, spec.name_ar, spec.qiraah_en,
                   spec.qiraah_ar, source, ayahs)
        r.release_year = spec.primary_year
        r.spec = spec
        if spec.primary_kind == "docx":
            from .layout import word_places
            r.places = word_places(path)

        if spec.csv_zip and spec.csv_member:
            csv_path = _extract(spec.csv_zip, spec.csv_member)
            csv_ayahs, meta = load_csv(csv_path)
            r.meta = meta
            r.crosscheck = {(a.surah, a.ayah): a.text for a in csv_ayahs}
            r.crosscheck_source = f"{spec.csv_zip}.zip :: {spec.csv_member}"
            r.crosscheck_year = spec.csv_year
        riwayahs.append(r)
    return riwayahs
