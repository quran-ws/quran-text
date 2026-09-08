/** quran-text — read the muṣḥaf files of the quran-text dataset. */

export type Layer = "surahs" | "ayahs" | "pages" | "lines" | "juz" | "marks" | "rasm_imlai";
export type MarkKind = "waqf" | "division" | "sajdah";
export type Relation = "same" | "merged" | "split" | "shifted" | "unnumbered";

export interface RenderOptions {
  /** `true` for every sign, or the kinds you want. Default: none. */
  marks?: boolean | MarkKind[];
  /** Append ۝ with the āyah number after each āyah that ends inside the span. */
  ayahMarks?: boolean;
  /** Break the text where the printed lines break. */
  lines?: boolean;
}

export const AYAH_MARK: string;
/** The end-of-āyah sign with its number, as the muṣḥaf prints it: ۝٢٥٥ */
export function ayahMark(number: number): string;
/** Plain letters for matching: no harakah, one alif, one yāʾ. Not a spelling. */
export function fold(text: string): string;

export class Mark {
  readonly kind: MarkKind;
  readonly side: "before" | "after";
  readonly sign: string;
}

export class Word {
  readonly position: number;
  readonly text: string;
  /** Plain modern spelling, Ḥafṣ only; null elsewhere. */
  readonly rasm_imlai: string | null;
  readonly surah: Surah;
  /** null for the unnumbered basmalah. */
  readonly ayah: Ayah | null;
  /** 1-based position within the āyah; null when unnumbered. */
  readonly index: number | null;
  readonly page: Page;
  readonly line: Line | null;
  readonly juz: Juz | null;
  /** The shared number: the same word in every riwāyah. */
  readonly number: number;
  readonly numberLast: number;
  readonly marks: Mark[];
  hasMark(kind: MarkKind): boolean;
  /** The same word in another riwāyah; null where it does not read it. */
  to(other: Mushaf): Word | null;
  /** The word with its signs: ۞ before, waqf and ۩ after. */
  render(marks?: boolean | MarkKind[]): string;
  toString(): string;
}

export class Span implements Iterable<Word> {
  readonly start: number;
  readonly end: number;
  readonly mushaf: Mushaf;
  readonly length: number;
  readonly words: string[];
  readonly wordList: Word[];
  /** The words joined with spaces, without any sign. */
  readonly text: string;
  render(options?: RenderOptions): string;
  /** Every numbered āyah with at least one word in the span. */
  readonly ayahs: Ayah[];
  readonly firstAyah: Ayah | null;
  readonly lastAyah: Ayah | null;
  readonly surahs: Surah[];
  readonly pages: Page[];
  /** The page the span starts on. */
  readonly page: Page;
  readonly juz: Juz | null;
  readonly marks: { word: Word; mark: Mark }[];
  /** The index-th word of the span, 1-based. */
  word(index: number): Word;
  [Symbol.iterator](): Iterator<Word>;
}

/** Where an āyah falls in another riwāyah. */
export class AyahMatch {
  readonly ayahs: Ayah[];
  readonly relation: Relation | "missing";
  readonly first: Ayah | null;
  readonly last: Ayah | null;
  /** "2:253-254" */
  readonly key: string;
}

export class Ayah extends Span {
  /** The shared numbers of this āyah's words. */
  readonly numbers: Set<number>;
  /** This āyah in another riwāyah, from the shared numbering. */
  to(other: Mushaf): AyahMatch;
  readonly surah: Surah;
  /** In this edition's own count. */
  readonly number: number;
  /** "2:255" */
  readonly key: string;
  /** 0-based ordinal of the āyah in the muṣḥaf. */
  readonly index: number;
  readonly line: Line | null;
  readonly lines: Line[];
  readonly rasm_imlai: (string | null)[] | null;
  readonly hasSajdah: boolean;
  /** ۝٢٥٥ */
  readonly marker: string;
  next(): Ayah | null;
  previous(): Ayah | null;
  equals(other: unknown): boolean;
}

export class Surah extends Span {
  readonly number: number;
  readonly nameAr: string;
  readonly nameEn: string;
  readonly revelation: "makki" | "madani";
  readonly hasBasmalah: boolean;
  readonly ayahCount: number;
  readonly ayahs: Ayah[];
  ayah(number: number): Ayah;
  /** The unnumbered basmalah before āyah 1, where the edition prints it so. */
  readonly basmalah: Span | null;
  readonly firstPage: Page;
  readonly lastPage: Page;
}

export class Page extends Span {
  readonly number: number;
  readonly lines: Line[];
  line(number: number): Line;
  next(): Page | null;
  previous(): Page | null;
}

/** One printed line. Reconstructed, not read: see layers.derived.line. */
export class Line extends Span {
  readonly page: Page;
  /** Within the page, 1-based. */
  readonly number: number;
  /** Within the muṣḥaf, 0-based. */
  readonly index: number;
}

export class Juz extends Span {
  readonly number: number;
}

export interface Font {
  /** e.g. "KFGQPC HAFS Uthmanic Script" — the name to use in CSS or a Typeface. */
  family: string;
  /** The file name; the copy lives under data/fonts/ in the dataset. */
  file: string;
  sha256: string;
  publisher: string;
  /** The font file when the package bundles it (Ḥafṣ); null otherwise. */
  url: string | null;
}

export class Mushaf {
  constructor(doc: object);
  /** The KFGQPC font this text is set in; ship it with the text. */
  readonly font: Font;
  /** A CSS @font-face rule for this muṣḥaf's font. */
  fontFace(url?: string): string;
  /** Ḥafṣ, bundled with the package. */
  static hafs(): Promise<Mushaf>;
  /** Any of the seven riwāyāt, Node only. In the browser: `Mushaf.fromJson(await res.json())`. */
  static load(path: string): Promise<Mushaf>;
  static fromJson(data: string | object): Mushaf;

  readonly words: string[];
  readonly key: string;
  readonly nameEn: string;
  readonly nameAr: string;
  readonly qiraahEn: string | null;
  readonly qiraahAr: string | null;
  readonly countingSystem: string;
  readonly basmalahCounted: boolean;
  readonly surahs: Surah[];

  readonly layers: Layer[];
  has(layer: Layer): boolean;
  readonly counting: Record<string, unknown>;
  readonly provenance: Record<string, unknown>;
  /** Where {@link Mushaf.checkForUpdate} looks by default. */
  static VERSION_URL: string;
  /**
   * Ask whether a newer build of this riwāyah exists. Never called for you,
   * never rejects: resolves to `null` when the check could not be made.
   */
  checkForUpdate(url?: string, timeoutMs?: number): Promise<UpdateStatus | null>;
  readonly wordCount: number;
  readonly ayahCount: number;
  readonly pageCount: number;
  readonly lineCount: number;
  readonly juzCount: number;

  surah(number: number): Surah;
  /** Āyah `number` of `surah` in this edition's own count. */
  ayah(surah: number, number: number): Ayah;
  page(number: number): Page;
  juz(number: number): Juz;
  line(page: number, number: number): Line;
  /** Word `index` (1-based) of an āyah. */
  word(surah: number, ayah: number, index: number): Word;
  span(start: number, end: number): Span;
  readonly all: Span;
  readonly ayahs: Ayah[];
  readonly pages: Page[];
  readonly ajza: Juz[];

  wordAt(position: number): Word;
  ayahAt(position: number): Ayah | null;
  surahAt(position: number): Surah;
  pageAt(position: number): Page;
  lineAt(position: number): Line | null;
  juzAt(position: number): Juz | null;

  /** The shared number of the word at `position`. */
  numberAt(position: number): number;
  /** null where this muṣḥaf does not read the number. */
  wordByNumber(number: number): Word | null;
  readonly missingNumbers: Set<number>;

  /** Every āyah printed with ۩. */
  sajdat(): Ayah[];
  /** Every word printed with ۞ before it. */
  divisionMarks(): Word[];
  /** Every place the words of `text` occur in sequence, matched on fold(). */
  search(text: string): Span[];
}

export class MappedAyah {
  readonly surah: number;
  readonly ayah: number;
  readonly relation: Relation;
  readonly ayahLast: number | null;
  /** "2:253-254" */
  readonly key: string;
}

export class AyahMap {
  constructor(doc: object);
  static load(path: string): Promise<AyahMap>;
  static fromJson(data: string | object): AyahMap;
  readonly editions: string[];
  /** convert(2, 255, "warsh") → { surah: 2, ayah: 253, ayahLast: 254, relation: "split" } */
  convert(surah: number, ayah: number, to: string): MappedAyah;
  all(surah: number, ayah: number): Record<string, MappedAyah>;
}

export interface HafsCoordinates { surah: number; ayah: number; position: number; }

export class IndexedWord {
  readonly number: number;
  readonly surah: number;
  readonly index: number;
  readonly key: string;
  readonly rasm_uthmani: string;
  readonly plain: string;
  readonly rasm: string;
  readonly pointed: string;
  readonly status: "identical" | "diacritic_variant" | "dotting_variant" | "alif_variant" | "rasm_variant" | "word_boundary" | "partial";
  readonly hafs: HafsCoordinates | null;
  readonly ayah: Record<string, number>;
  readonly forms: Record<string, string>;
  readonly groups: { text: string; riwayahs: string[] }[];
  readonly missing: string[];
  readonly writtenJoined: string[];
  form(riwayah: string): string | null;
  readonly raw: Record<string, unknown>;
}

export class WordIndex implements Iterable<IndexedWord> {
  constructor(doc: object);
  static load(path: string): Promise<WordIndex>;
  static fromJson(data: string | object): WordIndex;
  readonly mushafs: string[];
  readonly total: number;
  readonly length: number;
  word(number: number): IndexedWord;
  /** By Ḥafṣ coordinates: sūrah, āyah in the Kūfī count, 1-based word. */
  find(surah: number, ayah: number, index: number): IndexedWord | null;
  search(text: string): IndexedWord[];
  differing(): IndexedWord[];
  [Symbol.iterator](): Iterator<IndexedWord>;
}

/** What {@link Mushaf.checkForUpdate} found. */
export interface UpdateStatus {
  edition: string;
  upToDate: boolean;
  localSource: string | null;
  latestSource: string | null;
  dataset: string | null;
  downloadUrl: string;
}
