# The download service

An interactive download page and HTTP API over the built dataset in `out/`:
pick a riwāyah, a text form, the signs you want, a scope, a granularity and a
format, and the URL you get is the file. Built on `lib/python/quran_text.py`;
it reads `out/mushaf/<key>.json`, `out/ayah-map.json` and (lazily, for
`/compare`) `out/word-index.json` directly.

## Run

Locally, Python 3.11+:

```sh
cd service
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
.venv/bin/uvicorn app:app --reload          # http://127.0.0.1:8000
.venv/bin/pytest                            # the tests
```

The data directory is `../out` by default; set `QURAN_DATA=/path/to/out` to
serve a build kept elsewhere.

On the servers, Docker — build from the repository root so `lib/` and `out/`
are in the context:

```sh
docker build -f service/Dockerfile -t quran-text-service .
docker run -p 8000:8000 quran-text-service
```

Put a reverse proxy in front for TLS and caching: every `/download` response
is a pure function of its URL, so `Cache-Control` at the proxy is safe.

## The API

| path | what |
|---|---|
| `/` | the page |
| `/download?…` | one file; every option below is a query parameter |
| `/editions` | the seven riwāyāt: names, counts, which layers each carries |
| `/compare?ayah=2:255` | one Kūfī āyah in all seven, differing words flagged |
| `/map?from=warsh&to=duri&ayah=2:253` | the mapping dataset: every āyah (`by=ayah`, its counterpart āyāt and relation) or every word (`by=word`) of one riwāyah in the others, with the same scope and format options as `/download`; omit `to` for all six, omit the scope for the whole Qurʾān |
| `/files`, `/files/{path}` | every file under `out/` with size and SHA-256, and the file |
| `/docs` | the OpenAPI page with every parameter described |

`/download` parameters — the common case is `/download?edition=hafs&format=txt`:

| param | values | default | means |
|---|---|---|---|
| `edition` | `hafs shubah warsh qalun duri susi bazzi` | `hafs` | the riwāyah |
| `text` | `rasm_uthmani` `rasm_imlai` `plain` | `rasm_uthmani` | as printed; modern spelling (Ḥafṣ only); harakah stripped for search |
| `markers` | `none` `sign` `brackets` `latin` | `none` | end-of-āyah marker: ۝٢٥٥, ﴿٢٥٥﴾, (255) |
| `waqf` `sajdah` `division` | `1`/`0` | `1` | keep waqf marks, ۩, ۞ |
| `lines` | `1`/`0` | `0` | break the text where the printed lines break |
| `pages` | `1`/`0` | `0` | txt/md: a `# page N` line at every page turn |
| `fields` | comma list of `surah ayah position number page line juz hafs` | `surah,ayah` (+`position,number` per word) | the columns of structured formats; `hafs` = the Kūfī reference and relation |
| `surah` | `2` or `2-3` | — | scope |
| `juz` | `1`–`30` | — | scope (not Bazzī, which has no juz layer) |
| `page` | `3` or `1-10` | — | scope |
| `ayah` | `2:255` or `2:255-2:286` | — | scope, in the edition's own count |
| `by` | `ayah` `word` | `ayah` | one record per āyah or per printed word |
| `format` | `txt` `json` `csv` `xml` `sql` `md` | `txt` | |
| `prefix` | `1`/`0` | `1` | txt: `surah\|ayah\|` before each line |
| `nested` | `1`/`0` | `0` | json: sūrah → āyāt instead of a flat array |
| `header` | `1`/`0` | `1` | the provenance header (a comment in txt/csv/sql/xml/md, `meta` in json) |
| `limit` | N | — | only the first N records, for previews |
| `inline` | `1`/`0` | `0` | show in the browser instead of downloading |

Every response carries `Content-Disposition` with a descriptive filename and
`X-Checksum-SHA256` of the body. Errors are `400 {"error": "…"}` with the
edition's own counts in the message. Where an edition prints the basmalah of
al-Fātiḥah unnumbered (Warsh, Qālūn, Dūrī, Sūsī) it comes out as āyah `0`, as
in the dataset's CSV view.

## Files

| | |
|---|---|
| `app.py` | the routes |
| `download.py` | options → selection → records → the six formats |
| `dataset.py` | loads the dataset once; the inverse āyah map; the file list |
| `page.html` | the page: one static file, no build step |
| `tests/` | pytest |

The text is KFGQPC's; redistribution is subject to their terms (see the root
README, *Sources*). The service says so on the page and in every file header.
