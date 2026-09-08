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
  assert.ok(a.text.startsWith("ٱللَّهُ لَآ إِلَٰهَ"));
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
  assert.equal(hafs.divisionMarks()[0].render(), "۞ إِنَّ");
  assert.equal(hafs.numberAt(73948), 73950);
  assert.equal(hafs.wordAt(73948).numberLast, 73951);
  assert.equal(hafs.wordByNumber(25685), null);
  assert.equal(hafs.wordByNumber(73951).text, "وَأَلَّوِ");
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
  assert.equal(warsh.font.file, "data/fonts/UthmanicWarsh-v-3.0.ttf");
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
  assert.equal(idx.differing().length, 53134);
});
