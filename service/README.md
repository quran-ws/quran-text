# The download service

An interactive download page and HTTP API over the built dataset in `data/`:
pick a riwāyah, a text form, the signs you want, a scope, a granularity and a
format, and the URL you get is the file. Built on `lib/python/quran_text.py`;
it reads `data/mushaf/<key>.json`, `data/ayah-map.json` and (lazily, for
`/compare`) `data/word-index.json` directly.

## Run

Locally, Python 3.11+:

```sh
cd service
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
.venv/bin/uvicorn app:app --reload          # http://127.0.0.1:8000
.venv/bin/pytest                            # the tests
```

The data directory is `../data` by default; set `QURAN_DATA=/path/to/data` to
serve a build kept elsewhere.

On the servers, Docker — build from the repository root so `lib/` and `data/`
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
| `/files`, `/files/{path}` | every file under `data/` with size and SHA-256, and the file |
| `/version` | the dataset's release identity, for a client library checking for updates (below) |
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
edition's own counts in the message. A parameter `/download`, `/map` or
`/compare` does not take is an error too, named in the message with the list of
the ones it does take: `marks=0` is not a way to turn the marks off, and it no
longer looks like one. Where an edition prints the basmalah of
al-Fātiḥah unnumbered (Warsh, Qālūn, Dūrī, Sūsī) it comes out as āyah `0`, as
in the dataset's CSV view.

## `/version`

The smallest document a client can fetch to learn whether the copy it holds is
stale. The JS library's `Mushaf.checkForUpdate()` reads it; it is cached for an
hour (`Cache-Control: public, max-age=3600`) and readable from any origin.

```json
{"format": "quran-version", "format_version": "1.0", "dataset": "2026-09-08",
 "editions": {"hafs": {"source": "UthmanicHafs-v-3.0.zip", "source_sha256": "cdec…f013",
                       "file": "mushaf/hafs.json", "file_sha256": "9b9e…8075",
                       "ayah_count": 6236, "word_count": 77432}, …}}
```

| field | means |
|---|---|
| `format`, `format_version` | `quran-version`, `1.0`; a client ignores any other document |
| `dataset` | the dataset's `generated` date, from `data/catalog.json` |
| `editions.<key>.source` | the KFGQPC package the riwāyah was cut from |
| `editions.<key>.source_sha256` | its SHA-256, as in the muṣḥaf file's `provenance.text.sha256` |
| `editions.<key>.file` | the built file, relative to `/files/` on the same host |
| `editions.<key>.file_sha256` | the built file's SHA-256, as in `data/manifest.json` |
| `editions.<key>.ayah_count`, `word_count` | the riwāyah's own counts, from `data/catalog.json` |

`file` is relative to the service, not to a fixed host, so a mirror serving
`/version` and `/files/` side by side works unchanged:
`checkForUpdate(url)` resolves the download link against the address that
answered.

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
