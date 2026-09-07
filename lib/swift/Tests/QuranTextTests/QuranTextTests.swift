import XCTest
@testable import QuranText

// Run from lib/swift with the dataset built:  swift test
private let out = URL(fileURLWithPath: #filePath).deletingLastPathComponent()
    .appendingPathComponent("../../../../out").standardized
private func mushaf(_ key: String) throws -> Mushaf {
    try Mushaf.load(out.appendingPathComponent("mushaf/\(key).json"))
}

final class QuranTextTests: XCTestCase {
    static let hafs = try! mushaf("hafs")
    static let warsh = try! mushaf("warsh")
    static let bazzi = try! mushaf("bazzi")
    var hafs: Mushaf { QuranTextTests.hafs }

    func testAyahTextLayersAndRendering() {
        let a = hafs.ayah(2, 255)
        XCTAssertEqual(a.key, "2:255")
        XCTAssertEqual(a.count, 50)
        XCTAssertEqual([a.page.number, a.juz!.number, a.line!.number], [42, 3, 8])
        XCTAssertTrue(a.text.hasPrefix("ٱللَّهُ لَآ إِلَٰهَ"))
        XCTAssertTrue(a.render(ayahMarks: true).hasSuffix(" ۝٢٥٥"))
        // Waqf signs are combining marks: look at unicodeScalars, not Characters.
        XCTAssertTrue(a.render(marks: .all).unicodeScalars.contains("\u{06DA}"))
        XCTAssertTrue(a.render(marks: [.waqf]).unicodeScalars.contains("\u{06DA}"))
        XCTAssertFalse(a.render(marks: [.division]).unicodeScalars.contains("\u{06DA}"))
        XCTAssertFalse(a.render().unicodeScalars.contains("\u{06DA}"))
        XCTAssertEqual(a.next()?.key, "2:256")
        XCTAssertEqual(hafs.ayah(2, 286).next()?.key, "3:1")
        XCTAssertNil(hafs.ayah(1, 1).previous())
    }

    func testSurahPageLineJuz() {
        let s = hafs.surah(112)
        XCTAssertEqual(s.ayahs.count, 4)
        XCTAssertEqual(s.render(ayahMarks: true).unicodeScalars.filter { $0 == "\u{06DD}" }.count, 4)
        XCTAssertNil(s.basmalah)
        let p = hafs.page(3)
        XCTAssertEqual(p.lines.count, 15)
        XCTAssertEqual([p.ayahs.first!.key, p.ayahs.last!.key], ["2:6", "2:16"])
        XCTAssertEqual(p.render(lines: true).split(separator: "\n").count, 15)
        XCTAssertEqual(p.line(1).text, p.lines[0].text)
        XCTAssertEqual(hafs.juz(30)?.firstAyah?.key, "78:1")
        XCTAssertEqual(hafs.juz(30)?.pages.last?.number, 604)
        XCTAssertEqual(hafs.surah(2).lastPage.number, 49)
        XCTAssertEqual(hafs.line(1, 3).ayahs.map { $0.key }, ["1:3", "1:4"])
    }

    func testWordsMarksNumbering() {
        let w = hafs.word(1, 4, 1)
        XCTAssertEqual(w.text, "مَٰلِكِ")
        XCTAssertEqual(w.number, 11)
        XCTAssertEqual(w.rasm_imlai, "مالك")
        XCTAssertEqual(w.index, 1)
        XCTAssertEqual(hafs.sajdat().prefix(2).map { $0.key }, ["7:206", "13:15"])
        XCTAssertEqual(hafs.sajdat().count, 15)
        XCTAssertTrue(hafs.ayah(7, 206).hasSajdah)
        XCTAssertEqual(hafs.divisionMarks().count, 199)
        XCTAssertEqual(hafs.divisionMarks()[0].render(), "۞ إِنَّ")
        XCTAssertEqual(hafs.numberAt(73948), 73950)
        XCTAssertEqual(hafs.wordAt(73948).numberLast, 73951)
        XCTAssertNil(hafs.wordByNumber(25685))
        XCTAssertEqual(hafs.wordByNumber(73951)?.text, "وَأَلَّوِ")
        XCTAssertEqual(hafs.wordByNumber(11)?.text, "مَٰلِكِ")
    }

    func testUnnumberedBasmalahAndAbsentLayers() {
        let warsh = Self.warsh, bazzi = Self.bazzi
        XCTAssertFalse(warsh.basmalahCounted)
        XCTAssertEqual(warsh.surah(1).basmalah?.count, 4)
        XCTAssertNil(warsh.wordAt(0).ayah)
        XCTAssertNil(warsh.ayahAt(3))
        XCTAssertEqual(warsh.ayah(1, 1).count, 4)
        XCTAssertEqual(warsh.surah(1).ayahs.count, 7)
        XCTAssertTrue(warsh.ayah(2, 253).render(ayahMarks: true).hasSuffix("۝٢٥٣"))
        XCTAssertNil(bazzi.juz(1))
        XCTAssertNotNil(bazzi.whyAbsent("juz"))
        XCTAssertNil(bazzi.wordAt(5).juz)
        XCTAssertFalse(bazzi.has("juz"))
        XCTAssertNil(bazzi.wordAt(5).rasm_imlai)
    }

    func testSearch() {
        let hits = hafs.search("مالك يوم الدين")
        XCTAssertEqual(hits.count, 1)
        XCTAssertEqual(hits[0].firstAyah?.key, "1:4")
        XCTAssertEqual(fold("ٱلۡحَمۡدُ"), "الحمد")
        XCTAssertEqual(ayahMark(255), "۝٢٥٥")
    }

    func testBundledHafs() throws {
        let m = try Mushaf.hafs()
        XCTAssertEqual(m.key, "hafs")
        XCTAssertEqual(m.wordCount, hafs.wordCount)
        XCTAssertEqual(m.font.family, "KFGQPC HAFS Uthmanic Script")
        XCTAssertNotNil(m.font.url)
        XCTAssertEqual(Self.warsh.font.file, "out/fonts/UthmanicWarsh-v-3.0.ttf")
    }

    func testToAnotherRiwayah() {
        let warsh = Self.warsh, bazzi = Self.bazzi
        let m = hafs.ayah(2, 255).to(warsh)
        XCTAssertEqual(m.key, "2:253-254")
        XCTAssertEqual(m.relation, "split")
        XCTAssertEqual(warsh.ayah(2, 253).to(hafs).key, "2:255")
        XCTAssertEqual(hafs.ayah(1, 1).to(warsh).relation, "unnumbered")
        XCTAssertEqual(hafs.ayah(57, 24).to(warsh).relation, "shifted")
        XCTAssertEqual(hafs.ayah(112, 1).to(bazzi).relation, "same")
        XCTAssertNil(hafs.word(57, 24, 10).to(warsh))
        XCTAssertEqual(warsh.word(2, 253, 3).to(hafs)?.text, "إِلَٰهَ")
    }

    func testAyahMap() throws {
        let map = try AyahMap.load(out.appendingPathComponent("ayah-map.json"))
        let r = try map.convert(2, 255, to: "warsh")
        XCTAssertEqual(r, MappedAyah(surah: 2, ayah: 253, relation: "split", ayahLast: 254))
        XCTAssertEqual(r.key, "2:253-254")
        XCTAssertEqual(try map.all(1, 1)["warsh"]?.relation, "unnumbered")
        XCTAssertThrowsError(try map.convert(2, 255, to: "nope"))
    }

    func testWordIndex() throws {
        let idx = try WordIndex.load(out.appendingPathComponent("word-index.json"))
        XCTAssertEqual(idx.word(11).form("warsh"), "مَلِكِ")
        XCTAssertEqual(idx.find(2, 255, 3)?.rasm_uthmani, "إِلَٰهَ")
        XCTAssertTrue(idx.search("مالك").contains { $0.number == 11 })
        XCTAssertEqual(idx.differing().count, 53134)
    }
}
