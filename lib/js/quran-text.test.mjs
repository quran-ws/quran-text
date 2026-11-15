import { test } from "node:test";
import assert from "node:assert/strict";
import { Mushaf, AyahMap, WordIndex, ayahMark, fold } from "./quran-text.js";

const OUT = new URL("../../data/", import.meta.url).pathname;
const hafs = await Mushaf.load(OUT + "mushaf/hafs.json");
const warsh = await Mushaf.load(OUT + "mushaf/warsh.json");
const bazzi = await Mushaf.load(OUT + "mushaf/bazzi.json");

test("ayah text, layers and rendering", () => {
  const a = hafs.ayah(2, 255);
  assert.equal(a.key, "2:255");
  assert.equal(a.length, 50);
  assert.equal(a.page.number, 42);
  assert.equal(a.juz.number, 3);
  assert.equal(a.line.number, 8);
  // The expected strings are the release's own codepoint order, not NFC:
  // see `normalization` in any muṣḥaf file. Compare across datasets by
  // normalising both sides.
  assert.ok(a.text.startsWith("ٱللَّهُ لَآ إِلَٰهَ"));
  assert.ok(a.render({ ayahMarks: true }).endsWith(" ۝٢٥٥"));
  assert.ok(a.render({ marks: true }).includes("ۚ"));
  assert.ok(!a.render().includes("ۚ"));
  assert.equal(a.next().key, "2:256");
  assert.equal(hafs.ayah(2, 286).next().key, "3:1");
  assert.equal(hafs.ayah(1, 1).previous(), null);
});

test("surah, page, line, juz", () => {
  const s = hafs.surah(112);
  assert.equal(s.ayahs.length, 4);
  assert.equal(s.render({ ayahMarks: true }).split("۝").length, 5);
  assert.equal(s.basmalah, null);
  const p = hafs.page(3);
  assert.equal(p.lines.length, 15);
  assert.equal(p.ayahs[0].key, "2:6");
  assert.equal(p.ayahs.at(-1).key, "2:16");
  assert.equal(p.render({ lines: true }).split("\n").length, 15);
  assert.equal(p.line(1).text, p.lines[0].text);
  assert.equal(hafs.juz(30).firstAyah.key, "78:1");
  assert.equal(hafs.juz(30).pages.at(-1).number, 604);
  assert.equal(hafs.surah(2).lastPage.number, 49);
});

test("words, marks, numbering", () => {
  const w = hafs.word(1, 4, 1);
  assert.equal(w.text, "مَٰلِكِ");
  assert.equal(w.number, 11);
  assert.equal(w.rasm_imlai, "مالك");
  assert.equal(w.index, 1);
  assert.equal(hafs.sajdat().map((a) => a.key)[0], "7:206");
  assert.equal(hafs.sajdat().length, 15);
  assert.equal(hafs.divisionMarks().length, 199);
  assert.equal(hafs.divisionMarks()[0].render(), "۞ إِنَّ");
  assert.equal(hafs.numberAt(73948), 73950);
  assert.equal(hafs.wordAt(73948).numberLast, 73951);
  assert.equal(hafs.wordByNumber(25685), null);
  assert.equal(hafs.wordByNumber(73951).text, "وَأَلَّوِ");
  assert.equal(hafs.wordByNumber(11).text, "مَٰلِكِ");
});

test("unnumbered basmalah and absent layers", () => {
  assert.equal(warsh.basmalahCounted, false);
  assert.equal(warsh.surah(1).basmalah.length, 4);
  assert.equal(warsh.wordAt(0).ayah, null);
  assert.equal(warsh.ayahAt(3), null);
  assert.equal(warsh.ayah(1, 1).text.split(" ").length, 4);
  assert.equal(warsh.surah(1).ayahs.length, 7);
  assert.ok(warsh.ayah(2, 253).render({ ayahMarks: true }).endsWith("۝٢٥٣"));
  assert.throws(() => bazzi.juz(1), /no juz layer/);
  assert.equal(bazzi.wordAt(5).juz, null);
  assert.equal(bazzi.has("juz"), false);
  assert.equal(bazzi.wordAt(5).rasm_imlai, null);
});

test("search", () => {
  const hits = hafs.search("مالك يوم الدين");
  assert.equal(hits.length, 1);
  assert.equal(hits[0].firstAyah.key, "1:4");
  assert.equal(fold("ٱلۡحَمۡدُ"), "الحمد");
  assert.equal(ayahMark(255), "۝٢٥٥");
});

test("bundled hafs", async () => {
  const m = await Mushaf.hafs();
  assert.equal(m.key, "hafs");
  assert.equal(m.wordCount, hafs.wordCount);
  assert.equal(m.font.family, "KFGQPC HAFS Uthmanic Script");
  assert.ok(m.font.url.endsWith("UthmanicHafs-v-3.0.ttf"));
  assert.ok(m.fontFace().startsWith("@font-face"));
  assert.equal(warsh.font.family, "KFGQPC Warsh Uthmanic Script");
  assert.equal(warsh.font.file, "UthmanicWarsh-v-3.0.ttf");
});

test("fontFace: a rule that can load, or an error that says why not", async () => {
  // load() finds the font in data/fonts/, as the Python and PHP loaders do.
  assert.ok(warsh.font.url.startsWith("file:"));
  assert.ok(warsh.font.url.endsWith("/data/fonts/UthmanicWarsh-v-3.0.ttf"));
  assert.match(warsh.fontFace(), /src: url\("file:[^"]+UthmanicWarsh-v-3\.0\.ttf"\) format\("truetype"\);/);
  // Without a file beside it there is no URL, and no rule pointing at "null".
  const bare = Mushaf.fromJson(JSON.stringify(warsh._doc));
  assert.equal(bare.font.url, null);
  assert.throws(() => bare.fontFace(), /Warsh has no font URL: pass the URL of data\/fonts\/UthmanicWarsh-v-3\.0\.ttf/);
  // The format hint follows the URL, and is left out when the URL says nothing.
  const rule = (u) => bare.fontFace(u);
  assert.match(rule("https://cdn.example/w.woff2"), /format\("woff2"\)/);
  assert.match(rule("https://cdn.example/w.woff?v=3#x"), /format\("woff"\)/);
  assert.match(rule("/fonts/W.OTF"), /format\("opentype"\)/);
  assert.equal(rule("https://cdn.example/font?id=7"),
    '@font-face { font-family: "KFGQPC Warsh Uthmanic Script"; src: url("https://cdn.example/font?id=7"); }');
  assert.match(rule('https://cdn.example/a"b.ttf'), /url\("https:\/\/cdn\.example\/a\\"b\.ttf"\)/);
});

test("to(): the same ayah and word in another riwayah", () => {
  const m = hafs.ayah(2, 255).to(warsh);
  assert.equal(m.key, "2:253-254"); assert.equal(m.relation, "split"); assert.equal(m.ayahs.length, 2);
  assert.equal(warsh.ayah(2, 253).to(hafs).key, "2:255");
  assert.equal(warsh.ayah(2, 253).to(hafs).relation, "merged");
  assert.equal(hafs.ayah(1, 1).to(warsh).relation, "unnumbered");
  assert.equal(hafs.ayah(57, 24).to(warsh).relation, "shifted");
  assert.equal(hafs.ayah(112, 1).to(bazzi).relation, "same");
  assert.equal(hafs.word(57, 24, 10).text, "هُوَ");
  assert.equal(hafs.word(57, 24, 10).to(warsh), null);
  assert.equal(warsh.word(2, 253, 3).to(hafs).text, "إِلَٰهَ");
});

test("ayah map", async () => {
  const map = await AyahMap.load(OUT + "ayah-map.json");
  const r = map.convert(2, 255, "warsh");
  assert.deepEqual([r.surah, r.ayah, r.ayahLast, r.relation], [2, 253, 254, "split"]);
  assert.equal(r.key, "2:253-254");
  assert.equal(map.all(1, 1).warsh.relation, "unnumbered");
  assert.throws(() => map.convert(2, 255, "nope"), /no edition/);
});

test("word index", async () => {
  const idx = await WordIndex.load(OUT + "word-index.json");
  assert.equal(idx.word(11).form("warsh"), "مَلِكِ");
  assert.equal(idx.find(2, 255, 3).rasm_uthmani, "إِلَٰهَ");
  assert.ok(idx.search("مالك").some((w) => w.number === 11));
  assert.equal(idx.differing().length, 53128);
  // differing() is every spelling difference; differences.json is chosen by
  // status, and eight of its words are spelt alike where they are read.
  const listed = new Set(["rasm_variant", "alif_variant", "word_boundary", "partial"]);
  assert.equal(idx.differing().filter((w) => listed.has(w.status)).length, 269);
  assert.equal([...idx].filter((w) => listed.has(w.status)).length, 277);
  assert.equal(hafs.numberingTotal, idx.total);
  assert.equal(warsh.numberingTotal, idx.total);
  // The heading over sūrahs 2–114 is printed but not in words.
  assert.equal(hafs.surah(2).hasBasmalah, true);
  assert.equal(hafs.surah(2).basmalah, null);
  assert.equal(warsh.surah(2).basmalah, null);
});

test("checkForUpdate: the service host, and downloads from where it answered", async () => {
  const real = globalThis.fetch;
  const asked = [];
  const doc = {
    format: "quran-version", format_version: "1.0", dataset: "2026-09-08",
    editions: { hafs: { source: "UthmanicHafs-v-3.0.zip",
      source_sha256: hafs.provenance.text.sha256, file: "mushaf/hafs.json" } },
  };
  globalThis.fetch = async (url) => {
    asked.push(url);
    // A redirect is reported in r.url; the mirror case answers where it was asked.
    const final = url === Mushaf.VERSION_URL ? url : "https://mirror.example/quran/version";
    return { ok: true, url: final, json: async () => doc };
  };
  try {
    assert.equal(Mushaf.VERSION_URL, "https://text.quran.ws/version");
    const r = await hafs.checkForUpdate();
    assert.equal(asked[0], "https://text.quran.ws/version");
    assert.equal(r.upToDate, true);
    assert.equal(r.downloadUrl, "https://text.quran.ws/files/mushaf/hafs.json");
    const m = await hafs.checkForUpdate("https://mirror.example/quran/version");
    assert.equal(m.downloadUrl, "https://mirror.example/quran/files/mushaf/hafs.json");
    // Anything but the version document is "could not tell", never "up to date".
    globalThis.fetch = async () => ({ ok: true, url: "https://quran.ws/version",
      json: async () => { throw new SyntaxError("Unexpected token <"); } });
    assert.equal(await hafs.checkForUpdate(), null);
    globalThis.fetch = async () => ({ ok: false, url: "https://quran.ws/version/" });
    assert.equal(await hafs.checkForUpdate(), null);
  } finally { globalThis.fetch = real; }
});
