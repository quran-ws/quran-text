// quran-text — read the muṣḥaf files of the quran-text dataset.
//
//     val m = Mushaf.hafs()                                     // bundled Ḥafṣ
//     val m = Mushaf.load(File("warsh.json"))                   // another riwāyah
//     m.ayah(2, 255).text
//     m.ayah(2, 255).render(marks = MarkKind.all, ayahMarks = true)
//     m.page(3).lines
//     m.juz(30).firstAyah?.key          // "78:1"
//
// Everything is a slice of one `words` list.  A Span is a slice with `text`
// and `render()`; Surah, Ayah, Page, Line and Juz are spans that know their
// place.  Positions are 0-based indices into `words`; sūrah, āyah, page,
// line and juz numbers are 1-based, as printed.  Āyah numbers are in this
// edition's own count; use AyahMap to convert between editions.
//
// Depends on org.json only (built into Android).

package ws.quran.qurantext

import org.json.JSONArray
import org.json.JSONObject
import java.io.File

const val AYAH_MARK = "۝"

private const val ARABIC_INDIC = "٠١٢٣٤٥٦٧٨٩"

/** The end-of-āyah sign with its number, as the muṣḥaf prints it: ۝٢٥٥ */
fun ayahMark(number: Int): String =
    AYAH_MARK + number.toString().map { ARABIC_INDIC[it - '0'] }.joinToString("")

private val FOLD_ALEF = Regex("[\\u0670\\u0671\\u0623\\u0625\\u0622\\u0870-\\u0882]")
private val FOLD_YEH = Regex("[\\u06D2\\u06D1\\u0649]")
private val FOLD_DROP = Regex("[\\u0640\\u0610-\\u061A\\u064B-\\u065F\\u06D6-\\u06DC\\u06DF-\\u06E8\\u06EA-\\u06ED\\u08CA-\\u08FF\\u0888]")

/**
 * Reduce a word to plain letters for matching: no harakah, no waqf marks,
 * one alif, one yāʾ.  For search only — it is not a spelling of anything.
 */
fun fold(text: String): String =
    text.replace(FOLD_ALEF, "\u0627").replace(FOLD_YEH, "\u064A").replace(FOLD_DROP, "")

/** Index of the unit that contains [position] (-1 before the first). */
private fun indexOf(starts: IntArray, position: Int): Int {
    var lo = 0
    var hi = starts.size
    while (lo < hi) {
        val mid = (lo + hi) ushr 1
        if (starts[mid] <= position) lo = mid + 1 else hi = mid
    }
    return lo - 1
}

private fun JSONArray.toIntArray(): IntArray = IntArray(length()) { getInt(it) }
private fun JSONArray.toStringList(): List<String> = List(length()) { getString(it) }

/**
 * The KFGQPC font a muṣḥaf's text is set in — the only one guaranteed to draw
 * every codepoint the words use.  [open] gives the bytes when the library
 * bundles the font (Ḥafṣ): write them to a file and `Typeface.createFromFile`.
 */
data class Font(val family: String, val file: String, val sha256: String, val publisher: String) {
    /** The font bytes when bundled, else null. */
    fun open(): java.io.InputStream? = Font::class.java.getResourceAsStream("/" + file.substringAfterLast('/'))
}

// The names are the strings the data uses, so `valueOf` reads them directly.
@Suppress("EnumEntryName")
enum class MarkKind {
    waqf, division, sajdah, sajdah_line;

    companion object {
        /** Every kind of sign. */
        val all: Set<MarkKind> = entries.toSet()
    }
}

enum class MarkSide { before, after }

/** A sign printed against a word. */
data class Mark(val kind: MarkKind, val side: MarkSide, val sign: String) {
    override fun toString() = sign
}

/** One printed word and everything the muṣḥaf says about it. */
class Word internal constructor(private val m: Mushaf, val position: Int) {
    init {
        require(position in m.words.indices) { "position $position is outside the muṣḥaf" }
    }

    val text: String get() = m.words[position]
    /** Plain modern spelling, Ḥafṣ only; null elsewhere. */
    val rasm_imlai: String? get() = m.rasm_imlaiColumn?.get(position)
    val surah: Surah get() = m.surahAt(position)
    /** The āyah this word is in; null for the unnumbered basmalah. */
    val ayah: Ayah? get() = m.ayahAt(position)
    /** 1-based position within the āyah; null when unnumbered. */
    val index: Int? get() = ayah?.let { position - it.start + 1 }
    val page: Page get() = m.pageAt(position)
    val line: Line? get() = m.lineAt(position)
    val juz: Juz? get() = m.juzAt(position)
    /** The shared number: the same word in every riwāyah. */
    val number: Int get() = m.numbers[position].first
    /** Equal to [number] except where this muṣḥaf writes two numbers as one word. */
    val numberLast: Int get() = m.numbers[position].last
    val marks: List<Mark> get() = m.marksAt[position] ?: emptyList()
    fun hasMark(kind: MarkKind) = marks.any { it.kind == kind }

    /** The same word in another riwāyah, by the shared number; null where it does not read it. */
    fun to(other: Mushaf): Word? = other.wordByNumber(number)

    /** The word with its signs: ۞ before, waqf and ۩ after. */
    fun render(marks: Set<MarkKind> = MarkKind.all): String {
        var before = ""
        var after = ""
        for (mk in this.marks) {
            if (mk.kind !in marks) continue
            if (mk.side == MarkSide.before) before += mk.sign + " " else after += mk.sign
        }
        return before + text + after
    }

    override fun toString() = text
}

/** A run of positions start … end-1 of one muṣḥaf. */
open class Span internal constructor(internal val m: Mushaf, val start: Int, val end: Int) : Iterable<Word> {
    val mushaf: Mushaf get() = m
    val size: Int get() = end - start
    val words: List<String> get() = m.words.subList(start, end)
    val wordList: List<Word> get() = (start until end).map { Word(m, it) }
    override fun iterator() = wordList.iterator()

    /** The words joined with spaces, without any sign. */
    val text: String get() = words.joinToString(" ")

    /**
     * The text as the muṣḥaf prints it, with what you ask for.
     *
     * [marks]: the kinds of sign to print ([MarkKind.all] for every kind).
     * [ayahMarks] appends ۝ with the āyah number after each āyah that ends
     * inside the span.  [lines] breaks the text where the printed lines break.
     */
    fun render(marks: Set<MarkKind> = emptySet(), ayahMarks: Boolean = false, lines: Boolean = false): String {
        val out = StringBuilder()
        for (position in start until end) {
            if (lines && position != start && position in m.lineStartSet) out.append('\n')
            else if (position != start) out.append(' ')
            var token = m.words[position]
            for (mk in m.marksAt[position] ?: emptyList()) {
                if (mk.kind !in marks) continue
                token = if (mk.side == MarkSide.before) mk.sign + " " + token else token + mk.sign
            }
            out.append(token)
            if (ayahMarks) m.ayahEnds[position]?.let { out.append(' ').append(ayahMark(m.ayahNumber(it))) }
        }
        return out.toString()
    }

    /** Every numbered āyah with at least one word in the span. */
    open val ayahs: List<Ayah>
        get() {
            val first = maxOf(indexOf(m.ayahStarts, start), 0)
            val last = indexOf(m.ayahStarts, end - 1)
            return (first..last).map { Ayah.fromIndex(m, it) }
        }
    val firstAyah: Ayah? get() = ayahs.firstOrNull()
    val lastAyah: Ayah? get() = ayahs.lastOrNull()

    val surahs: List<Surah> get() = m.surahs.subList(indexOf(m.surahStarts, start), indexOf(m.surahStarts, end - 1) + 1)
    val pages: List<Page> get() = (indexOf(m.pageStarts, start)..indexOf(m.pageStarts, end - 1)).map { Page(m, it + 1) }
    /** The page the span starts on. */
    open val page: Page get() = m.pageAt(start)
    val juz: Juz? get() = m.juzAt(start)

    /** Every sign inside the span, with the word it is printed on. */
    val marks: List<Pair<Word, Mark>>
        get() = (start until end).flatMap { p -> (m.marksAt[p] ?: emptyList()).map { Word(m, p) to it } }

    /** The [index]-th word of the span, 1-based. */
    fun word(index: Int): Word {
        require(index in 1..size) { "word $index: the span has $size words" }
        return Word(m, start + index - 1)
    }

    override fun toString() = "Span($start, $end)"
}

/**
 * Where an āyah falls in another riwāyah.  [relation]: same (one āyah, the
 * same words), merged (one āyah holding more), split (several āyāt), shifted
 * (one āyah, boundaries crossing), unnumbered (the basmalah printed without a
 * number), missing (no word of it).
 */
data class AyahMatch(val ayahs: List<Ayah>, val relation: String) {
    val first: Ayah? get() = ayahs.firstOrNull()
    val last: Ayah? get() = ayahs.lastOrNull()
    /** "2:253-254" */
    val key: String get() {
        val a = ayahs.firstOrNull() ?: return ""
        val b = ayahs.last()
        return if (a == b) a.key else "${a.key}-${b.number}"
    }
    override fun toString() = "${key.ifEmpty { "-" }} ($relation)"
}

/** One numbered āyah, in this edition's own count. */
class Ayah private constructor(m: Mushaf, val surah: Surah, val number: Int, /** 0-based ordinal in the muṣḥaf. */ val index: Int) :
    Span(m, m.ayahStarts[index], if (index + 1 < m.ayahStarts.size) m.ayahStarts[index + 1] else m.words.size) {

    companion object {
        internal operator fun invoke(m: Mushaf, surah: Int, number: Int): Ayah {
            val s = m.surah(surah)
            require(number in 1..s.ayahCount) { "${s.nameEn} has ${s.ayahCount} āyāt in ${m.nameEn}, not $number" }
            return Ayah(m, s, number, s.firstAyahIndex + number - 1)
        }

        internal fun fromIndex(m: Mushaf, k: Int): Ayah {
            val s = m.surahs[m.surahOfAyahIndex(k)]
            return Ayah(m, s, k - s.firstAyahIndex + 1, k)
        }
    }

    /** "2:255" */
    val key: String get() = "${surah.number}:$number"
    /** The printed line the āyah starts on. */
    val line: Line? get() = m.lineAt(start)
    /** Every printed line the āyah touches. */
    val lines: List<Line> get() = m.linesBetween(start, end)
    val rasm_imlai: List<String?>? get() = m.rasm_imlaiColumn?.subList(start, end)
    val hasSajdah: Boolean get() = marks.any { it.second.kind == MarkKind.sajdah }
    /** ۝٢٥٥ */
    val marker: String get() = ayahMark(number)
    /** The shared numbers of this āyah's words. */
    val numbers: Set<Int>
        get() = (m.numbers[start].first..m.numbers[end - 1].last).filterNot { it in m.missingNumbers }.toSet()

    /**
     * This āyah in another riwāyah: `hafs.ayah(2, 255).to(warsh)` → 2:253-254, split.
     * Computed from the shared numbering, so it works between any two riwāyāt.
     */
    fun to(other: Mushaf): AyahMatch {
        val mine = numbers
        val hits = ArrayList<Ayah>()
        var unnumbered = false
        for (n in mine.sorted()) {
            val w = other.wordByNumber(n) ?: continue
            val a = w.ayah
            if (a == null) unnumbered = true
            else if (hits.isEmpty() || hits.last() != a) hits.add(a)
        }
        if (hits.isEmpty()) return AyahMatch(emptyList(), if (unnumbered) "unnumbered" else "missing")
        if (hits.size > 1) return AyahMatch(hits, "split")
        val theirs = hits[0].numbers
        val relation = if (theirs == mine) "same" else if (theirs.containsAll(mine)) "merged" else "shifted"
        return AyahMatch(hits, relation)
    }

    fun next(): Ayah? = if (index + 1 < m.ayahCount) fromIndex(m, index + 1) else null
    fun previous(): Ayah? = if (index > 0) fromIndex(m, index - 1) else null

    override fun equals(other: Any?) = other is Ayah && other.m === m && other.index == index
    override fun hashCode() = 31 * System.identityHashCode(m) + index
    override fun toString() = key
}

class Surah internal constructor(m: Mushaf, val number: Int, info: JSONObject) :
    Span(m, m.surahStarts[number - 1], if (number < m.surahStarts.size) m.surahStarts[number] else m.words.size) {
    val nameAr: String = info.getString("name_ar")
    val nameEn: String = info.getString("name_en")
    val revelation: String = info.getString("revelation")
    val hasBasmalah: Boolean = info.getBoolean("has_basmalah")
    val ayahCount: Int = info.getInt("ayah_count")
    internal val firstAyahIndex: Int = info.getInt("first_ayah")

    override val ayahs: List<Ayah> get() = (1..ayahCount).map { Ayah(m, number, it) }
    fun ayah(number: Int): Ayah = Ayah(m, this.number, number)

    /**
     * The basmalah where it is printed unnumbered before āyah 1 (Warsh,
     * Qālūn, Dūrī, Sūsī at al-Fātiḥah); null otherwise.
     */
    val basmalah: Span?
        get() {
            val first = m.ayahStarts[firstAyahIndex]
            return if (first > start) Span(m, start, first) else null
        }
    val firstPage: Page get() = page
    val lastPage: Page get() = m.pageAt(end - 1)
    override fun toString() = "$number $nameEn"
}

class Page internal constructor(m: Mushaf, val number: Int) :
    Span(m, m.pageStarts[checkPage(m, number) - 1], if (number < m.pageStarts.size) m.pageStarts[number] else m.words.size) {
    private companion object {
        fun checkPage(m: Mushaf, number: Int): Int {
            require(number in 1..m.pageStarts.size) { "page $number: ${m.nameEn} has ${m.pageStarts.size} pages" }
            return number
        }
    }

    val lines: List<Line> get() = m.linesBetween(start, end)
    fun line(number: Int): Line {
        val all = lines
        require(number in 1..all.size) { "line $number: page ${this.number} has ${all.size} lines" }
        return all[number - 1]
    }
    fun next(): Page? = if (number < m.pageCount) Page(m, number + 1) else null
    fun previous(): Page? = if (number > 1) Page(m, number - 1) else null
    override fun toString() = "page $number"
}

/** One printed line.  Reconstructed, not read: see `layers.derived.line`. */
class Line internal constructor(m: Mushaf, /** Within the muṣḥaf, 0-based. */ val index: Int) :
    Span(m, m.lineStarts!![index], if (index + 1 < m.lineStarts!!.size) m.lineStarts[index + 1] else m.words.size) {
    override val page: Page = m.pageAt(start)
    /** Within the page, 1-based. */
    val number: Int = index - indexOf(m.lineStarts!!, page.start) + 1
    override fun toString() = "page ${page.number}, line $number"
}

class Juz internal constructor(m: Mushaf, val number: Int, starts: IntArray) :
    Span(m, starts[checkJuz(number, starts) - 1], if (number < starts.size) starts[number] else m.words.size) {
    private companion object {
        fun checkJuz(number: Int, starts: IntArray): Int {
            require(number in 1..starts.size) { "juz $number: there are ${starts.size}" }
            return number
        }
    }
    override fun toString() = "juz $number"
}

// --- the muṣḥaf ---------------------------------------------------------------

/** One muṣḥaf file, `data/mushaf/<key>.json`. */
class Mushaf(private val doc: JSONObject) {
    init {
        require(doc.optString("format") == "quran-mushaf") { "not a quran-mushaf file" }
    }

    val words: List<String> = doc.getJSONArray("words").toStringList()
    val key: String = doc.getJSONObject("mushaf").getString("key")
    val nameEn: String = doc.getJSONObject("mushaf").getString("name_en")
    val nameAr: String = doc.getJSONObject("mushaf").getString("name_ar")
    val qiraahEn: String? = doc.getJSONObject("mushaf").optString("qiraah_en", null)
    val qiraahAr: String? = doc.getJSONObject("mushaf").optString("qiraah_ar", null)
    /** The `counting` block of the file. */
    val counting: JSONObject = doc.getJSONObject("counting")
    /** The `provenance` block of the file. */
    val provenance: JSONObject = doc.getJSONObject("provenance")
    val countingSystem: String = counting.getString("system")
    /**
     * The counting system this muṣḥaf's qāriʾ is associated with. Compare with
     * [countingSystem], the system this edition measures onto: for Dūrī and
     * Sūsī they differ.
     */
    val countingSystemAssociatedWithQari: String =
        counting.getString("system_associated_with_qari")
    val basmalahCounted: Boolean = counting.getBoolean("basmalah_counted")
    /** The layers the file carries, e.g. `[surahs, ayahs, pages, lines, marks, juz, rasm_imlai]`. */
    val layers: List<String> = doc.getJSONObject("layers").getJSONArray("present").toStringList()

    internal val rasm_imlaiColumn: List<String?>? =
        doc.optJSONArray("rasm_imlai")?.let { a -> List(a.length()) { if (a.isNull(it)) null else a.getString(it) } }
    internal val surahStarts = doc.getJSONArray("surah_starts").toIntArray()
    internal val ayahStarts = doc.getJSONArray("ayah_starts").toIntArray()
    internal val pageStarts = doc.getJSONArray("page_starts").toIntArray()
    internal val lineStarts: IntArray? = doc.optJSONArray("line_starts")?.toIntArray()
    internal val juzStarts: IntArray? = doc.optJSONArray("juz_starts")?.toIntArray()
    internal val lineStartSet: Set<Int> = lineStarts?.toSet() ?: emptySet()
    val surahs: List<Surah> = (1..114).map { Surah(this, it, doc.getJSONArray("surahs").getJSONObject(it - 1)) }
    private val surahFirstAyah = IntArray(114) { surahs[it].firstAyahIndex }
    internal val ayahEnds: Map<Int, Int> = ayahStarts.indices.associateBy { k ->
        (if (k + 1 < ayahStarts.size) ayahStarts[k + 1] else words.size) - 1
    }
    internal val marksAt: Map<Int, List<Mark>>
    private val numberingBlock = doc.getJSONObject("numbering")
    private var numbersCache: List<IntRange>? = null
    private var foldCache: List<String>? = null

    init {
        val types = doc.getJSONArray("mark_types").let { a ->
            List(a.length()) {
                val t = a.getJSONObject(it)
                Mark(MarkKind.valueOf(t.getString("kind")), MarkSide.valueOf(t.getString("side")), t.getString("sign"))
            }
        }
        val marks = HashMap<Int, MutableList<Mark>>()
        val pairs = doc.getJSONArray("marks")
        for (i in 0 until pairs.length()) {
            val pair = pairs.getJSONArray(i)
            marks.getOrPut(pair.getInt(0)) { ArrayList(1) }.add(types[pair.getInt(1)])
        }
        marksAt = marks
    }

    companion object {
        /** Ḥafṣ, the riwāyah nearly every app uses, bundled with the library. */
        fun hafs(): Mushaf = fromJson(
            Mushaf::class.java.getResourceAsStream("/hafs.json")!!.bufferedReader().readText()
        )
        /** Any of the seven riwāyāt, from the text of `data/mushaf/<key>.json`. */
        fun fromJson(json: String) = Mushaf(JSONObject(json))
        fun load(file: File) = fromJson(file.readText())
    }

    // -- what the file carries --

    /** The font to ship with this text; see [Font]. */
    val font: Font
        get() = doc.getJSONObject("font").let { Font(it.getString("family"), it.getString("file"), it.getString("sha256"), it.getString("publisher")) }

    /** `has("juz")`, `has("rasm_imlai")`, `has("lines")` … */
    fun has(layer: String) = layer in layers
    /** Why a layer is absent, e.g. Bazzī's juz. */
    fun whyAbsent(layer: String): String? = doc.getJSONObject("layers").optJSONObject("absent")?.optString(layer, null)
    val wordCount: Int get() = words.size
    val ayahCount: Int get() = ayahStarts.size
    val pageCount: Int get() = pageStarts.size
    val lineCount: Int get() = lineStarts?.size ?: 0
    val juzCount: Int get() = juzStarts?.size ?: 0

    // -- units by number --

    fun surah(number: Int): Surah {
        require(number in 1..114) { "sūrah $number: there are 114" }
        return surahs[number - 1]
    }
    /** Āyah [number] of [surah] in this edition's own count. */
    fun ayah(surah: Int, number: Int): Ayah = Ayah(this, surah, number)
    fun page(number: Int): Page = Page(this, number)
    /** Throws [IllegalStateException] when the file has no juz layer (Bazzī); see [whyAbsent]. */
    fun juz(number: Int): Juz = Juz(this, number, juzStarts ?: throw IllegalStateException(absent("juz")))
    fun line(page: Int, number: Int): Line = Page(this, page).line(number)
    /** Word [index] (1-based) of an āyah. */
    fun word(surah: Int, ayah: Int, index: Int): Word = Ayah(this, surah, ayah).word(index)
    /** Any run of positions, e.g. to render a selection. */
    fun span(start: Int, end: Int): Span {
        require(start >= 0 && start < end && end <= words.size) { "span $start:$end is outside the muṣḥaf" }
        return Span(this, start, end)
    }
    val all: Span get() = Span(this, 0, words.size)
    val ayahs: List<Ayah> get() = (0 until ayahCount).map { Ayah.fromIndex(this, it) }
    val pages: List<Page> get() = (1..pageCount).map { Page(this, it) }
    val ajza: List<Juz> get() = juzStarts?.let { s -> (1..s.size).map { Juz(this, it, s) } } ?: emptyList()

    private fun absent(layer: String) = "$nameEn has no $layer layer: ${whyAbsent(layer) ?: "not in this file"}"

    // -- units by position --

    fun wordAt(position: Int) = Word(this, position)
    fun ayahAt(position: Int): Ayah? = indexOf(ayahStarts, position).let { if (it >= 0) Ayah.fromIndex(this, it) else null }
    fun surahAt(position: Int): Surah = surahs[indexOf(surahStarts, position)]
    fun pageAt(position: Int): Page = Page(this, indexOf(pageStarts, position) + 1)
    fun lineAt(position: Int): Line? = lineStarts?.let { Line(this, indexOf(it, position)) }
    fun juzAt(position: Int): Juz? = juzStarts?.let { Juz(this, indexOf(it, position) + 1, it) }
    internal fun linesBetween(start: Int, end: Int): List<Line> {
        val starts = lineStarts ?: return emptyList()
        return (indexOf(starts, start)..indexOf(starts, end - 1)).map { Line(this, it) }
    }

    // -- the shared numbering --

    internal val numbers: List<IntRange>
        get() {
            numbersCache?.let { return it }
            val missing = numberingBlock.getJSONArray("missing").toIntArray().toHashSet()
            val joined = HashMap<Int, IntRange>()
            val wj = numberingBlock.getJSONArray("written_joined")
            for (i in 0 until wj.length()) {
                val j = wj.getJSONObject(i)
                val ns = j.getJSONArray("numbers")
                joined[j.getInt("position")] = ns.getInt(0)..ns.getInt(1)
            }
            val runs = ArrayList<IntRange>(words.size)
            var n = 1
            for (position in words.indices) {
                while (n in missing) n++
                val run = joined[position] ?: (n..n)
                runs.add(run)
                n = run.last + 1
            }
            numbersCache = runs
            return runs
        }
    /** The shared numbers this riwāyah does not read. */
    val missingNumbers: Set<Int> by lazy { numberingBlock.getJSONArray("missing").toIntArray().toHashSet() }
    /** The shared number of the word at [position]. */
    fun numberAt(position: Int): Int = numbers[position].first
    /** The printed word carrying a shared number; null where this muṣḥaf does not read it. */
    fun wordByNumber(number: Int): Word? {
        val runs = numbers
        var lo = 0
        var hi = runs.size
        while (lo < hi) {
            val mid = (lo + hi) ushr 1
            if (runs[mid].first <= number) lo = mid + 1 else hi = mid
        }
        val i = lo - 1
        return if (i >= 0 && number in runs[i]) Word(this, i) else null
    }

    // -- signs and search --

    /** Every āyah printed with ۩. */
    fun sajdat(): List<Ayah> = positionsWith(MarkKind.sajdah).mapNotNull { ayahAt(it) }
    /** Every word printed with ۞ before it, as the release prints them. */
    fun divisionMarks(): List<Word> = positionsWith(MarkKind.division).map { Word(this, it) }
    private fun positionsWith(kind: MarkKind) = marksAt.filterValues { ms -> ms.any { it.kind == kind } }.keys.sorted()

    /**
     * Every place the words of [text] occur in sequence, matched on [fold]:
     * harakah and hamzah forms do not matter.
     */
    fun search(text: String): List<Span> {
        val query = text.trim().split(Regex("\\s+")).filter { it.isNotEmpty() }.map(::fold)
        if (query.isEmpty() || query.any { it.isEmpty() }) return emptyList()
        val folded = foldCache ?: words.map(::fold).also { foldCache = it }
        val n = query.size
        val out = ArrayList<Span>()
        for (i in 0..folded.size - n) {
            if (folded[i] != query[0]) continue
            if ((1 until n).all { folded[i + it] == query[it] }) out.add(Span(this, i, i + n))
        }
        return out
    }

    internal fun surahOfAyahIndex(k: Int) = indexOf(surahFirstAyah, k)
    internal fun ayahNumber(k: Int) = k - surahFirstAyah[surahOfAyahIndex(k)] + 1
    override fun toString() = "Mushaf($key)"
}

// --- āyah map ----------------------------------------------------------------

/**
 * Where a Kūfī āyah falls in one edition.  [relation] is same, merged, split
 * (then [ayahLast] is set), shifted or unnumbered ([ayah] is 0).
 */
data class MappedAyah(val surah: Int, val ayah: Int, val relation: String, val ayahLast: Int? = null) {
    /** "2:253-254" */
    val key: String get() = if (ayahLast != null) "$surah:$ayah-$ayahLast" else "$surah:$ayah"
    override fun toString() = key
}

/** `data/ayah-map.json`: what a Ḥafṣ (Kūfī) reference is in every edition. */
class AyahMap(doc: JSONObject) {
    init {
        require(doc.optString("format") == "quran-ayah-map") { "not a quran-ayah-map file" }
    }

    val editions: List<String> = doc.getJSONArray("editions").toStringList()
    private val rows: Map<String, JSONObject> = doc.getJSONArray("ayahs").let { a ->
        (0 until a.length()).associate { i -> a.getJSONObject(i).let { "${it.getInt("surah")}:${it.getInt("ayah")}" to it } }
    }

    companion object {
        fun fromJson(json: String) = AyahMap(JSONObject(json))
        fun load(file: File) = fromJson(file.readText())
    }

    /** `convert(2, 255, "warsh")` → `MappedAyah(2, 253, "split", 254)` */
    fun convert(surah: Int, ayah: Int, to: String): MappedAyah {
        val row = rows["$surah:$ayah"] ?: throw IllegalArgumentException("$surah:$ayah is not a Kūfī āyah")
        val r = row.optJSONObject(to) ?: throw IllegalArgumentException("no edition '$to'; editions are $editions")
        return MappedAyah(r.getInt("surah"), r.getInt("ayah"), r.getString("relation"), if (r.has("ayah_last")) r.getInt("ayah_last") else null)
    }

    /** The reference in every edition. */
    fun all(surah: Int, ayah: Int): Map<String, MappedAyah> = editions.associateWith { convert(surah, ayah, it) }
}

// --- word index --------------------------------------------------------------

/** One record of `data/word-index.json`: a shared number and what it is. */
class IndexedWord(val raw: JSONObject) {
    val number: Int get() = raw.getInt("number")
    val surah: Int get() = raw.getInt("surah")
    val index: Int get() = raw.getInt("index")
    val key: String get() = raw.getString("key")
    val rasm_uthmani: String get() = raw.getString("rasm_uthmani")
    val plain: String get() = raw.getString("plain")
    val rasm: String get() = raw.getString("rasm")
    val pointed: String get() = raw.getString("pointed")
    val status: String get() = raw.getString("status")
    /** `(surah, ayah, position)` in the Kūfī count, or null where Ḥafṣ lacks the word. */
    val hafs: Triple<Int, Int, Int>? get() = raw.optJSONObject("hafs")?.let { Triple(it.getInt("surah"), it.getInt("ayah"), it.getInt("position")) }
    /** Āyah number per riwāyah. */
    val ayah: Map<String, Int> get() = raw.getJSONObject("ayah").let { o -> o.keySet().associateWith { o.getInt(it) } }
    /** Each riwāyah's own spelling; absent where it does not read the word. */
    val forms: Map<String, String> get() = raw.getJSONObject("forms").let { o -> o.keySet().associateWith { o.getString(it) } }
    val groups: List<JSONObject> get() = raw.optJSONArray("groups")?.let { a -> List(a.length()) { a.getJSONObject(it) } } ?: emptyList()
    val missing: List<String> get() = raw.optJSONArray("missing")?.toStringList() ?: emptyList()
    val writtenJoined: List<String> get() = raw.optJSONArray("written_joined")?.toStringList() ?: emptyList()
    /** How one riwāyah spells it; null where it does not read the word. */
    fun form(riwayah: String): String? = raw.getJSONObject("forms").optString(riwayah, null)
    override fun toString() = "$number $rasm_uthmani"
}

/** `data/word-index.json`: the numbering shared by all seven muṣḥafs. */
class WordIndex(doc: JSONObject) : Iterable<IndexedWord> {
    init {
        require(doc.optString("format") == "quran-word-index") { "not a quran-word-index file" }
    }

    val mushafs: List<String> = doc.getJSONArray("mushafs").toStringList()
    val total: Int = doc.getInt("total")
    private val records: JSONArray = doc.getJSONArray("words")
    private var byHafs: Map<String, JSONObject>? = null
    private var byPlain: Map<String, List<JSONObject>>? = null

    companion object {
        fun fromJson(json: String) = WordIndex(JSONObject(json))
        fun load(file: File) = fromJson(file.readText())
    }

    private fun record(i: Int): JSONObject = records.getJSONObject(i)

    fun word(number: Int): IndexedWord {
        require(number in 1..total) { "number $number: the numbering is 1 … $total" }
        return IndexedWord(record(number - 1))
    }

    /** By Ḥafṣ coordinates: sūrah, āyah in the Kūfī count, 1-based word. */
    fun find(surah: Int, ayah: Int, index: Int): IndexedWord? {
        val by = byHafs ?: HashMap<String, JSONObject>().also { map ->
            for (i in 0 until records.length()) {
                val r = record(i)
                r.optJSONObject("hafs")?.let { h -> map.putIfAbsent("${h.getInt("surah")}:${h.getInt("ayah")}:${h.getInt("position")}", r) }
            }
            byHafs = map
        }
        return by["$surah:$ayah:$index"]?.let { IndexedWord(it) }
    }

    /** Every number whose folded spelling equals [text], folded. */
    fun search(text: String): List<IndexedWord> {
        val by = byPlain ?: HashMap<String, MutableList<JSONObject>>().also { map ->
            for (i in 0 until records.length()) {
                val r = record(i)
                map.getOrPut(fold(r.getString("rasm_uthmani"))) { ArrayList(1) }.add(r)
            }
            byPlain = map
        }
        return by[fold(text)]?.map { IndexedWord(it) } ?: emptyList()
    }

    /** Every number the riwāyāt spell in more than one way. */
    fun differing(): List<IndexedWord> = (0 until records.length()).map { record(it) }.filter { it.has("groups") }.map { IndexedWord(it) }

    val size: Int get() = total
    override fun iterator(): Iterator<IndexedWord> = (0 until records.length()).asSequence().map { IndexedWord(record(it)) }.iterator()
}
