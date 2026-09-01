"""Loaders for the KFGQPC packages shipped in ``data/``.

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
from pathlib import Path

from . import chars
from .normalize import strip_controls

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

DATA = Path("data")
WORK = Path("work/raw")


@dataclass(frozen=True)
class Ayah:
    sura: int
    aya: int
    text: str


@dataclass
class Riwaya:
    key: str
    name_en: str
    name_ar: str
    qari_en: str
    qari_ar: str
    counting: str            # āyah-numbering tradition
    source: str              # provenance of ``ayat``
    ayat: list[Ayah] = field(default_factory=list)
    #: (sura, aya) -> {jozz, page, line_start, line_end}, from the v2 CSVs.
    meta: dict[tuple[int, int], dict] = field(default_factory=dict)
    #: (sura, aya) -> text, from the *other* release of the same riwāyah.
    crosscheck: dict[tuple[int, int], str] = field(default_factory=dict)
    crosscheck_source: str = ""


# --------------------------------------------------------------------------
# .docx
# --------------------------------------------------------------------------

def docx_paragraphs(path: Path) -> list[str]:
    """Text of every non-empty paragraph, in document order."""
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    out = []
    for para in root.iter(W + "p"):
        # Only <w:t> carries literal text; walking the element tree (rather
        # than regexing the XML) keeps <w:pPr> attribute noise out.
        text = "".join(node.text or "" for node in para.iter(W + "t"))
        if text.strip():
            out.append(text)
    return out


_SURA_HEAD = re.compile(r"^\s*سُ?ورَ?ةُ?\s")
_AR_NUM = "".join(chars.ARABIC_DIGITS)

# v3.0 marks an āyah with NBSP + U+06DD + digits; the 2022 Dūrī release omits
# the U+06DD and leaves only NBSP + digits.
_AYAH_MARK = re.compile(rf"[  ]?۝?([{_AR_NUM}]+)")

#: The basmalah, reduced to letters, as it appears across all seven releases.
_BASMALAH_RASM = "بسماللهالرحمنالرحيم"


def _arabic_int(s: str) -> int:
    return int("".join(chars.ARABIC_DIGITS[c] for c in s))


def _is_heading(para: str) -> bool:
    return bool(_SURA_HEAD.match(para)) and not re.search(rf"[{_AR_NUM}]", para)


def _is_bare_basmalah(para: str) -> bool:
    """A basmalah printed as a sūrah opening rather than counted as an āyah."""
    if re.search(rf"[{_AR_NUM}]", para):
        return False          # numbered: it *is* āyah 1 (Kufi/Makki Al-Fātiḥah)
    from .normalize import rasm
    return rasm(para).replace(" ", "") == _BASMALAH_RASM


def load_docx(path: Path) -> list[Ayah]:
    """Split a KFGQPC Word mushaf into āyāt.

    Sūrah boundaries are taken from resets in the āyah numbering, not from the
    headings: the v3.0 Qālūn document is missing the heading for Al-Baqarah, so
    heading-driven segmentation silently shifts every sūrah after it by one.
    Numbering resets are intrinsic to the text and let us assert 114 sūrahs of
    contiguous 1..N āyāt at the end.
    """
    body = " ".join(
        para for para in docx_paragraphs(path)
        if not _is_heading(para) and not _is_bare_basmalah(para)
    )
    body = strip_controls(body)

    numbered: list[tuple[int, str]] = []
    pos = 0
    for m in _AYAH_MARK.finditer(body):
        numbered.append((_arabic_int(m.group(1)), body[pos:m.start()].strip()))
        pos = m.end()
    tail = body[pos:].strip()
    if tail:
        raise ValueError(f"{path.name}: {len(tail)} chars trail the last āyah mark: {tail[:80]!r}")

    ayat: list[Ayah] = []
    sura = 0
    prev = 1 << 30            # force the first āyah to open sūrah 1
    for n, text in numbered:
        if n <= prev:            # numbering restarted -> next sūrah
            sura += 1
            prev = 0
        if n != prev + 1:
            raise ValueError(f"{path.name}: sūrah {sura} jumps from āyah {prev} to {n}")
        ayat.append(Ayah(sura, n, text))
        prev = n
    if sura != 114:
        raise ValueError(f"{path.name}: found {sura} sūrahs, expected 114")
    return ayat


# --------------------------------------------------------------------------
# v2 CSV
# --------------------------------------------------------------------------

def load_csv(path: Path) -> tuple[list[Ayah], dict[tuple[int, int], dict]]:
    """Read a ``*Data_v2-*.csv`` release.

    The v2 files encode the āyah number as a single Arabic Presentation
    Forms-A codepoint (U+FC00 + n - 1).  It is stripped here and, since the
    row already carries ``aya_no``, used only as a consistency check.
    """
    ayat: list[Ayah] = []
    meta: dict[tuple[int, int], dict] = {}
    with path.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            sura, aya = int(row["sura_no"]), int(row["aya_no"])
            text = "".join(
                ch for ch in row["aya_text"]
                if chars.ayah_number_from_ligature(ch) is None
            )
            ayat.append(Ayah(sura, aya, strip_controls(text).strip()))
            meta[(sura, aya)] = {
                "jozz": row.get("jozz", ""),
                "page": row.get("page", ""),
                "line_start": row.get("line_start", ""),
                "line_end": row.get("line_end", ""),
                "emlaey": row.get("aya_text_emlaey", ""),
            }
    return ayat, meta


# --------------------------------------------------------------------------
# registry
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class SourceSpec:
    key: str
    name_en: str
    name_ar: str
    qari_en: str
    qari_ar: str
    counting: str
    primary_zip: str
    primary_member: str
    primary_kind: str          # "docx" | "csv"
    csv_zip: str | None = None
    csv_member: str | None = None


REGISTRY: list[SourceSpec] = [
    SourceSpec("hafs", "Ḥafṣ", "حفص", "ʿĀṣim al-Kūfī", "عاصم الكوفي", "kufi",
               "UthmanicHafs-v-3.0", "UthmanicHafs-v-3.0.docx", "docx",
               "UthmanicHafs_v2-0", "UthmanicHafs_v2-0 data/hafsData_v2-0.csv"),
    SourceSpec("shuba", "Shuʿbah", "شعبة", "ʿĀṣim al-Kūfī", "عاصم الكوفي", "kufi",
               "UthmanicShubah-v-3.0", "UthmanicShubah-v-3.0.docx", "docx",
               "UthmanicShuba_v2-0", "UthmanicShuba_v2-0 data/shubaData_v2-0.csv"),
    SourceSpec("warsh", "Warsh", "ورش", "Nāfiʿ al-Madanī", "نافع المدني", "madani",
               "UthmanicWarsh-v-3.0", "UthmanicWarsh-v-3.0.docx", "docx",
               "UthmanicWarsh_v2-1", "UthmanicWarsh_v2-1 data/warshData_v2-1.csv"),
    SourceSpec("qaloun", "Qālūn", "قالون", "Nāfiʿ al-Madanī", "نافع المدني", "madani",
               "UthmanicQaloun-v-3.0", "UthmanicQaloun-v-3.0.docx", "docx",
               "UthmanicQaloun_v2-1", "UthmanicQaloun_v2-1 data/QalounData_v2-1.csv"),
    SourceSpec("douri", "Dūrī", "الدوري", "Abū ʿAmr al-Baṣrī", "أبو عمرو البصري", "basri",
               "UthmanicDouri_V20", "UthmanicDouri V20.docx", "docx",
               "UthmanicDouri_v2-0", "UthmanicDouri_v2-0 data/DouriData_v2-0.csv"),
    SourceSpec("sousi", "Sūsī", "السوسي", "Abū ʿAmr al-Baṣrī", "أبو عمرو البصري", "basri",
               "UthmanicSousi-v-3.0", "UthmanicSousi-v-3.0.docx", "docx",
               "UthmanicSousi_v2-0", "UthmanicSousi_v2-0 data/SousiData_v2-0.csv"),
    SourceSpec("bazzi", "Bazzī", "البزي", "Ibn Kathīr al-Makkī", "ابن كثير المكي", "makki",
               "UthmanicBazzi-v-3.0", "UthmanicBazzi-v-3.0.docx", "docx"),
]


def _extract(zip_name: str, member: str) -> Path:
    """Pull one member out of a data zip into ``work/raw`` and return its path."""
    dest = WORK / zip_name / member
    if dest.exists():
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(DATA / f"{zip_name}.zip") as z:
        with z.open(member) as src, dest.open("wb") as out:
            out.write(src.read())
    return dest


def load_all() -> list[Riwaya]:
    riwayat = []
    for spec in REGISTRY:
        path = _extract(spec.primary_zip, spec.primary_member)
        if spec.primary_kind == "docx":
            ayat = load_docx(path)
            source = f"{spec.primary_zip}.zip :: {spec.primary_member}"
        else:
            ayat, _ = load_csv(path)
            source = f"{spec.primary_zip}.zip :: {spec.primary_member}"

        r = Riwaya(spec.key, spec.name_en, spec.name_ar, spec.qari_en,
                   spec.qari_ar, spec.counting, source, ayat)

        if spec.csv_zip and spec.csv_member:
            csv_path = _extract(spec.csv_zip, spec.csv_member)
            csv_ayat, meta = load_csv(csv_path)
            r.meta = meta
            r.crosscheck = {(a.sura, a.aya): a.text for a in csv_ayat}
            r.crosscheck_source = f"{spec.csv_zip}.zip :: {spec.csv_member}"
        riwayat.append(r)
    return riwayat
