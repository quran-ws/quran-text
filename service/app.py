"""The quran-text download service.

    uvicorn app:app --reload          # from service/

GET /                      the page
GET /download?…            one file, every option a query parameter
GET /editions              the seven riwāyāt and what each carries
GET /map                   every āyah or word of one riwāyah with its counterpart in the others
GET /compare?ayah=2:255    one Kūfī āyah in all seven, differing words flagged
GET /files                 every dataset file with size and SHA-256
GET /files/{path}          the file itself
GET /docs                  this API, generated
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated
from urllib.parse import quote

from fastapi import FastAPI, HTTPException, Query, Request, Response
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

from dataset import EDITIONS, Dataset
from download import (FIELDS, FORMATS, GRANULARITIES, MARKER_STYLES, SIGN_LAYOUTS,
                      TEXT_FORMS, BadRequest, Options, build)
from download import _ayah_key  # the one ayah parser, reused by /compare
from mapping import MapOptions, build as build_map

HERE = Path(__file__).resolve().parent

app = FastAPI(
    title="quran-text download service",
    version="1.0",
    description=(
        "The Qurʾān as text in seven riwāyāt — Ḥafṣ, Shuʿbah, Warsh, Qālūn, Dūrī, Sūsī, "
        "Bazzī — from the King Fahd Complex's own releases, in the format your app wants. "
        "Every option is a query parameter, so the URL you build here is the file forever.\n\n"
        "The common case is one URL: `/download?edition=hafs&format=txt`."),
    docs_url="/docs", redoc_url=None,
)
data = Dataset.load()


@app.exception_handler(BadRequest)
async def bad_request(_: Request, e: BadRequest):
    return JSONResponse(status_code=400, content={"error": str(e)})


@app.get("/", include_in_schema=False)
def page() -> HTMLResponse:
    return HTMLResponse((HERE / "page.html").read_text(encoding="utf-8"))


Edition = Annotated[str, Query(description="Riwāyah: " + ", ".join(EDITIONS), pattern="^[a-z]+$")]
Flag = Annotated[bool, Query()]


@app.get("/download", summary="Download the text with the options you choose")
def download(
    request: Request,
    edition: Edition = "hafs",
    text: Annotated[str, Query(description=(
        "Text forms, comma-separated, each its own column: `rasm_uthmani` as the KFGQPC muṣḥaf "
        "prints it; `rasm_imlai` plain modern spelling (Ḥafṣ only — the only release that carries "
        "it); `plain` harakah stripped for search indexes — a matching form, not a spelling. "
        "The first is the `text` column; e.g. `rasm_uthmani,rasm_imlai`"),
        examples=["rasm_uthmani", "rasm_uthmani,rasm_imlai", "rasm_uthmani,plain"])] = "rasm_uthmani",
    markers: Annotated[str, Query(description=(
        "End-of-āyah marker appended to each āyah: `sign` ۝٢٥٥, `brackets` ﴿٢٥٥﴾, "
        "`latin` (255), or `none`"), enum=list(MARKER_STYLES))] = "none",
    waqf: Annotated[bool, Query(description="Keep the waqf marks ۖ ۗ ۚ … as printed")] = True,
    sajdah: Annotated[bool, Query(description="Keep the sajdah sign ۩")] = True,
    sajdah_line: Annotated[bool, Query(description=(
        "Keep the line drawn over the words that make the sajdah due"))] = True,
    division: Annotated[bool, Query(description="Keep the ۞ sign")] = True,
    lines: Annotated[bool, Query(description=(
        "Break the text where the printed lines break (lines are reconstructed, see docs/format.md)"))] = False,
    pages: Annotated[bool, Query(description="txt/md: a `# page N` line at every page turn")] = False,
    fields: Annotated[str | None, Query(description=(
        "Extra columns, comma-separated, from: " + ", ".join(FIELDS) + ". `hafs` adds the Kūfī "
        "(Ḥafṣ) reference and its relation for non-Ḥafṣ editions. Default `surah,ayah`, "
        "plus `position,number` per word"))] = None,
    surah: Annotated[str | None, Query(description="Scope: one sūrah `2` or a range `2-3`")] = None,
    juz: Annotated[int | None, Query(description="Scope: one juz 1–30 (Bazzī has no juz layer)")] = None,
    page: Annotated[str | None, Query(description="Scope: one page `3` or a range `1-10`")] = None,
    ayah: Annotated[str | None, Query(description=(
        "Scope: one āyah `2:255` or a range `2:255-2:286`, in this edition's own count"))] = None,
    by: Annotated[str, Query(description="One record per `ayah` or per printed `word`",
                             enum=list(GRANULARITIES))] = "ayah",
    signs: Annotated[str, Query(description=(
        "Per word: `columns` puts the waqf marks, ۩, the sajdah line and ۞ in their own "
        "`waqf`, `sajdah`, `sajdah_line`, `division` columns and leaves `text` bare; `attached` "
        "prints them on the word as the muṣḥaf does. Which kinds appear follows the "
        "waqf/sajdah/sajdah_line/division switches"),
        enum=list(SIGN_LAYOUTS))] = "columns",
    format: Annotated[str, Query(description=(
        "`txt` one āyah per line · `json` array or nested · `csv` · `xml` Tanzil-compatible · "
        "`sql` CREATE TABLE + INSERTs · `md`"), enum=list(FORMATS))] = "txt",
    prefix: Annotated[bool, Query(description="txt: prefix each line with `surah|ayah|`")] = True,
    nested: Annotated[bool, Query(description="json: nest as surah → ayahs instead of a flat array")] = False,
    header: Annotated[bool, Query(description="Start the file with the provenance header")] = True,
    limit: Annotated[int | None, Query(description="Only the first N records (for previews)", ge=1)] = None,
    inline: Annotated[bool, Query(description="Show in the browser instead of downloading")] = False,
) -> Response:
    options = Options(
        edition=edition, text=text, markers=markers, waqf=waqf, sajdah=sajdah,
        sajdah_line=sajdah_line, division=division,
        lines=lines, pages=pages,
        fields=tuple(f.strip() for f in fields.split(",") if f.strip()) if fields is not None else None,
        surah=surah, juz=juz, page=page, ayah=ayah, by=by, signs=signs, format=format,
        prefix=prefix, nested=nested, header=header, limit=limit)
    try:
        data.mushaf(edition)
    except KeyError as e:
        raise BadRequest(str(e)) from e
    file = build(data, options, url=_canonical_url(request))
    disposition = "inline" if inline or limit else "attachment"
    return Response(
        content=file.body, media_type=file.media_type,
        headers={
            "Content-Disposition": f"{disposition}; filename*=UTF-8''{quote(file.filename)}",
            "X-Checksum-SHA256": file.sha256,
            "Access-Control-Allow-Origin": "*",
        })


def _canonical_url(request: Request) -> str:
    params = [(k, v) for k, v in request.query_params.multi_items() if k not in ("limit", "inline")]
    base = str(request.url.replace(query=None))
    return base + ("?" + "&".join(f"{k}={quote(v, safe=':,-|')}" for k, v in params) if params else "")


@app.get("/map", summary="Every āyah, or every word, of one riwāyah with its counterpart in the others")
def map_dataset(
    request: Request,
    source: Annotated[Edition, Query(alias="from", description="The riwāyah being mapped from; scope and references are in its own count")] = "hafs",
    to: Annotated[str | None, Query(description="Target riwāyāt, comma-separated; every other one when omitted")] = None,
    surah: Annotated[str | None, Query(description="Scope: one sūrah `2` or a range `2-3`")] = None,
    juz: Annotated[int | None, Query(description="Scope: one juz 1–30")] = None,
    page: Annotated[str | None, Query(description="Scope: one page `3` or a range `1-10`")] = None,
    ayah: Annotated[str | None, Query(description="Scope: one āyah `2:253` or a range `2:253-2:286`")] = None,
    by: Annotated[str, Query(description="One row per `ayah` (its counterpart āyāt and relation) or per `word` (its counterpart word)", enum=list(GRANULARITIES))] = "ayah",
    text: Annotated[str, Query(description="Per word, which text form to show: rasm_uthmani, rasm_imlai (Ḥafṣ only), plain", enum=list(TEXT_FORMS))] = "rasm_uthmani",
    format: Annotated[str, Query(description="`json` (default) · `csv` · `txt` · `xml` · `sql` · `md`", enum=list(FORMATS))] = "json",
    header: Annotated[bool, Query(description="Start the file with the provenance header")] = True,
    limit: Annotated[int | None, Query(description="Only the first N rows (for previews)", ge=1)] = None,
    inline: Annotated[bool, Query(description="Show in the browser instead of downloading")] = False,
) -> Response:
    """Computed from the shared word numbering — the same number is the same
    word in every riwāyah — so it works between any two of the seven and agrees
    with `ayah-map.json`. `relation` is same, merged, split, shifted,
    unnumbered or missing. Join your data on `number`, never on sūrah:āyah."""
    options = MapOptions(
        source=source, to=tuple(t.strip() for t in to.split(",") if t.strip()) if to else (),
        surah=surah, juz=juz, page=page, ayah=ayah, by=by, text=text, format=format,
        header=header, limit=limit)
    file = build_map(data, options, url=_canonical_url(request))
    disposition = "inline" if inline or limit or format == "json" else "attachment"
    return Response(
        content=file.body, media_type=file.media_type,
        headers={
            "Content-Disposition": f"{disposition}; filename*=UTF-8''{quote(file.filename)}",
            "X-Checksum-SHA256": file.sha256,
            "Access-Control-Allow-Origin": "*",
        })


@app.get("/editions", summary="The seven riwāyāt and what each file carries")
def editions() -> list[dict]:
    return [data.edition_info(key) for key in EDITIONS]


_DIFF_KIND = {"identical": "notation", "diacritic_variant": "vowels"}


@app.get("/compare", summary="One āyah in every riwāyah, differing words flagged")
def compare(
    ayah: Annotated[str, Query(description="A Kūfī (Ḥafṣ) reference like `2:255`")] = "1:4",
    waqf: Flag = False,
) -> dict:
    """Converts the Kūfī reference with the āyah map, then walks each edition's
    words. A word `differs` when the seven do not all spell it the same, and
    `kind` says how much: `letters` (rasm, ā, dotting, presence or boundary),
    `vowels` (same letters and dots, different vowelling), `notation` (the
    same qiraah written with different codepoints)."""
    ref = _ayah_key(data.mushaf("hafs"), ayah)
    index = data.word_index
    out = {"ayah": ref.key, "editions": []}
    for key in EDITIONS:
        m = data.mushaf(key)
        target = data.ayah_map.convert(ref.surah.number, ref.number, key)
        if target.relation == "unnumbered":
            span = m.surah(target.surah).basmalah
        else:
            span = m.span(m.ayah(target.surah, target.ayah).start,
                          m.ayah(target.surah, target.ayah_last or target.ayah).end)
        words = []
        for w in span:
            entry = index.word(w.number)
            differs = bool(entry.groups) or w.number_last != w.number
            words.append({
                "text": w.render(marks={"waqf"} if waqf else set()),
                "number": w.number, "ayah": w.ayah.number if w.ayah else 0,
                "differs": differs,
                "kind": _DIFF_KIND.get(entry.status, "letters") if differs else None,
                "status": entry.status,
            })
        out["editions"].append({
            "key": key, "name_en": m.name_en, "name_ar": m.name_ar,
            "ref": target.key, "relation": target.relation, "words": words})
    return out


@app.get("/version", summary="Dataset release identity, for client libraries checking for updates")
def version(response: Response) -> dict:
    """The smallest thing a client can fetch to learn whether its bundled copy
    is stale.  Cached hard: a library polling this daily should almost always
    get a 304 or a CDN hit rather than touching the application."""
    response.headers["Cache-Control"] = "public, max-age=3600"
    response.headers["Access-Control-Allow-Origin"] = "*"
    return data.versions()


@app.get("/files", summary="Every dataset file with size, SHA-256 and what it answers")
def files(request: Request) -> list[dict]:
    base = str(request.url.replace(query=None, path="/files/"))
    return [dict(f, url=base + f["path"]) for f in data.files()]


@app.api_route("/files/{path:path}", methods=["GET", "HEAD"], summary="One dataset file, as built")
def file(path: str) -> FileResponse:
    target = data.file_path(path)
    if target is None or not target.is_file():
        raise HTTPException(404, f"no such file: {path}; see /files")
    return FileResponse(target, filename=target.name)
