/**
 * quran-text — read the muṣḥaf files of the quran-text dataset.
 *
 *   import { Mushaf } from "quran-text";
 *   const m = await Mushaf.hafs();                             // bundled Ḥafṣ
 *   const m = await Mushaf.load("out/mushaf/warsh.json");     // another riwāyah, Node
 *   const m = Mushaf.fromJson(await (await fetch(url)).json()); // browser
 *   m.ayah(2, 255).text
 *   m.ayah(2, 255).render({ marks: true, ayahMarkers: true })
 *   m.page(3).lines
 *   m.juz(30).firstAyah.key                                    // "78:1"
 *
 * Everything is a slice of one `words` array.  A Span is a slice with `text`
 * and `render()`; Sura, Ayah, Page, Line and Juz are spans that know their
 * place.  Positions are 0-based indices into `words`; sūrah, āyah, page, line
 * and juz numbers are 1-based, as printed.  Āyah numbers are in this
 * edition's own count; use AyahMap to convert between editions.
 *
 * No dependencies.  ES2020.
 */

export const END_OF_AYAH = "۝";

const ARABIC_INDIC = "٠١٢٣٤٥٦٧٨٩";

/** The end-of-āyah sign with its number, as the muṣḥaf prints it: ۝٢٥٥ */
export function ayahMarker(number) {
  return END_OF_AYAH + String(number).replace(/\d/g, (d) => ARABIC_INDIC[d]);
}

const FOLD_ALEF = /[\u0671\u0623\u0625\u0622\u0870-\u0882]/g;
const FOLD_YEH = /[\u06D2\u06D1\u0649]/g;
const FOLD_DROP = /[\u0640\u0610-\u061A\u064B-\u065F\u06D6-\u06DC\u06DF-\u06E8\u06EA-\u06ED\u08CA-\u08FF\u0888]/g;

/**
 * Reduce a word to plain letters for matching: no diacritics, no pause marks,
 * one alif, one yāʾ.  For search only — it is not a spelling of anything.
 */
export function fold(text) {
  return text
    .replace(/\u0670/g, "\u0627")
    .replace(FOLD_ALEF, "ا")
    .replace(FOLD_YEH, "ي")
    .replace(FOLD_DROP, "");
}

/** Index of the unit that contains `position` (-1 before the first). */
function indexOf(starts, position) {
  let lo = 0, hi = starts.length;
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (starts[mid] <= position) lo = mid + 1; else hi = mid;
  }
  return lo - 1;
}

const ALL_KINDS = new Set(["waqf", "hizb", "sajdah"]);

function markKinds(marks) {
  if (marks === true) return ALL_KINDS;
  if (!marks) return new Set();
  return new Set(marks);
}

// --- records -----------------------------------------------------------------

/** A sign printed against a word: kind is waqf, hizb or sajdah. */
export class Mark {
  constructor(kind, side, sign) {
    this.kind = kind;
    this.side = side;
    this.sign = sign;
    Object.freeze(this);
  }
}

/** One printed word and everything the muṣḥaf says about it. */
export class Word {
  constructor(mushaf, position) {
    if (!(position >= 0 && position < mushaf.words.length)) {
      throw new RangeError(`position ${position} is outside the muṣḥaf`);
    }
    this._m = mushaf;
    this.position = position;
  }
  get text() { return this._m.words[this.position]; }
  /** Plain modern spelling, Ḥafṣ only; null elsewhere. */
  get imlaei() { const c = this._m._doc.imlaei; return c ? c[this.position] : null; }
  get sura() { return this._m.suraAt(this.position); }
  /** The āyah this word is in; null for the unnumbered basmalah. */
  get ayah() { return this._m.ayahAt(this.position); }
  /** 1-based position within the āyah; null when unnumbered. */
  get index() { const a = this.ayah; return a ? this.position - a.start + 1 : null; }
  get page() { return this._m.pageAt(this.position); }
  get line() { return this._m.lineAt(this.position); }
  get juz() { return this._m.juzAt(this.position); }
  /** The shared number: the same word in every riwāyah. */
  get number() { return this._m._numbers[this.position][0]; }
  /** Equal to `number` except where this muṣḥaf writes two numbers as one word. */
  get numberLast() { return this._m._numbers[this.position][1]; }
  /** @returns {Mark[]} */
  get marks() { return this._m._marksAt.get(this.position) ?? []; }
  hasMark(kind) { return this.marks.some((mk) => mk.kind === kind); }
  /** The same word in another riwāyah, by the shared number; null where it does not read it. */
  to(other) { return other.wordByNumber(this.number); }
  /** The word with its signs: ۞ before, waqf and ۩ after. */
  render(marks = true) {
    const kinds = markKinds(marks);
    let before = "", after = "";
    for (const mk of this.marks) {
      if (!kinds.has(mk.kind)) continue;
      if (mk.side === "before") before += mk.sign + " "; else after += mk.sign;
    }
    return before + this.text + after;
  }
  toString() { return this.text; }
}

/** A run of positions start … end-1 of one muṣḥaf. */
export class Span {
  constructor(mushaf, start, end) {
    this._m = mushaf;
    this.start = start;
    this.end = end;
  }
  get mushaf() { return this._m; }
  get length() { return this.end - this.start; }
  /** @returns {string[]} */
  get words() { return this._m.words.slice(this.start, this.end); }
  /** @returns {Word[]} */
  get wordList() {
    const out = [];
    for (let p = this.start; p < this.end; p++) out.push(new Word(this._m, p));
    return out;
  }
  /** The words joined with spaces, without any sign. */
  get text() { return this.words.join(" "); }
  /**
   * The text as the muṣḥaf prints it, with what you ask for.
   * @param {{marks?: boolean|string[], ayahMarkers?: boolean, lines?: boolean}} options
   *   `marks`: true for every sign, or an array of kinds among "waqf", "hizb",
   *   "sajdah".  `ayahMarkers` appends ۝ with the āyah number after each āyah
   *   that ends inside the span.  `lines` breaks the text where the printed
   *   lines break.
   */
  render({ marks = false, ayahMarkers = false, lines = false } = {}) {
    const m = this._m;
    const kinds = markKinds(marks);
    const lineStarts = lines ? m._lineStartSet : null;
    let out = "";
    for (let pos = this.start; pos < this.end; pos++) {
      if (lineStarts && pos !== this.start && lineStarts.has(pos)) out += "\n";
      else if (pos !== this.start) out += " ";
      let token = m.words[pos];
      const marksHere = m._marksAt.get(pos);
      if (marksHere) {
        for (const mk of marksHere) {
          if (!kinds.has(mk.kind)) continue;
          token = mk.side === "before" ? mk.sign + " " + token : token + mk.sign;
        }
      }
      out += token;
      if (ayahMarkers) {
        const k = m._ayahEnds.get(pos);
        if (k !== undefined) out += " " + ayahMarker(m._ayahNumber(k));
      }
    }
    return out;
  }
  /** Every numbered āyah with at least one word in the span. @returns {Ayah[]} */
  get ayat() {
    const m = this._m;
    const first = Math.max(indexOf(m._doc.ayah_starts, this.start), 0);
    const last = indexOf(m._doc.ayah_starts, this.end - 1);
    const out = [];
    for (let k = first; k <= last; k++) out.push(Ayah._fromIndex(m, k));
    return out;
  }
  get firstAyah() { const a = this.ayat; return a.length ? a[0] : null; }
  get lastAyah() { const a = this.ayat; return a.length ? a[a.length - 1] : null; }
  /** @returns {Sura[]} */
  get suras() {
    const m = this._m;
    const first = indexOf(m._doc.sura_starts, this.start);
    const last = indexOf(m._doc.sura_starts, this.end - 1);
    return m.suras.slice(first, last + 1);
  }
  /** @returns {Page[]} */
  get pages() {
    const m = this._m;
    const first = indexOf(m._doc.page_starts, this.start);
    const last = indexOf(m._doc.page_starts, this.end - 1);
    const out = [];
    for (let n = first; n <= last; n++) out.push(new Page(m, n + 1));
    return out;
  }
  /** The page the span starts on. */
  get page() { return this._m.pageAt(this.start); }
  get juz() { return this._m.juzAt(this.start); }
  /** Every sign inside the span, with the word it is printed on. @returns {{word: Word, mark: Mark}[]} */
  get marks() {
    const out = [];
    for (let p = this.start; p < this.end; p++) {
      for (const mark of this._m._marksAt.get(p) ?? []) out.push({ word: new Word(this._m, p), mark });
    }
    return out;
  }
  /** The index-th word of the span, 1-based. */
  word(index) {
    if (!(index >= 1 && index <= this.length)) {
      throw new RangeError(`word ${index}: the span has ${this.length} words`);
    }
    return new Word(this._m, this.start + index - 1);
  }
  *[Symbol.iterator]() { for (let p = this.start; p < this.end; p++) yield new Word(this._m, p); }
}

/**
 * Where an āyah falls in another riwāyah.  `relation`: same (one āyah, the
 * same words), merged (one āyah holding more), split (several āyāt), shifted
 * (one āyah, boundaries crossing), unnumbered (the basmalah printed without a
 * number), missing (no word of it).
 */
export class AyahMatch {
  constructor(ayat, relation) { this.ayat = ayat; this.relation = relation; Object.freeze(this); }
  get first() { return this.ayat[0] ?? null; }
  get last() { return this.ayat[this.ayat.length - 1] ?? null; }
  /** "2:253-254" */
  get key() {
    if (!this.ayat.length) return "";
    const a = this.ayat[0], b = this.ayat[this.ayat.length - 1];
    return a.equals(b) ? a.key : `${a.key}-${b.number}`;
  }
  toString() { return `${this.key || "-"} (${this.relation})`; }
}

/** One numbered āyah, in this edition's own count. */
export class Ayah extends Span {
  constructor(mushaf, sura, number) {
    const s = mushaf.sura(sura);
    if (!(number >= 1 && number <= s.ayahCount)) {
      throw new RangeError(`${s.nameEn} has ${s.ayahCount} āyāt in ${mushaf.nameEn}, not ${number}`);
    }
    const k = s._firstAyah + number - 1;
    const starts = mushaf._doc.ayah_starts;
    super(mushaf, starts[k], k + 1 < starts.length ? starts[k + 1] : mushaf.words.length);
    this.sura = s;
    this.number = number;
    this._k = k;
  }
  static _fromIndex(mushaf, k) {
    const s = mushaf.suras[mushaf._suraOfAyahIndex(k)];
    return new Ayah(mushaf, s.number, k - s._firstAyah + 1);
  }
  /** "2:255" */
  get key() { return `${this.sura.number}:${this.number}`; }
  /** 0-based index into ayah_starts: the āyah's ordinal in the muṣḥaf. */
  get index() { return this._k; }
  /** The printed line the āyah starts on. */
  get line() { return this._m.lineAt(this.start); }
  /** Every printed line the āyah touches. @returns {Line[]} */
  get lines() { return this._m._linesBetween(this.start, this.end); }
  get imlaei() { const c = this._m._doc.imlaei; return c ? c.slice(this.start, this.end) : null; }
  get hasSajdah() { return this.marks.some(({ mark }) => mark.kind === "sajdah"); }
  /** ۝٢٥٥ */
  get marker() { return ayahMarker(this.number); }
  /** The shared numbers of this āyah's words. @returns {Set<number>} */
  get numbers() {
    const m = this._m, first = m._numbers[this.start][0], last = m._numbers[this.end - 1][1];
    const out = new Set();
    for (let n = first; n <= last; n++) if (!m.missingNumbers.has(n)) out.add(n);
    return out;
  }
  /**
   * This āyah in another riwāyah: `hafs.ayah(2, 255).to(warsh)` → 2:253-254, split.
   * Computed from the shared numbering, so it works between any two riwāyāt.
   * @returns {AyahMatch}
   */
  to(other) {
    const mine = this.numbers, hits = [];
    let unnumbered = false;
    for (const n of [...mine].sort((a, b) => a - b)) {
      const w = other.wordByNumber(n);
      if (!w) continue;
      const a = w.ayah;
      if (!a) unnumbered = true;
      else if (!hits.length || !hits[hits.length - 1].equals(a)) hits.push(a);
    }
    if (!hits.length) return new AyahMatch([], unnumbered ? "unnumbered" : "missing");
    if (hits.length > 1) return new AyahMatch(hits, "split");
    const theirs = hits[0].numbers;
    const same = theirs.size === mine.size && [...mine].every((n) => theirs.has(n));
    const superset = [...mine].every((n) => theirs.has(n));
    return new AyahMatch(hits, same ? "same" : superset ? "merged" : "shifted");
  }
  next() { const k = this._k + 1; return k < this._m.ayahCount ? Ayah._fromIndex(this._m, k) : null; }
  previous() { const k = this._k - 1; return k >= 0 ? Ayah._fromIndex(this._m, k) : null; }
  equals(other) { return other instanceof Ayah && other._m === this._m && other._k === this._k; }
  toString() { return this.key; }
}

export class Sura extends Span {
  constructor(mushaf, number) {
    if (!(number >= 1 && number <= 114)) throw new RangeError(`sūrah ${number}: there are 114`);
    const info = mushaf._doc.suras[number - 1];
    const starts = mushaf._doc.sura_starts;
    super(mushaf, starts[number - 1], number < starts.length ? starts[number] : mushaf.words.length);
    this.number = number;
    this.nameAr = info.name_ar;
    this.nameEn = info.name_en;
    this.revelation = info.revelation;
    this.hasBasmalah = info.has_basmalah;
    this.ayahCount = info.ayah_count;
    this._firstAyah = info.first_ayah;
  }
  /** @returns {Ayah[]} */
  get ayat() {
    const out = [];
    for (let n = 1; n <= this.ayahCount; n++) out.push(new Ayah(this._m, this.number, n));
    return out;
  }
  ayah(number) { return new Ayah(this._m, this.number, number); }
  /**
   * The basmalah where it is printed unnumbered before āyah 1 (Warsh, Qālūn,
   * Dūrī, Sūsī at al-Fātiḥah); null otherwise.
   */
  get basmalah() {
    const first = this._m._doc.ayah_starts[this._firstAyah];
    return first > this.start ? new Span(this._m, this.start, first) : null;
  }
  get firstPage() { return this.page; }
  get lastPage() { return this._m.pageAt(this.end - 1); }
  toString() { return `${this.number} ${this.nameEn}`; }
}

export class Page extends Span {
  constructor(mushaf, number) {
    const starts = mushaf._doc.page_starts;
    if (!(number >= 1 && number <= starts.length)) {
      throw new RangeError(`page ${number}: ${mushaf.nameEn} has ${starts.length} pages`);
    }
    super(mushaf, starts[number - 1], number < starts.length ? starts[number] : mushaf.words.length);
    this.number = number;
  }
  /** @returns {Line[]} */
  get lines() { return this._m._linesBetween(this.start, this.end); }
  line(number) {
    const lines = this.lines;
    if (!(number >= 1 && number <= lines.length)) {
      throw new RangeError(`line ${number}: page ${this.number} has ${lines.length} lines`);
    }
    return lines[number - 1];
  }
  next() { const n = this.number + 1; return n <= this._m.pageCount ? new Page(this._m, n) : null; }
  previous() { const n = this.number - 1; return n >= 1 ? new Page(this._m, n) : null; }
  toString() { return `page ${this.number}`; }
}

/** One printed line.  Reconstructed, not read: see layers.derived.line. */
export class Line extends Span {
  constructor(mushaf, page, number, index) {
    const starts = mushaf._doc.line_starts;
    super(mushaf, starts[index], index + 1 < starts.length ? starts[index + 1] : mushaf.words.length);
    this._page = page;
    this.number = number;   // within the page, 1-based
    this.index = index;     // within the muṣḥaf, 0-based
  }
  static _fromIndex(mushaf, index) {
    const starts = mushaf._doc.line_starts;
    const page = mushaf.pageAt(starts[index]);
    const first = indexOf(starts, page.start);
    return new Line(mushaf, page, index - first + 1, index);
  }
  get page() { return this._page; }
  toString() { return `page ${this._page.number}, line ${this.number}`; }
}

export class Juz extends Span {
  constructor(mushaf, number) {
    const starts = mushaf._doc.juz_starts;
    if (!starts) throw new Error(mushaf._absent("juz"));
    if (!(number >= 1 && number <= starts.length)) throw new RangeError(`juz ${number}: there are ${starts.length}`);
    super(mushaf, starts[number - 1], number < starts.length ? starts[number] : mushaf.words.length);
    this.number = number;
  }
  toString() { return `juz ${this.number}`; }
}

// --- the muṣḥaf ---------------------------------------------------------------

/** One muṣḥaf file, out/mushaf/<key>.json. */
export class Mushaf {
  /** Where {@link Mushaf#checkForUpdate} looks by default. */
  static VERSION_URL = "https://quran.ws/version";

  constructor(doc) {
    if (doc?.format !== "quran-mushaf") throw new TypeError("not a quran-mushaf file");
    this._doc = doc;
    /** @type {string[]} */
    this.words = doc.words;
    this.key = doc.mushaf.key;
    this.nameEn = doc.mushaf.name_en;
    this.nameAr = doc.mushaf.name_ar;
    this.qariEn = doc.mushaf.qari_en ?? null;
    this.qariAr = doc.mushaf.qari_ar ?? null;
    this.countingSystem = doc.counting.system;
    this.basmalahCounted = doc.counting.basmalah_counted;
    /** @type {Sura[]} */
    this.suras = [];
    for (let n = 1; n <= 114; n++) this.suras.push(new Sura(this, n));
    this._suraFirstAyah = this.suras.map((s) => s._firstAyah);
    this._ayahEnds = new Map();
    const starts = doc.ayah_starts;
    for (let k = 0; k < starts.length; k++) {
      const end = k + 1 < starts.length ? starts[k + 1] : this.words.length;
      this._ayahEnds.set(end - 1, k);
    }
    const types = doc.mark_types.map((t) => new Mark(t.kind, t.side, t.sign));
    this._marksAt = new Map();
    for (const [pos, t] of doc.marks) {
      if (!this._marksAt.has(pos)) this._marksAt.set(pos, []);
      this._marksAt.get(pos).push(types[t]);
    }
    this._lineStartSet = new Set(doc.line_starts ?? []);
    this._numbersCache = null;
    this._foldCache = null;
  }

  // -- loading --

  /** Ḥafṣ, the riwāyah nearly every app uses, bundled with the package together with its font. */
  static async hafs() {
    const url = new URL("./data/hafs.json", import.meta.url);
    let m;
    if (url.protocol === "file:" && typeof process !== "undefined" && process.versions?.node) {
      const { readFile } = await import("node:fs/promises");
      m = new Mushaf(JSON.parse(await readFile(url, "utf8")));
    } else {
      m = new Mushaf(await (await fetch(url)).json());
    }
    m._fontUrl = new URL("./data/UthmanicHafs-v-3.0.ttf", import.meta.url).href;
    return m;
  }
  /**
   * The KFGQPC font this text is set in — the only one guaranteed to draw every
   * codepoint the words use. `url` is the file when the package has it
   * (bundled for Ḥafṣ); otherwise take `file` from `out/fonts/`.
   * @returns {{family: string, file: string, sha256: string, publisher: string, url: string | null}}
   */
  get font() {
    const f = this._doc.font;
    return { family: f.family, file: f.file, sha256: f.sha256, publisher: f.publisher, url: this._fontUrl ?? null };
  }
  /** A CSS `@font-face` rule for this muṣḥaf's font, from `url` or the one you pass. */
  fontFace(url = this.font.url) {
    return `@font-face { font-family: "${this.font.family}"; src: url("${url}") format("truetype"); }`;
  }
  /** Any of the seven riwāyāt: read `out/mushaf/<key>.json` (Node only).  In the browser use `Mushaf.fromJson(await res.json())`. */
  static async load(path) {
    const { readFile } = await import("node:fs/promises");
    return new Mushaf(JSON.parse(await readFile(path, "utf8")));
  }
  static fromJson(data) { return new Mushaf(typeof data === "string" ? JSON.parse(data) : data); }

  // -- what the file carries --

  /** @returns {string[]} */
  get layers() { return [...this._doc.layers.present]; }
  /** has("juz"), has("imlaei"), has("lines") … */
  has(layer) { return this._doc.layers.present.includes(layer); }
  _absent(layer) {
    const why = this._doc.layers.absent?.[layer] ?? "not in this file";
    return `${this.nameEn} has no ${layer} layer: ${why}`;
  }
  get counting() { return this._doc.counting; }
  get provenance() { return this._doc.provenance; }

  /**
   * Ask whether a newer build of this riwāyah has been published.
   *
   * The library never reaches the network on its own — nothing calls this for
   * you. Run it when it suits your app: at start-up without awaiting it, behind
   * a "check for updates" control, or on a timer. It resolves to `null` when
   * the check could not be made (offline, timeout, unexpected body), and never
   * rejects: a text this stable is not worth failing an app over.
   *
   * @param {string} [url] where to look; point at your own mirror if you host one
   * @param {number} [timeoutMs=5000]
   * @returns {Promise<?{edition: string, upToDate: boolean, localSource: ?string,
   *   latestSource: ?string, dataset: ?string, downloadUrl: string}>}
   */
  async checkForUpdate(url = Mushaf.VERSION_URL, timeoutMs = 5000) {
    let doc;
    try {
      const ctl = new AbortController();
      const t = setTimeout(() => ctl.abort(), timeoutMs);
      try {
        const r = await fetch(url, { signal: ctl.signal });
        if (!r.ok) return null;
        doc = await r.json();
      } finally { clearTimeout(t); }
    } catch { return null; }
    if (doc?.format !== "quran-version") return null;
    const latest = doc.editions?.[this.key];
    if (!latest) return null;
    const mine = this._doc.provenance?.text ?? {};
    return {
      edition: this.key,
      upToDate: mine.sha256 === latest.source_sha256,
      localSource: mine.package ?? null,
      latestSource: latest.source ?? null,
      dataset: doc.dataset ?? null,
      downloadUrl: `https://quran.ws/files/${latest.file}`,
    };
  }
  get wordCount() { return this.words.length; }
  get ayahCount() { return this._doc.ayah_starts.length; }
  get pageCount() { return this._doc.page_starts.length; }
  get lineCount() { return (this._doc.line_starts ?? []).length; }
  get juzCount() { return (this._doc.juz_starts ?? []).length; }

  // -- units by number --

  sura(number) {
    if (!(number >= 1 && number <= 114)) throw new RangeError(`sūrah ${number}: there are 114`);
    return this.suras[number - 1];
  }
  /** Āyah `number` of `sura` in this edition's own count. */
  ayah(sura, number) { return new Ayah(this, sura, number); }
  page(number) { return new Page(this, number); }
  juz(number) { return new Juz(this, number); }
  line(page, number) { return new Page(this, page).line(number); }
  /** Word `index` (1-based) of an āyah. */
  word(sura, ayah, index) { return new Ayah(this, sura, ayah).word(index); }
  /** Any run of positions, e.g. to render a selection. */
  span(start, end) {
    if (!(start >= 0 && start < end && end <= this.words.length)) {
      throw new RangeError(`span ${start}:${end} is outside the muṣḥaf`);
    }
    return new Span(this, start, end);
  }
  get all() { return new Span(this, 0, this.words.length); }
  /** @returns {Ayah[]} */
  get ayat() { const out = []; for (let k = 0; k < this.ayahCount; k++) out.push(Ayah._fromIndex(this, k)); return out; }
  /** @returns {Page[]} */
  get pages() { const out = []; for (let n = 1; n <= this.pageCount; n++) out.push(new Page(this, n)); return out; }
  /** @returns {Juz[]} */
  get ajza() { const out = []; for (let n = 1; n <= this.juzCount; n++) out.push(new Juz(this, n)); return out; }

  // -- units by position --

  wordAt(position) { return new Word(this, position); }
  ayahAt(position) { const k = indexOf(this._doc.ayah_starts, position); return k >= 0 ? Ayah._fromIndex(this, k) : null; }
  suraAt(position) { return this.suras[indexOf(this._doc.sura_starts, position)]; }
  pageAt(position) { return new Page(this, indexOf(this._doc.page_starts, position) + 1); }
  lineAt(position) {
    const starts = this._doc.line_starts;
    return starts ? Line._fromIndex(this, indexOf(starts, position)) : null;
  }
  juzAt(position) {
    const starts = this._doc.juz_starts;
    return starts ? new Juz(this, indexOf(starts, position) + 1) : null;
  }
  _linesBetween(start, end) {
    const starts = this._doc.line_starts;
    if (!starts) return [];
    const first = indexOf(starts, start), last = indexOf(starts, end - 1);
    const out = [];
    for (let i = first; i <= last; i++) out.push(Line._fromIndex(this, i));
    return out;
  }

  // -- the shared numbering --

  get _numbers() {
    if (!this._numbersCache) {
      const block = this._doc.numbering;
      const missing = new Set(block.missing);
      const joined = new Map(block.written_joined.map((j) => [j.position, j.numbers]));
      const runs = [];
      let n = 1;
      for (let pos = 0; pos < this.words.length; pos++) {
        while (missing.has(n)) n++;
        const [first, last] = joined.get(pos) ?? [n, n];
        runs.push([first, last]);
        n = last + 1;
      }
      this._numbersCache = runs;
    }
    return this._numbersCache;
  }
  /** The shared numbers this riwāyah does not read. @returns {Set<number>} */
  get missingNumbers() { return (this._missing ??= new Set(this._doc.numbering.missing)); }
  /** The shared number of the word at `position`. */
  numberAt(position) { return this._numbers[position][0]; }
  /** The printed word carrying a shared number; null where this muṣḥaf does not read it. */
  wordByNumber(number) {
    const runs = this._numbers;
    let lo = 0, hi = runs.length;
    while (lo < hi) { const mid = (lo + hi) >> 1; if (runs[mid][0] <= number) lo = mid + 1; else hi = mid; }
    const i = lo - 1;
    return i >= 0 && runs[i][0] <= number && number <= runs[i][1] ? new Word(this, i) : null;
  }

  // -- signs and search --

  /** Every āyah printed with ۩. @returns {Ayah[]} */
  sajdat() { return this._positionsWith("sajdah").map((p) => this.ayahAt(p)); }
  /** Every word printed with ۞ before it, as the release prints them. @returns {Word[]} */
  hizbMarks() { return this._positionsWith("hizb").map((p) => new Word(this, p)); }
  _positionsWith(kind) {
    return [...this._marksAt.entries()]
      .filter(([, ms]) => ms.some((mk) => mk.kind === kind))
      .map(([p]) => p)
      .sort((a, b) => a - b);
  }
  /**
   * Every place the words of `text` occur in sequence, matched on fold():
   * diacritics and hamza forms do not matter.
   * @returns {Span[]}
   */
  search(text) {
    const query = text.split(/\s+/).filter(Boolean).map(fold);
    if (!query.length || query.some((q) => !q)) return [];
    if (!this._foldCache) this._foldCache = this.words.map(fold);
    const folded = this._foldCache, n = query.length, out = [];
    for (let i = 0; i + n <= folded.length; i++) {
      if (folded[i] !== query[0]) continue;
      let ok = true;
      for (let j = 1; j < n; j++) if (folded[i + j] !== query[j]) { ok = false; break; }
      if (ok) out.push(new Span(this, i, i + n));
    }
    return out;
  }

  // -- internals --

  _suraOfAyahIndex(k) { return indexOf(this._suraFirstAyah, k); }
  _ayahNumber(k) { return k - this._suraFirstAyah[this._suraOfAyahIndex(k)] + 1; }
  toString() { return `Mushaf(${this.key})`; }
}

// --- āyah map ----------------------------------------------------------------

/**
 * Where a Kūfī āyah falls in one edition.  `relation` is same, merged, split
 * (then `ayahLast` is set), shifted or unnumbered (`ayah` is 0).
 */
export class AyahRef {
  constructor(sura, ayah, relation, ayahLast = null) {
    this.sura = sura; this.ayah = ayah; this.relation = relation; this.ayahLast = ayahLast;
    Object.freeze(this);
  }
  get key() { return this.ayahLast ? `${this.sura}:${this.ayah}-${this.ayahLast}` : `${this.sura}:${this.ayah}`; }
  toString() { return this.key; }
}

/** out/ayah-map.json: what a Ḥafṣ (Kūfī) reference is in every edition. */
export class AyahMap {
  constructor(doc) {
    if (doc?.format !== "quran-ayah-map") throw new TypeError("not a quran-ayah-map file");
    /** @type {string[]} */
    this.editions = doc.editions;
    this._rows = new Map(doc.ayat.map((r) => [`${r.sura}:${r.ayah}`, r]));
  }
  static async load(path) {
    const { readFile } = await import("node:fs/promises");
    return new AyahMap(JSON.parse(await readFile(path, "utf8")));
  }
  static fromJson(data) { return new AyahMap(typeof data === "string" ? JSON.parse(data) : data); }
  /** convert(2, 255, "warsh") → AyahRef { sura: 2, ayah: 253, relation: "split", ayahLast: 254 } */
  convert(sura, ayah, to) {
    const row = this._rows.get(`${sura}:${ayah}`);
    if (!row) throw new RangeError(`${sura}:${ayah} is not a Kūfī āyah`);
    const r = row[to];
    if (!r) throw new RangeError(`no edition "${to}"; editions are ${this.editions.join(", ")}`);
    return new AyahRef(r.sura, r.ayah, r.relation, r.ayah_last ?? null);
  }
  /** The reference in every edition. @returns {Record<string, AyahRef>} */
  all(sura, ayah) {
    return Object.fromEntries(this.editions.map((e) => [e, this.convert(sura, ayah, e)]));
  }
}

// --- word index --------------------------------------------------------------

/** One record of out/word-index.json: a shared number and what it is. */
export class IndexedWord {
  constructor(record) { this._r = record; }
  get number() { return this._r.number; }
  get sura() { return this._r.sura; }
  get index() { return this._r.index; }
  get key() { return this._r.key; }
  get uthmani() { return this._r.uthmani; }
  get simple() { return this._r.simple; }
  get rasm() { return this._r.rasm; }
  get pointed() { return this._r.pointed; }
  get status() { return this._r.status; }
  /** {sura, ayah, pos} in the Kūfī count, or null where Ḥafṣ lacks the word. */
  get hafs() { return this._r.hafs; }
  /** Āyah number per riwāyah. */
  get ayah() { return this._r.ayah; }
  /** Each riwāyah's own spelling; absent where it does not read the word. */
  get forms() { return this._r.forms; }
  get groups() { return this._r.groups ?? []; }
  get missing() { return this._r.missing ?? []; }
  get writtenJoined() { return this._r.written_joined ?? []; }
  /** How one riwāyah spells it; null where it does not read the word. */
  form(riwayah) { return this._r.forms[riwayah] ?? null; }
  get raw() { return this._r; }
  toString() { return `${this.number} ${this.uthmani}`; }
}

/** out/word-index.json: the numbering shared by all seven muṣḥafs. */
export class WordIndex {
  constructor(doc) {
    if (doc?.format !== "quran-word-index") throw new TypeError("not a quran-word-index file");
    /** @type {string[]} */
    this.mushafs = doc.mushafs;
    this.total = doc.total;
    this._words = doc.words;
    this._byHafs = null;
    this._bySimple = null;
  }
  static async load(path) {
    const { readFile } = await import("node:fs/promises");
    return new WordIndex(JSON.parse(await readFile(path, "utf8")));
  }
  static fromJson(data) { return new WordIndex(typeof data === "string" ? JSON.parse(data) : data); }
  word(number) {
    if (!(number >= 1 && number <= this.total)) throw new RangeError(`number ${number}: the numbering is 1 … ${this.total}`);
    return new IndexedWord(this._words[number - 1]);
  }
  /** By Ḥafṣ coordinates: sūrah, āyah in the Kūfī count, 1-based word. */
  find(sura, ayah, index) {
    if (!this._byHafs) {
      this._byHafs = new Map();
      for (const r of this._words) {
        const h = r.hafs;
        if (h) { const k = `${h.sura}:${h.ayah}:${h.pos}`; if (!this._byHafs.has(k)) this._byHafs.set(k, r); }
      }
    }
    const r = this._byHafs.get(`${sura}:${ayah}:${index}`);
    return r ? new IndexedWord(r) : null;
  }
  /** Every number whose folded spelling equals `text`, folded. @returns {IndexedWord[]} */
  search(text) {
    if (!this._bySimple) {
      this._bySimple = new Map();
      for (const r of this._words) {
        const k = fold(r.uthmani);
        if (!this._bySimple.has(k)) this._bySimple.set(k, []);
        this._bySimple.get(k).push(r);
      }
    }
    return (this._bySimple.get(fold(text)) ?? []).map((r) => new IndexedWord(r));
  }
  /** Every number the riwāyāt spell in more than one way. @returns {IndexedWord[]} */
  differing() { return this._words.filter((r) => r.groups).map((r) => new IndexedWord(r)); }
  get length() { return this.total; }
  *[Symbol.iterator]() { for (const r of this._words) yield new IndexedWord(r); }
}
