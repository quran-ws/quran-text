import ws.quran.qurantext.AyahMap
import ws.quran.qurantext.MappedAyah
import ws.quran.qurantext.MarkKind
import ws.quran.qurantext.Mushaf
import ws.quran.qurantext.WordIndex
import ws.quran.qurantext.ayahMark
import ws.quran.qurantext.fold
import java.io.File
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith
import kotlin.test.assertFalse
import kotlin.test.assertNotNull
import kotlin.test.assertNull
import kotlin.test.assertTrue

// Run from lib/kotlin with the dataset built:  gradle test
class QuranTextTest {
    companion object {
        val data = File(System.getProperty("quran.data") ?: "../../data")
        val hafs = Mushaf.load(File(data, "mushaf/hafs.json"))
        val warsh = Mushaf.load(File(data, "mushaf/warsh.json"))
        val bazzi = Mushaf.load(File(data, "mushaf/bazzi.json"))
    }

    @Test fun ayahTextLayersAndRendering() {
        val a = hafs.ayah(2, 255)
        assertEquals("2:255", a.key)
        assertEquals(50, a.size)
        assertEquals(listOf(42, 3, 8), listOf(a.page.number, a.juz!!.number, a.line!!.number))
        assertTrue(a.text.startsWith("ٱللَّهُ لَآ إِلَٰهَ"))
        assertTrue(a.render(ayahMarks = true).endsWith(" ۝٢٥٥"))
        assertTrue(a.render(marks = MarkKind.all).contains("ۚ"))
        assertTrue(a.render(marks = setOf(MarkKind.waqf)).contains("ۚ"))
        assertFalse(a.render(marks = setOf(MarkKind.division)).contains("ۚ"))
        assertFalse(a.render().contains("ۚ"))
        assertEquals("2:256", a.next()!!.key)
        assertEquals("3:1", hafs.ayah(2, 286).next()!!.key)
        assertNull(hafs.ayah(1, 1).previous())
        assertFailsWith<IllegalArgumentException> { hafs.ayah(2, 287) }
    }

    @Test fun surahPageLineJuz() {
        val s = hafs.surah(112)
        assertEquals(4, s.ayahs.size)
        assertEquals(4, s.render(ayahMarks = true).count { it == '۝' })
        assertNull(s.basmalah)
        val p = hafs.page(3)
        assertEquals(15, p.lines.size)
        assertEquals(listOf("2:6", "2:16"), listOf(p.ayahs.first().key, p.ayahs.last().key))
        assertEquals(15, p.render(lines = true).split("\n").size)
        assertEquals(p.lines[0].text, p.line(1).text)
        assertEquals("78:1", hafs.juz(30).firstAyah!!.key)
        assertEquals(604, hafs.juz(30).pages.last().number)
        assertEquals(49, hafs.surah(2).lastPage.number)
        assertEquals(listOf("1:3", "1:4"), hafs.line(1, 3).ayahs.map { it.key })
    }

    @Test fun wordsMarksNumbering() {
        val w = hafs.word(1, 4, 1)
        assertEquals(listOf("مَٰلِكِ", 11, "مالك", 1), listOf(w.text, w.number, w.rasm_imlai, w.index))
        assertEquals(listOf("7:206", "13:15"), hafs.sajdat().take(2).map { it.key })
        assertEquals(15, hafs.sajdat().size)
        assertTrue(hafs.ayah(7, 206).hasSajdah)
        assertEquals(199, hafs.divisionMarks().size)
        assertEquals("۞ إِنَّ", hafs.divisionMarks()[0].render())
        assertEquals(73950, hafs.numberAt(73948))
        assertEquals(73951, hafs.wordAt(73948).numberLast)
        assertNull(hafs.wordByNumber(25685))
        assertEquals("وَأَلَّوِ", hafs.wordByNumber(73951)!!.text)
        assertEquals("مَٰلِكِ", hafs.wordByNumber(11)!!.text)
    }

    @Test fun unnumberedBasmalahAndAbsentLayers() {
        assertFalse(warsh.basmalahCounted)
        assertEquals(4, warsh.surah(1).basmalah!!.size)
        assertNull(warsh.wordAt(0).ayah)
        assertNull(warsh.ayahAt(3))
        assertEquals(4, warsh.ayah(1, 1).size)
        assertEquals(7, warsh.surah(1).ayahs.size)
        assertTrue(warsh.ayah(2, 253).render(ayahMarks = true).endsWith("۝٢٥٣"))
        val e = assertFailsWith<IllegalStateException> { bazzi.juz(1) }
        assertTrue(e.message!!.contains("no juz layer"))
        assertNotNull(bazzi.whyAbsent("juz"))
        assertNull(bazzi.wordAt(5).juz)
        assertFalse(bazzi.has("juz"))
        assertNull(bazzi.wordAt(5).rasm_imlai)
    }

    @Test fun hizbAndItsParts() {
        // Ḥafṣ divides the ḥizb into four; Warsh into eight; Bazzī's print was not read.
        assertEquals(listOf(60, 240, 0), listOf(hafs.hizbCount, hafs.rubuAlHizbCount, hafs.thumnCount))
        assertEquals(listOf(60, 0, 480), listOf(warsh.hizbCount, warsh.rubuAlHizbCount, warsh.thumnCount))
        assertEquals("1:1", hafs.hizb(1).firstAyah!!.key)
        assertEquals("2:75", hafs.hizb(2).firstAyah!!.key)
        assertEquals("87:1", hafs.hizb(60).firstAyah!!.key)
        assertEquals(60, hafs.hizbs.size)
        assertEquals(hafs.wordCount, hafs.hizbs.sumOf { it.size })
        assertEquals(240, hafs.rubuAlHizbs.size)
        assertEquals(480, warsh.thumns.size)
        assertTrue(hafs.thumns.isEmpty())
        val q = hafs.rubuAlHizb(2)
        assertEquals(listOf("2:26", 1, 2), listOf(q.firstAyah!!.key, q.hizb.number, q.numberInHizb))
        assertEquals(4, hafs.rubuAlHizb(240).numberInHizb)
        val a = hafs.ayah(2, 255)
        assertEquals(listOf(5, 17), listOf(a.hizb!!.number, a.rubuAlHizb!!.number))
        assertNull(a.thumn)
        val t = warsh.thumn(480)
        assertEquals(listOf("106:1", 60, 8), listOf(t.firstAyah!!.key, t.hizb.number, t.numberInHizb))
        assertEquals(1, warsh.wordAt(0).thumn!!.number)
        assertEquals("thumn 9", warsh.thumn(9).toString())
        // Where the print and the layout CSV start a juz at different āyāt, each layer keeps its own.
        assertEquals(listOf("3:92", "3:93"), listOf(hafs.juz(4).firstAyah!!.key, hafs.hizb(7).firstAyah!!.key))
        assertTrue(hafs.has("hizb") && hafs.has("rubu_al_hizb") && !hafs.has("thumn"))
        val e = assertFailsWith<IllegalStateException> { hafs.thumn(1) }
        assertTrue(e.message!!.contains("no thumn layer: this muṣḥaf divides the ḥizb into 4"))
        val b = assertFailsWith<IllegalStateException> { bazzi.hizb(1) }
        assertTrue(b.message!!.contains("no hizb layer: no printed muṣḥaf"))
        assertNull(bazzi.wordAt(5).hizb)
        val r = assertFailsWith<IllegalArgumentException> { hafs.hizb(61) }
        assertEquals("hizb 61: there are 60", r.message)
    }

    @Test fun search() {
        val hits = hafs.search("مالك يوم الدين")
        assertEquals(1, hits.size)
        assertEquals("1:4", hits[0].firstAyah!!.key)
        assertEquals("الحمد", fold("ٱلۡحَمۡدُ"))
        assertEquals("۝٢٥٥", ayahMark(255))
    }

    @Test fun bundledHafs() {
        val m = Mushaf.hafs()
        assertEquals("hafs", m.key)
        assertEquals(hafs.wordCount, m.wordCount)
        assertEquals("KFGQPC HAFS Uthmanic Script", m.font.family)
        assertNotNull(m.font.open())
        assertEquals("UthmanicWarsh-v-3.0.ttf", warsh.font.file)
    }

    @Test fun toAnotherRiwayah() {
        val m = hafs.ayah(2, 255).to(warsh)
        assertEquals("2:253-254", m.key)
        assertEquals("split", m.relation)
        assertEquals("2:255", warsh.ayah(2, 253).to(hafs).key)
        assertEquals("unnumbered", hafs.ayah(1, 1).to(warsh).relation)
        assertEquals("shifted", hafs.ayah(57, 24).to(warsh).relation)
        assertEquals("same", hafs.ayah(112, 1).to(bazzi).relation)
        assertNull(hafs.word(57, 24, 10).to(warsh))
        assertEquals("إِلَٰهَ", warsh.word(2, 253, 3).to(hafs)!!.text)
    }

    @Test fun ayahMap() {
        val map = AyahMap.load(File(data, "ayah-map.json"))
        assertEquals(MappedAyah(2, 253, "split", 254), map.convert(2, 255, "warsh"))
        assertEquals("2:253-254", map.convert(2, 255, "warsh").key)
        assertEquals("unnumbered", map.all(1, 1)["warsh"]!!.relation)
        assertFailsWith<IllegalArgumentException> { map.convert(2, 255, "nope") }
    }

    @Test fun wordIndex() {
        val idx = WordIndex.load(File(data, "word-index.json"))
        assertEquals("مَلِكِ", idx.word(11).form("warsh"))
        assertEquals("إِلَٰهَ", idx.find(2, 255, 3)!!.rasm_uthmani)
        assertTrue(idx.search("مالك").any { it.number == 11 })
        assertEquals(53128, idx.differing().size)
        val listed = setOf("rasm_variant", "alif_variant", "word_boundary", "partial")
        assertEquals(269, idx.differing().count { it.status in listed })
        assertEquals(277, idx.count { it.status in listed })
        assertEquals(idx.total, hafs.numberingTotal)
        assertEquals(idx.total, warsh.numberingTotal)
        // The heading over sūrahs 2–114 is printed but not in words.
        assertTrue(hafs.surah(2).hasBasmalah)
        assertNull(hafs.surah(2).basmalah)
        assertNull(warsh.surah(2).basmalah)
    }
}
