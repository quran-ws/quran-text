// quran-text — read the muṣḥaf files of the quran-text dataset.
//
//     let m = try Mushaf.hafs()                                   // bundled Ḥafṣ
//     let m = try Mushaf.load(URL(fileURLWithPath: "warsh.json")) // another riwāyah
//     m.ayah(2, 255).text
//     m.ayah(2, 255).render(marks: .all, ayahMarks: true)
//     m.page(3).lines
//     m.juz(30)?.firstAyah?.key          // "78:1"
//
// Everything is a slice of one `words` array.  A Span is a slice with `text`
// and `render`; Surah, Ayah, Page, Line and Juz are spans that know their
// place.  Positions are 0-based indices into `words`; sūrah, āyah, page,
// line and juz numbers are 1-based, as printed.  Āyah numbers are in this
// edition's own count; use AyahMap to convert between editions.
//
// Lookups by number are checked with `precondition`, like array subscripts:
// asking for āyah 287 of sūrah 2 is a programming error, not a runtime
// condition.  Layers a file may lack (juz, lines, imlāʾī) come back as `nil`.
//
// No dependencies.  Foundation only.

import Foundation

public let ayahMarkSign = "\u{06DD}"

private let arabicIndic = Array("٠١٢٣٤٥٦٧٨٩")

/// The end-of-āyah sign with its number, as the muṣḥaf prints it: ۝٢٥٥
public func ayahMark(_ number: Int) -> String {
    ayahMarkSign + String(String(number).map { arabicIndic[Int(String($0))!] })
}

private let foldAlef: Set<Unicode.Scalar> = {
    var s: Set<Unicode.Scalar> = ["\u{0670}", "\u{0671}", "\u{0623}", "\u{0625}", "\u{0622}"]
    for v in 0x0870...0x0882 { s.insert(Unicode.Scalar(v)!) }
    return s
}()
private let foldYeh: Set<Unicode.Scalar> = ["\u{06D2}", "\u{06D1}", "\u{0649}"]

private func isDropped(_ v: UInt32) -> Bool {
    v == 0x0640 || v == 0x0888
        || (0x0610...0x061A).contains(v) || (0x064B...0x065F).contains(v)
        || (0x06D6...0x06DC).contains(v) || (0x06DF...0x06E8).contains(v)
        || (0x06EA...0x06ED).contains(v) || (0x08CA...0x08FF).contains(v)
}

/// Reduce a word to plain letters for matching: no harakah, no waqf
/// marks, one alif, one yāʾ.  For search only — it is not a spelling.
public func fold(_ text: String) -> String {
    var out = String.UnicodeScalarView()
    for u in text.unicodeScalars {
        if foldAlef.contains(u) { out.append("\u{0627}") }
        else if foldYeh.contains(u) { out.append("\u{064A}") }
        else if isDropped(u.value) { continue }
        else { out.append(u) }
    }
    return String(out)
}

/// Index of the unit that contains `position` (-1 before the first).
private func indexOf(_ starts: [Int], _ position: Int) -> Int {
    var lo = 0, hi = starts.count
    while lo < hi {
        let mid = (lo + hi) >> 1
        if starts[mid] <= position { lo = mid + 1 } else { hi = mid }
    }
    return lo - 1
}

/// The KFGQPC font a muṣḥaf's text is set in — the only one guaranteed to draw
/// every codepoint the words use.  `url` is the file when the package has it
/// (bundled for Ḥafṣ); register it with `CTFontManagerRegisterFontsForURL`
/// and use `family` as the font name.
public struct Font: Sendable {
    public let family: String
    /// The file name; the copy lives under data/fonts/ in the dataset.
    public let file: String
    public let sha256: String
    public let publisher: String
    public let url: URL?
}

public enum MarkKind: String, CaseIterable, Sendable {
    case waqf, division, sajdah, sah
    case sajdahLine = "sajdah_line"
    case raisedDot = "raised_dot"
}

public enum MarkSide: String, Sendable { case before, after }

/// A sign printed against a word.
public struct Mark: Hashable, Sendable {
    public let kind: MarkKind
    public let side: MarkSide
    public let sign: String
}

extension Set where Element == MarkKind {
    /// Every kind of sign.
    public static var all: Set<MarkKind> { Set(MarkKind.allCases) }
}

/// One printed word and everything the muṣḥaf says about it.
public struct Word: CustomStringConvertible {
    let m: Mushaf
    public let position: Int

    init(_ m: Mushaf, _ position: Int) {
        precondition(position >= 0 && position < m.words.count, "position \(position) is outside the muṣḥaf")
        self.m = m
        self.position = position
    }

    public var text: String { m.words[position] }
    /// Plain modern spelling, Ḥafṣ only; nil elsewhere.
    public var rasm_imlai: String? { m.rasm_imlaiColumn?[position] }
    public var surah: Surah { m.surahAt(position) }
    /// The āyah this word is in; nil for the unnumbered basmalah.
    public var ayah: Ayah? { m.ayahAt(position) }
    /// 1-based position within the āyah; nil when unnumbered.
    public var index: Int? { ayah.map { position - $0.start + 1 } }
    public var page: Page { m.pageAt(position) }
    public var line: Line? { m.lineAt(position) }
    public var juz: Juz? { m.juzAt(position) }
    /// The shared number: the same word in every riwāyah.
    public var number: Int { m.numbers[position].first }
    /// Equal to `number` except where this muṣḥaf writes two numbers as one word.
    public var numberLast: Int { m.numbers[position].last }
    public var marks: [Mark] { m.marksAt[position] ?? [] }
    public func hasMark(_ kind: MarkKind) -> Bool { marks.contains { $0.kind == kind } }

    /// The same word in another riwāyah, by the shared number; nil where it does not read it.
    public func to(_ other: Mushaf) -> Word? { other.wordByNumber(number) }

    /// The word with its signs: ۞ before, waqf and ۩ after.
    public func render(marks kinds: Set<MarkKind> = .all) -> String {
        var before = "", after = ""
        for mk in marks where kinds.contains(mk.kind) {
            if mk.side == .before { before += mk.sign + " " } else { after += mk.sign }
        }
        return before + text + after
    }

    public var description: String { text }
}

/// A run of positions start … end-1 of one muṣḥaf.
public class Span: Sequence {
    let m: Mushaf
    public let start: Int
    public let end: Int

    init(_ m: Mushaf, _ start: Int, _ end: Int) {
        self.m = m
        self.start = start
        self.end = end
    }

    public var mushaf: Mushaf { m }
    public var count: Int { end - start }
    public var words: ArraySlice<String> { m.words[start..<end] }
    public var wordList: [Word] { (start..<end).map { Word(m, $0) } }
    public func makeIterator() -> IndexingIterator<[Word]> { wordList.makeIterator() }

    /// The words joined with spaces, without any sign.
    public var text: String { words.joined(separator: " ") }

    /// The text as the muṣḥaf prints it, with what you ask for.
    ///
    /// `marks`: the kinds of sign to print (`.all` for every kind).
    /// `ayahMarks` appends ۝ with the āyah number after each āyah that ends
    /// inside the span.  `lines` breaks the text where the printed lines break.
    public func render(marks kinds: Set<MarkKind> = [], ayahMarks: Bool = false, lines: Bool = false) -> String {
        var out = ""
        for position in start..<end {
            if lines, position != start, m.lineStartSet.contains(position) { out += "\n" }
            else if position != start { out += " " }
            var token = m.words[position]
            for mk in m.marksAt[position] ?? [] where kinds.contains(mk.kind) {
                token = mk.side == .before ? mk.sign + " " + token : token + mk.sign
            }
            out += token
            if ayahMarks, let k = m.ayahEnds[position] { out += " " + ayahMark(m.ayahNumber(k)) }
        }
        return out
    }

    /// Every numbered āyah with at least one word in the span.
    public var ayahs: [Ayah] {
        let first = Swift.max(indexOf(m.ayahStarts, start), 0)
        let last = indexOf(m.ayahStarts, end - 1)
        return first > last ? [] : (first...last).map { Ayah(m, index: $0) }
    }
    public var firstAyah: Ayah? { ayahs.first }
    public var lastAyah: Ayah? { ayahs.last }

    public var surahs: [Surah] {
        Array(m.surahs[indexOf(m.surahStarts, start)...indexOf(m.surahStarts, end - 1)])
    }
    public var pages: [Page] {
        (indexOf(m.pageStarts, start)...indexOf(m.pageStarts, end - 1)).map { Page(m, $0 + 1) }
    }
    /// The page the span starts on.
    public var page: Page { m.pageAt(start) }
    public var juz: Juz? { m.juzAt(start) }

    /// Every sign inside the span, with the word it is printed on.
    public var marks: [(word: Word, mark: Mark)] {
        (start..<end).flatMap { p in (m.marksAt[p] ?? []).map { (Word(m, p), $0) } }
    }

    /// The index-th word of the span, 1-based.
    public func word(_ index: Int) -> Word {
        precondition(index >= 1 && index <= count, "word \(index): the span has \(count) words")
        return Word(m, start + index - 1)
    }
}

/// Where an āyah falls in another riwāyah.  `relation`: same (one āyah, the
/// same words), merged (one āyah holding more), split (several āyāt), shifted
/// (one āyah, boundaries crossing), unnumbered (the basmalah printed without a
/// number), missing (no word of it).
public struct AyahMatch: CustomStringConvertible {
    public let ayahs: [Ayah]
    public let relation: String
    public var first: Ayah? { ayahs.first }
    public var last: Ayah? { ayahs.last }
    /// "2:253-254"
    public var key: String {
        guard let a = ayahs.first, let b = ayahs.last else { return "" }
        return a == b ? a.key : "\(a.key)-\(b.number)"
    }
    public var description: String { "\(key.isEmpty ? "-" : key) (\(relation))" }
}

/// One numbered āyah, in this edition's own count.
public final class Ayah: Span, CustomStringConvertible, Equatable {
    public let surah: Surah
    public let number: Int
    /// 0-based ordinal of the āyah in the muṣḥaf.
    public let index: Int

    convenience init(_ m: Mushaf, surah: Int, number: Int) {
        let s = m.surah(surah)
        precondition(number >= 1 && number <= s.ayahCount,
                     "\(s.nameEn) has \(s.ayahCount) āyāt in \(m.nameEn), not \(number)")
        self.init(m, surah: s, number: number, index: s.firstAyahIndex + number - 1)
    }

    convenience init(_ m: Mushaf, index k: Int) {
        let s = m.surahs[m.surahOfAyahIndex(k)]
        self.init(m, surah: s, number: k - s.firstAyahIndex + 1, index: k)
    }

    private init(_ m: Mushaf, surah: Surah, number: Int, index: Int) {
        self.surah = surah
        self.number = number
        self.index = index
        let starts = m.ayahStarts
        super.init(m, starts[index], index + 1 < starts.count ? starts[index + 1] : m.words.count)
    }

    /// "2:255"
    public var key: String { "\(surah.number):\(number)" }
    /// The printed line the āyah starts on.
    public var line: Line? { m.lineAt(start) }
    /// Every printed line the āyah touches.
    public var lines: [Line] { m.linesBetween(start, end) }
    public var rasm_imlai: [String?]? { m.rasm_imlaiColumn.map { Array($0[start..<end]) } }
    public var hasSajdah: Bool { marks.contains { $0.mark.kind == .sajdah } }
    /// ۝٢٥٥
    public var marker: String { ayahMark(number) }
    /// The shared numbers of this āyah's words.
    public var numbers: Set<Int> {
        let first = m.numbers[start].first, last = m.numbers[end - 1].last
        return Set((first...last).filter { !m.missingNumbers.contains($0) })
    }

    /// This āyah in another riwāyah: `hafs.ayah(2, 255).to(warsh)` → 2:253-254, split.
    /// Computed from the shared numbering, so it works between any two riwāyāt.
    public func to(_ other: Mushaf) -> AyahMatch {
        let mine = numbers
        var hits: [Ayah] = []
        var unnumbered = false
        for n in mine.sorted() {
            guard let w = other.wordByNumber(n) else { continue }
            if let a = w.ayah {
                if hits.last != a { hits.append(a) }
            } else {
                unnumbered = true
            }
        }
        if hits.isEmpty { return AyahMatch(ayahs: [], relation: unnumbered ? "unnumbered" : "missing") }
        if hits.count > 1 { return AyahMatch(ayahs: hits, relation: "split") }
        let theirs = hits[0].numbers
        let relation = theirs == mine ? "same" : theirs.isSuperset(of: mine) ? "merged" : "shifted"
        return AyahMatch(ayahs: hits, relation: relation)
    }

    public func next() -> Ayah? { index + 1 < m.ayahCount ? Ayah(m, index: index + 1) : nil }
    public func previous() -> Ayah? { index > 0 ? Ayah(m, index: index - 1) : nil }

    public static func == (a: Ayah, b: Ayah) -> Bool { a.m === b.m && a.index == b.index }
    public var description: String { key }
}

public final class Surah: Span, CustomStringConvertible {
    public let number: Int
    public let nameAr: String
    public let nameEn: String
    public let revelation: String
    public let hasBasmalah: Bool
    public let ayahCount: Int
    let firstAyahIndex: Int

    init(_ m: Mushaf, _ number: Int, _ info: [String: Any]) {
        self.number = number
        nameAr = info["name_ar"] as! String
        nameEn = info["name_en"] as! String
        revelation = info["revelation"] as! String
        hasBasmalah = info["has_basmalah"] as! Bool
        ayahCount = info["ayah_count"] as! Int
        firstAyahIndex = info["first_ayah"] as! Int
        let starts = m.surahStarts
        super.init(m, starts[number - 1], number < starts.count ? starts[number] : m.words.count)
    }

    public override var ayahs: [Ayah] { (1...ayahCount).map { Ayah(m, surah: number, number: $0) } }
    public func ayah(_ number: Int) -> Ayah { Ayah(m, surah: self.number, number: number) }
    /// The basmalah where it is printed unnumbered before āyah 1 (Warsh,
    /// Qālūn, Dūrī, Sūsī at al-Fātiḥah); nil otherwise.
    public var basmalah: Span? {
        let first = m.ayahStarts[firstAyahIndex]
        return first > start ? Span(m, start, first) : nil
    }
    public var firstPage: Page { page }
    public var lastPage: Page { m.pageAt(end - 1) }
    public var description: String { "\(number) \(nameEn)" }
}

public final class Page: Span, CustomStringConvertible {
    public let number: Int

    init(_ m: Mushaf, _ number: Int) {
        let starts = m.pageStarts
        precondition(number >= 1 && number <= starts.count, "page \(number): \(m.nameEn) has \(starts.count) pages")
        self.number = number
        super.init(m, starts[number - 1], number < starts.count ? starts[number] : m.words.count)
    }

    public var lines: [Line] { m.linesBetween(start, end) }
    public func line(_ number: Int) -> Line {
        let all = lines
        precondition(number >= 1 && number <= all.count, "line \(number): page \(self.number) has \(all.count) lines")
        return all[number - 1]
    }
    public func next() -> Page? { number < m.pageCount ? Page(m, number + 1) : nil }
    public func previous() -> Page? { number > 1 ? Page(m, number - 1) : nil }
    public var description: String { "page \(number)" }
}

/// One printed line.  Reconstructed, not read: see `layers.derived.line`.
public final class Line: Span, CustomStringConvertible {
    private let ofPage: Page
    /// Within the page, 1-based.
    public let number: Int
    /// Within the muṣḥaf, 0-based.
    public let index: Int

    init(_ m: Mushaf, index: Int) {
        let starts = m.lineStarts!
        ofPage = m.pageAt(starts[index])
        number = index - indexOf(starts, ofPage.start) + 1
        self.index = index
        super.init(m, starts[index], index + 1 < starts.count ? starts[index + 1] : m.words.count)
    }

    public override var page: Page { ofPage }
    public var description: String { "page \(ofPage.number), line \(number)" }
}

public final class Juz: Span, CustomStringConvertible {
    public let number: Int

    init(_ m: Mushaf, _ number: Int, starts: [Int]) {
        precondition(number >= 1 && number <= starts.count, "juz \(number): there are \(starts.count)")
        self.number = number
        super.init(m, starts[number - 1], number < starts.count ? starts[number] : m.words.count)
    }

    public var description: String { "juz \(number)" }
}

// MARK: - the muṣḥaf

/// One muṣḥaf file, `data/mushaf/<key>.json`.
public final class Mushaf {
    public let words: [String]
    public let key: String
    public let nameEn: String
    public let nameAr: String
    public let qiraahEn: String?
    public let qiraahAr: String?
    public let countingSystem: String
    /// The counting system this muṣḥaf's qāriʾ is associated with. Compare with
    /// ``countingSystem``, the system this edition measures onto: for Dūrī and
    /// Sūsī they differ.
    public let countingSystemAssociatedWithQari: String
    public let basmalahCounted: Bool
    public private(set) var surahs: [Surah] = []
    /// The `counting` block of the file.
    public let counting: [String: Any]
    /// The `provenance` block of the file.
    public let provenance: [String: Any]
    /// The layers the file carries, e.g. `["surahs", "ayahs", "pages", "lines", "marks", "juz", "rasm_imlai"]`.
    public let layers: [String]
    private let absentLayers: [String: String]

    let rasm_imlaiColumn: [String?]?
    let surahStarts: [Int]
    let ayahStarts: [Int]
    let pageStarts: [Int]
    let lineStarts: [Int]?
    let juzStarts: [Int]?
    let lineStartSet: Set<Int>
    private var surahFirstAyah: [Int] = []
    var ayahEnds: [Int: Int] = [:]
    var marksAt: [Int: [Mark]] = [:]
    private let numbering: [String: Any]
    private let fontBlock: [String: Any]
    private var numbersCache: [(first: Int, last: Int)]?
    private var foldCache: [String]?

    public enum Error: Swift.Error { case notAMushafFile, badField(String) }

    public init(json doc: [String: Any]) throws {
        guard doc["format"] as? String == "quran-mushaf" else { throw Error.notAMushafFile }
        func field<T>(_ name: String) throws -> T {
            guard let v = doc[name] as? T else { throw Error.badField(name) }
            return v
        }
        words = try field("words")
        let info: [String: Any] = try field("mushaf")
        key = info["key"] as! String
        nameEn = info["name_en"] as! String
        nameAr = info["name_ar"] as! String
        qiraahEn = info["qiraah_en"] as? String
        qiraahAr = info["qiraah_ar"] as? String
        counting = try field("counting")
        countingSystem = counting["system"] as! String
        countingSystemAssociatedWithQari = counting["system_associated_with_qari"] as! String
        basmalahCounted = counting["basmalah_counted"] as! Bool
        provenance = try field("provenance")
        let layersBlock: [String: Any] = try field("layers")
        layers = layersBlock["present"] as! [String]
        absentLayers = layersBlock["absent"] as? [String: String] ?? [:]
        rasm_imlaiColumn = (doc["rasm_imlai"] as? [Any]).map { $0.map { $0 as? String } }
        surahStarts = try field("surah_starts")
        ayahStarts = try field("ayah_starts")
        pageStarts = try field("page_starts")
        lineStarts = doc["line_starts"] as? [Int]
        juzStarts = doc["juz_starts"] as? [Int]
        lineStartSet = Set(lineStarts ?? [])
        numbering = try field("numbering")
        fontBlock = try field("font")

        let surahInfo: [[String: Any]] = try field("surahs")
        surahs = (1...114).map { Surah(self, $0, surahInfo[$0 - 1]) }
        surahFirstAyah = surahs.map { $0.firstAyahIndex }
        for k in ayahStarts.indices {
            let end = k + 1 < ayahStarts.count ? ayahStarts[k + 1] : words.count
            ayahEnds[end - 1] = k
        }
        let types: [[String: Any]] = try field("mark_types")
        let marks = types.map { Mark(kind: MarkKind(rawValue: $0["kind"] as! String)!,
                                     side: MarkSide(rawValue: $0["side"] as! String)!,
                                     sign: $0["sign"] as! String) }
        let pairs: [[Int]] = try field("marks")
        for pair in pairs { marksAt[pair[0], default: []].append(marks[pair[1]]) }
    }

    // MARK: loading

    public convenience init(data: Data) throws {
        guard let doc = try JSONSerialization.jsonObject(with: data) as? [String: Any] else { throw Error.notAMushafFile }
        try self.init(json: doc)
    }

    /// Any of the seven riwāyāt: `data/mushaf/<key>.json`.
    public static func load(_ url: URL) throws -> Mushaf { try Mushaf(data: Data(contentsOf: url)) }

    /// Ḥafṣ, the riwāyah nearly every app uses, bundled with the package together with its font.
    public static func hafs() throws -> Mushaf {
        let m = try load(Bundle.module.url(forResource: "hafs", withExtension: "json")!)
        m.fontURL = Bundle.module.url(forResource: "UthmanicHafs-v-3.0", withExtension: "ttf")
        return m
    }

    private var fontURL: URL?

    /// The font to ship with this text; see `Font`.
    public var font: Font {
        let f = fontBlock
        return Font(family: f["family"] as! String, file: f["file"] as! String,
                    sha256: f["sha256"] as! String, publisher: f["publisher"] as! String, url: fontURL)
    }

    // MARK: what the file carries

    /// `has("juz")`, `has("rasm_imlai")`, `has("lines")` …
    public func has(_ layer: String) -> Bool { layers.contains(layer) }
    /// Why a layer is absent, e.g. Bazzī's juz.
    public func whyAbsent(_ layer: String) -> String? { absentLayers[layer] }
    public var wordCount: Int { words.count }
    public var ayahCount: Int { ayahStarts.count }
    public var pageCount: Int { pageStarts.count }
    public var lineCount: Int { lineStarts?.count ?? 0 }
    public var juzCount: Int { juzStarts?.count ?? 0 }

    // MARK: units by number

    public func surah(_ number: Int) -> Surah {
        precondition(number >= 1 && number <= 114, "sūrah \(number): there are 114")
        return surahs[number - 1]
    }
    /// Āyah `number` of `surah` in this edition's own count.
    public func ayah(_ surah: Int, _ number: Int) -> Ayah { Ayah(self, surah: surah, number: number) }
    public func page(_ number: Int) -> Page { Page(self, number) }
    /// nil when the file has no juz layer (Bazzī); see `whyAbsent("juz")`.
    public func juz(_ number: Int) -> Juz? { juzStarts.map { Juz(self, number, starts: $0) } }
    public func line(_ page: Int, _ number: Int) -> Line { Page(self, page).line(number) }
    /// Word `index` (1-based) of an āyah.
    public func word(_ surah: Int, _ ayah: Int, _ index: Int) -> Word { Ayah(self, surah: surah, number: ayah).word(index) }
    /// Any run of positions, e.g. to render a selection.
    public func span(_ start: Int, _ end: Int) -> Span {
        precondition(start >= 0 && start < end && end <= words.count, "span \(start):\(end) is outside the muṣḥaf")
        return Span(self, start, end)
    }
    public var all: Span { Span(self, 0, words.count) }
    public var ayahs: [Ayah] { (0..<ayahCount).map { Ayah(self, index: $0) } }
    public var pages: [Page] { (1...pageCount).map { Page(self, $0) } }
    public var ajza: [Juz] { juzStarts.map { s in (1...s.count).map { Juz(self, $0, starts: s) } } ?? [] }

    // MARK: units by position

    public func wordAt(_ position: Int) -> Word { Word(self, position) }
    public func ayahAt(_ position: Int) -> Ayah? {
        let k = indexOf(ayahStarts, position)
        return k >= 0 ? Ayah(self, index: k) : nil
    }
    public func surahAt(_ position: Int) -> Surah { surahs[indexOf(surahStarts, position)] }
    public func pageAt(_ position: Int) -> Page { Page(self, indexOf(pageStarts, position) + 1) }
    public func lineAt(_ position: Int) -> Line? { lineStarts.map { Line(self, index: indexOf($0, position)) } }
    public func juzAt(_ position: Int) -> Juz? { juzStarts.map { Juz(self, indexOf($0, position) + 1, starts: $0) } }
    func linesBetween(_ start: Int, _ end: Int) -> [Line] {
        guard let starts = lineStarts else { return [] }
        return (indexOf(starts, start)...indexOf(starts, end - 1)).map { Line(self, index: $0) }
    }

    // MARK: the shared numbering

    var numbers: [(first: Int, last: Int)] {
        if let c = numbersCache { return c }
        let missing = Set(numbering["missing"] as! [Int])
        var joined: [Int: [Int]] = [:]
        for j in numbering["written_joined"] as! [[String: Any]] { joined[j["position"] as! Int] = (j["numbers"] as! [Int]) }
        var runs: [(first: Int, last: Int)] = []
        runs.reserveCapacity(words.count)
        var n = 1
        for position in words.indices {
            while missing.contains(n) { n += 1 }
            let run = joined[position].map { ($0[0], $0[1]) } ?? (n, n)
            runs.append(run)
            n = run.1 + 1
        }
        numbersCache = runs
        return runs
    }
    /// The shared numbers this riwāyah does not read.
    public private(set) lazy var missingNumbers: Set<Int> = Set(numbering["missing"] as! [Int])
    /// The shared number of the word at `position`.
    public func numberAt(_ position: Int) -> Int { numbers[position].first }
    /// The printed word carrying a shared number; nil where this muṣḥaf does not read it.
    public func wordByNumber(_ number: Int) -> Word? {
        let runs = numbers
        var lo = 0, hi = runs.count
        while lo < hi { let mid = (lo + hi) >> 1; if runs[mid].first <= number { lo = mid + 1 } else { hi = mid } }
        let i = lo - 1
        return i >= 0 && runs[i].first <= number && number <= runs[i].last ? Word(self, i) : nil
    }

    // MARK: signs and search

    /// Every āyah printed with ۩.
    public func sajdat() -> [Ayah] { positionsWith(.sajdah).compactMap { ayahAt($0) } }
    /// Every word printed with ۞ before it, as the release prints them.
    public func divisionMarks() -> [Word] { positionsWith(.division).map { Word(self, $0) } }
    private func positionsWith(_ kind: MarkKind) -> [Int] {
        marksAt.filter { $0.value.contains { $0.kind == kind } }.keys.sorted()
    }
    /// Every place the words of `text` occur in sequence, matched on `fold`:
    /// harakah and hamzah forms do not matter.
    public func search(_ text: String) -> [Span] {
        let query = text.split(whereSeparator: { $0.isWhitespace }).map { fold(String($0)) }
        guard !query.isEmpty, !query.contains("") else { return [] }
        if foldCache == nil { foldCache = words.map(fold) }
        let folded = foldCache!, n = query.count
        guard folded.count >= n else { return [] }
        var out: [Span] = []
        for i in 0...(folded.count - n) where folded[i] == query[0] {
            if (1..<n).allSatisfy({ folded[i + $0] == query[$0] }) { out.append(Span(self, i, i + n)) }
        }
        return out
    }

    func surahOfAyahIndex(_ k: Int) -> Int { indexOf(surahFirstAyah, k) }
    func ayahNumber(_ k: Int) -> Int { k - surahFirstAyah[surahOfAyahIndex(k)] + 1 }
}

// MARK: - āyah map

/// Where a Kūfī āyah falls in one edition.  `relation` is same, merged,
/// split (then `ayahLast` is set), shifted or unnumbered (`ayah` is 0).
public struct MappedAyah: Hashable, CustomStringConvertible, Sendable {
    public let surah: Int
    public let ayah: Int
    public let relation: String
    public let ayahLast: Int?
    /// "2:253-254"
    public var key: String { ayahLast.map { "\(surah):\(ayah)-\($0)" } ?? "\(surah):\(ayah)" }
    public var description: String { key }
}

/// `data/ayah-map.json`: what a Ḥafṣ (Kūfī) reference is in every edition.
public final class AyahMap {
    public let editions: [String]
    private let rows: [String: [String: Any]]

    public enum Error: Swift.Error { case notAnAyahMapFile, notAKufiAyah(String), noEdition(String) }

    public init(json doc: [String: Any]) throws {
        guard doc["format"] as? String == "quran-ayah-map", let ayahs = doc["ayahs"] as? [[String: Any]] else {
            throw Error.notAnAyahMapFile
        }
        editions = doc["editions"] as! [String]
        var rows: [String: [String: Any]] = [:]
        for r in ayahs { rows["\(r["surah"] as! Int):\(r["ayah"] as! Int)"] = r }
        self.rows = rows
    }
    public convenience init(data: Data) throws {
        guard let doc = try JSONSerialization.jsonObject(with: data) as? [String: Any] else { throw Error.notAnAyahMapFile }
        try self.init(json: doc)
    }
    public static func load(_ url: URL) throws -> AyahMap { try AyahMap(data: Data(contentsOf: url)) }

    /// `convert(2, 255, to: "warsh")` → `MappedAyah(surah: 2, ayah: 253, relation: "split", ayahLast: 254)`
    public func convert(_ surah: Int, _ ayah: Int, to edition: String) throws -> MappedAyah {
        guard let row = rows["\(surah):\(ayah)"] else { throw Error.notAKufiAyah("\(surah):\(ayah)") }
        guard let r = row[edition] as? [String: Any] else { throw Error.noEdition(edition) }
        return MappedAyah(surah: r["surah"] as! Int, ayah: r["ayah"] as! Int,
                       relation: r["relation"] as! String, ayahLast: r["ayah_last"] as? Int)
    }
    /// The reference in every edition.
    public func all(_ surah: Int, _ ayah: Int) throws -> [String: MappedAyah] {
        var out: [String: MappedAyah] = [:]
        for e in editions { out[e] = try convert(surah, ayah, to: e) }
        return out
    }
}

// MARK: - word index

/// One record of `data/word-index.json`: a shared number and what it is.
public struct IndexedWord: CustomStringConvertible {
    public let raw: [String: Any]
    public var number: Int { raw["number"] as! Int }
    public var surah: Int { raw["surah"] as! Int }
    public var index: Int { raw["index"] as! Int }
    public var key: String { raw["key"] as! String }
    public var rasm_uthmani: String { raw["rasm_uthmani"] as! String }
    public var plain: String { raw["plain"] as! String }
    public var rasm: String { raw["rasm"] as! String }
    public var pointed: String { raw["pointed"] as! String }
    public var status: String { raw["status"] as! String }
    /// `(surah, ayah, position)` in the Kūfī count, or nil where Ḥafṣ lacks the word.
    public var hafs: (surah: Int, ayah: Int, position: Int)? {
        (raw["hafs"] as? [String: Int]).map { ($0["surah"]!, $0["ayah"]!, $0["position"]!) }
    }
    /// Āyah number per riwāyah.
    public var ayah: [String: Int] { raw["ayah"] as! [String: Int] }
    /// Each riwāyah's own spelling; absent where it does not read the word.
    public var forms: [String: String] { raw["forms"] as! [String: String] }
    public var groups: [[String: Any]] { raw["groups"] as? [[String: Any]] ?? [] }
    public var missing: [String] { raw["missing"] as? [String] ?? [] }
    public var writtenJoined: [String] { raw["written_joined"] as? [String] ?? [] }
    /// How one riwāyah spells it; nil where it does not read the word.
    public func form(_ riwayah: String) -> String? { forms[riwayah] }
    public var description: String { "\(number) \(rasm_uthmani)" }
}

/// `data/word-index.json`: the numbering shared by all seven muṣḥafs.
public final class WordIndex: Sequence {
    public let mushafs: [String]
    public let total: Int
    private let records: [[String: Any]]
    private var byHafs: [String: [String: Any]]?
    private var byPlain: [String: [[String: Any]]]?

    public enum Error: Swift.Error { case notAWordIndexFile }

    public init(json doc: [String: Any]) throws {
        guard doc["format"] as? String == "quran-word-index", let words = doc["words"] as? [[String: Any]] else {
            throw Error.notAWordIndexFile
        }
        mushafs = doc["mushafs"] as! [String]
        total = doc["total"] as! Int
        records = words
    }
    public convenience init(data: Data) throws {
        guard let doc = try JSONSerialization.jsonObject(with: data) as? [String: Any] else { throw Error.notAWordIndexFile }
        try self.init(json: doc)
    }
    public static func load(_ url: URL) throws -> WordIndex { try WordIndex(data: Data(contentsOf: url)) }

    public func word(_ number: Int) -> IndexedWord {
        precondition(number >= 1 && number <= total, "number \(number): the numbering is 1 … \(total)")
        return IndexedWord(raw: records[number - 1])
    }
    /// By Ḥafṣ coordinates: sūrah, āyah in the Kūfī count, 1-based word.
    public func find(_ surah: Int, _ ayah: Int, _ index: Int) -> IndexedWord? {
        if byHafs == nil {
            var by: [String: [String: Any]] = [:]
            for r in records {
                if let h = r["hafs"] as? [String: Int] {
                    let k = "\(h["surah"]!):\(h["ayah"]!):\(h["position"]!)"
                    if by[k] == nil { by[k] = r }
                }
            }
            byHafs = by
        }
        return byHafs!["\(surah):\(ayah):\(index)"].map { IndexedWord(raw: $0) }
    }
    /// Every number whose folded spelling equals `text`, folded.
    public func search(_ text: String) -> [IndexedWord] {
        if byPlain == nil {
            var by: [String: [[String: Any]]] = [:]
            for r in records { by[fold(r["rasm_uthmani"] as! String), default: []].append(r) }
            byPlain = by
        }
        return (byPlain![fold(text)] ?? []).map { IndexedWord(raw: $0) }
    }
    /// Every number the riwāyāt spell in more than one way.
    public func differing() -> [IndexedWord] { records.filter { $0["groups"] != nil }.map { IndexedWord(raw: $0) } }
    public var count: Int { total }
    public func makeIterator() -> AnyIterator<IndexedWord> {
        var it = records.makeIterator()
        return AnyIterator { it.next().map { IndexedWord(raw: $0) } }
    }
}
