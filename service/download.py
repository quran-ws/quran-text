"""Turn one download request into a file.

    options = Options(edition="warsh", format="json", markers="sign")
    file = build(data, options, url="https://…/download?…")
    file.body, file.filename, file.media_type, file.sha256

Everything is read through ``quran_text``: a request is a :class:`Span` of
one :class:`Mushaf`, the records are its āyāt or its words, and a format is a
function from records to text.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
from dataclasses import dataclass, field
from datetime import date
from xml.sax.saxutils import quoteattr

from dataset import Dataset
from quran_text import Ayah, Mushaf, Span, Word, ayah_mark, fold

PROJECT_URL = "https://github.com/quran-ws/quran-text"
LICENSE_NOTE = ("The text is the King Fahd Glorious Qur'an Printing Complex's (KFGQPC); "
                "redistribution is subject to their terms.")

TEXT_FORMS = ("rasm_uthmani", "rasm_imlai", "plain")
MARKER_STYLES = ("none", "sign", "brackets", "latin")
FORMATS = ("txt", "json", "csv", "xml", "sql", "md")
GRANULARITIES = ("ayah", "word")
SIGN_LAYOUTS = ("columns", "attached")
SIGN_KINDS = ("waqf", "sajdah", "sajdah_line", "division", "sah", "raised_dot")
FIELDS = ("surah", "ayah", "position", "number", "page", "line", "juz", "hafs")
DEFAULT_FIELDS = {"ayah": ("surah", "ayah"), "word": ("surah", "ayah", "position", "number")}


class BadRequest(ValueError):
    """A request that cannot be served, with a message meant for the caller."""


@dataclass
class Options:
    edition: str = "hafs"
    text: str = "rasm_uthmani"
    markers: str = "none"
    waqf: bool = True
    sajdah: bool = True
    sajdah_line: bool = True
    division: bool = True
    sah: bool = True
    raised_dot: bool = True
    lines: bool = False
    pages: bool = False
    fields: tuple[str, ...] | None = None
    surah: str | None = None
    juz: int | None = None
    page: str | None = None
    ayah: str | None = None
    by: str = "ayah"
    signs: str = "columns"
    format: str = "txt"
    prefix: bool = True
    nested: bool = False
    header: bool = True
    limit: int | None = None

    def __post_init__(self):
        # `text` is a comma list: every form asked for becomes a column, the
        # first one is `text` itself, so a single form reads as before.
        self.forms = tuple(dict.fromkeys(t.strip() for t in self.text.split(",") if t.strip())) or ("rasm_uthmani",)
        for form in self.forms:
            _one_of("text", form, TEXT_FORMS)
        self.text = ",".join(self.forms)
        _one_of("markers", self.markers, MARKER_STYLES)
        _one_of("by", self.by, GRANULARITIES)
        _one_of("signs", self.signs, SIGN_LAYOUTS)
        _one_of("format", self.format, FORMATS)
        if self.fields is None:
            self.fields = DEFAULT_FIELDS[self.by]
        for f in self.fields:
            _one_of("fields", f, FIELDS)
        scopes = [k for k in ("surah", "juz", "page", "ayah") if getattr(self, k) is not None]
        if len(scopes) > 1:
            raise BadRequest(f"give one scope, not {', '.join(scopes)}")
        if self.limit is not None and self.limit < 1:
            raise BadRequest("limit must be at least 1")

    @property
    def extra_forms(self) -> tuple[str, ...]:
        """The text forms after the first, each its own column."""
        return self.forms[1:]

    @property
    def mark_kinds(self) -> frozenset:
        return frozenset(k for k in SIGN_KINDS if getattr(self, k))

    @property
    def scope(self) -> str:
        for k in ("surah", "juz", "page", "ayah"):
            v = getattr(self, k)
            if v is not None:
                return f"{k} {v}"
        return "whole Qurʾān"

    def describe(self) -> dict:
        """The options as the file header states them."""
        return {
            "edition": self.edition, "text": " ".join(self.forms), "markers": self.markers,
            "marks": sorted(self.mark_kinds), "lines": self.lines, "pages": self.pages,
            "fields": list(self.fields), "scope": self.scope, "by": self.by,
            "signs": self.signs if self.by == "word" else None,
            "format": self.format,
        }


@dataclass
class File:
    body: bytes
    filename: str
    media_type: str
    sha256: str = field(init=False)

    def __post_init__(self):
        self.sha256 = hashlib.sha256(self.body).hexdigest()


# --- the selection ------------------------------------------------------------

def select(m: Mushaf, o: Options) -> Span:
    """The run of words a request asks for, validated against this edition."""
    try:
        if o.surah is not None:
            a, b = _range(o.surah, "surah")
            _check(1 <= a <= b <= 114, f"surah {o.surah}: there are 114 sūrahs")
            return m.span(m.surah(a).start, m.surah(b).end)
        if o.juz is not None:
            if not m.has("juz"):
                raise BadRequest(m._absent("juz"))
            _check(1 <= o.juz <= m.juz_count, f"juz {o.juz}: there are {m.juz_count}")
            j = m.juz(o.juz)
            return m.span(j.start, j.end)
        if o.page is not None:
            a, b = _range(o.page, "page")
            _check(1 <= a <= b <= m.page_count,
                   f"page {o.page}: {m.name_en} has {m.page_count} pages")
            return m.span(m.page(a).start, m.page(b).end)
        if o.ayah is not None:
            first, last = _ayah_range(m, o.ayah)
            _check(first.start <= last.start, f"ayah {o.ayah}: the range runs backwards")
            return m.span(first.start, last.end)
    except IndexError as e:               # raised by the library with a clear message
        raise BadRequest(str(e)) from e
    return m.all


def _ayah_range(m: Mushaf, spec: str) -> tuple[Ayah, Ayah]:
    parts = spec.replace("–", "-").split("-")
    if len(parts) > 2 or not all(parts):
        raise BadRequest(f"ayah {spec!r}: write 2:255 or 2:255-2:286")
    refs = [_ayah_key(m, p) for p in parts]
    return refs[0], refs[-1]


def _ayah_key(m: Mushaf, text: str) -> Ayah:
    match = re.fullmatch(r"(\d+):(\d+)", text.strip())
    if not match:
        raise BadRequest(f"ayah {text!r}: write surah:ayah, e.g. 2:255")
    surah, ayah = int(match.group(1)), int(match.group(2))
    _check(1 <= surah <= 114, f"surah {surah}: there are 114 sūrahs")
    try:
        return m.ayah(surah, ayah)
    except IndexError as e:         # the library names the edition's own count
        raise BadRequest(str(e)) from e


def _range(spec: str, what: str) -> tuple[int, int]:
    parts = spec.replace("–", "-").split("-")
    if len(parts) > 2 or not all(p.strip().isdigit() for p in parts):
        raise BadRequest(f"{what} {spec!r}: write a number or a range like 1-3")
    a, b = int(parts[0]), int(parts[-1])
    _check(a <= b, f"{what} {spec}: the range runs backwards")
    return a, b


def _check(ok: bool, message: str):
    if not ok:
        raise BadRequest(message)


def _one_of(name: str, value, allowed):
    if value not in allowed:
        raise BadRequest(f"{name}={value!r}: one of {', '.join(allowed)}")


# --- records ------------------------------------------------------------------

def units(m: Mushaf, span: Span) -> list[tuple[Span, int, int]]:
    """``(span, surah, ayah)`` per āyah in the selection; the unnumbered basmalah
    of al-Fātiḥah comes first as āyah 0 where the edition prints it so."""
    out = []
    basmalah = m.surah(1).basmalah
    if basmalah is not None and span.start <= basmalah.start:
        out.append((basmalah, 1, 0))
    for a in span.ayahs:
        out.append((a, a.surah.number, a.number))
    return out


def word_form(w: Word, text: str) -> str:
    if text == "rasm_imlai":
        return w.rasm_imlai if w.rasm_imlai is not None else w.text
    if text == "plain":
        return fold(w.text)
    return w.text


def render(span: Span, o: Options, form: str) -> str:
    """The words of one span as the file prints them, in one text form."""
    if form == "rasm_uthmani":
        return span.render(marks=o.mark_kinds, lines=o.lines)
    m = span.mushaf
    line_starts = set(m._doc.get("line_starts") or []) if o.lines else set()
    out = []
    for w in span:
        if out:
            out.append("\n" if w.position in line_starts else " ")
        before = "".join(mk.sign + " " for mk in w.marks
                         if mk.side == "before" and mk.kind in o.mark_kinds)
        after = "".join(mk.sign for mk in w.marks
                        if mk.side == "after" and mk.kind in o.mark_kinds)
        out.append(before + word_form(w, form) + after)
    return "".join(out)


def marker(number: int, style: str) -> str:
    if style == "none" or number == 0:
        return ""
    if style == "sign":
        return " " + ayah_mark(number)
    if style == "brackets":
        return " ﴿" + ayah_mark(number)[1:] + "﴾"
    return f" ({number})"


def records(data: Dataset, m: Mushaf, span: Span, o: Options) -> list[dict]:
    if o.by == "word":
        return _word_records(data, m, span, o)
    out = []
    for unit, surah, ayah in units(m, span):
        r = {"surah": surah, "ayah": ayah}
        r["text"] = render(unit, o, o.forms[0]) + marker(ayah, o.markers)
        for form in o.extra_forms:
            r[form] = render(unit, o, form) + marker(ayah, o.markers)
        if "page" in o.fields:
            r["page"] = unit.page.number
        if "line" in o.fields:
            line = m.line_at(unit.start)
            r["line"] = line.number if line else None
        if "juz" in o.fields:
            r["juz"] = unit.juz.number if unit.juz else None
        if "hafs" in o.fields:
            r.update(_hafs_ref(data, m, surah, ayah))
        out.append(r)
        if o.limit and len(out) >= o.limit:
            break
    return out


def _word_records(data: Dataset, m: Mushaf, span: Span, o: Options) -> list[dict]:
    out = []
    for w in span:
        a = w.ayah
        surah, ayah = w.surah.number, (a.number if a else 0)
        r = {"surah": surah, "ayah": ayah, "position": w.index or 0}
        r["number"] = w.number
        r["text"] = _word_text(w, o.forms[0], o)
        for form in o.extra_forms:
            r[form] = _word_text(w, form, o)
        if o.signs == "columns":
            for kind in SIGN_KINDS:
                if kind in o.mark_kinds:
                    r[kind] = "".join(mk.sign for mk in w.marks if mk.kind == kind)
        if "page" in o.fields:
            r["page"] = w.page.number
        if "line" in o.fields:
            r["line"] = w.line.number if w.line else None
        if "juz" in o.fields:
            r["juz"] = w.juz.number if w.juz else None
        if "hafs" in o.fields:
            r.update(_hafs_ref(data, m, surah, ayah))
        out.append(r)
        if o.limit and len(out) >= o.limit:
            break
    return out


def _word_text(w: Word, form: str, o: Options) -> str:
    """One word in one form; with ``signs=attached`` the signs ride on the word
    as the muṣḥaf prints them (never on the plain form, which is for matching)."""
    text = word_form(w, form)
    if o.signs != "attached" or form == "plain":
        return text
    before = "".join(mk.sign + " " for mk in w.marks if mk.side == "before" and mk.kind in o.mark_kinds)
    after = "".join(mk.sign for mk in w.marks if mk.side == "after" and mk.kind in o.mark_kinds)
    return before + text + after


def _hafs_ref(data: Dataset, m: Mushaf, surah: int, ayah: int) -> dict:
    refs = data.kufi_refs(m.key, surah, ayah)
    if not refs:
        return {"hafs": None, "hafs_relation": None}
    keys = [f"{r['surah']}:{r['ayah']}" for r in refs]
    return {"hafs": keys[0] if len(keys) == 1 else f"{keys[0]}-{refs[-1]['ayah']}",
            "hafs_relation": refs[0]["relation"]}


def columns(o: Options) -> list[str]:
    """The record keys in output order."""
    cols = ["surah", "ayah"]
    if o.by == "word":
        cols += ["position", "number"]
    cols.append("text")
    cols += o.extra_forms
    if o.by == "word" and o.signs == "columns":
        cols += [k for k in SIGN_KINDS if k in o.mark_kinds]
    cols += [f for f in ("page", "line", "juz") if f in o.fields]
    if "hafs" in o.fields:
        cols += ["hafs", "hafs_relation"]
    return cols


# --- the file ------------------------------------------------------------------

def build(data: Dataset, o: Options, url: str = "") -> File:
    m = data.mushaf(o.edition)
    if "rasm_imlai" in o.forms and not m.has("rasm_imlai"):
        raise BadRequest(f"text=rasm_imlai: {m._absent('rasm_imlai')}; imlāʾī is published for Ḥafṣ only")
    if "juz" in o.fields and not m.has("juz"):
        raise BadRequest(m._absent("juz"))
    span = select(m, o)
    rows = records(data, m, span, o)
    meta = provenance(m, o, url, len(rows))
    body = FORMATTERS[o.format](rows, meta, o, m)
    return File(body.encode("utf-8"), filename(m, o), MEDIA_TYPES[o.format])


def provenance(m: Mushaf, o: Options, url: str, count: int) -> dict:
    src = m.provenance["text"]
    return {
        "edition": {"key": m.key, "name_en": m.name_en, "name_ar": m.name_ar,
                    "qiraah_en": m.qiraah_en, "counting_system": m.counting_system,
                    "counting_system_en": m.counting.get("system_name_en", m.counting_system),
                    "counting_system_associated_with_qari": m.counting_system_associated_with_qari,
                    "ayah_count": m.ayah_count},
        "source": {"package": src["package"], "member": src["member"],
                   "release_year": src.get("release_year"), "sha256": src["sha256"]},
        "options": o.describe(),
        "records": count,
        "limited": bool(o.limit and count >= o.limit),
        "generated": date.today().isoformat(),
        "url": url,
        "project": PROJECT_URL,
        "license": LICENSE_NOTE,
    }


def header_lines(meta: dict) -> list[str]:
    e, s, o = meta["edition"], meta["source"], meta["options"]
    lines = [
        f"quran-text — {e['name_en']} ({e['name_ar']}), {e['qiraah_en']}, "
        f"{e['counting_system_en']} count, {e['ayah_count']} āyāt",
        f"source: KFGQPC {s['package']} :: {s['member']}  sha256 {s['sha256']}",
        f"text: {o['text']} | marks: {' '.join(o['marks']) or 'none'} | ayah markers: {o['markers']}"
        f" | scope: {o['scope']} | by: {o['by']}"
        + (f" | signs: {o['signs']}" if o.get("signs") else "")
        + (" | lines" if o["lines"] else "") + (" | pages" if o["pages"] else ""),
        f"generated: {meta['generated']}" + (f" from {meta['url']}" if meta["url"] else ""),
        f"{meta['license']} {meta['project']}",
    ]
    if meta["limited"]:
        lines.append(f"PREVIEW: limited to the first {meta['records']} records")
    return lines


def filename(m: Mushaf, o: Options) -> str:
    parts = ["quran", m.key, *o.forms]
    for k in ("surah", "juz", "page", "ayah"):
        v = getattr(o, k)
        if v is not None:
            parts.append(f"{k}{str(v).replace(':', '_').replace('–', '-')}")
    if o.by == "word":
        parts.append("words")
    return "-".join(parts) + "." + o.format


# --- formats ------------------------------------------------------------------

def _new_page(prev: dict | None, r: dict, o: Options, m: Mushaf) -> int | None:
    """The page number when ``pages`` is on and this record starts a new page."""
    if not o.pages:
        return None
    if "page" not in r:
        r["page"] = (m.ayah(r["surah"], r["ayah"]).page.number if r["ayah"]
                     else m.surah(r["surah"]).page.number)
    return r["page"] if prev is None or prev["page"] != r["page"] else None


def as_txt(rows: list[dict], meta: dict, o: Options, m: Mushaf) -> str:
    out = []
    if o.header:
        out += ["# " + line for line in header_lines(meta)] + [""]
    prev = None
    for r in rows:
        page = _new_page(prev, r, o, m)
        if page is not None:
            out.append(("" if prev is None else "\n") + f"# page {page}")
        line = "|".join([r["text"], *(r[f] for f in o.extra_forms)])
        if o.prefix:
            key = f"{r['surah']}|{r['ayah']}|"
            if o.by == "word":
                key += f"{r['position']}|"
            line = key + line
        out.append(line)
        prev = r
    return "\n".join(out) + "\n"


def as_md(rows: list[dict], meta: dict, o: Options, m: Mushaf) -> str:
    out = []
    if o.header:
        out += ["> " + line for line in header_lines(meta)] + [""]
    prev = None
    for r in rows:
        if prev is None or prev["surah"] != r["surah"]:
            s = m.surah(r["surah"])
            out += [f"## {s.number}. {s.name_ar} — {s.name_en}", ""]
        page = _new_page(prev, r, o, m)
        if page is not None:
            out += [f"*page {page}*", ""]
        label = f"{r['surah']}:{r['ayah']}" + (f"/{r['position']}" if o.by == "word" else "")
        # plain Markdown: the text, then its reference as a code span; one
        # paragraph per record so a viewer lays the Arabic out right-to-left
        out += [f"{r['text']} `{label}`", ""]
        for form in o.extra_forms:
            out += [f"{r[form]} `{form}`", ""]
        prev = r
    return "\n".join(out) + "\n"


def as_json(rows: list[dict], meta: dict, o: Options, m: Mushaf) -> str:
    cols = columns(o)
    clean = [{k: r.get(k) for k in cols} for r in rows]
    doc: dict = {"meta": meta} if o.header else {}
    if o.nested:
        surahs: list[dict] = []
        for r in clean:
            if not surahs or surahs[-1]["number"] != r["surah"]:
                s = m.surah(r["surah"])
                surahs.append({"number": s.number, "name_ar": s.name_ar,
                              "name_en": s.name_en, "ayahs": []})
            surahs[-1]["ayahs"].append({k: v for k, v in r.items() if k != "surah"})
        doc["surahs"] = surahs
    else:
        doc["words" if o.by == "word" else "ayahs"] = clean
    return json.dumps(doc, ensure_ascii=False, indent=1) + "\n"


def as_csv(rows: list[dict], meta: dict, o: Options, m: Mushaf) -> str:
    buf = io.StringIO()
    if o.header:
        buf.write("".join("# " + line + "\n" for line in header_lines(meta)))
    cols = columns(o)
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(cols)
    for r in rows:
        w.writerow(["" if r.get(k) is None else r.get(k) for k in cols])
    return buf.getvalue()


def as_xml(rows: list[dict], meta: dict, o: Options, m: Mushaf) -> str:
    """Tanzil's element names — ``<surah index name><ayah index text/>`` — so a
    Tanzil reader can be pointed here unchanged; extra columns are attributes."""
    e, s = meta["edition"], meta["source"]
    out = ['<?xml version="1.0" encoding="UTF-8"?>']
    if o.header:
        out.append("<!--\n" + "\n".join("  " + line.replace("--", "—") for line in header_lines(meta)) + "\n-->")
    out.append(f'<quran edition={quoteattr(e["key"])} text={quoteattr(o.forms[0])} '
               f'source={quoteattr(s["package"])} sha256={quoteattr(s["sha256"])}>')
    extra = [c for c in columns(o) if c not in ("surah", "ayah", "text")]
    current = None
    for r in rows:
        if r["surah"] != current:
            if current is not None:
                out.append("</surah>")
            surah = m.surah(r["surah"])
            out.append(f'<surah index="{surah.number}" name={quoteattr(surah.name_ar)}>')
            current = r["surah"]
        attrs = [f'index="{r["ayah"]}"'] + [
            f"{c}={quoteattr(str(r[c]))}" for c in extra if r.get(c) is not None]
        out.append(f'<ayah {" ".join(attrs)} text={quoteattr(r["text"])}/>')
    if current is not None:
        out.append("</surah>")
    out.append("</quran>")
    return "\n".join(out) + "\n"


_SQL_TYPES = {"text": "TEXT", "waqf": "TEXT", "sajdah": "TEXT", "sajdah_line": "TEXT",
              "division": "TEXT", "sah": "TEXT", "raised_dot": "TEXT",
              "hafs": "VARCHAR(16)", "hafs_relation": "VARCHAR(16)",
              **{form: "TEXT" for form in TEXT_FORMS}}


def as_sql(rows: list[dict], meta: dict, o: Options, m: Mushaf) -> str:
    """One ``quran`` table; MySQL and SQLite both read it."""
    cols = columns(o)
    out = []
    if o.header:
        out += ["-- " + line for line in header_lines(meta)]
    out.append("CREATE TABLE quran (")
    out.append("  id INTEGER PRIMARY KEY,")
    out.append(",\n".join(f"  {c} {_SQL_TYPES.get(c, 'INTEGER')}" for c in cols))
    out.append(");")
    for i, r in enumerate(rows, 1):
        values = [str(i)] + [_sql(r.get(c)) for c in cols]
        out.append(f"INSERT INTO quran (id, {', '.join(cols)}) VALUES ({', '.join(values)});")
    return "\n".join(out) + "\n"


def _sql(v) -> str:
    if v is None:
        return "NULL"
    if isinstance(v, int):
        return str(v)
    return "'" + str(v).replace("'", "''") + "'"


FORMATTERS = {"txt": as_txt, "json": as_json, "csv": as_csv,
              "xml": as_xml, "sql": as_sql, "md": as_md}
MEDIA_TYPES = {"txt": "text/plain; charset=utf-8", "json": "application/json; charset=utf-8",
               "csv": "text/csv; charset=utf-8", "xml": "application/xml; charset=utf-8",
               "sql": "application/sql; charset=utf-8", "md": "text/markdown; charset=utf-8"}
