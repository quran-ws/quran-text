"""Build ``out/reports/compare.html`` — a self-contained word-by-word comparison.

The whole corpus is 36 MB of JSON, which is too much to paste into a page, and
a page that fetched the per-sūrah files would need a web server to escape the
``file://`` origin.  So the data is packed to about a tenth of its size, gzipped,
base64'd, and inflated in the browser with ``DecompressionStream``.

The packing is where the saving is: a word is stored as its *distinct*
spellings, each with a bitmask of the riwāyāt that use it, rather than as seven
separate strings.  Most words have two or three distinct spellings, not seven.
"""

from __future__ import annotations

import base64
import gzip
import json
from datetime import date

from .build import ORDER, OUT, Word
from .sources import Riwaya
from .suras import names

#: Status codes, packed as an index into this list.
STATUSES = ["identical", "diacritic_variant", "dotting_variant",
            "alif_variant", "rasm_variant", "word_boundary", "partial"]


def _pack(words: list[Word]) -> dict:
    """The corpus in the smallest shape the page can still read."""
    bit = {k: 1 << i for i, k in enumerate(ORDER)}
    suras: dict[str, list] = {}
    for w in words:
        groups: dict[str, int] = {}
        for k in ORDER:
            if k in w.forms:
                groups[w.forms[k]] = groups.get(w.forms[k], 0) | bit[k]
        # aya numbers: one per riwāyah, but they are equal far more often than
        # not, so store the distinct values with their masks too.
        ayat: dict[int, int] = {}
        for k in ORDER:
            if k in w.aya:
                ayat[w.aya[k]] = ayat.get(w.aya[k], 0) | bit[k]
        rec = [
            w.index,
            w.id,
            w.rasm,
            STATUSES.index(w.status),
            [[t, m] for t, m in groups.items()],
            [[a, m] for a, m in ayat.items()],
        ]
        extra = 0
        if w.boundary:
            extra |= 1
        if w.missing:
            extra |= 2
        if extra:
            rec.append(extra)
        suras.setdefault(str(w.sura), []).append(rec)
    return suras


def write_viewer(words: list[Word], riwayat: list[Riwaya]) -> None:
    payload = {
        "generated": date.today().isoformat(),
        "order": ORDER,
        "statuses": STATUSES,
        "riwayat": {r.key: {"en": r.name_en, "ar": r.name_ar, "qari": r.qari_en}
                    for r in riwayat},
        "suras": {str(s): {"name_ar": names()[s]["name_ar"],
                           "name_en": names()[s]["name_en"]}
                  for s in range(1, 115)},
        "words": _pack(words),
    }
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    blob = base64.b64encode(
        gzip.compress(raw.encode("utf-8"), 9)).decode("ascii")
    (OUT / "reports").mkdir(exist_ok=True)
    (OUT / "reports" / "compare.html").write_text(
        _TEMPLATE.replace("__DATA__", blob).replace("__WORDS__", f"{len(words):,}"),
        encoding="utf-8")


_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Qur'anic word index — cross-riwāyah comparison</title>
<style>
:root{
  --bg:#fbfaf7; --panel:#fff; --ink:#1b1a17; --dim:#6b675f; --line:#e3ded4;
  --accent:#7a5c2e; --chip:#f1ece1;
  --identical:#9aa79a; --diacritic:#7f9bb5; --dotting:#c08a3e;
  --rasm:#b5543f; --alif:#c2857a; --boundary:#8a6bb0; --partial:#4f8a7b;
}
@media (prefers-color-scheme: dark){:root:not([data-theme=light]){
  --bg:#14140f; --panel:#1c1c17; --ink:#eae6dc; --dim:#9c968a; --line:#2e2d26;
  --accent:#d3ab68; --chip:#26251e;
}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font:15px/1.5 ui-sans-serif,system-ui,"Segoe UI",Roboto,sans-serif}
header{padding:22px 20px 14px;border-bottom:1px solid var(--line)}
h1{margin:0 0 4px;font-size:19px;font-weight:650;letter-spacing:-.01em}
.sub{color:var(--dim);font-size:13px}
.bar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;
  padding:12px 20px;border-bottom:1px solid var(--line);
  position:sticky;top:0;background:var(--bg);z-index:5}
select,input[type=search]{font:inherit;padding:6px 9px;border:1px solid var(--line);
  border-radius:7px;background:var(--panel);color:var(--ink)}
input[type=search]{min-width:190px}
.filters{display:flex;flex-wrap:wrap;gap:6px}
.f{border:1px solid var(--line);background:var(--panel);color:var(--dim);
  border-radius:999px;padding:4px 11px;font-size:12.5px;cursor:pointer}
.f[aria-pressed=true]{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.f .n{opacity:.6;margin-inline-start:5px;font-variant-numeric:tabular-nums}
main{padding:14px 20px 60px;max-width:1180px}
.word{background:var(--panel);border:1px solid var(--line);border-radius:11px;
  margin-bottom:9px;overflow:hidden}
.whead{display:flex;gap:14px;align-items:baseline;padding:10px 14px;cursor:pointer}
.ref{color:var(--dim);font-size:12px;font-variant-numeric:tabular-nums;
  min-width:96px;flex:none}
.rasm{font-size:20px;direction:rtl;font-family:"Scheherazade New","Amiri",
  "Noto Naskh Arabic",serif;flex:none;min-width:120px}
.tag{font-size:11px;letter-spacing:.03em;text-transform:uppercase;
  padding:2px 8px;border-radius:999px;background:var(--chip);color:var(--dim);
  flex:none;align-self:center}
.tag.rasm_variant{background:var(--rasm);color:#fff}
.tag.alif_variant{background:var(--alif);color:#1b1a17}
.tag.dotting_variant{background:var(--dotting);color:#1b1a17}
.tag.word_boundary{background:var(--boundary);color:#fff}
.tag.partial{background:var(--partial);color:#fff}
.tag.diacritic_variant{background:var(--diacritic);color:#fff}
.groups{display:flex;flex-wrap:wrap;gap:8px;flex:1;justify-content:flex-end}
.g{display:flex;flex-direction:column;align-items:flex-end;gap:2px;
  border-inline-start:2px solid var(--line);padding-inline-start:9px}
.g b{font-weight:400;font-size:23px;direction:rtl;line-height:1.7;
  font-family:"Scheherazade New","Amiri","Noto Naskh Arabic",serif}
.g span{font-size:10.5px;color:var(--dim);letter-spacing:.02em}
.detail{border-top:1px solid var(--line);padding:6px 14px 12px;display:none}
.word.open .detail{display:block}
table{border-collapse:collapse;width:100%}
td{padding:5px 8px;border-bottom:1px solid var(--line);vertical-align:middle}
td.k{color:var(--dim);font-size:12px;width:150px}
td.v{font-size:22px;direction:rtl;
  font-family:"Scheherazade New","Amiri","Noto Naskh Arabic",serif}
td.a{color:var(--dim);font-size:12px;width:70px;font-variant-numeric:tabular-nums}
tr.differs td.v{color:var(--accent)}
.empty{color:var(--dim);padding:40px 0;text-align:center}
.note{color:var(--dim);font-size:12.5px;margin:0 0 14px}
kbd{background:var(--chip);border-radius:4px;padding:1px 5px;font-size:11px}
</style>
</head>
<body>
<header>
  <h1>Qur'anic word index — cross-riwāyah comparison</h1>
  <div class="sub">__WORDS__ words · 114 sūrahs · 7 riwāyāt. One ID means one
    word in every riwāyah that has it. Click a word for the full breakdown.</div>
</header>

<div class="bar">
  <select id="sura"></select>
  <input type="search" id="q" placeholder="search rasm or spelling…">
  <div class="filters" id="filters"></div>
</div>

<main>
  <p class="note" id="note"></p>
  <div id="list"></div>
</main>

<script id="data" type="application/gzip;base64">__DATA__</script>
<script>
const B64 = document.getElementById('data').textContent.trim();

async function load(){
  const bytes = Uint8Array.from(atob(B64), c => c.charCodeAt(0));
  if (typeof DecompressionStream === 'undefined')
    throw new Error('This browser cannot inflate the embedded data.');
  const stream = new Blob([bytes]).stream()
    .pipeThrough(new DecompressionStream('gzip'));
  return JSON.parse(await new Response(stream).text());
}

let D, state = {sura: 1, status: null, q: ''};

const has = (mask, i) => (mask >> i) & 1;
const namesOf = mask => D.order.filter((_, i) => has(mask, i));

function counts(rows){
  const c = {};
  for (const r of rows) c[D.statuses[r[3]]] = (c[D.statuses[r[3]]] || 0) + 1;
  return c;
}

function render(){
  const rows = D.words[state.sura] || [];
  const q = state.q.trim();
  const shown = rows.filter(r =>
    (!state.status || D.statuses[r[3]] === state.status) &&
    (!q || r[2].includes(q) || r[4].some(g => g[0].includes(q))));

  const c = counts(rows);
  document.getElementById('filters').innerHTML = D.statuses.map(s =>
    `<button class="f" data-s="${s}" aria-pressed="${state.status===s}">${
      s.replace(/_/g,' ')}<span class="n">${c[s]||0}</span></button>`).join('');

  document.getElementById('note').textContent =
    `${shown.length} of ${rows.length} words shown.` +
    (state.status ? ` Filtered to ${state.status.replace(/_/g,' ')}.` : '');

  document.getElementById('list').innerHTML = shown.length ? shown.map(r => {
    const [i, id, rasm, st, groups, ayat] = r;
    const status = D.statuses[st];
    const aya = ayat.map(a => a[0]);
    const ref = aya.every(a => a === aya[0])
      ? `${state.sura}:${aya[0]}` : `${state.sura}:${Math.min(...aya)}–${Math.max(...aya)}`;
    return `<div class="word" data-id="${id}">
      <div class="whead">
        <span class="ref">${ref} · #${i}</span>
        <span class="rasm">${rasm}</span>
        <span class="tag ${status}">${status.replace(/_/g,' ')}</span>
        <span class="groups">${groups.map(g =>
          `<span class="g"><b>${g[0]}</b><span>${namesOf(g[1]).join(' · ')}</span></span>`
        ).join('')}</span>
      </div>
      <div class="detail"></div></div>`;
  }).join('') : `<p class="empty">Nothing matches.</p>`;
}

function detail(el, id){
  const r = (D.words[state.sura] || []).find(x => x[1] === +id);
  if (!r) return;
  const [i, wid, rasm, st, groups, ayat] = r;
  const spelling = {}, aya = {};
  for (const [t, m] of groups) namesOf(m).forEach(k => spelling[k] = t);
  for (const [a, m] of ayat) namesOf(m).forEach(k => aya[k] = a);
  const many = groups.length > 1;
  el.innerHTML = `<table>${D.order.map(k => {
    const s = spelling[k];
    const differs = many && s !== groups[0][0];
    return `<tr class="${differs ? 'differs' : ''}">
      <td class="k">${D.riwayat[k].en} · ${D.riwayat[k].ar}</td>
      <td class="v">${s === undefined ? '—' : s}</td>
      <td class="a">${aya[k] === undefined ? '' : 'āyah ' + aya[k]}</td></tr>`;
  }).join('')}</table>
  <p class="note" style="margin:9px 0 0">word id <b>${wid}</b> · rasm <b>${rasm}</b>
   · ${groups.length} distinct spelling${groups.length > 1 ? 's' : ''}</p>`;
}

document.addEventListener('click', e => {
  const f = e.target.closest('.f');
  if (f){ state.status = state.status === f.dataset.s ? null : f.dataset.s;
          return render(); }
  const head = e.target.closest('.whead');
  if (head){
    const w = head.parentElement;
    w.classList.toggle('open');
    if (w.classList.contains('open')) detail(w.querySelector('.detail'), w.dataset.id);
  }
});

load().then(data => {
  D = data;
  const sel = document.getElementById('sura');
  sel.innerHTML = Object.entries(D.suras).map(([n, s]) =>
    `<option value="${n}">${n}. ${s.name_en} — ${s.name_ar}</option>`).join('');
  sel.onchange = () => { state.sura = sel.value; render(); };
  document.getElementById('q').oninput = e => { state.q = e.target.value; render(); };
  render();
}).catch(err => {
  document.getElementById('list').innerHTML =
    `<p class="empty">${err.message}</p>`;
});
</script>
</body>
</html>
"""
