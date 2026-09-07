import org.quranpedia.qurantext.AyahMap
import org.quranpedia.qurantext.MappedAyah
import org.quranpedia.qurantext.MarkKind
import org.quranpedia.qurantext.Mushaf
import org.quranpedia.qurantext.WordIndex
import org.quranpedia.qurantext.ayahMark
import org.quranpedia.qurantext.fold
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
        val out = File(System.getProperty("quran.out") ?: "../../out")
        val hafs = Mushaf.load(File(out, "mushaf/hafs.json"))
        val warsh = Mushaf.load(File(out, "mushaf/warsh.json"))
        val bazzi = Mushaf.load(File(out, "mushaf/bazzi.json"))
    }

    @Test fun ayahTextLayersAndRendering() {
        val a = hafs.ayah(2, 255)
        assertEquals("2:255", a.key)
        assertEquals(50, a.size)
        assertEquals(listOf(42, 3, 8), listOf(a.page.number, a.juz!!.number, a.line!!.number))
        assertTrue(a.text.startsWith("ٱللَّهُ لَآ إِلَٰهَ"))
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
        assertEquals("۞ إِنَّ", hafs.divisionMarks()[0].render())
        assertEquals(73950, hafs.numberAt(73948))
        assertEquals(73951, hafs.wordAt(73948).numberLast)
        assertNull(hafs.wordByNumber(25685))
        assertEquals("وَأَلَّوِ", hafs.wordByNumber(73951)!!.text)
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
        assertEquals("out/fonts/UthmanicWarsh-v-3.0.ttf", warsh.font.file)
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
        val map = AyahMap.load(File(out, "ayah-map.json"))
        assertEquals(MappedAyah(2, 253, "split", 254), map.convert(2, 255, "warsh"))
        assertEquals("2:253-254", map.convert(2, 255, "warsh").key)
        assertEquals("unnumbered", map.all(1, 1)["warsh"]!!.relation)
        assertFailsWith<IllegalArgumentException> { map.convert(2, 255, "nope") }
    }

    @Test fun wordIndex() {
        val idx = WordIndex.load(File(out, "word-index.json"))
        assertEquals("مَلِكِ", idx.word(11).form("warsh"))
        assertEquals("إِلَٰهَ", idx.find(2, 255, 3)!!.rasm_uthmani)
        assertTrue(idx.search("مالك").any { it.number == 11 })
        assertEquals(53134, idx.differing().size)
    }
}
