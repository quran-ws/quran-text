"""The mapping dataset: every āyah, or every word, of one riwāyah with its
counterpart in the others.

Built on ``Ayah.to`` and ``Word.to`` of ``quran_text`` — the shared word
numbering — so it works between any two of the seven. It follows the same
conventions as ``/download``: a scope, ``by=ayah|word``, every format, a
provenance header, and a URL that is the file.
"""

from __future__ import annotations

import csv
import io
import json
from dataclasses import dataclass, field
from datetime import date
from xml.sax.saxutils import quoteattr

from dataset import Dataset, EDITIONS
from download import (FORMATS, GRANULARITIES, LICENSE_NOTE, MEDIA_TYPES,
                      PROJECT_URL, BadRequest, File, Options, _one_of, select,
                      units, word_form, TEXT_FORMS)
from quran_text import Mushaf


@dataclass
class MapOptions:
    source: str = "hafs"
    to: tuple[str, ...] = ()
    surah: str | None = None
    juz: int | None = None
    page: str | None = None
    ayah: str | None = None
    by: str = "ayah"
    text: str = "rasm_uthmani"
    format: str = "json"
    header: bool = True
    limit: int | None = None

    def __post_init__(self):
        if self.source not in EDITIONS:
            raise BadRequest(f"no riwāyah {self.source!r}; riwāyāt are {', '.join(EDITIONS)}")
        self.to = tuple(dict.fromkeys(self.to)) or tuple(k for k in EDITIONS if k != self.source)
        for t in self.to:
            if t not in EDITIONS:
                raise BadRequest(f"no riwāyah {t!r}; riwāyāt are {', '.join(EDITIONS)}")
            if t == self.source:
                raise BadRequest(f"to={t}: that is the riwāyah being mapped from")
        _one_of("by", self.by, GRANULARITIES)
        _one_of("text", self.text, TEXT_FORMS)
        _one_of("format", self.format, FORMATS)
        if self.limit is not None and self.limit < 1:
            raise BadRequest("limit must be at least 1")

    def scope_options(self) -> Options:
        """The scope, expressed as download options so ``select`` validates it."""
        return Options(edition=self.source, surah=self.surah, juz=self.juz, page=self.page,
                       ayah=self.ayah, text=self.text)

    @property
    def scope(self) -> str:
        return self.scope_options().scope


def columns(o: MapOptions) -> list[str]:
    cols = ["surah", "ayah"]
    if o.by == "word":
        cols += ["position", "number", "text"]
    else:
        cols += ["first_number", "last_number"]
    for t in o.to:
        cols += [f"{t}_ayah", f"{t}_relation"] if o.by == "ayah" else [f"{t}_word", f"{t}_text"]
    return cols


def records(data: Dataset, o: MapOptions) -> list[dict]:
    m = data.mushaf(o.source)
    targets = {t: data.mushaf(t) for t in o.to}
    span = select(m, o.scope_options())
    out: list[dict] = []
    if o.by == "word":
        for w in span:
            a = w.ayah
            r = {"surah": w.surah.number, "ayah": a.number if a else 0, "position": w.index or 0,
                 "number": w.number, "text": word_form(w, o.text)}
            for t, tm in targets.items():
                x = w.to(tm)
                r[f"{t}_word"] = None if x is None else f"{x.surah.number}:{x.ayah.number if x.ayah else 0}:{x.index or 0}"
                r[f"{t}_text"] = None if x is None else word_form(x, o.text)
            out.append(r)
            if o.limit and len(out) >= o.limit:
                break
        return out
    for unit, surah, ayah in units(m, span):
        if ayah == 0:
            continue                      # the unnumbered basmalah is no āyah to map
        numbers = unit.numbers
        r = {"surah": surah, "ayah": ayah, "first_number": min(numbers), "last_number": max(numbers)}
        for t, tm in targets.items():
            match = unit.to(tm)
            r[f"{t}_ayah"] = match.key or None
            r[f"{t}_relation"] = match.relation
        out.append(r)
        if o.limit and len(out) >= o.limit:
            break
    return out


def build(data: Dataset, o: MapOptions, url: str = "") -> File:
    m = data.mushaf(o.source)
    rows = records(data, o)
    meta = {
        "from": {"key": m.key, "name_en": m.name_en, "name_ar": m.name_ar,
                 "counting_system": m.counting_system, "ayah_count": m.ayah_count},
        "to": list(o.to),
        "options": {"by": o.by, "scope": o.scope, "text": o.text, "format": o.format},
        "columns": columns(o),
        "note": ("Computed from the shared word numbering: the same number is the same word "
                 "in every riwāyah. relation: same, merged, split, shifted, unnumbered, missing."),
        "records": len(rows),
        "limited": bool(o.limit and len(rows) >= o.limit),
        "generated": date.today().isoformat(),
        "url": url,
        "project": PROJECT_URL,
        "license": LICENSE_NOTE,
    }
    body = FORMATTERS[o.format](rows, meta, o)
    name = f"quran-map-{m.key}-to-{'-'.join(o.to)}" + (f"-{o.scope.replace(' ', '').replace(':', '_')}" if o.scope != "whole Qurʾān" else "") + ("-words" if o.by == "word" else "") + "." + o.format
    return File(body.encode("utf-8"), name, MEDIA_TYPES[o.format])


def header_lines(meta: dict) -> list[str]:
    f, o = meta["from"], meta["options"]
    lines = [
        f"quran-text map — from {f['name_en']} ({f['name_ar']}, {f['counting_system']} count) "
        f"to {', '.join(meta['to'])}",
        f"by: {o['by']} | scope: {o['scope']} | columns: {', '.join(meta['columns'])}",
        meta["note"],
        f"generated: {meta['generated']}" + (f" from {meta['url']}" if meta["url"] else ""),
        f"{meta['license']} {meta['project']}",
    ]
    if meta["limited"]:
        lines.append(f"PREVIEW: limited to the first {meta['records']} records")
    return lines


def _cell(v) -> str:
    return "" if v is None else str(v)


def as_txt(rows, meta, o) -> str:
    out = ["# " + l for l in header_lines(meta)] + [""] if o.header else []
    cols = columns(o)
    out.append("|".join(cols))
    out += ["|".join(_cell(r.get(c)) for c in cols) for r in rows]
    return "\n".join(out) + "\n"


def as_md(rows, meta, o) -> str:
    out = ["> " + l for l in header_lines(meta)] + [""] if o.header else []
    cols = columns(o)
    out.append("| " + " | ".join(cols) + " |")
    out.append("|" + "---|" * len(cols))
    out += ["| " + " | ".join(_cell(r.get(c)) for c in cols) + " |" for r in rows]
    return "\n".join(out) + "\n"


def as_json(rows, meta, o) -> str:
    cols = columns(o)
    doc = {"meta": meta} if o.header else {}
    doc["rows"] = [{c: r.get(c) for c in cols} for r in rows]
    return json.dumps(doc, ensure_ascii=False, indent=1) + "\n"


def as_csv(rows, meta, o) -> str:
    buf = io.StringIO()
    if o.header:
        buf.write("".join("# " + l + "\n" for l in header_lines(meta)))
    cols = columns(o)
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(cols)
    for r in rows:
        w.writerow([_cell(r.get(c)) for c in cols])
    return buf.getvalue()


def as_xml(rows, meta, o) -> str:
    cols = columns(o)
    out = ['<?xml version="1.0" encoding="UTF-8"?>']
    if o.header:
        out.append("<!--\n" + "\n".join("  " + l.replace("--", "—") for l in header_lines(meta)) + "\n-->")
    out.append(f'<map from={quoteattr(meta["from"]["key"])} to={quoteattr(",".join(meta["to"]))} by={quoteattr(o.by)}>')
    for r in rows:
        attrs = " ".join(f"{c}={quoteattr(_cell(r.get(c)))}" for c in cols if r.get(c) is not None)
        out.append(f"<row {attrs}/>")
    out.append("</map>")
    return "\n".join(out) + "\n"


def as_sql(rows, meta, o) -> str:
    cols = columns(o)
    types = {c: ("INTEGER" if c in ("surah", "ayah", "position", "number", "first_number", "last_number") else "TEXT") for c in cols}
    table = "quran_map_words" if o.by == "word" else "quran_map"
    out = ["-- " + l for l in header_lines(meta)] if o.header else []
    out.append(f"CREATE TABLE {table} (")
    out.append("  id INTEGER PRIMARY KEY,")
    out.append(",\n".join(f"  {c} {types[c]}" for c in cols))
    out.append(");")
    for i, r in enumerate(rows, 1):
        values = [str(i)] + ["NULL" if r.get(c) is None else (str(r[c]) if isinstance(r[c], int) else "'" + str(r[c]).replace("'", "''") + "'") for c in cols]
        out.append(f"INSERT INTO {table} (id, {', '.join(cols)}) VALUES ({', '.join(values)});")
    return "\n".join(out) + "\n"


FORMATTERS = {"txt": as_txt, "json": as_json, "csv": as_csv, "xml": as_xml, "sql": as_sql, "md": as_md}
