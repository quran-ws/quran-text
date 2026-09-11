<?php

declare(strict_types=1);

namespace QuranText;

/**
 * One muṣḥaf file, data/mushaf/<key>.json.
 *
 *   $m = Mushaf::hafs();                       // bundled; or Mushaf::load('data/mushaf/warsh.json')
 *   $m->ayah(2, 255)->text();
 *   $m->ayah(2, 255)->render(marks: true, ayahMarks: true);
 *   $m->page(3)->lines();
 *   $m->juz(30)->firstAyah()->key();          // "78:1"
 *
 * Positions are 0-based indices into $words; sūrah, āyah, page, line and juz
 * numbers are 1-based, as printed.  Āyah numbers are in this edition's own
 * count; use AyahMap to convert between editions.
 */
final class Mushaf
{
    /** @var string[] */
    public readonly array $words;
    public readonly string $key;
    public readonly string $nameEn;
    public readonly string $nameAr;
    public readonly ?string $qiraahEn;
    public readonly ?string $qiraahAr;
    public readonly string $countingSystem;
    /**
     * The counting system this muṣḥaf's qāriʾ is associated with. Compare with
     * $countingSystem, the system this edition measures onto: for Dūrī and
     * Sūsī they differ.
     */
    public readonly string $countingSystemAssociatedWithQari;
    public readonly bool $basmalahCounted;
    /** @var Surah[] */
    public readonly array $surahs;

    /** @internal */
    public readonly array $doc;
    /** @internal position of an āyah's last word => index into ayah_starts */
    public readonly array $ayahEnds;
    /** @internal position => Mark[] */
    public readonly array $marksAt;
    /** @internal position => true for every line start */
    public readonly array $lineStartSet;
    private readonly array $surahFirstAyah;
    private ?array $numbers = null;
    private ?array $folded = null;

    public function __construct(array $doc)
    {
        if (($doc['format'] ?? null) !== 'quran-mushaf') {
            throw new \InvalidArgumentException('not a quran-mushaf file');
        }
        $this->doc = $doc;
        $this->words = $doc['words'];
        $this->key = $doc['mushaf']['key'];
        $this->nameEn = $doc['mushaf']['name_en'];
        $this->nameAr = $doc['mushaf']['name_ar'];
        $this->qiraahEn = $doc['mushaf']['qiraah_en'] ?? null;
        $this->qiraahAr = $doc['mushaf']['qiraah_ar'] ?? null;
        $this->countingSystem = $doc['counting']['system'];
        $this->countingSystemAssociatedWithQari = $doc['counting']['system_associated_with_qari'];
        $this->basmalahCounted = $doc['counting']['basmalah_counted'];
        $surahs = [];
        for ($n = 1; $n <= 114; $n++) {
            $surahs[] = new Surah($this, $n);
        }
        $this->surahs = $surahs;
        $this->surahFirstAyah = array_map(fn (Surah $s) => $s->firstAyah, $surahs);
        $ends = [];
        $starts = $doc['ayah_starts'];
        $total = count($this->words);
        foreach ($starts as $k => $start) {
            $ends[($starts[$k + 1] ?? $total) - 1] = $k;
        }
        $this->ayahEnds = $ends;
        $types = array_map(fn ($t) => new Mark($t['kind'], $t['side'], $t['sign']), $doc['mark_types']);
        $marks = [];
        foreach ($doc['marks'] as [$position, $t]) {
            $marks[$position][] = $types[$t];
        }
        $this->marksAt = $marks;
        $this->lineStartSet = array_fill_keys($doc['line_starts'] ?? [], true);
    }

    // -- loading --

    /** Ḥafṣ, the riwāyah nearly every app uses, bundled with the package. */
    public static function hafs(): self
    {
        return self::load(__DIR__ . '/../data/hafs.json');
    }

    /** Any of the seven riwāyāt: data/mushaf/<key>.json */
    public static function load(string $path): self
    {
        $json = file_get_contents($path);
        if ($json === false) {
            throw new \RuntimeException("cannot read $path");
        }
        $m = self::fromJson($json);
        $m->dir = dirname(realpath($path));
        return $m;
    }

    private ?string $dir = null;

    /** The font to ship with this text; see Font. */
    public function font(): Font
    {
        $f = $this->doc['font'];
        $name = basename($f['file']);
        $path = null;
        if ($this->dir !== null) {
            foreach ([$this->dir . '/' . $name, dirname($this->dir) . '/fonts/' . $name] as $candidate) {
                if (is_file($candidate)) {
                    $path = $candidate;
                    break;
                }
            }
        }
        return new Font($f['family'], $f['file'], $f['sha256'], $f['publisher'], $path);
    }

    public static function fromJson(string|array $data): self
    {
        return new self(is_string($data) ? json_decode($data, true, 512, JSON_THROW_ON_ERROR) : $data);
    }

    // -- what the file carries --

    /** @return string[] */
    public function layers(): array
    {
        return $this->doc['layers']['present'];
    }

    /** has('juz'), has('rasm_imlai'), has('lines') … */
    public function has(string $layer): bool
    {
        return in_array($layer, $this->doc['layers']['present'], true);
    }

    /** @internal */
    public function absent(string $layer): string
    {
        $why = $this->doc['layers']['absent'][$layer] ?? 'not in this file';
        return "{$this->nameEn} has no $layer layer: $why";
    }

    public function counting(): array
    {
        return $this->doc['counting'];
    }

    public function provenance(): array
    {
        return $this->doc['provenance'];
    }

    public function wordCount(): int
    {
        return count($this->words);
    }

    public function ayahCount(): int
    {
        return count($this->doc['ayah_starts']);
    }

    public function pageCount(): int
    {
        return count($this->doc['page_starts']);
    }

    public function lineCount(): int
    {
        return count($this->doc['line_starts'] ?? []);
    }

    public function juzCount(): int
    {
        return count($this->doc['juz_starts'] ?? []);
    }

    // -- units by number --

    public function surah(int $number): Surah
    {
        if ($number < 1 || $number > 114) {
            throw new \OutOfRangeException("sūrah $number: there are 114");
        }
        return $this->surahs[$number - 1];
    }

    /** Āyah $number of $surah in this edition's own count. */
    public function ayah(int $surah, int $number): Ayah
    {
        return new Ayah($this, $surah, $number);
    }

    public function page(int $number): Page
    {
        return new Page($this, $number);
    }

    public function juz(int $number): Juz
    {
        return new Juz($this, $number);
    }

    public function line(int $page, int $number): Line
    {
        return (new Page($this, $page))->line($number);
    }

    /** Word $index (1-based) of an āyah. */
    public function word(int $surah, int $ayah, int $index): Word
    {
        return (new Ayah($this, $surah, $ayah))->word($index);
    }

    /** Any run of positions, e.g. to render a selection. */
    public function span(int $start, int $end): Span
    {
        if ($start < 0 || $start >= $end || $end > count($this->words)) {
            throw new \OutOfRangeException("span $start:$end is outside the muṣḥaf");
        }
        return new Span($this, $start, $end);
    }

    public function all(): Span
    {
        return new Span($this, 0, count($this->words));
    }

    /** @return Ayah[] */
    public function ayahs(): array
    {
        $out = [];
        for ($k = 0; $k < $this->ayahCount(); $k++) {
            $out[] = Ayah::fromIndex($this, $k);
        }
        return $out;
    }

    /** @return Page[] */
    public function pages(): array
    {
        $out = [];
        for ($n = 1; $n <= $this->pageCount(); $n++) {
            $out[] = new Page($this, $n);
        }
        return $out;
    }

    /** @return Juz[] */
    public function ajza(): array
    {
        $out = [];
        for ($n = 1; $n <= $this->juzCount(); $n++) {
            $out[] = new Juz($this, $n);
        }
        return $out;
    }

    // -- units by position --

    public function wordAt(int $position): Word
    {
        return new Word($this, $position);
    }

    public function ayahAt(int $position): ?Ayah
    {
        $k = Text::indexOf($this->doc['ayah_starts'], $position);
        return $k >= 0 ? Ayah::fromIndex($this, $k) : null;
    }

    public function surahAt(int $position): Surah
    {
        return $this->surahs[Text::indexOf($this->doc['surah_starts'], $position)];
    }

    public function pageAt(int $position): Page
    {
        return new Page($this, Text::indexOf($this->doc['page_starts'], $position) + 1);
    }

    public function lineAt(int $position): ?Line
    {
        $starts = $this->doc['line_starts'] ?? null;
        return $starts ? Line::fromIndex($this, Text::indexOf($starts, $position)) : null;
    }

    public function juzAt(int $position): ?Juz
    {
        $starts = $this->doc['juz_starts'] ?? null;
        return $starts ? new Juz($this, Text::indexOf($starts, $position) + 1) : null;
    }

    /** @internal @return Line[] */
    public function linesBetween(int $start, int $end): array
    {
        $starts = $this->doc['line_starts'] ?? null;
        if (!$starts) {
            return [];
        }
        $out = [];
        for ($i = Text::indexOf($starts, $start), $last = Text::indexOf($starts, $end - 1); $i <= $last; $i++) {
            $out[] = Line::fromIndex($this, $i);
        }
        return $out;
    }

    // -- the shared numbering --

    /**
     * The run of shared numbers each position covers, as two parallel columns:
     * [first[], last[]], both indexed by position.  Two flat int arrays rather
     * than one array of pairs: at ~77k words a pair per position costs tens of
     * megabytes, and several muṣḥafs are commonly open at once.
     * @internal
     */
    public function numbers(): array
    {
        if ($this->numbers === null) {
            $block = $this->doc['numbering'];
            $missing = array_fill_keys($block['missing'], true);
            $joined = [];
            foreach ($block['written_joined'] as $j) {
                $joined[$j['position']] = $j['numbers'];
            }
            $firsts = [];
            $lasts = [];
            $n = 1;
            for ($position = 0, $total = count($this->words); $position < $total; $position++) {
                while (isset($missing[$n])) {
                    $n++;
                }
                [$first, $last] = $joined[$position] ?? [$n, $n];
                $firsts[] = $first;
                $lasts[] = $last;
                $n = $last + 1;
            }
            $this->numbers = [$firsts, $lasts];
        }
        return $this->numbers;
    }

    /** The shared numbers this riwāyah does not read. @return array<int,true> */
    public function missingNumbers(): array
    {
        return array_fill_keys($this->doc['numbering']['missing'], true);
    }

    /** The shared number of the word at $position. */
    public function numberAt(int $position): int
    {
        return $this->numbers()[0][$position];
    }

    /** The printed word carrying a shared number; null where this muṣḥaf does not read it. */
    public function wordByNumber(int $number): ?Word
    {
        [$firsts, $lasts] = $this->numbers();
        $lo = 0;
        $hi = count($firsts);
        while ($lo < $hi) {
            $mid = ($lo + $hi) >> 1;
            if ($firsts[$mid] <= $number) {
                $lo = $mid + 1;
            } else {
                $hi = $mid;
            }
        }
        $i = $lo - 1;
        return $i >= 0 && $firsts[$i] <= $number && $number <= $lasts[$i] ? new Word($this, $i) : null;
    }

    // -- signs and search --

    /** Every āyah printed with ۩. @return Ayah[] */
    public function sajdat(): array
    {
        return array_map(fn ($p) => $this->ayahAt($p), $this->positionsWith('sajdah'));
    }

    /** Every word printed with ۞ before it, as the release prints them. @return Word[] */
    public function divisionMarks(): array
    {
        return array_map(fn ($p) => new Word($this, $p), $this->positionsWith('division'));
    }

    /** @return int[] */
    private function positionsWith(string $kind): array
    {
        $out = [];
        foreach ($this->marksAt as $position => $marks) {
            foreach ($marks as $mark) {
                if ($mark->kind === $kind) {
                    $out[] = $position;
                    break;
                }
            }
        }
        sort($out);
        return $out;
    }

    /**
     * Every place the words of $text occur in sequence, matched on
     * Text::fold() — harakah and hamzah forms do not matter.
     * @return Span[]
     */
    public function search(string $text): array
    {
        $query = array_map([Text::class, 'fold'], preg_split('/\s+/u', trim($text), -1, PREG_SPLIT_NO_EMPTY));
        if (!$query || in_array('', $query, true)) {
            return [];
        }
        if ($this->folded === null) {
            $this->folded = array_map([Text::class, 'fold'], $this->words);
        }
        $n = count($query);
        $out = [];
        for ($i = 0, $limit = count($this->folded) - $n; $i <= $limit; $i++) {
            if ($this->folded[$i] !== $query[0]) {
                continue;
            }
            for ($j = 1; $j < $n; $j++) {
                if ($this->folded[$i + $j] !== $query[$j]) {
                    continue 2;
                }
            }
            $out[] = new Span($this, $i, $i + $n);
        }
        return $out;
    }

    // -- internals --

    /** @internal */
    public function surahOfAyahIndex(int $k): int
    {
        return Text::indexOf($this->surahFirstAyah, $k);
    }

    /** @internal */
    public function ayahNumber(int $k): int
    {
        return $k - $this->surahFirstAyah[$this->surahOfAyahIndex($k)] + 1;
    }
}
